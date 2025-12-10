# DEIA Project Briefing for Claude.ai

**Purpose:** This document provides context for feature discussions and strategic planning on Claude.ai (Projects), keeping Claude Code focused on implementation.

**Last Updated:** 2025-10-09

---

## What is DEIA?

**DEIA** = Development Evidence & Insights Automation

A toolkit for learning from AI-assisted development sessions:
- **Auto-logs** AI conversations (insurance against crashes)
- **Sanitizes** logs for safe sharing (removes PII/secrets)
- **Builds** a community Body of Knowledge (BOK) from shared patterns
- **Integrates** with Claude Code, Cursor, GitHub Copilot, and other AI tools

---

## Current Architecture

### Components

1. **Python Package** (`src/deia/`)
   - Core CLI: `deia install`, `deia init`, `deia sanitize`, etc.
   - Platform-agnostic (works with any AI or manually)
   - Published to PyPI: `pip install deia`

2. **VS Code Extension** (`extensions/vscode-deia/`)
   - Optional UI layer
   - Calls Python CLI under the hood
   - Chat participant: `@deia log`, `@deia status`
   - Status bar: Shows auto-log status
   - Currently supports: GitHub Copilot Chat

3. **Multi-tier Memory System**
   - **Enterprise**: Company-wide patterns (future)
   - **User**: `~/.deia/` - Your personal BOK
   - **Team**: Shared team knowledge (future)
   - **Project**: `.deia/` - Project-specific logs

4. **Submission Workflow** (IN DESIGN)
   - Project → User → Global BOK
   - Sanitization → Validation → Review → Acceptance
   - Admin tools for quality control

---

## Project Status

### ✅ Implemented (v0.1.0)

- Python CLI structure
- Basic logging (`deia log create`)
- Sanitization (PII/secrets removal)
- Validation
- BOK search/sync
- Admin security scanning
- VS Code extension (basic)
- Chat participant (`@deia` in GitHub Copilot)

### 🚧 In Progress

- Unicode bug fix (Windows terminals)
- Documentation cleanup
- TDD enforcement
- Submission workflow redesign

### ❌ Not Yet Implemented

- **Auto-logging** (status bar shows it, but doesn't work)
- Claude Code integration (startup hooks)
- Multi-tier submission workflow
- Token tracking
- Dashboard (local + web)
- AI-assisted review (`#deia review`)
- GitHub Issues integration
- Hallucination reporting

---

## Key Design Decisions

### ADR-0001: Installation Strategy
- **Phase 1** (NOW): Separate installs (pip + extension)
- **Phase 2** (later): Auto-install when mature

### Principles
- **Python does the work, AI is the interface**
- **Platform-agnostic** (not locked to one AI tool)
- **TDD always** (tests first, no exceptions)
- **Automation-first** (minimize manual steps)
- **Privacy-first** (sanitize, user controls data)

---

## Recent Developments (2025-10-09 Session)

### Bugs Fixed
1. ✅ Unicode crash on Windows (`safe_print()` helper with fallback)
2. ✅ Syntax error in `tests/conftest.py`

### New Systems Created
1. **Dave Questions Workflow**
   - `docs/Dave Questions.md` - Add questions here
   - `docs/Dave-Questions-Dialog.md` - Answers & tracking
   - Keeps questions organized and answered

2. **Preferences System**
   - `~/.deia/dave/preferences.md` - Dave's dev preferences
   - Communication patterns (e.g., "Yes, but..." handling)
   - Development standards (TDD, automation-first)

### Submissions Created (Pending Review)
1. Pattern: "Yes, but..." response handling
2. Bug: Claude Code startup integration missing
3. Bug: Unicode error in sanitize command
4. 10 improvement suggestions

---

## Dave's Vision (From Recent Questions)

### AI Integration
- AI-assisted review: `#deia review <submission>` in VS Code
- Auto-generate solutions + documentation
- Hallucination detection & reporting
- Token usage tracking (transparency + efficiency)

### Vendor Support
- ✅ GitHub Copilot / GitHub Chat (current)
- ⏳ Claude Code (in progress)
- ⏳ Cursor
- ⏳ Other AI platforms

### Dashboards
- **Local** (VS Code): Personal submissions, token usage, sessions
- **Global** (Web): Admin view - downloads, users, submissions, quality metrics

### Quality & Safety
- Two-tier sanitization (`--for-ai` vs `--for-public`)
- AI self-check before human review
- Hallucination reporting to DEIA Global
- Share findings with AI vendors (OpenAI, Anthropic, etc.)

### Workflow
- Issue numbering: `DEIA-YYYY-NNN-TYPE` (e.g., `DEIA-2025-001-BUG`)
- Priority system: P0 (critical) → P3 (low)
- Flexible prioritization (can do feature before bug if strategic)
- All submissions (even from Dave) go through standard process

---

## Current Challenges

1. **Auto-logging doesn't work** - Status bar is misleading
2. **Claude Code integration missing** - No startup hooks
3. **Submission workflow incomplete** - Designed but not implemented
4. **Token tracking missing** - Can't measure efficiency yet
5. **No prioritization system** - Hard to decide what to build next

---

## Tech Stack

### Python
- Click (CLI framework)
- Rich (terminal UI)
- pytest (testing, with TDD)
- Python 3.8+

### VS Code Extension
- TypeScript
- VS Code API
- Chat Participant API (GitHub Copilot)
- Calls Python CLI via subprocess

### Future
- Web dashboard: FastAPI + React
- Database: PostgreSQL
- Analytics: Track usage, submissions, quality

---

## Dave's Development Standards

### TDD (Test-Driven Development)
- Write tests FIRST, always
- No code without tests
- No exceptions

### Communication
- "Yes, but..." pattern: STOP, answer question, then proceed
- No multiple yes/no questions (use A/B/C alternatives)
- Ask clarifying questions when ambiguous

### Workflow
- Question complexity
- Automation over manual steps
- Platform-agnostic design
- Privacy and security first

---

## File Structure

```
deiasolutions/
├── src/deia/               # Python package
│   ├── cli.py              # Main CLI commands
│   ├── cli_utils.py        # Helpers (safe_print, etc.)
│   ├── core.py             # Core functionality
│   ├── bok.py              # Body of Knowledge
│   ├── admin.py            # Admin tools
│   ├── logger.py           # Conversation logging
│   └── ...
├── extensions/vscode-deia/ # VS Code extension
│   ├── src/
│   │   ├── extension.ts    # Main extension
│   │   ├── chatParticipant.ts # @deia chat
│   │   ├── statusBar.ts    # Status bar item
│   │   └── ...
│   └── package.json
├── tests/                  # Test suite (pytest)
├── docs/                   # Documentation
│   ├── Dave Questions.md   # New questions
│   ├── Dave-Questions-Dialog.md # Q&A history
│   ├── CLAUDE-PROJECT-BRIEFING.md # This file
│   └── decisions/          # ADRs
├── bok/                    # Body of Knowledge
│   └── patterns/
├── .deia/                  # Project DEIA (dogfooding)
│   ├── config.json
│   ├── sessions/           # Logged conversations
│   └── submissions/        # Pending submissions
└── ~/.deia/                # User-level DEIA
    └── dave/
        └── preferences.md  # Dave's preferences
```

---

## Next Steps (In Priority Order)

### Immediate
1. Turn off misleading auto-log status ✅
2. Create bug report for auto-log issue
3. Process bug report via official workflow
4. Document dev practices (CONTRIBUTING.md)

### High Priority
1. Implement submission ID system (`DEIA-YYYY-NNN-TYPE`)
2. Create prioritization framework
3. Fix Claude Code startup integration
4. Enhance sanitization for AI review

### Medium Priority
1. Token tracking system
2. AI review commands (`#deia review`)
3. Local dashboard (VS Code)
4. GitHub Issues integration

### Long-term
1. Web admin dashboard
2. AI-assisted documentation generation
3. Hallucination reporting system
4. Multi-vendor support (Cursor, etc.)

---

## Questions for Strategic Discussion

### Feature Planning
1. Should we prioritize AI review features before fixing bugs?
2. How much should we invest in the web dashboard vs local tools?
3. What's the MVP for Phase 2 (auto-install)?
4. Should we support Cursor before or after Claude Code?

### Architecture
1. Should we build a monorepo now or wait?
2. How do we handle version sync between Python + Extension?
3. Database for global BOK: PostgreSQL or something else?
4. Should hallucination reports be anonymous or attributed?

### Community
1. How do we bootstrap the global BOK before we have users?
2. Should we open-source immediately or build more first?
3. How do we incentivize quality submissions?
4. Should there be a DEIA certification/badging system?

### Business Model & Sustainability

**DEIA is free and always will be.** No paid tiers, no data selling, no ads.

**Funding model:**
- Community donations/sponsorships (GitHub Sponsors, Patreon, etc.)
- University partnerships (grant funding for research)
- Ethical commercial partnerships (aligned with our values)
- Goal: Cover Dave's development costs + future infrastructure (GitHub presence, hosting)

**Why donations?**
- Dave has a full-time job but would rather work on DEIA
- Development has real costs (time, infrastructure, tools)
- Supporters benefit from the tool and want to help sustain it
- Community-funded = community-owned (no VC capture, no feature paywalls)

**Open questions:**
1. Should we partner with AI vendors (OpenAI, Anthropic, etc.)?
2. What's the growth strategy for global adoption?
3. How do we recognize/incentivize major contributors?

---

## How to Use This Brief

**On Claude.ai (Projects):**
1. Upload this file to a new Project
2. Add other context files as needed:
   - `docs/Dave-Questions-Dialog.md` (recent Q&A)
   - `ROADMAP.md` (current roadmap)
   - `PRINCIPLES.md` (development principles)
3. Use for:
   - Strategic feature discussions
   - Architecture planning
   - Long-term vision refinement
   - Community/business strategy

**Keep Claude Code for:**
- Bug fixes
- Feature implementation
- Code reviews
- TDD workflows
- Documentation updates

---

## Contact & Collaboration

**Dave Eichler** (@davee)
- Primary developer
- DEIA Global admin
- Vision holder

**Current AI Assistants:**
- Claude Code (Sonnet 4.5) - Implementation
- Claude.ai Projects - Strategy & planning
- GitHub Copilot - Code assistance

---

**Last Session Summary:**
- Fixed Unicode bug (Windows terminal crash)
- Created Dave Questions workflow
- Answered 8 strategic questions
- Identified need for prioritization system
- Documented TDD as hard requirement

**Current Focus:**
- Bug reporting workflow
- Development practices documentation
- Prioritization framework
- Keeping feature discussions separate from implementation

---

## Glossary

- **BOK**: Body of Knowledge (community patterns)
- **TDD**: Test-Driven Development
- **ADR**: Architecture Decision Record
- **Sanitization**: Removing PII/secrets from logs
- **Hallucination**: AI generating false/incorrect information
- **Token**: Unit of text processed by AI (costs money)
- **Submission**: Bug/feature/pattern contribution to DEIA Global

---

**Ready for strategic discussion!** 🚀
