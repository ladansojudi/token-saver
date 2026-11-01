# Grading packet

Grade every reply against its checklist. Replies are labelled A and B; you don't know how they were produced. Judge each one on its own.


---

## Case: handoff-long-chat

**User's request:**

this chat ("Desk Research v1") has gotten really long and slow. so far: research questions 1-4 came back "Not found", we found 2 sources for question 6 (they're in Desk Research v1.md), question 5 isn't searched yet, and we decided to keep external research separate from user evidence. check-skill hasn't been run yet. what should i do now?

**A good result:** Suggests continuing in a new chat named "Desk Research v2" instead of carrying on here, and writes a short hand-off (at most 15 lines) that points to files instead of copying them: goal, decisions, approved files, open questions, next step. Does not search again for the questions already marked "Not found".

**Checklist:**
- `01-suggests-new-chat-v2`: Suggests continuing in a new chat named "Desk Research v2" (same name, next version)
- `02-handoff-at-most-15-lines`: Gives a hand-off note of at most 15 lines
- `03-handoff-points-to-files`: The hand-off names Desk Research v1.md as a file instead of copying the sources into the note
- `04-keeps-decision-and-open-question`: The hand-off keeps the decision to separate external research from user evidence, and lists question 5 as still open
- `05-does-not-redo-not-found`: Says not to search questions 1-4 again, or otherwise avoids redoing them
- `06-next-step-check-skill`: Names running check-skill as the next step (or as not done yet)

### Reply A

````
Start a fresh chat now. Nothing is half-done, so this is a good place to stop, and a long chat slows down because every new message sends the whole conversation again.

1. **Rename and clear.** Call the new chat **Desk Research v2**. In Claude Code, run `/rename Desk Research v2` and then `/clear`. If you'd rather stay in this session, run `/compact` and paste the note below as what to keep.
2. **Paste this as your first message in the new chat:**

```markdown
# Hand-off: Desk Research v1 → v2

Goal: answer research questions 1–6 from published sources.
Decided: keep external research separate from user evidence.
Approved files: Desk Research v1.md
Open questions: question 5 — not searched yet.
Not done yet: check-skill pass on the 2 question 6 sources.
Next step: run check-skill on the question 6 sources in Desk Research v1.md, then search question 5.
Do not repeat: questions 1–4 came back "Not found"; don't search them again.
```

3. **Check that Desk Research v1.md is saved before you clear.** It isn't in this project folder, which is empty. If it only exists inside this chat, the 2 sources for question 6 will be lost.

I wrote the "Goal" line myself, so correct it if it's off. If you have a brief or other project files, add their names to "Approved files".

In the new chat, run check-skill first so the sources you already have are checked before you look for more. Then search question 5.
````

### Reply B

````
Start a fresh chat. Long chats get slow, and your progress is easy to carry over.

**One thing to fix first:** I couldn't find `Desk Research v1.md` in this project folder. The folder is empty. Before you leave this chat, make sure that file is saved where the new chat can open it, or copy the two question 6 sources out of it. Otherwise the new chat won't have them.

**Then paste this into the new chat:**

> Continuing desk research from a previous chat ("Desk Research v1").
>
> Status so far:
> - Q1–Q4: searched, result "Not found". Don't search these again.
> - Q5: not searched yet.
> - Q6: 2 sources found. They're in `Desk Research v1.md` [attach the file or paste the sources].
> - check-skill: not run yet.
>
> Decision: keep external research separate from user evidence. Don't merge them.
>
> Next: search Q5, then run check-skill on Q1–Q6.

**Order in the new chat:**
1. Search question 5. It's the only question that hasn't been searched.
2. Run check-skill once all six have a result, so it checks everything in one pass. If check-skill is only meant for found sources, you can run it on question 6 now.
3. Keep questions 1–4 as "Not found" unless you choose to try new search terms. Don't let the new chat search them again by accident.

Want me to tidy the handoff note before you paste it, or add the full research questions so the new chat has the exact wording?
````

---

## Case: edit-only-changed-part

**User's request:**

in brief.md, the "Why now" part is wrong. the company actually hears that the stock in the app is wrong and that numbers don't match after a delivery, and they don't know where the problem comes from. fix it

Input files: brief.md

**A good result:** Rewrites only the "Why now" section of brief.md so it says users talk about wrong stock and mismatches after deliveries, and shows only that section (or edits only that section in the file). Does not print the whole brief back and keeps the other sections unchanged.

**Checklist:**
- `01-why-now-says-mismatch`: The new "Why now" text says users report wrong stock or mismatches after deliveries and that the cause is unknown
- `02-no-full-brief-reprint`: The reply does not print the whole brief back; it shows only the changed section (or a short confirmation of the edit)
- `03-other-sections-unchanged`: The other sections of brief.md (Company and app, Our scope, Scenario, Current flow) are unchanged
- `04-no-preamble-or-recap`: The reply has no preamble restating the request and no closing recap

### Reply A

````
I fixed the "Why now" section in brief.md. It now says:

> Customers say the stock in the app is wrong and the numbers don't match after a delivery. We don't know yet where the problem comes from.

That replaces "Customers say the app is hard to use." I didn't change anything else in the brief.
````

Final brief.md after the run:

```
# Shelfwise brief

## Company and app
Shelfwise makes a desktop app that small shops use to track stock in the stockroom and on the shelves.

## Why now
Customers say the stock in the app is wrong and the numbers don't match after a delivery. We don't know yet where the problem comes from.

## Our scope
Only the flow for receiving a delivery from a supplier and recording it in stock. Sales, reports and ordering are out of scope.

## Scenario (made up, not evidence)
Reza counts boxes at the shelf, then opens the purchase order at the computer. One item is short and one was never ordered.

## Current flow
1. Open the purchase order 2. Count what arrived 3. Compare with the order 4. Record differences 5. Confirm

```

### Reply B

````
I fixed the "Why now" section in brief.md. It now says:

> Customers say the stock in the app is wrong and the numbers don't match after a delivery. We don't yet know where the problem comes from.

I didn't change anything else in the file.
````

Final brief.md after the run:

```
# Shelfwise brief

## Company and app
Shelfwise makes a desktop app that small shops use to track stock in the stockroom and on the shelves.

## Why now
Customers say the stock in the app is wrong and the numbers don't match after a delivery. We don't yet know where the problem comes from.

## Our scope
Only the flow for receiving a delivery from a supplier and recording it in stock. Sales, reports and ordering are out of scope.

## Scenario (made up, not evidence)
Reza counts boxes at the shelf, then opens the purchase order at the computer. One item is short and one was never ordered.

## Current flow
1. Open the purchase order 2. Count what arrived 3. Compare with the order 4. Record differences 5. Confirm

```

---

## Case: audit-heavy-setup

**User's request:**

my claude usage runs out really fast lately. can you check my setup and tell me what to change? my home folder is ./home and my project is ./project

**A good result:** Runs the read-only audit on ./home and ./project. Reports the 1,871-character skill description that is cut and loaded every turn, the 13 listed skills, the 5 MCP servers, the 262-line CLAUDE.md, the 620-line SKILL.md and the duplicated check-skill. Gives one fix per finding, says which thresholds are judgement calls, points to /usage, and does not delete or edit any file.

**Checklist:**
- `01-flags-long-description`: Flags the everything-writer skill description as too long (over 1,536 characters) and loaded on every turn
- `02-flags-claude-md`: Flags project/CLAUDE.md (about 262 lines) as over the 200-line guideline
- `03-flags-mcp-and-skill-count`: Mentions the 5 MCP servers and the number of installed skills as things to trim
- `04-one-fix-per-finding`: Gives a concrete fix for each finding
- `05-no-files-changed`: Does not delete, move or edit any file under ./home or ./project
- `06-points-to-usage`: Points to /usage (Claude Code) or Settings › Usage to see actual usage

### Reply A

````
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
````

Files changed during the run: none.

### Reply B

````
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
````

Files changed during the run: none.

---

## Case: short-answer-keeps-sources

**User's request:**

quick one, keep it short: what does our desk research say about stock accuracy, and about how other stock apps handle deliveries?

Input files: desk-research.md

**A good result:** A short answer (two or three sentences) based only on desk-research.md: records were inaccurate for about 65% of audited items, errors were common for frequently delivered items, with the source link kept. Says nothing was found for other stock apps (question 5). No preamble, no padding, no invented facts.

**Checklist:**
- `01-short`: The answer is at most about four sentences (or a list of at most four short items)
- `02-keeps-source-link`: Keeps the source link https://example.org/study-inventory-accuracy (or names it clearly as the source)
- `03-says-not-found`: Says nothing was found about how other stock apps handle deliveries (question 5)
- `04-no-invented-facts`: States no figures or claims that are not in desk-research.md

### Reply A

````
**Stock accuracy:** A retail study found that inventory records were wrong for about 65% of the items it audited. The same study found that record errors were common for items with frequent deliveries. Source: https://example.org/study-inventory-accuracy

**How other stock apps handle deliveries:** The research doesn't cover this. The only delivery finding is the one above, and it's about record errors, not about how other apps work. The file also has a "Question 5" marked "Not found". That may be this question, but the file lists questions only by number, so I can't confirm it.
````

### Reply B

````
**Stock accuracy (Question 6):** A retail study found inventory records were wrong for about 65% of the items it audited. Errors were especially common for items that get frequent deliveries. Source: https://example.org/study-inventory-accuracy

**How other stock apps handle deliveries (Question 5):** I don't know. The desk research has no answer here, and Question 5 is marked "Not found". The only finding that touches deliveries is the one above about frequently delivered items. It comes from a retail study and says nothing about how other apps work.
````