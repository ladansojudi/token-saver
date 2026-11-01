# Token audit

- Skills: 13 installed, 13 listed to Claude (2,748 description characters, sent every turn)
- Subagents: 1
- CLAUDE.md files: 1
- MCP servers: 5

| # | Costs | Finding | Fix | Basis |
|---|---|---|---|---|
| 1 | every turn | Skill `everything-writer` (personal): description is 1,871 characters, over the 1,536 cap, so it is cut in the listing and loaded every turn. | Shorten the description and put the main use case first, or remove the skill if you don't use it. | official |
| 2 | every turn | 13 skills are listed to Claude on every turn (2,748 description characters in total). | Remove skills you don't use. In Claude Code, `/usage` shows which skills you actually use. | judgement call |
| 3 | every turn | 5 MCP servers are configured: figma, linear, notion, old-crm, slack. | Disable the ones you don't use (Claude Code: `/mcp`). | judgement call |
| 4 | every session | `examples/heavy-setup/project/CLAUDE.md` is 262 lines and loads at the start of every session. | Keep it under 200 lines; move workflows into skills, which load only when used. | official |
| 5 | when used | Skill `big-reference`: SKILL.md body is 620 lines; once loaded it stays in the chat. | Move reference material into separate files and keep SKILL.md under 500 lines. | official |
| 6 | when used | Skill `check-skill` is installed both personally and in the project; the personal one runs. | Delete one copy so you know which version runs. | official |

This audit only reads files. It does not see claude.ai usage, plugins installed with `/plugin`, or which skills you use.

