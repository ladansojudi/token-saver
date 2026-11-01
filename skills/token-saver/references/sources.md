# Sources

Every rule in `SKILL.md` comes from one of these official Anthropic pages. Quotes are verbatim. Checked 2026-10-31.

## Usage limit best practices (Claude Help Center)

<https://support.claude.com/en/articles/9797557-usage-limit-best-practices>

| Rule in SKILL.md | Quote |
|---|---|
| One message, all questions | "If you have multiple related tasks or questions, group them in a single message." |
| Context up front | "Include relevant context to help Claude understand your needs better." |
| Point to it, don't repeat it | "Refer back to previous information instead of repeating it." |
| Project files are cheaper | "cached portions count less against your limits than new content." |
| The cache expires | "Caches expire after a period of inactivity." / "your first message counts that content in full again." |
| What uses more | "Message length", "File attachment size", "Current conversation length", "Tool usage (e.g., Research, web search)", "Model choice", "Effort level", "Artifact creation and usage", "Multi-step tasks, like running code, creating files, or browsing websites" |
| Research tasks | "Clearly define your research question and focus areas initially." |
| Where to look | "navigate to Settings > Usage" |

## Manage costs effectively (Claude Code docs)

<https://code.claude.com/docs/en/costs>

| Rule in SKILL.md | Quote |
|---|---|
| Whole conversation every time | "Claude Code sends your full conversation with every request" |
| Fresh chat between tasks | "Use `/clear` to start fresh when switching to unrelated work. Stale context wastes tokens on every subsequent message." |
| Keep the name | "Use `/rename` before clearing so you can find the session later, then `/resume` to return to it." |
| Compact with a focus | "`/compact Focus on code samples and API usage` tells Claude what to preserve during summarization." |
| CLAUDE.md size | "Aim to keep CLAUDE.md under 200 lines by including only essentials." |
| Workflows belong in skills | "Skills load on-demand only when invoked, so moving specialized instructions into skills keeps your base context smaller." |
| Subagents | "the verbose output stays in the subagent's context while only a summary returns" / "The subagent's own requests still draw on your usage." |
| Unused MCP servers | "Run `/mcp` to see configured servers and disable any you're not actively using." |
| Effort | "you can reduce costs by lowering the effort level with `/effort`" |
| Specific prompts | "Vague requests like 'improve this codebase' trigger broad scanning." |
| Where to look | `/usage` shows "recent usage attributed to skills, subagents, plugins, and individual MCP servers" with recommendations; "Run `/context` to see what's consuming space." |

## Extend Claude with skills (Claude Code docs)

<https://code.claude.com/docs/en/skills>

| Rule | Quote |
|---|---|
| Installed skills cost every turn | "Every skill in the skill listing adds to your context on every turn, whether or not Claude ever uses it." |
| Description cap | "the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing" |
| A loaded skill stays | "Once a skill loads, its content stays in context across turns, so every line is a recurring token cost." |
| Length | "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files." |
| Name clash | "personal over project" |

## Not from an official source

- The 15-line hand-off and the `Name v1 → v2` chat naming are this skill's own conventions.
- The audit thresholds that are not quoted above (for example, "more than 10 installed skills") are judgement calls, marked as such in the report.
