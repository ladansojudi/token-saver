# Approximate evaluation · 2026-10-31

A first, small measurement. Read the limits before the numbers.

## Setup

- **Runner:** Claude Code subagents (general-purpose, same model as the parent session, Opus 5.5), because `claude plugin eval` is in early access and headless `claude -p` was not signed in.
- **Arms:** 4 cases × 2 arms × 1 run = 8 runs. In the *with* arm the agent was told to read `SKILL.md` first and follow it, so this measures the skill **when it loads** (best case), not whether Claude picks it up by itself. The installed copy was moved out of `~/.claude/skills` during the runs, so the *without* arm never saw it.
- **Judge:** one Claude Haiku subagent, blind: replies were labelled A/B at random ([`mapping.json`](mapping.json)) and graded against each case's checklist ([`packet.md`](packet.md), raw verdicts in [`judge.json`](judge.json)).
- **Tokens and time:** the subagent totals the harness reports ([`usage.tsv`](usage.tsv)). Each total includes about 60k tokens of fixed system prompt and tools, the same in both arms.

## Results

| Case | Arm | Checklist (judge) | Checklist (corrected) | Tokens | Seconds | Reply characters |
|---|---|---|---|---|---|---|
| handoff-long-chat | with | 6/6 | 6/6 | 67,990 | 24.0 | 1,415 |
| | without | 5/6 | 5/6 | 64,590 | 12.6 | 1,385 |
| edit-only-changed-part | with | 3/4 | 4/4 | 65,909 | 7.1 | 241 |
| | without | 2/4 | 3/4 | 64,282 | 7.5 | 296 |
| audit-heavy-setup | with | 6/6 | 6/6 | 68,706 | 31.7 | 2,676 |
| | without | 2/6 | 2/6 | 75,192 | 37.3 | 3,697 |
| short-answer-keeps-sources | with | 3/4 | 3/4 | 65,736 | 6.3 | 558 |
| | without | 3/4 | 3/4 | 64,147 | 7.1 | 586 |
| **Total** | **with** | **18/20 (90%)** | **19/20 (95%)** | **268,341** | | **4,890** |
| | **without** | **12/20 (60%)** | **13/20 (65%)** | **268,211** | | **5,964** |

**Correction:** in `edit-only-changed-part` the judge failed both replies on "does not print the whole brief back". The packet showed the final `brief.md` under each reply, and the judge took it for part of the reply. The replies themselves are 241 and 296 characters and do not reprint the brief, so that item is corrected to pass for both.

## What this shows

- **Quality:** with the skill loaded, replies met more of the checklist (95% vs 65%). Most of the gap is the audit case (6/6 vs 2/6) and the hand-off naming (`Desk Research v2`).
- **Tokens on a single short task: no saving.** Totals are equal (+0.05%). Reading `SKILL.md` adds about 1.5–3.5k tokens to a short task; the audit case was 6.5k tokens (9%) cheaper with the skill because it ran the script instead of exploring the files.
- **Replies were about 18% shorter** in total (4,890 vs 5,964 characters), almost all from the audit reply.
- **Not measured:** savings across a long session (fresh chats, pointing instead of pasting, fewer re-reads), which is where the skill is meant to pay off. That needs a multi-turn test.

## Limits

- One run per arm: no variance, so treat every number as a direction.
- The checklists were written together with the skill, so some items reward its wording (for example, citing the 1,536-character cap or naming `/usage`). The *without* audit reply found most of the same problems but did not cite the limits.
- The *with* arm was told to load the skill; in real use Claude decides from the description.
- The judge is a small model and made one clear mistake (corrected above).
