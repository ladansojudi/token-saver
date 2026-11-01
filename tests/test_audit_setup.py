"""Unit tests for skills/token-saver/scripts/audit_setup.py (standard library only)."""

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("audit_setup", ROOT / "skills/token-saver/scripts/audit_setup.py")
audit_setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_setup)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def skill(root, name, description, body_lines=3, extra=""):
    body = "\n".join(f"line {i}" for i in range(body_lines))
    write(root / name / "SKILL.md", f"---\nname: {name}\ndescription: {description}\n{extra}---\n\n{body}\n")


class FrontmatterTests(unittest.TestCase):
    def test_plain_and_quoted_values(self):
        fm = audit_setup.parse_frontmatter('---\nname: a\ndescription: "Does a thing"\n---\nbody')
        self.assertEqual(fm["name"], "a")
        self.assertEqual(fm["description"], "Does a thing")

    def test_block_scalar_is_joined(self):
        fm = audit_setup.parse_frontmatter("---\nname: a\ndescription: >\n  first line\n  second line\nlicense: MIT\n---\n")
        self.assertEqual(fm["description"], "first line second line")
        self.assertEqual(fm["license"], "MIT")

    def test_no_frontmatter(self):
        self.assertEqual(audit_setup.parse_frontmatter("# just text"), {})


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.home, self.project = base / "home", base / "project"
        self.home.mkdir()
        self.project.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def kinds(self, report):
        return [f["finding"] for f in report["findings"]]

    def test_clean_setup_has_no_findings(self):
        skill(self.home / ".claude/skills", "small", "Short description.")
        report = audit_setup.audit(self.home, self.project)
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["summary"]["skills"], 1)

    def test_long_description_is_flagged_as_every_turn(self):
        skill(self.home / ".claude/skills", "wordy", "x" * 1600)
        f = audit_setup.audit(self.home, self.project)["findings"][0]
        self.assertEqual(f["when"], "turn")
        self.assertTrue(f["official"])
        self.assertIn("wordy", f["finding"])

    def test_when_to_use_counts_toward_cap(self):
        skill(self.home / ".claude/skills", "split", "y" * 1000, extra="when_to_use: " + "z" * 600 + "\n")
        self.assertTrue(any("split" in t for t in self.kinds(audit_setup.audit(self.home, self.project))))

    def test_long_skill_md(self):
        skill(self.home / ".claude/skills", "huge", "Fine.", body_lines=520)
        self.assertTrue(any("520 lines" in t for t in self.kinds(audit_setup.audit(self.home, self.project))))

    def test_many_skills_is_a_judgement_call(self):
        for i in range(11):
            skill(self.home / ".claude/skills", f"s{i}", "Short.")
        f = [x for x in audit_setup.audit(self.home, self.project)["findings"] if "listed" in x["finding"]][0]
        self.assertFalse(f["official"])

    def test_disabled_skills_are_not_counted_as_listed(self):
        for i in range(11):
            skill(self.home / ".claude/skills", f"s{i}", "Short.", extra="disable-model-invocation: true\n")
        report = audit_setup.audit(self.home, self.project)
        self.assertEqual(report["summary"]["skills_listed"], 0)
        self.assertEqual(report["findings"], [])

    def test_name_clash_between_personal_and_project(self):
        skill(self.home / ".claude/skills", "dup", "Personal.")
        skill(self.project / ".claude/skills", "dup", "Project.")
        self.assertTrue(any("personal one runs" in t for t in self.kinds(audit_setup.audit(self.home, self.project))))

    def test_long_claude_md_is_every_session(self):
        write(self.project / "CLAUDE.md", "\n".join(["- note"] * 210))
        f = audit_setup.audit(self.home, self.project)["findings"][0]
        self.assertEqual(f["when"], "session")

    def test_mcp_servers_from_both_files(self):
        write(self.project / ".mcp.json", json.dumps({"mcpServers": {"a": {}, "b": {}}}))
        write(self.home / ".claude.json", json.dumps({"mcpServers": {"c": {}}, "projects": {str(self.project.resolve()): {"mcpServers": {"d": {}}}}}))
        report = audit_setup.audit(self.home, self.project)
        self.assertEqual(report["mcp_servers"], ["a", "b", "c", "d"])
        self.assertTrue(any("4 MCP servers" in t for t in self.kinds(report)))

    def test_broken_json_is_ignored(self):
        write(self.project / ".mcp.json", "{not json")
        self.assertEqual(audit_setup.audit(self.home, self.project)["mcp_servers"], [])

    def test_audit_is_read_only(self):
        skill(self.home / ".claude/skills", "wordy", "x" * 1600)
        write(self.project / "CLAUDE.md", "\n".join(["- note"] * 210))
        before = {p: p.stat().st_mtime_ns for p in Path(self.tmp.name).rglob("*")}
        audit_setup.to_markdown(audit_setup.audit(self.home, self.project))
        after = {p: p.stat().st_mtime_ns for p in Path(self.tmp.name).rglob("*")}
        self.assertEqual(before, after)

    def test_findings_sorted_turn_before_session(self):
        write(self.project / "CLAUDE.md", "\n".join(["- note"] * 210))
        skill(self.home / ".claude/skills", "wordy", "x" * 1600)
        whens = [f["when"] for f in audit_setup.audit(self.home, self.project)["findings"]]
        self.assertEqual(whens, sorted(whens, key=audit_setup.SEVERITY_ORDER.get))

    def test_cli_markdown_and_json(self):
        skill(self.home / ".claude/skills", "wordy", "x" * 1600)
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            audit_setup.main(["--home", str(self.home), "--project", str(self.project)])
        self.assertIn("# Token audit", buf.getvalue())
        buf = io.StringIO()
        with redirect_stdout(buf):
            audit_setup.main(["--home", str(self.home), "--project", str(self.project), "--json"])
        self.assertEqual(json.loads(buf.getvalue())["summary"]["skills"], 1)


class ExampleTests(unittest.TestCase):
    def test_example_report_is_current(self):
        ex = ROOT / "examples/heavy-setup"
        cwd = os.getcwd()
        os.chdir(ROOT)
        try:
            md = audit_setup.to_markdown(audit_setup.audit("examples/heavy-setup/home", "examples/heavy-setup/project"))
        finally:
            os.chdir(cwd)
        self.assertEqual(md.strip(), (ex / "report.md").read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    unittest.main()
