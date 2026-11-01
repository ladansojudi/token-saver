I went through `./home/.claude` and `./project`. I didn't change anything. A few things in your setup add a lot to every conversation for no benefit. Here they are, biggest first.

## 1. `project/CLAUDE.md` is about 13 KB and contains nothing useful (biggest fix)
This file loads into **every session** in this project, so you pay for it on every request. It's 262 lines, and apart from the heading every line is a placeholder:

```
- Remember detail 0 about the Shelfwise project.
- Remember detail 1 about the Shelfwise project.
...
- Remember detail 259 about the Shelfwise project.
```

That's roughly 3,000+ tokens of context that tell Claude nothing.
**Change:** replace it with 10–30 lines of real facts, such as what Shelfwise is, how to run and test it, and conventions Claude keeps getting wrong. If there's nothing real to say yet, delete the file.

## 2. Five MCP servers are on for this project (`project/.mcp.json`)
`figma`, `notion`, `linear`, `slack`, `old-crm`. Each connected server adds its tool definitions to the context, and they all start every time you open the project.
**Change:**
- Remove `old-crm`. The name suggests you don't use it anymore.
- Remove any of the others you don't actually use *in this project*. Turn on ones you only need sometimes when you need them (via `/mcp`), or move them to a different project.

## 3. The `everything-writer` skill description is the same paragraph pasted 6 times
`home/.claude/skills/everything-writer/SKILL.md`: skill descriptions are loaded into every session so Claude knows when to use them. This one is about 1,900 characters, about 450 tokens, every session. The paragraph only needs to appear once. "Every kind of document… any tone, for any audience" is also so broad that the skill will trigger on almost any writing request.
**Change:** cut it to one specific sentence about when to use it.

## 4. `big-reference` skill is about 25 KB of one repeated rule
`home/.claude/skills/big-reference/SKILL.md` has 620 lines that all say "keep spacing on an 8 px grid". It only costs anything when it's used, but then it adds about 6,000 tokens each time. Its description ("Huge reference skill used for design systems") is vague enough that it may get pulled into any design task.
**Change:** reduce it to the rules you actually mean (that might be a single line), and give it a specific description. Or delete it and put "use an 8 px spacing grid" in CLAUDE.md.

## 5. Smaller cleanups
- **Duplicate `check-skill`**: one copy is in `home/.claude/skills/` and an older one in `project/.claude/skills/` ("Old steps"). Delete the outdated project copy so there's one clear version.
- **Placeholder descriptions**: most of your other skills have descriptions like "Short description for X. Use when the task matches X." They cost little, but Claude can't tell when to use them, so they get used at the wrong times or not at all. Give each one a real sentence, and delete any you don't use. `research-en`, `research-synthesis` and `user-research` look like they overlap.
- `web-search-agent` is fine as is.

## Habits that help as well
- Run `/context` at the start of a session to see what's taking up space. After the fixes above it should drop noticeably.
- Use `/clear` when you switch tasks. Long conversations re-send all their history on every message.
- Use a lighter model for simple tasks if your plan lets you choose (`/model`).

I didn't find a `settings.json` in either folder, so I couldn't check your model or other settings, and I can't see your actual usage history. Everything above is based only on the files.

If you'd like, I can draft a trimmed `CLAUDE.md` and a cleaned-up `.mcp.json` for you to look over.
