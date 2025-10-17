# DEIA Repository Index

**For Claude Code: Read this on startup to understand repo structure**

---

## Core Files (Load These First)

**Startup (READ EVERY SESSION):**
- `.claude/STARTUP_CHECKLIST.md` - **CHECK THIS FIRST**
- `.claude/REPO_INDEX.md` - This file (navigation)
- `.claude/INSTRUCTIONS.md` - Auto-log procedures
- `ROADMAP.md` - Current status, what works vs what's infrastructure

**User Entry Points:**
- `README.md` - Project overview, what DEIA does
- `QUICKSTART.md` - 3-step install (the SIMPLE path)
- `PRINCIPLES.md` - Why DEIA exists (common good, Ostrom, etc.)

**Code:**
- `src/deia/cli.py` - CLI commands (init, install, config, etc.)
- `src/deia/cli_utils.py` - Helper functions (safe_print, etc.)
- `src/deia/logger.py` - ConversationLogger class (writes logs)
- `src/deia/installer.py` - Installation logic

**Claude Integration:**
- `.claude/preferences/deia.md` - Memory content (what user pastes into `# deia-user`)
- `.claude/CAPABILITIES.md` - What Claude can/can't do

---

## Process & Workflow Docs

**Admin Process (DEIA Global Admin):**
- `docs/SUBMISSION_WORKFLOW.md` - **THE** admin review process (3-tier submission)
- `docs/SUBMISSION_WORKFLOW_AUDIT.md` - Gap analysis (what exists vs what's planned)
- `docs/IMPLEMENTATION_PLAN.md` - Technical roadmap for missing features

**Development Standards:**
- `docs/DEV-PRACTICES-SUMMARY.md` - **Quick reference** (TDD, communication, standards)
- `docs/decisions/0001-extension-python-installation-strategy.md` - ADR: Installation approach
- `CONTRIBUTING.md` - How to submit bugs, patterns, PRs

**Dave's Workflow:**
- `docs/Dave Questions.md` - New questions go here (small file)
- `docs/Dave-Questions-Dialog.md` - Q&A history with actions/outcomes
- `~/.deia/dave/preferences.md` - Dave's dev preferences (TDD, communication)

**Strategic Planning:**
- `.private/docs/CLAUDE-PROJECT-BRIEFING.md` - For Claude.ai Projects (PRIVATE - not in git)

## Setup Docs (Reference When Needed)

- `DEIA_MEMORY_SETUP.md` - How to set `# deia-user` memory
- `DEIA_MEMORY_HIERARCHY.md` - Advanced: 4 memory levels (enterprise/user/team/project)

---

## Reference (Don't Load Unless Relevant)

**Governance:**
- `CONSTITUTION.md` - Full governance framework
- `docs/governance/ostrom-alignment.md` - Design rationale
- `docs/governance/deferred-amendments.md` - Pending changes

**Architecture:**
- `docs/architecture/security.md` - Privacy-first design
- `docs/architecture/scaling-bok.md` - How BOK scales

**Patterns (Book of Knowledge):**
- `bok/` - Community-contributed patterns
  - `bok/patterns/` - Collaboration patterns
  - `bok/platforms/` - Platform-specific solutions
  - `bok/anti-patterns/` - What NOT to do

**Process Docs:**
- `docs/sanitization-guide.md` - How to sanitize logs
- `docs/vendor-feedback-channel.md` - Library feedback process
- `docs/conversation-logging.md` - Logging deep dive

---

## Experiments & Demos

**Game Development (Flappy Bird):**
- `.deia/flappy-gerald.html` - Game A: Zero-shot implementation (Gerald the Anxious Bird)
- `.deia/flappy-bird-story.md` - Game A: Prose description
- `.deia/flappy-gerald-README.md` - Game A: Documentation
- `.deia/flappy-bird-game-b.html` - Game B: SDLC implementation (Phoenix the Overconfident Bird)
- `.deia/flappy-bird-game-b-story.md` - Game B: Phoenix's story & features
- `.deia/flappy-bird-technical-design.md` - Game B: Technical architecture
- `.deia/flappy-bird-visual-design.md` - Game B: Visual specifications
- `.deia/flappy-bird-game-b-README.md` - Game B: User documentation
- `.deia/flappy-bird-test-plan.md` - Game B: QA test plan
- `.deia/BLUEPRINT-flappy-bird-full-sdlc.md` - Game B: Complete SDLC blueprint

**AI/ML Experiments:**
- `.deia/flappy-bird-ai-research-proposal.md` - Neural network training proposal (Round 1 & 2)
- `.deia/sessions/20251012-flappy-bird-ai-experiment-start.md` - Experiment session log
- [Future: Training scripts, results, analysis]

**Handoffs (Multi-Role Coordination Demos):**
- `.deia/handoffs/` - Role transition documents for Game B
  - `queen-to-designer-game-b-phase1.md` - Design phase kickoff
  - `designer-to-queen-game-b-phase1-complete.md` - Design approval
  - `queen-to-developer-game-b-phase2.md` - Implementation kickoff
  - `developer-to-tester-game-b-phase3.md` - Testing kickoff
  - `GAME-B-COMPLETE-FINAL-SUMMARY.md` - Project completion summary

**Process Demonstrations:**
- Game A vs Game B comparison (zero-shot vs full SDLC)
- Multi-role coordination (Designer → Developer → Tester → Documentation)
- File-based handoffs for async collaboration

---

## Working/Private (Gitignored)

**Repo-Level Private (Dave's personal workspace):**
- `.private/` - Private docs, notes, experiments
  - `.private/docs/` - Documents with PII or strategic info
  - `.private/logs/` - Private conversation logs
  - `.private/README.md` - Usage guide

**Project-Level Private (per-user workspace):**
- `.deia/private/` - Every user's private space
  - `.deia/private/drafts/` - Pre-sanitization submissions
  - `.deia/private/logs/` - Unsanitized conversation logs
  - `.deia/private/notes/` - Personal project notes
  - `.deia/private/README.md` - Usage guide
  - `.deia/SANITIZATION_REQUIREMENTS.md` - Submission guidelines

**Other Gitignored:**
- `admin/` - Dave's backlog, decisions, ideas
- `.deia/sessions/` - Conversation logs (experiment documentation)
- `docs/backlog/` - WIP features

**Don't commit these. Don't reference in public docs.**

---

## Files to Ignore/Archive

**Redundant (covered by QUICKSTART.md):**
- `CONVERSATION_LOGGING_QUICKSTART.md` - Superseded by QUICKSTART.md
- `DEIA_INTEGRATION_GUIDE.md` - Superseded by MEMORY_SETUP.md

**Stale:**
- `BOK_MOVED.md` - Delete (BOK is here, not moved)
- `docs/how-to-save-logs.md` - Redundant with QUICKSTART

**Unclear:**
- `docs/ditto-tracking.md` - What is this?

---

## Decision Rules for Claude

### When User Asks "How do I install DEIA?"
→ Reference `QUICKSTART.md` ONLY
→ Don't show MEMORY_HIERARCHY or technical details

### When User Asks "How does memory work?"
→ Show `DEIA_MEMORY_SETUP.md` simple path
→ Link to MEMORY_HIERARCHY for advanced

### When Working on Code
→ Read `ROADMAP.md` to know what's working vs not
→ Check `src/deia/logger.py` for current implementation
→ Don't assume features work (check ROADMAP first)

### When User Reports Bug
→ Use `gh issue create --repo deiasolutions/deia`
→ Follow template in `CONTRIBUTING.md`

### When Confused About Scope
→ Ask Dave: "Should I focus on X or Y?"
→ Don't try to do everything at once

---

## Simplification Needed

**Too many overlapping docs:**
- QUICKSTART vs CONVERSATION_LOGGING_QUICKSTART vs INTEGRATION_GUIDE
- MEMORY_SETUP vs MEMORY_HIERARCHY (merge into ONE with simple path first)

**Recommendation:**
1. Merge memory docs into one (simple at top, advanced at bottom)
2. Delete redundant quickstarts
3. Archive stale docs to `docs/archive/`
4. Keep root-level simple (5-6 files max)

---

## Summary

**EVERY SESSION START (new or resumed):**
1. Read `.claude/STARTUP_CHECKLIST.md` - **ALWAYS FIRST**
2. Read this index (navigation)
3. Read `ROADMAP.md` (know what works)
4. Check `.deia/config.json` auto-log status

**When Dave asks about process:**
- Admin review? → `docs/SUBMISSION_WORKFLOW.md`
- Dev standards? → `docs/DEV-PRACTICES-SUMMARY.md`
- How to install? → `QUICKSTART.md`
- **Don't search - check index first**

**Reference when needed:**
- Memory setup docs
- Contributing guide
- Specific code files

**Ignore unless Dave says:**
- `admin/`
- `.deia/` (except config.json)
- Governance deep dives
- BOK patterns (separate concern)

**Focus:** Help users install and use DEIA simply. Don't overwhelm with 119 files.

---

## Index Maintenance

**Update this index:**
- ✅ When creating new docs
- ✅ When moving/renaming files
- ✅ Weekly during active development
- ✅ Before major releases

**Check index accuracy:**
```bash
deia doctor index  # (planned command)
```

**Manual check:**
- Are all new docs listed?
- Are paths correct?
- Are descriptions accurate?
- Remove deleted files
