## Nightly Queen Checklist (Lean)

1) Instruction Token Lint (edge-light)
- PowerShell: `.\\.deia\\tools\\nightly-instruction-lint.ps1 -Threshold 800`
- Reviews all `*-instructions.md`, writes JSON report to `.deia/reports/`, and bumps status board `rev`.
- If an alert is generated, see `.deia/reports/instruction-token-alert-*.md` and schedule trims (move background to links).

2) Orders Review
- Open `.deia/bot-status-board.json`, confirm `task_id`, `status`, `expectation` for active bots.
- If you change orders, bump `rev` (drones will auto-apply).

3) Telemetry Snapshot (optional)
- Glance at `.deia/bot-logs/*-activity.jsonl` for today’s orders/events.
- Summarize in `.deia/reports/queen-notes-<YYYYMMDD>.md` if needed.

4) Announcements (optional)
- Add an announcement to the board if new guidance or templates were added.

Done = Lint run, board confirmed, and changes (if any) recorded in hive log/telemetry.

