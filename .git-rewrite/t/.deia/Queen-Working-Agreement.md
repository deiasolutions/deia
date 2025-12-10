## Quick Start (Player/Coach)
- type .\\.deia\\bot-status-board.json
- type .\\.deia\\instructions\\BOT-00002-instructions.md
- type .\\.deia\\instructions\\BOT-00003-instructions.md
- type .\\.deia\\instructions\\BOT-00005-instructions.md
- type .\\.deia\\instructions\\LAUNCH-BOT-00004-15MIN.md
- Edit .\\.deia\\bot-status-board.json (set status/task_id/expectation), bump ev, save
- Send bot to its file: type .\\.deia\\instructions\\BOT-xxxxx-instructions.md

# Queen Working Agreement

- Plan, Assign, Review — keep tasks scoped and testable.
- Write tasks in the drone instruction files under "Current Task" with:
  - Task summary, acceptance criteria, target files, priority.
- Expect drone heartbeats and a handoff doc per task.
- Close the loop by reviewing handoffs and assigning the next step.

## Human Requests Rule (New)
- Any request sent to a human MUST point to a single .md file to open and follow.
- The .md must be actionable for both a human and a bot (clear steps, copy/paste commands, minimal context, links for background).
- Prefer existing launch/assignment docs (e.g., .deia/instructions/LAUNCH-...md or bot instruction files). If missing, create one under .deia/ and reference it.

## Queen Turn Loop (Player/Coach)

- Status sweep (read-only)
  - type .\.deia\bot-status-board.json
  - type .\.deia\instructions\BOT-00002-instructions.md
  - type .\.deia\instructions\BOT-00003-instructions.md
  - type .\.deia\instructions\BOT-00005-instructions.md
  - type .\.deia\instructions\LAUNCH-BOT-00004-15MIN.md

- Assign/advance idle bots (source of truth)
  - Edit .\.deia\bot-status-board.json: set status/task_id/expectation; bump `rev`; save
  - Then send the bot to its instructions:
    - type .\.deia\instructions\BOT-xxxxx-instructions.md

- Player action (Queen picks a job)
  - If docs actions exist: type .\.deia\reports\repo-health-actions.md (assign next single step)
  - If link suggestions exist: type .\.deia\reports\link-fix-<latest>.md (assign 2–3 safe items)

- Principles
  - One step at a time; keep instruction files lean and link background
  - Orders live in the board; instruction files mirror for humans
  - After any assignment, bump `rev` so drones Auto-Check and comply


