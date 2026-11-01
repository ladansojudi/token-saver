I ran a read-only check of `./home` and `./project` and didn't change anything. Here's what uses up your allowance, biggest first:

**Loaded on every message**

1. **5 MCP servers** (figma, linear, notion, slack, old-crm in `project/.mcp.json`). Each one adds its tools to the context. `old-crm` looks like a leftover.
   **Fix:** turn off the ones you don't use day to day with `/mcp`, or remove them from `.mcp.json`. Start with `old-crm`.

2. **The `everything-writer` skill** (`home/.claude/skills/everything-writer/SKILL.md`). Its description is 1,871 characters, which is over the 1,536-character limit. It's sent with every message and gets cut off in the list Claude sees, so the end of it never reaches Claude anyway.
   **Fix:** shorten it to one or two sentences that lead with the main use (for example "Writes UX documents such as personas, research plans and specs"). Or remove the skill if your other writing and research skills already cover it.

3. **13 personal skills**, which add up to about 2,700 characters of descriptions on every message.
   **Fix:** run `/usage` to see which ones you actually use and remove the rest. Several seem to overlap: `research-en`, `research-synthesis`, `user-research`, `competitive-brief` and `everything-writer`.

**Loaded at the start of every session**

4. **`project/CLAUDE.md` is 262 lines**, and it's all under one heading. The guideline is under 200 lines.
   **Fix:** keep only the rules Claude needs every time. Move step-by-step workflows into skills, which load only when they're used.

**Loaded only when used**

5. **The `big-reference` skill's SKILL.md is 620 lines**, and once it loads it stays in the chat.
   **Fix:** move the reference material into separate files in that skill's folder and keep SKILL.md under 500 lines.

6. **`check-skill` exists twice**, in your home folder and in the project. Your personal copy is the one that runs. The project copy says "Old steps", so it looks stale.
   **Fix:** delete `project/.claude/skills/check-skill` so it's clear which version runs.

**Habits that help too**
- Start a fresh chat with `/clear` when you switch tasks, or use `/compact` to shrink a long one. Every message resends the whole conversation.
- For simple tasks, use a lower `/effort` or a smaller `/model`.
- Check `/usage` and `/context` to see where your allowance actually goes.

This check only reads your files. It can't see your claude.ai usage, plugins installed with `/plugin`, or which skills you actually use, so `/usage` is the best next step to confirm items 1 and 3. I can draft a shorter `everything-writer` description or a trimmed `CLAUDE.md` for you to review if you'd like.
