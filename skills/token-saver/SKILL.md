---
name: token-saver
description: Keeps Claude's usage low without losing quality. Short answers that keep every source, reading and editing only what the task needs, one batched round of questions, a hand-off to a fresh chat when the conversation grows long, and a read-only audit of the setup that loads tokens on every turn (skills, agents, CLAUDE.md, MCP servers). Use during long working sessions, research, writing and design work, and whenever the user mentions tokens, usage limits, cost, running out, a long or slow chat, or asks to save usage.
license: Apache-2.0. Complete terms in LICENSE.txt
---

# Token saver

Every new message sends the whole conversation again, so long chats, big files and repeated text cost usage on every turn. Project files are cached and cost less when reused, but the cache expires after a period of inactivity. Sources: [references/sources.md](references/sources.md).

The goal is **fewer tokens per useful result** — never fewer facts, sources or checks.

## Never cut

- Source links and quotes the task needs, and "I don't know" when the sources don't say.
- What people said, kept apart from your interpretation and guesses — and marked as such.
- Looking before saying something doesn't exist: list the folder or search for the file first.
- Checks, tests and verification steps.
- Anything the user asked for explicitly.
- Warnings about safety, privacy or accessibility.

If saving tokens would remove one of these, keep it and save elsewhere.

## Answer lean

1. Answer first. No preamble, no restating the question, no closing recap of what you just wrote.
2. Don't paste back text the user or a file already contains. Point to it: "see brief.md, Research question 2".
3. When editing a document, return only the changed part and where it goes, unless the user asks for the full text.
4. Use a table or list only when it is shorter than prose.
5. Need clarification? Ask every question in one message, not one at a time.
6. Follow any format the user asks for ("one line each", a word limit, a table) exactly, in a fresh chat too.

## Work lean

- Read only the files and sections the task needs. Don't re-read a file that is already in this chat unless it changed.
- Research, web search, large attachments, artifacts and multi-step tasks use more usage. Before one the user didn't ask for, say so in one line. Run Research once, with the full prompt.
- Subagents keep verbose work out of the chat, but their requests still count. Use them for big, noisy jobs, not short questions or back-and-forth.
- For a simple task, suggest a lower effort level or a smaller model (Claude Code: `/effort`, `/model`).

## Keep the chat short

A fresh chat pays again for the fixed setup (system prompt, tools, skills) and re-reads files, so it saves usage only once the conversation itself is large. Offer one at a natural break (never mid-task) when:

- the topic changes, or
- the conversation itself has grown large: a context or compaction warning appears, the user says the chat is slow, or `/context` shows messages and files taking about as much room as the fixed setup, or more.

Don't offer one for length alone while the conversation is still small. When you offer it, do all of this in the same message, without asking first:

1. Suggest a new chat with the same name and the next version: `Desk Research v1` → `Desk Research v2`.
2. Write the hand-off, at most 15 lines, using [references/handoff.md](references/handoff.md): goal, the file that holds the current state, decisions, approved files, open questions, next step.
3. In Claude Code: `/rename`, then `/clear` for a fresh start, or `/compact <what to keep>` to continue in the same session.

**Starting from a hand-off:** the note is a pointer, not the full picture. Before answering anything about status, progress or what is still open, read the file it names as the current state.

## Audit the setup

When the user asks why usage runs out, or asks for a token check, run the read-only audit:

```bash
python3 scripts/audit_setup.py --home ~ --project .
```

Report the top findings, each with one fix. What the audit checks and why: [references/audit.md](references/audit.md). Never delete, move or edit the user's files yourself; list the change and let the user decide.

## Where to see usage

- Claude apps: **Settings › Usage** (session and weekly limits).
- Claude Code: `/usage` (breakdown by skills, subagents, plugins and MCP servers, with recommendations) and `/context`.

End a long task with one line: what you skipped to save usage, if anything.
