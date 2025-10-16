## Consideration — Edge Instruction Lightweighting (Minimize Boot Load)

Intent
- Keep edge instructions (what bots read at boot and while working) as light as possible so LLMs focus on project context and the immediate task.

Why
- Large prompts/instructions dilute task focus, increase token cost/latency, and raise error rates.

Principles
- Just‑in‑time loading: link to background docs; do not inline long guidance.
- Small working set: keep Current Task and next 1–2 steps visible; link the rest.
- Canonical pointers: reference the status board and process index rather than duplicating content.
- Stageable payloads: use short checklists and links to “mother ship” docs (.deia/*, docs/, bok/).
- Measurable targets: track prompt size, token use, and response latency per agent.

Practices
- Instruction files
  - Include a “Boot Load Check” and keep it under a small token target (e.g., <= 500–800 tokens).
  - Use links to `.deia/DRONE-START.md`, `.deia/hive/ORDERS-PROTOCOL.md`, process docs, and templates.
  - Prefer concise acceptance criteria; move rationale/background to linked docs.
- Orders
  - Update `.deia/bot-status-board.json` with short expectations; details live in instruction files or linked docs.
- Telemetry
  - Log token counts and durations per agent (`.deia/tools/telemetry.ps1|.sh`).
  - Periodically summarize prompt sizes and time to first token for tuning.
- Workers
  - Offload non‑LLM tasks to workers and log counts to `.deia/reports/worker-usage.json`.

Open Questions
- Set global token targets per role (queen/drone/worker)?
- Automate prompt size linting for instruction files?
- Dynamic “include on demand” helpers for longer procedures?

Next Steps (proposal)
1) Add Boot Load Check to instruction templates and status board guidance.
2) Track prompt/token metrics per agent in bot‑logs and review weekly.
3) Evolve a checklist for writing minimal, link‑heavy instruction files.

