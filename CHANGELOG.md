# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [1.2.0] - 2026-10-31

### Changed
- A fresh chat is offered for length only once the conversation itself is large (about the size of the fixed setup, or a context warning, or the user says it is slow). A topic change still qualifies. The 1.1.0 long session showed a hand-off in a small chat costing more than it saved.
- The hand-off is written in the same message as the offer, without asking first. Asking added a whole turn.
- Any format the user asks for ("one line each", a word limit) is followed exactly, in a fresh chat too.

### Measured
- Long-session re-run (`benchmarks/2026-10-31-long-session-v1.2`): 12% fewer input tokens than without the skill (1.29M vs 1.47M), and the same quality within judge noise (14/17 in two blind runs; the unchanged baseline scored 13–15 over four).
  - No fresh chat was offered while the chat was small.
  - The last answer kept "one line each" and covered every research question.

## [1.1.0] - 2026-10-31

### Changed
- A hand-off now names the one file that holds the current state, and a fresh chat reads that file before answering about progress or what is still open. The long-session test showed a fresh chat answering from the note alone and missing a research question.
- "Never cut" now includes keeping what people said apart from interpretation, and looking for a file before saying it doesn't exist.

### Measured
- Long-session re-run (`benchmarks/2026-10-31-long-session-v1.1`):
  - **Fixes worked:** the fresh chat read the dashboard and covered every open question, and the synthesis kept quotes apart from interpretation.
  - **Tokens:** the skill saved 15% over turns 1–9, but the hand-off cost more than it saved, so the whole session used 9% more input tokens than without the skill.
- Token counts in both long-session reports now use exact per-request usage from the transcripts instead of an estimate. The 1.0.0 run was 11% lower than without the skill, not 2%.

## [1.0.0] - 2026-10-31

### Added
- `token-saver` skill: lean answers, lean work, hand-off to a fresh chat, and a setup audit, each rule traced to an official Anthropic page.
- "Never cut" list: sources, "I don't know", checks and anything the user asked for are never dropped to save tokens.
- `scripts/audit_setup.py`: read-only audit of skills, subagents, CLAUDE.md files and MCP servers, with Markdown or JSON output. Standard library only.
- References: official sources with verbatim quotes, the hand-off template, and the audit checks.
- Four evaluation cases (hand-off, edit only the changed part, setup audit, short answer that keeps sources).
- Example: a heavy setup and its audit report.
- `tools/run_evals.py`: runs the cases with and without the skill through headless Claude Code and records tokens, time, skill use and file changes.
- First approximate measurement (`benchmarks/2026-10-31-approx`): checklist 95% with the skill vs 65% without; equal tokens on four short tasks.
- Long-session measurement (`benchmarks/2026-10-31-long-session`): about 2% fewer estimated tokens over 10 turns, but 71% vs 88% on the final files; the fresh chat answered from the hand-off note without opening the files it named.
