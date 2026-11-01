# Hand-off to a fresh chat

Use when the topic changes or the conversation itself has grown large (see SKILL.md, "Keep the chat short"). Write it in the same message as the offer; don't ask first. The new chat starts from this note plus the Project files, not from the old conversation.

Rules:

- At most 15 lines. Point to files instead of copying them.
- Name the one file that holds the current state (a dashboard, `state.md`, a status table). The new chat reads it before answering about progress.
- Only what is decided or approved. Mark guesses as guesses.
- Name the new chat with the same name and the next version.

Template:

```markdown
# Hand-off: <Task name> v<n> → v<n+1>

Goal: <one line>
Current state: <file> — read it before answering about progress
Decided: <decision> — <why> (one line each, at most 4)
Approved files: <file names only>
Open questions: <one line each, at most 3>
Not done yet: <one line>
Next step: <one line>
Do not repeat: <what the new chat should not redo>
```

Example:

```markdown
# Hand-off: Desk Research v1 → v2

Goal: answer Shelfwise research questions 1–6 from published sources.
Current state: Desk Research v1.md — read it before answering about progress
Decided: keep external research apart from user evidence — it is about other people.
Approved files: brief.md, README.md, state.md, Desk Research v1.md
Open questions: question 5 (other stock apps) — not searched yet.
Not done yet: check-skill pass on the question 6 sources.
Next step: run check-skill on Desk Research v1.md in a new chat.
Do not repeat: questions 1–4 were "Not found"; don't search them again.
```
