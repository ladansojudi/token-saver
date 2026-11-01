# Long session, v1.1 · 2026-10-31 (approximate)

A re-run of the [long session](../2026-10-31-long-session/README.md) with token-saver 1.1.0, which added three fixes:
- name the current-state file in a hand-off;
- read that file in the fresh chat before answering about progress;
- keep what people said apart from interpretation, and look for a file before saying it doesn't exist.

Only the *with* arm was re-run. It is compared with the same baseline session (*without*) as before.

## Setup

- **Session, project files and messages:** the same as the first run ([`../2026-10-31-long-session/project`](../2026-10-31-long-session/project)).
- **Hand-off rule:** as before.
  - At turn 9 the agent offered a fresh chat but asked before writing the hand-off.
  - The simulated user said yes, which added a turn (**9b**). It is counted against the skill.
  - Turn 10 went to a new agent that received only the hand-off note.
- **Tokens: exact, from the transcripts.** Every model request's usage was read from the agent transcripts for all three sessions (v1.0, v1.1, baseline): input (uncached, cache write, cache read) and output.
  - Raw numbers: [`usage.tsv`](usage.tsv).
  - This replaces the estimate used in the first report (see "Correction" below).
- **Quality:** the final files and the last answer were graded blind by a Claude Haiku subagent against the same checklist as before ([`packet.md`](packet.md), [`mapping.json`](mapping.json), [`judge.json`](judge.json)). Every quote in the synthesis was also checked mechanically against the interview notes.

## Results

| | v1.0 | **v1.1** | Without |
|---|---|---|---|
| Model requests | 19 | 23 | 21 |
| Input tokens processed, whole session | 1.30M | 1.60M | 1.47M |
| … turns 1–9 only | 1.18M | **1.19M** | 1.39M |
| … hand-off and the turn after | 0.12M | 0.41M | 0.08M |
| Output tokens | 8.5k | 11.4k | 10.8k |
| Price-weighted tokens¹ | 249k | 300k | 249k |
| Quotes not found verbatim in the notes | 0 | 0 | 0 |
| Blind checklist, this judge run | — | 12/17 | 13/17 |

¹ Uncached input × 1, cache write × 1.25, cache read × 0.1, output × 5. These are API price ratios, used only to compare the arms; how a Claude subscription counts usage is not published at this level of detail.

Checklist by artifact, v1.1 / without:

| Artifact | v1.1 | Without |
|---|---|---|
| Interview guide | 2/4 | 2/4 |
| Synthesis | **4/5** | 3/5 |
| Dashboard | 5/5 | 5/5 |
| Last answer | 1/3 | **3/3** |

## What this shows

### The fixes worked
- **Every open question was covered.** The fresh chat opened `Dashboard v1.md` before answering, and its last answer covered all six research questions (f2 passed). In v1.0 it had missed research question 3.
- **Interpretation stayed separate from quotes.** The synthesis kept participants' words apart from interpretation (s3 passed). v1.0 failed this.
- **No false "it doesn't exist".** At turn 4 the agent said "I couldn't check" instead of "it doesn't exist".

### The last answer got worse in format
Its points ran to several sentences instead of one line each, and research questions 5 and 6 were described only as "no research yet". That cost 2 of the 3 points.

### Tokens: the hand-off cost more than it saved
- **Up to turn 9, the skill saved 15%** (1.19M vs 1.39M input tokens). About 63k of that gap comes from one extra request the baseline needed in turn 1 because of the test harness. Without it, the saving is about 10%.
- **The hand-off then cost 0.41M**, against 0.08M for the baseline's last turn.
  - Asking "shall I write it?" added a whole turn (155k).
  - The fresh chat had to pay again for the fixed setup (system prompt, tools and the skill), about 64k per request. It then made four requests to read the skill, the dashboard and the brief (260k).
- **Why it didn't pay off:**
  - At turn 9 the conversation itself was only about 13k tokens on top of about 64k of fixed setup.
  - A fresh chat removes only the conversation part, so it saves about 13k per later turn.
  - The setup and file reads cost more than that.
  - A hand-off pays off only when the conversation part is large, or when many turns follow.

### Judge noise is about ±2 points
The baseline files are unchanged from the first run, but this judge run scored them 13/17 instead of 15/17. Differences of one or two points between the arms are within that noise.

## Fix suggested by this run

1. When a hand-off is due, write it in the same message as the offer. Don't ask first.
2. Offer a fresh chat for length only when the conversation itself is large. In Claude Code, `/context` shows how much is messages and how much is fixed setup. A topic change still justifies a fresh chat.
3. The "one line each" format is something the user asked for. Keep it even in a fresh chat.

## Correction to the first long-session report

The first report estimated tokens as (tool calls + 1) × context size. With exact per-request usage from the transcripts:
- v1.0 processed **1.30M** input tokens and the baseline **1.47M**. That is 11% fewer, not 2% fewer.
- Price-weighted, the two are equal (249k each), because a fresh chat writes the cache again.
- The v1.0 report has been updated.

## Limits

- One session per arm and one run, so there is no variance across sessions. The judge varies by about ±2 points on identical files.
- The checklists were written by the skill's author.
- The fixed setup here (about 64k tokens) is a Claude Code subagent's. A regular Claude Code session or claude.ai has a different setup size, so the break-even point for a hand-off is different there.
