#!/usr/bin/env python3
"""Read-only audit of a Claude setup: what adds tokens to every turn or every session.

Checks installed skills, subagents, CLAUDE.md files and MCP servers, and prints a
Markdown report (or JSON with --json). It never writes, moves or deletes anything
and makes no network calls. Standard library only.

Usage:
    python3 audit_setup.py --home ~ --project .
    python3 audit_setup.py --home ~ --project . --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

DESC_CAP = 1536          # official: description + when_to_use cut at 1,536 chars in the skill listing
SKILL_MD_MAX = 500       # official: keep SKILL.md under 500 lines
CLAUDE_MD_MAX = 200      # official: keep CLAUDE.md under 200 lines
MANY_SKILLS = 10         # judgement call
MANY_MCP = 3             # judgement call

SEVERITY_ORDER = {"turn": 0, "session": 1, "other": 2}


def parse_frontmatter(text):
    """Return a dict of top-level frontmatter fields. Handles `key: value`,
    quoted values and YAML block scalars (`key: >` / `key: |`)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*(\n|$)", text, re.S)
    if not m:
        return {}
    fields, key, buf = {}, None, []

    def flush():
        if key is not None:
            fields[key] = " ".join(s.strip() for s in buf if s.strip())

    for line in m.group(1).splitlines():
        top = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if top and not line.startswith((" ", "\t")):
            flush()
            key, value = top.group(1), top.group(2).strip()
            if value in (">", "|", ">-", "|-", ">+", "|+", ""):
                buf = []
            else:
                buf = [value.strip("\"'")]
        elif key is not None:
            buf.append(line)
    flush()
    return fields


def body_lines(text):
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)
    body = parts[2] if len(parts) == 3 else text
    return len(body.strip("\n").splitlines())


def read(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def scan_skills(folder, scope):
    out = []
    if not folder.is_dir():
        return out
    for skill_md in sorted(folder.glob("*/SKILL.md")):
        text = read(skill_md)
        fm = parse_frontmatter(text)
        listing = (fm.get("description", "") + " " + fm.get("when_to_use", "")).strip()
        out.append({
            "scope": scope,
            "folder": skill_md.parent.name,
            "name": fm.get("name") or skill_md.parent.name,
            "listing_chars": len(listing),
            "skill_md_lines": body_lines(text),
            "model_invocable": fm.get("disable-model-invocation", "").lower() != "true",
            "path": str(skill_md),
        })
    return out


def scan_agents(folder, scope):
    out = []
    if not folder.is_dir():
        return out
    for md in sorted(folder.glob("*.md")):
        fm = parse_frontmatter(read(md))
        out.append({"scope": scope, "name": fm.get("name") or md.stem,
                    "description_chars": len(fm.get("description", "")), "path": str(md)})
    return out


def count_mcp(home, project):
    servers = {}
    pj = project / ".mcp.json"
    try:
        data = json.loads(read(pj) or "{}")
        for name in (data.get("mcpServers") or {}):
            servers[name] = str(pj)
    except ValueError:
        pass
    hj = home / ".claude.json"
    try:
        data = json.loads(read(hj) or "{}")
        for name in (data.get("mcpServers") or {}):
            servers.setdefault(name, str(hj))
        proj = (data.get("projects") or {}).get(str(project.resolve())) or {}
        for name in (proj.get("mcpServers") or {}):
            servers.setdefault(name, str(hj))
    except ValueError:
        pass
    return servers


def audit(home, project):
    home, project = Path(home).expanduser(), Path(project).expanduser()
    skills = scan_skills(home / ".claude" / "skills", "personal") + scan_skills(project / ".claude" / "skills", "project")
    agents = scan_agents(home / ".claude" / "agents", "personal") + scan_agents(project / ".claude" / "agents", "project")
    claude_mds = []
    for p, scope in [(home / ".claude" / "CLAUDE.md", "personal"), (project / "CLAUDE.md", "project"), (project / ".claude" / "CLAUDE.md", "project")]:
        if p.is_file():
            claude_mds.append({"scope": scope, "path": str(p), "lines": len(read(p).splitlines())})
    mcp = count_mcp(home, project)

    findings = []

    def add(kind, severity, official, text, fix):
        findings.append({"kind": kind, "when": severity, "official": official, "finding": text, "fix": fix})

    listed = [s for s in skills if s["model_invocable"]]
    total_listing = sum(s["listing_chars"] for s in listed)
    for s in skills:
        if s["listing_chars"] > DESC_CAP:
            add("skill", "turn", True,
                f"Skill `{s['name']}` ({s['scope']}): description is {s['listing_chars']:,} characters, over the {DESC_CAP:,} cap, so it is cut in the listing and loaded every turn.",
                "Shorten the description and put the main use case first, or remove the skill if you don't use it.")
        if s["skill_md_lines"] >= SKILL_MD_MAX:
            add("skill", "other", True,
                f"Skill `{s['name']}`: SKILL.md body is {s['skill_md_lines']} lines; once loaded it stays in the chat.",
                f"Move reference material into separate files and keep SKILL.md under {SKILL_MD_MAX} lines.")
    if len(listed) > MANY_SKILLS:
        add("skill", "turn", False,
            f"{len(listed)} skills are listed to Claude on every turn ({total_listing:,} description characters in total).",
            "Remove skills you don't use. In Claude Code, `/usage` shows which skills you actually use.")
    by_name = {}
    for s in skills:
        by_name.setdefault(s["name"], []).append(s["scope"])
    for name, scopes in sorted(by_name.items()):
        if "personal" in scopes and "project" in scopes:
            add("skill", "other", True,
                f"Skill `{name}` is installed both personally and in the project; the personal one runs.",
                "Delete one copy so you know which version runs.")
    for a in agents:
        if a["description_chars"] > DESC_CAP:
            add("agent", "turn", False,
                f"Agent `{a['name']}` ({a['scope']}): description is {a['description_chars']:,} characters.",
                "Shorten it: agent descriptions are in context too.")
    for c in claude_mds:
        if c["lines"] >= CLAUDE_MD_MAX:
            add("claude_md", "session", True,
                f"`{c['path']}` is {c['lines']} lines and loads at the start of every session.",
                f"Keep it under {CLAUDE_MD_MAX} lines; move workflows into skills, which load only when used.")
    if len(mcp) > MANY_MCP:
        add("mcp", "turn", False,
            f"{len(mcp)} MCP servers are configured: {', '.join(sorted(mcp))}.",
            "Disable the ones you don't use (Claude Code: `/mcp`).")

    findings.sort(key=lambda f: (SEVERITY_ORDER[f["when"]], not f["official"]))
    return {
        "summary": {
            "skills": len(skills), "skills_listed": len(listed), "listing_chars": total_listing,
            "agents": len(agents), "claude_md_files": len(claude_mds), "mcp_servers": len(mcp),
        },
        "skills": skills, "agents": agents, "claude_md": claude_mds, "mcp_servers": sorted(mcp),
        "findings": findings,
    }


WHEN_LABEL = {"turn": "every turn", "session": "every session", "other": "when used"}


def to_markdown(r):
    s = r["summary"]
    lines = ["# Token audit", "",
             f"- Skills: {s['skills']} installed, {s['skills_listed']} listed to Claude ({s['listing_chars']:,} description characters, sent every turn)",
             f"- Subagents: {s['agents']}",
             f"- CLAUDE.md files: {s['claude_md_files']}",
             f"- MCP servers: {s['mcp_servers']}", ""]
    if not r["findings"]:
        lines += ["No findings. Check `/usage` in Claude Code, or Settings › Usage in the Claude apps, for what you actually use.", ""]
    else:
        lines += ["| # | Costs | Finding | Fix | Basis |", "|---|---|---|---|---|"]
        for i, f in enumerate(r["findings"], 1):
            basis = "official" if f["official"] else "judgement call"
            lines.append(f"| {i} | {WHEN_LABEL[f['when']]} | {f['finding']} | {f['fix']} | {basis} |")
        lines.append("")
    lines += ["This audit only reads files. It does not see claude.ai usage, plugins installed with `/plugin`, or which skills you use.", ""]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--home", default="~", help="home folder that holds .claude/ (default: ~)")
    ap.add_argument("--project", default=".", help="project folder (default: current folder)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    args = ap.parse_args(argv)
    report = audit(args.home, args.project)
    print(json.dumps(report, indent=2) if args.json else to_markdown(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
