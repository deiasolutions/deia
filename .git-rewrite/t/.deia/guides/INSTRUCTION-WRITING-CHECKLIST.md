## Instruction Writing Checklist (Edge-Light)

Goal
- Keep edge instructions lightweight so agents focus on user context and the task.

Before You Write
- Confirm the current orders in `.deia/bot-status-board.json` (rev and task).
- Check whether a process already exists under `.deia/processes/`.

Structure
- Header: Role and purpose (1–2 lines).
- Current Task: Single task with acceptance criteria and immediate next step.
- Heartbeats & Telemetry: Example one-liners.
- Links: point to background docs instead of inlining.
- Boot Load Check: reminder to keep working memory small.

Content Targets
- Token budget: <= 800 tokens (drone), <= 1200 (queen).
- Keep acceptance criteria concrete and testable.
- Include a “Done = …” line.

Do
- Link to: `.deia/hive/ORDERS-PROTOCOL.md`, `.deia/DRONE-START.md`, relevant process docs, and templates.
- Use bullets, short sentences, and one command per code block.
- Add Heartbeat examples (start/mid/end) and telemetry events (start/end/orders_apply).
- Reference worker helpers for non‑LLM tasks.

Don’t
- Inline long background or rationale—link it.
- Assign multiple tasks in one file; avoid deep nesting.
- Duplicate content that lives in status board or processes.

Validation
- Run token lint: PowerShell `.\\.deia\\tools\\instruction-token-lint.ps1 -Threshold 800` or POSIX `bash ./.deia/tools/instruction-token-lint.sh 800`.
- If over budget, move content into linked docs.

After Publish
- Bump the status board `rev` if the task meaningfully changes.
- Log a short telemetry event: `instruction_update`.

