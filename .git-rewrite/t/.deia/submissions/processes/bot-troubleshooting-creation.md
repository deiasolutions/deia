## Submission — New/Updated Process

Meta
- Title: Bot Troubleshooting Guide Creation
- Date: 2025-10-13
- Owner: BOT-00005
- Scope: Documentation / Troubleshooting

1) What you tried to do
- Create concise troubleshooting guide for common drone issues
- Keep it ≤200 words with copy/pasteable solutions
- Cover: paths/typos, execution policy, python/py, model runners, next steps

2) Your solution/process
- Structured as 5 sections with specific issues and fixes
- Used bullet points and code blocks for copy/paste
- Added links to detailed docs
- Included bot signature per protocol
- Deliverable: `.deia/guides/BOT-TROUBLESHOOTING.md` (~190 words)

Preconditions:
- Detected new orders via Auto-Check
- Logged orders_apply telemetry
- Sent "Orders applied" heartbeat

Steps (timeboxed):
1. Detected orders and sent heartbeats (2 min)
2. Created BOT-TROUBLESHOOTING.md (5 min)
3. Sent completion heartbeat (1 min)
4. Updated status board to STANDBY (1 min)
5. Created process submission (2 min)
Total: ~11 minutes

Expected outputs:
- File exists at `.deia/guides/BOT-TROUBLESHOOTING.md`
- ≤200 words with practical solutions
- Links to detailed docs
- Bot signature included

Success criteria met: ✓ All acceptance criteria fulfilled

3) Cost & Telemetry
- Tokens: ~117,000 total
- Duration: ~11 minutes
- Events:
  - telemetry: orders_apply
  - heartbeat: "Orders applied (bot-troubleshooting-v1)"
  - heartbeat: "Working bot-troubleshooting-v1"
  - heartbeat: "Guide written: .deia/guides/BOT-TROUBLESHOOTING.md"

4) Worker Usage (if any)
- Workers invoked: None
- Task completed entirely within Claude Code session

5) Evidence
- Deliverable: `.deia/guides/BOT-TROUBLESHOOTING.md`
- Heartbeats: `.deia/instructions/BOT-00005-instructions.md` (lines 71-73)
- Status board updated: `.deia/bot-status-board.json`
- Telemetry: `.deia/bot-logs/BOT-00005-activity.jsonl`

6) Recommendation for the collective
- Classify: process suggestion
- Why it should be added:
  - Demonstrates proper telemetry logging (orders_apply event)
  - Quick turnaround for practical troubleshooting doc
  - Shows structured problem/solution format
  - Pattern for concise reference guides
- Proposed location: `bok/patterns/documentation/troubleshooting-guide-creation.md`

Appendix
- Open questions: None
- Future improvements:
  - Could add troubleshooting for git/GitHub CLI issues
  - Could include network/proxy issues for model downloads
