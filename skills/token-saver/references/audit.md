# The setup audit

`scripts/audit_setup.py` reads your Claude setup and lists what adds tokens to every turn or every session. It only reads files: it never changes, moves or deletes anything, and it makes no network calls. Standard library only.

```bash
python3 scripts/audit_setup.py --home ~ --project .          # Markdown report
python3 scripts/audit_setup.py --home ~ --project . --json   # machine-readable
```

## What it checks

| Check | Why it costs | Flagged when | Source |
|---|---|---|---|
| Installed skills (`~/.claude/skills`, `<project>/.claude/skills`) | Every skill's description is in context on every turn | Description + `when_to_use` over 1,536 characters (it gets cut) | Official |
| | | More than 10 skills installed | Judgement call |
| `SKILL.md` length | A loaded skill stays in context for the rest of the chat | 500 lines or more | Official |
| Same skill name in personal and project folders | The personal one wins; the project copy is dead weight | Any clash | Official |
| Subagents (`~/.claude/agents`, `<project>/.claude/agents`) | Their descriptions are in context too | Description over 1,536 characters | Judgement call (same cap as skills) |
| `CLAUDE.md` (`~/.claude/CLAUDE.md`, `<project>/CLAUDE.md`, `<project>/.claude/CLAUDE.md`) | Loaded at the start of every session | 200 lines or more | Official |
| MCP servers (`<project>/.mcp.json`, `~/.claude.json`) | Each server adds tool names and instructions | More than 3 servers | Judgement call |

## What it can't see

- Usage on claude.ai or in the Claude desktop chat. Use **Settings › Usage** there.
- Which skills you actually use. In Claude Code, `/usage` shows the share of recent usage per skill, subagent, plugin and MCP server.
- Plugins installed through `/plugin`. Run `/plugin` to list them.

## How to report the result

1. Start with the finding that applies to every turn (skills, agents), then every session (CLAUDE.md), then the rest.
2. Give each finding one fix, for example "Remove `old-skill` if you don't use it: its 1,900-character description is cut and loaded every turn."
3. Say which thresholds are judgement calls.
4. Let the user make every change. Show the command or the edit; don't run it.
