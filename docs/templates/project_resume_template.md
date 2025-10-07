# DEIA Project Resume

**⚠️ IMPORTANT: Read This First**

## For AI Assistants Starting a Session

Welcome! You're working in a DEIA-enabled project. Before proceeding:

### 1. Check Your Memory Settings

**If you're Claude Code or another AI assistant with memory/preferences:**
- Check if you have a memory set up for DEIA (search for "DEIA" or "conversation logging" in your memories)
- If you have DEIA memory: Great! Follow those instructions.
- If you don't have DEIA memory: Read `.claude/preferences/deia.md` to understand how this project works.

### 2. What is DEIA?

DEIA (Development Evidence & Insights Automation) is a conversation logging and knowledge capture system. This means:
- Conversations should be logged in real-time to `.deia/sessions/`
- Important decisions and patterns should be captured
- Project context is preserved across sessions
- You help maintain this project resume document

### 3. Your Responsibilities in DEIA Projects

- **Log as you go:** After significant steps (file changes, decisions, fixes), log them
- **Update this resume:** Keep the "Current State" section below current
- **Read context:** Check recent session logs in `.deia/sessions/` to understand what happened before
- **Ask clarifying questions:** When user responses are ambiguous (see `.claude/preferences/deia.md`)

### 4. Quick Orientation

- **Project:** DEIA - Infrastructure for human-AI collaboration
- **Main repo:** deiasolutions/deia
- **BOK repo:** deiasolutions/deia-bok (Book of Knowledge)
- **Your role:** Help develop DEIA tools, document patterns, maintain quality

---

## Current State

### What's Working
- ✅ Conversation logging (`ConversationLogger` class)
- ✅ CLI commands (`deia init`, `deia doctor`, `deia admin`)
- ✅ BOK structure in separate repository
- ✅ Admin quality control tools
- ✅ VSCode extension (basic implementation)
- ✅ SpecKit integration

### Recent Work (Last Session)
- Added admin quality control tools (`src/deia/admin.py`)
- Created `ADMIN_REVIEW_PROCESS.md` in BOK repo
- Added clarifying questions policy to prevent ambiguous response handling

### Pending Tasks
- Test admin commands functionality
- Implement GitHub Actions workflow for automated PR review
- Future: Admin web dashboard

### Known Issues
- Auto-logging not yet tested in this session
- VSCode extension needs marketplace publishing
- Hybrid storage (Phase 2) on backlog

---

## Project Structure

```
deiasolutions/
├── src/deia/
│   ├── logger.py        # ConversationLogger class
│   ├── cli.py           # CLI commands
│   ├── installer.py     # deia init
│   ├── doctor.py        # deia doctor
│   └── admin.py         # deia admin (quality control)
├── .deia/
│   ├── config.json      # Project config
│   ├── sessions/        # Logged conversations
│   └── project_resume.md # This file
├── .claude/
│   ├── preferences/deia.md  # Claude Code memory template
│   └── commands/            # Slash commands
├── docs/                # Documentation
└── extensions/vscode-deia/  # VSCode extension

deia-bok/  (separate repo)
├── patterns/            # Collaboration patterns
├── platforms/           # Platform-specific solutions
├── anti-patterns/       # What NOT to do
└── sessions/            # Sanitized community logs
```

---

## Key Commands

```bash
# Installation
pip install -e .
deia install       # Global setup
deia init          # Initialize in project

# Diagnostics
deia doctor        # Check installation health
deia doctor --repair  # Fix common issues

# Admin (quality control)
deia admin scan <file>     # Security scan
deia admin review <file>   # Full review
deia admin ban-user <user> # Ban bad actor

# Logging
python -m deia.logger  # Manual logging
```

---

## Important Documents

- **[CONSTITUTION.md](../CONSTITUTION.md)** - Governance principles (Ostrom-based)
- **[PRINCIPLES.md](../PRINCIPLES.md)** - Common good, sustainability, human flourishing
- **[ROADMAP.md](../ROADMAP.md)** - Honest 7-phase roadmap
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to contribute
- **[.claude/preferences/deia.md](../.claude/preferences/deia.md)** - Your instructions as Claude

---

## Context from Previous Sessions

### Session Summary (Most Recent)
- Implemented admin quality control system
- Added clarifying questions policy after user feedback
- Committed changes to both main and BOK repos

### User Preferences
- Direct, concise communication
- "Plan now, build later" approach
- Strong emphasis on safety and clarification
- Phrase: "sometimes the safety of the entire universe is on the line"

---

## Next Steps

When starting work:
1. Check recent session logs in `.deia/sessions/`
2. Review any TODOs in code comments
3. Ask user what they want to work on
4. Log as you go

---

**Last updated:** 2025-10-07 (automated by DEIA)
