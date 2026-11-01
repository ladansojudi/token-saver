#!/usr/bin/env python3
"""Run the eval cases with and without the skill using headless Claude Code (`claude -p`).

A stand-in for `claude plugin eval` while that command is in early access. For every
case, arm (with / without) and run it:
  1. copies the case files into a fresh folder (and, in the "with" arm, the skill into
     <folder>/.claude/skills/token-saver),
  2. runs `claude -p` with the case prompt and records tokens, cost, time, turns, whether
     the Skill tool was called, and which files changed,
  3. asks a judge model (default: haiku) to mark every grader pass or fail.

Results: one JSON file per run plus summary.json and summary.md in --out.

    python3 tools/run_evals.py --out /tmp/token-saver-evals --runs 3 --jobs 4

This spends real usage: about (cases x 2 arms x runs) agent runs plus as many judge calls.
"""

import argparse
import concurrent.futures as cf
import hashlib
import json
import re
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "token-saver"
EVALS = SKILL / "evals"


def split_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2).strip()


def load_cases(only=None):
    cases = []
    for d in sorted(p for p in EVALS.iterdir() if (p / "prompt.md").is_file()):
        if only and d.name not in only:
            continue
        meta, prompt = split_frontmatter((d / "prompt.md").read_text(encoding="utf-8"))
        tools = re.findall(r"[A-Za-z]+", meta.get("allowed_tools", "")) or ["Read", "Glob", "Grep", "Skill"]
        expected = (d / "case.yaml").read_text(encoding="utf-8")
        expected = re.search(r"expected_outcome: \|\n((?:  .*\n?)+)", expected)
        graders = []
        for g in sorted((d / "graders").glob("*.md")):
            gm, gtext = split_frontmatter(g.read_text(encoding="utf-8"))
            graders.append({"id": g.stem, "focus": gm.get("focus", "outcome"), "text": gtext})
        cases.append({
            "name": d.name, "dir": d, "prompt": prompt, "tools": tools,
            "max_turns": int(meta.get("max_turns", 10)), "timeout": int(meta.get("timeout_seconds", 300)),
            "expected": re.sub(r"\n\s+", " ", expected.group(1)).strip() if expected else "",
            "graders": graders, "files": d / "files",
        })
    return cases


def snapshot(folder):
    out = {}
    for p in folder.rglob("*"):
        if p.is_file() and ".claude/skills/token-saver" not in str(p):
            out[str(p.relative_to(folder))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def run_agent(case, arm, i, out, model):
    work = out / "work" / case["name"] / f"{arm}-{i}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    if case["files"].is_dir():
        shutil.copytree(case["files"], work, dirs_exist_ok=True)
    if arm == "with":
        shutil.copytree(SKILL, work / ".claude" / "skills" / "token-saver", ignore=shutil.ignore_patterns("evals", "__pycache__"))
    before = snapshot(work)
    cmd = ["claude", "-p", case["prompt"], "--output-format", "stream-json", "--verbose",
           "--max-turns", str(case["max_turns"]), "--allowedTools", *case["tools"],
           "--permission-mode", "acceptEdits", "--no-session-persistence"]
    if model:
        cmd += ["--model", model]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=case["timeout"] + 60)
        lines = proc.stdout.splitlines()
    except subprocess.TimeoutExpired as e:
        lines = (e.stdout or "").splitlines() if isinstance(e.stdout, str) else []
    wall = time.time() - t0
    result, skill_called, tools_used = {}, False, []
    for line in lines:
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "tool_use":
                    tools_used.append(c.get("name"))
                    if c.get("name") == "Skill" and "token-saver" in json.dumps(c.get("input", {})):
                        skill_called = True
        if ev.get("type") == "result":
            result = ev
    after = snapshot(work)
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    usage = result.get("usage", {}) or {}
    rec = {
        "case": case["name"], "arm": arm, "run": i,
        "reply": result.get("result", ""), "is_error": result.get("is_error", True),
        "num_turns": result.get("num_turns"), "duration_s": round((result.get("duration_ms") or wall * 1000) / 1000, 1),
        "cost_usd": result.get("total_cost_usd"),
        "input_tokens": usage.get("input_tokens", 0), "output_tokens": usage.get("output_tokens", 0),
        "cache_read": usage.get("cache_read_input_tokens", 0), "cache_write": usage.get("cache_creation_input_tokens", 0),
        "skill_called": skill_called, "tools_used": tools_used, "files_changed": changed,
        "files_after": {k: (work / k).read_text(encoding="utf-8", errors="replace")[:4000] for k in changed if (work / k).is_file() and k.endswith(".md")},
    }
    rec["total_tokens"] = rec["input_tokens"] + rec["output_tokens"] + rec["cache_read"] + rec["cache_write"]
    return rec


JUDGE = """You are grading one run of an AI assistant against a checklist. Be strict and literal.

Task the user gave:
<task>
{prompt}
</task>

What a good result looks like:
<expected>
{expected}
</expected>

The assistant's final reply:
<reply>
{reply}
</reply>

Files the assistant changed during the run: {changed}
{files}

Checklist. For each item decide pass (true) or fail (false):
{items}

Answer with JSON only, no prose:
{{"scores": [{{"id": "<item id>", "pass": true, "why": "<at most 15 words>"}}]}}"""


def judge(case, rec, model):
    items = "\n".join(f"- {g['id']}: {g['text']}" for g in case["graders"])
    files = "".join(f"\nFinal content of {k}:\n<file>\n{v}\n</file>" for k, v in rec["files_after"].items())
    prompt = JUDGE.format(prompt=case["prompt"], expected=case["expected"], reply=rec["reply"] or "(no reply)",
                          changed=", ".join(rec["files_changed"]) or "none", files=files, items=items)
    proc = subprocess.run(["claude", "-p", prompt, "--output-format", "json", "--model", model, "--max-turns", "1",
                           "--no-session-persistence", "--tools", ""],
                          capture_output=True, text=True, timeout=300, cwd="/tmp")
    try:
        text = json.loads(proc.stdout).get("result", "")
        data = json.loads(re.search(r"\{.*\}", text, re.S).group(0))
        got = {s["id"]: s for s in data["scores"]}
    except (ValueError, AttributeError, KeyError, TypeError):
        got = {}
    scores = []
    for g in case["graders"]:
        s = got.get(g["id"], {"pass": False, "why": "judge gave no verdict"})
        scores.append({"id": g["id"], "pass": bool(s.get("pass")), "why": s.get("why", "")})
    return scores


def summarise(records):
    by = {}
    for r in records:
        by.setdefault((r["case"], r["arm"]), []).append(r)
    rows = []
    for (case, arm), rs in sorted(by.items()):
        passed = sum(s["pass"] for r in rs for s in r["scores"])
        total = sum(len(r["scores"]) for r in rs)
        rows.append({
            "case": case, "arm": arm, "runs": len(rs), "score": round(passed / total, 3) if total else 0,
            "passed": passed, "graders": total,
            "tokens_median": int(statistics.median(r["total_tokens"] for r in rs)),
            "output_tokens_median": int(statistics.median(r["output_tokens"] for r in rs)),
            "cost_usd_median": round(statistics.median((r["cost_usd"] or 0) for r in rs), 4),
            "seconds_median": round(statistics.median(r["duration_s"] for r in rs), 1),
            "reply_chars_median": int(statistics.median(len(r["reply"]) for r in rs)),
            "skill_called": sum(r["skill_called"] for r in rs), "errors": sum(bool(r["is_error"]) for r in rs),
        })
    return rows


def to_md(rows):
    out = ["| Case | Arm | Score | Median tokens | Median output tokens | Median reply chars | Median s | Skill called |", "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['case']} | {r['arm']} | {r['passed']}/{r['graders']} ({r['score']:.0%}) | {r['tokens_median']:,} | {r['output_tokens_median']:,} | {r['reply_chars_median']:,} | {r['seconds_median']} | {r['skill_called']}/{r['runs']} |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--case", nargs="*")
    ap.add_argument("--arms", nargs="*", default=["with", "without"])
    ap.add_argument("--model", default=None, help="model for the agent runs (default: your Claude Code default)")
    ap.add_argument("--judge-model", default="haiku")
    args = ap.parse_args()
    out = Path(args.out)
    (out / "runs").mkdir(parents=True, exist_ok=True)
    cases = load_cases(args.case)
    jobs = [(c, a, i) for c in cases for a in args.arms for i in range(1, args.runs + 1)]

    def one(job):
        c, a, i = job
        rec = run_agent(c, a, i, out, args.model)
        rec["scores"] = judge(c, rec, args.judge_model)
        (out / "runs" / f"{c['name']}--{a}-{i}.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
        print(f"done {c['name']} {a} {i}: {sum(s['pass'] for s in rec['scores'])}/{len(rec['scores'])}, {rec['total_tokens']:,} tokens", flush=True)
        return rec

    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        records = list(ex.map(one, jobs))
    rows = summarise(records)
    (out / "summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    (out / "summary.md").write_text(to_md(rows), encoding="utf-8")
    print(to_md(rows))


if __name__ == "__main__":
    sys.exit(main())
