## Submission — New/Updated Process

Meta
- Title: Commands Index Creation
- Date: 2025-10-13
- Owner: BOT-00005
- Scope: Documentation / Quick Reference

1) What you tried to do
- Create a concise index of canonical one-line commands for starting/continuing work per bot
- Keep it minimal (≤150 words)
- Include only the four canonical commands, no extras

2) Your solution/process
- Reviewed task requirements from instruction file
- Created simple structure with heading and four bot commands
- Used exact paths as specified in requirements
- Added single sentence stating these are canonical commands
- Deliverable: `.deia/guides/COMMANDS-INDEX.md` (~75 words)

Preconditions:
- Detected new orders via Auto-Check
- Sent "Orders applied" heartbeat
- Read updated instruction file

Steps (timeboxed):
1. Detected orders and sent heartbeats (2 min)
2. Created COMMANDS-INDEX.md (3 min)
3. Sent completion heartbeat (1 min)
4. Updated status board to STANDBY (1 min)
5. Created process submission (2 min)
Total: ~9 minutes

Expected outputs:
- File exists at `.deia/guides/COMMANDS-INDEX.md`
- Contains exactly four canonical one-liners
- Single sentence confirming canonicity
- No additional shortcuts

Success criteria met: ✓ All acceptance criteria fulfilled

3) Cost & Telemetry
- Tokens: ~85,000 total (including context and generation)
- Duration: ~9 minutes
- Events:
  - heartbeat: "Orders applied (commands-index-v1)"
  - heartbeat: "Working commands-index-v1"
  - heartbeat: "Commands index written: .deia/guides/COMMANDS-INDEX.md"

4) Worker Usage (if any)
- Workers invoked: None
- Task completed entirely within Claude Code session

5) Evidence
- Deliverable: `.deia/guides/COMMANDS-INDEX.md`
- Heartbeats: `.deia/instructions/BOT-00005-instructions.md` (lines 68-70)
- Status board updated: `.deia/bot-status-board.json`

6) Recommendation for the collective
- Classify: process suggestion
- Why it should be added:
  - Demonstrates proper Auto-Check workflow (detect orders → apply → work → complete)
  - Shows rapid turnaround for simple documentation tasks
  - Example of staying within strict word limits
  - Pattern for minimal reference docs
- Proposed location: `bok/patterns/documentation/commands-index-creation.md`

Appendix
- Open questions: None
- Future improvements:
  - Could automate commands index generation from bot registry
  - Could add validation to ensure paths exist
