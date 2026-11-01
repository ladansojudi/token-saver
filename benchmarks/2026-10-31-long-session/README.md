# Long session · 2026-10-31 (approximate)

The skill's main purpose is long working sessions. This run measures one: 10 user messages on one made-up project, the same in both arms.

## Setup

- **Session:** one Claude Code subagent per arm (Opus 5.5), kept alive across turns. The 10 messages move from an interview guide (turns 1–5) to interview synthesis and a dashboard (turns 6–10). Project files: [`project/`](project) (all made up for a course exercise).
- **Arms:** *with* — the agent read `SKILL.md` at the start and followed it all session; *without* — no skill. The installed copy was moved out of `~/.claude/skills` during the run.
- **Hand-off rule:** if an agent offered a fresh chat with a hand-off, the simulated user accepted, and the next messages went to a new agent that received only the hand-off note. The rule applied to both arms; only the *with* arm offered one (after turn 9).
- **Tokens:** the harness reports the agent's context size at the end of each turn and its tool calls. Processed tokens per turn are estimated as (tool calls + 1) × context size, since each request re-sends the context. This is an approximation, used only to compare the arms. Raw numbers: [`usage.tsv`](usage.tsv).
- **Quality:** the final files and the last answer, graded blind by a Claude Haiku subagent ([`packet.md`](packet.md), [`mapping.json`](mapping.json), [`judge.json`](judge.json)). Every quote in both syntheses was also checked mechanically against the interview notes.

## Results

> **Correction (same day):** the token estimate below was replaced by exact per-request usage from the transcripts in the [v1.1 re-run](../2026-10-31-long-session-v1.1/README.md). Exact: **1.30M** input tokens with the skill vs **1.47M** without (11% fewer), and equal when weighted by price (249k each), because the fresh chat writes the cache again.

| | With skill | Without |
|---|---|---|
| Estimated tokens processed, 10 turns (superseded, see above) | **2,173,860** | 2,223,532 |
| Context growth by turn 9 (above the first turn) | **+9.2k** | +12.8k |
| Context for turn 10 | **65.6k** (fresh chat) | 78.9k |
| Time | 206 s | 223 s |
| Fresh-chat offers | 1 (after turn 9) | 0 |
| Quotes not found verbatim in the notes | 0 | 0 |
| Synthesis / dashboard length | 3,105 / 2,349 characters | 4,449 / 3,917 characters |
| Blind checklist, final files + last answer | 12/17 (71%) | **15/17 (88%)** |

Checklist by artifact (with / without): interview guide 2/4 vs 3/4, synthesis 3/5 vs 4/5, dashboard 5/5 vs 5/5, last answer 2/3 vs 3/3.

## What this shows

- **Tokens: about 2% fewer by this estimate; 11% fewer by exact count, equal by price (see the correction above).** The conversation grew about 28% more slowly with the skill, and the fresh chat made the last turn run on 17% less context. Because about 64k of every request is fixed system prompt and tools, the total saving is small over 10 turns. It would grow over longer sessions, but this run does not show that.
- **Quality: slightly worse in this run.** The clearest loss is caused by the skill: after the hand-off, the new chat answered "what's still open?" from the 5-line note alone and missed research question 3. The note pointed to `Dashboard v1.md`, but the new chat did not open it. The synthesis also lost one point for not marking interpretation apart from quotes. The interview-guide difference is likely run-to-run noise: both guides were written at turn 2 with the same rules.
- **Shorter files** with the same facts and no invented quotes.

## Fix suggested by this run

1. In a fresh chat, read the files the hand-off names before answering about status or progress.
2. The hand-off should name the one file that holds the current state (for example the dashboard), not only list approved files.
3. Add "keep what people said apart from interpretation" to the "Never cut" list.

## Limits

- One session per arm, one run: no variance. The judge is a small model. The checklists were written by the skill's author.
- Both arms failed turn 4 the same way (they didn't find `desk-research.md`), so both dashboards say no desk research exists. This is an environment issue, not a skill effect, and it applies to both arms equally.
- Token figures are estimates from context size and tool calls, not billed usage.
