# Long session, v1.2 · 2026-10-31 (approximate)

A third run of the [long session](../2026-10-31-long-session/README.md), this time with token-saver 1.2.0. Version 1.2 changes three rules:
- a fresh chat is offered for length only once the conversation itself is large;
- the hand-off is written in the same message as the offer, without asking first;
- any format the user asks for is followed exactly.

Only the *with* arm was re-run. It is compared with the same baseline session (*without*) as the two earlier runs.

## Setup

- **The same as the [v1.1 run](../2026-10-31-long-session-v1.1/README.md):** the same project files, the same 10 messages word for word, and the same hand-off rule.
- **Tokens:** exact per-request usage from the agent transcripts. Raw numbers for all four sessions: [`usage.tsv`](usage.tsv).
- **Quality:** the same checklist, graded blind by Claude Haiku **twice**, with the A/B order reversed the second time, to measure the judge's own noise ([`packet1.md`](packet1.md), [`packet2.md`](packet2.md), mappings, [`judge1.json`](judge1.json), [`judge2.json`](judge2.json)). Every quote in the synthesis was also checked mechanically against the interview notes.

## Results

| | v1.0 | v1.1 | **v1.2** | Without |
|---|---|---|---|---|
| Fresh-chat offers | 1 | 1 (+1 turn to ask) | **0** | 0 |
| Model requests | 19 | 23 | **18** | 21 |
| Input tokens, whole session | 1.30M | 1.60M | **1.29M** | 1.47M |
| … vs without | −11% | +9% | **−12%** | — |
| Output tokens | 8.5k | 11.4k | 11.5k | 10.8k |
| Price-weighted tokens¹ | 249k | 300k | 279k (235k adjusted²) | 249k |
| Quotes not found verbatim in the notes | 0 | 0 | 0 | 0 |
| Blind checklist | 12/17 | 12/17 | **14/17, 14/17** | 15, 13, 14, 13 /17 |

¹ Uncached input × 1, cache write × 1.25, cache read × 0.1, output × 5. These are API price ratios, used only to compare the runs.

² In this run, turn 1 wrote 66k tokens to the cache, against about 29k in every other session. The session started after the shared prompt cache had expired, which comes from the test setup, not the skill. With a turn-1 cache write like the others', the weighted figure is about 235k, **about 5% below** the baseline.

Checklist by artifact (v1.2, judge 1 / judge 2):
- interview guide 2/4, 2/4;
- synthesis 4/5, 4/5;
- dashboard 5/5, 5/5;
- last answer 3/3, 3/3.

## What this shows

- **Tokens: 12% fewer input tokens, with nothing lost.**
  - The skill kept the chat lean in every turn.
  - At turn 9 it no longer offered a fresh chat, because the conversation was still small. So the hand-off costs from v1.1 (an extra turn plus a new chat re-reading files) were gone.
- **Quality: the same as without the skill, within judge noise.**
  - Over four judge runs the unchanged baseline files scored between 13 and 15. v1.2 scored 14 in both of its runs.
  - The last answer kept "one line each" and covered every research question (3/3 in both runs; v1.1 got 1/3).
  - Quotes stayed apart from interpretation in both runs (s3).
- **One format slip remains.** The intro script was four sentences against the requested two or three. The agent added a consent line on purpose and said so in its reply, but the file still breaks the request. The skill already says to follow the format the user asks for exactly, so this is the model's judgement call, and both judges marked it down.

## Caveats

- **Desk research.** At turn 4, this run found and read `desk-research.md`. All three earlier sessions, including the baseline, failed to list the folder at that turn. So the v1.2 dashboard could cite desk research for research question 6 and the baseline's could not. The dashboard scored 5/5 for both, so the checklist doesn't reward this, but the files are not a like-for-like comparison.
- **The fresh-chat rule went untested here.** This run tests the "don't offer while the chat is small" side of the rule. No session here grew large enough to check the other side, offering a hand-off when the chat is large.
- **Small sample.** One session per arm. The checklists were written by the skill's author. The judge is a small model.
