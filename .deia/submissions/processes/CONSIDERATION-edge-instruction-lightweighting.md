## Submission — Consideration: Edge Instruction Lightweighting

Meta
- Title: Edge Instruction Lightweighting (Minimize Boot Load)
- Date: 2025-10-13
- Owner: BOT-00001 (Queen)
- Scope: Hive coordination, instruction creation, and runtime guidance

1) What we tried to do
- Reduce cognitive/token overhead for drones at boot and during task execution by moving background guidance to linked docs and keeping instruction files concise.

2) Solution/proposal
- Add a Consideration doc: `.deia/considerations/EDGE-INSTRUCTIONS-LIGHTWEIGHTING.md`
- Add "Boot Load Check" sections to instruction files reminding agents to load only immediate task know‑how and follow links for background.
- Keep `.deia/bot-status-board.json` as SOT for orders; use instruction files as human mirrors.

3) Cost & Telemetry
- Tokens: N/A (local edits); Duration: ~10 min; Events: orders_board_update, rev_bump (queen)

4) Worker Usage
- N/A

5) Evidence
- Instruction files updated with "Boot Load Check"; Consideration doc added; status board rev bumped

6) Recommendation for the collective
- Adopt edge instruction lightweighting as a writing standard; set token targets per role and review weekly prompt metrics.

Appendix
- Open questions: token targets, prompt linting, dynamic include helpers

