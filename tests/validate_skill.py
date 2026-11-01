#!/usr/bin/env python3
"""Check every skills/*/SKILL.md against the Agent Skills frontmatter rules.

Rules (from Anthropic's skill authoring best practices):
  - name: required, <= 64 chars, lowercase letters/digits/hyphens, no "anthropic"/"claude"
  - description: required, <= 1024 chars, no XML tags
  - body: under 500 lines
  - every relative Markdown link in SKILL.md points to an existing file

Standard library only. Exits 1 on any problem.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return fields


def check(skill_md: Path) -> list:
    problems = []
    text = skill_md.read_text(encoding="utf-8")
    fm = frontmatter(text)
    name, desc = fm.get("name", ""), fm.get("description", "")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        problems.append(f"name {name!r} must be 1-64 lowercase letters, digits or hyphens")
    if re.search(r"anthropic|claude", name):
        problems.append("name must not contain reserved words 'anthropic' or 'claude'")
    if name and name != skill_md.parent.name:
        problems.append(f"name {name!r} should match folder {skill_md.parent.name!r}")
    if not desc:
        problems.append("description is required")
    if len(desc) > 1024:
        problems.append(f"description is {len(desc)} chars (max 1024)")
    if re.search(r"<[a-zA-Z/][^>]*>", desc):
        problems.append("description must not contain XML tags")
    body_lines = text.split("\n---\n", 1)[-1].count("\n")
    if body_lines >= 500:
        problems.append(f"body is {body_lines} lines (keep under 500)")
    for link in re.findall(r"\]\(([^)#:]+)\)", text):
        if not (skill_md.parent / link).exists():
            problems.append(f"broken link: {link}")
    return problems


def main() -> int:
    skills = sorted(ROOT.glob("skills/*/SKILL.md"))
    if not skills:
        print("no skills/*/SKILL.md found")
        return 1
    failed = False
    for s in skills:
        problems = check(s)
        rel = s.relative_to(ROOT)
        if problems:
            failed = True
            for p in problems:
                print(f"FAIL {rel}: {p}")
        else:
            print(f"OK   {rel}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
