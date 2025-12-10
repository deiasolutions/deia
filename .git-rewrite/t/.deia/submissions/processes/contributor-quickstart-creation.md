## Submission — New/Updated Process

Meta
- Title: Contributor Quickstart Guide Creation
- Date: 2025-10-13
- Owner: BOT-00005
- Scope: Documentation / Onboarding

1) What you tried to do
- Create a single-page quickstart guide for new contributors covering: join hive, Auto-Check orders, heartbeats, telemetry basics, and worker usage
- Keep it concise (≤400 words), copy/paste friendly, with links to detailed docs

2) Your solution/process
- Read reference documents: `00-STARTUP-INSTRUCTIONS.md` and `bot-status-board.json`
- Extracted key concepts for each section (join/claim, Auto-Check, heartbeats, telemetry, workers)
- Structured as 6 numbered sections with code blocks and bullet points
- Linked to detailed documentation instead of inlining long explanations
- Final deliverable: `.deia/guides/CONTRIBUTOR-QUICKSTART.md` (~350 words)

Preconditions:
- Claimed BOT-00005 identity via hive join
- Read instruction file with task requirements

Steps (timeboxed):
1. Join hive as BOT-00005 (2 min)
2. Update instruction file with Instance ID (1 min)
3. Send start heartbeat (1 min)
4. Read reference docs (3 min)
5. Write quickstart guide (10 min)
6. Send completion heartbeat (1 min)
Total: ~18 minutes

Expected outputs:
- File exists at `.deia/guides/CONTRIBUTOR-QUICKSTART.md`
- ≤400 words
- Covers all 5 required topics
- Links to background docs

Success criteria met: ✓ All acceptance criteria fulfilled

3) Cost & Telemetry
- Tokens: ~46,000 total (context loading + generation)
- Duration: ~18 minutes
- Events:
  - session_start (implicit via hive join)
  - heartbeat: "Working contributor-quickstart-v1"
  - heartbeat: "Quickstart written: .deia/guides/CONTRIBUTOR-QUICKSTART.md"
  - heartbeat: "Standing by - contributor-quickstart-v1 complete"

4) Worker Usage (if any)
- Workers invoked: None
- This task was completed entirely within Claude Code session
- No external LLM API calls required

5) Evidence
- Deliverable: `.deia/guides/CONTRIBUTOR-QUICKSTART.md`
- Heartbeats: `.deia/instructions/BOT-00005-instructions.md` (lines 65-67)
- No reports generated (documentation task)

6) Recommendation for the collective
- Classify: process suggestion
- Why it should be added:
  - Provides standard workflow for documentation tasks
  - Demonstrates proper sign-in → work → heartbeat → submission flow
  - Shows how to stay within word limits while covering required topics
  - Example of linking vs. inlining for lightweight instructions
- Proposed location: `bok/patterns/documentation/quickstart-guide-creation.md`

Appendix
- Open questions: None
- Future improvements:
  - Could automate word count checking in documentation tasks
  - Could create template for quickstart guides to ensure consistency
