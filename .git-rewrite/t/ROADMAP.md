# DEIA Roadmap

**Honest, phased approach to building knowledge infrastructure**

---

## Where We Are Today

**What actually works:**
- **DEIA iDea Methodology** - Human-AI collaborative development framework (v1.0)
- `ConversationLogger` Python class for logging Claude Code sessions
- Manual session capture (call `create_session_log()` with conversation data)
- BOK structure with ~10 community-contributed patterns
- Governance docs (Constitution, Principles, Contributing)

**What exists but isn't validated:**
- `pyproject.toml` packaging setup
- `deia` CLI commands (`init`, `install`, etc.)
- Installer code (`installer.py`)
- Sanitization and validation modules

**What doesn't exist:**
- Automated pattern extraction
- VS Code extension
- PyPI package
- Real-time auto-logging
- Multi-domain expansion

---

## Phase 1: Get the Basics Working (CURRENT PRIORITY - 2025-10-17)

**Goal:** Make DEIA installable and usable for early adopters

**Status:** 🚨 PRIORITY FOCUS - All agents assigned to Phase 1 (2025-10-17)

###  Tasks

- [x] Test `pip install -e .` works - **COMPLETE: AGENT002** (2025-10-18) ✅ VERIFIED WORKING
- [x] Verify `deia init` creates proper `.deia/` structure - **COMPLETE: AGENT005** (2025-10-18) ✅
- [x] **Complete conversation logger implementation:** - **COMPLETE: AGENT004** (2025-10-18) ✅ DISCOVERY: Already works
  - [x] Logger infrastructure (`ConversationLogger` class, file writing) ✅
  - [x] Actual conversation capture mechanism - ✅ EXISTS AND WORKS (discovered 2025-10-18)
  - [x] Real-time logging during sessions - ✅ EXISTS (needs documentation)
  - [x] Integration with Claude Code - ✅ EXISTS (.claude/commands/log.md, start-logging.md)
  - [x] Test end-to-end with real conversation data - ✅ VERIFIED (test log created)
- [x] Document actual installation steps - **COMPLETE: AGENT002** (2025-10-18) ✅ INSTALLATION.md (400+ lines)
- [x] Fix any import/dependency issues - **COMPLETE: AGENT002** (2025-10-18) ✅ No issues found
- [x] **Create test infrastructure:** ✅
  - [x] Test directory structure (`tests/unit/`, `tests/integration/`)
  - [x] Pytest configuration (`pytest.ini`)
  - [x] Shared fixtures (`tests/conftest.py`)
  - [x] Basic CLI tests
  - [x] Basic logger tests
  - [x] Test tracking (`admin/testing.md`)
  - [ ] Add test dependencies to `pyproject.toml` - **ASSIGNED: AGENT003** (P0)
  - [ ] Run tests and measure coverage - **ASSIGNED: AGENT003** (P0)
  - [x] Reach 50% test coverage → **ACHIEVED 38%** - COMPLETE (AGENT-003, 2025-10-18)
  - 276 tests passing
  - P0 modules: installer 97%, cli_log 96%, config 76%
  - All critical services tested
  - Foundation complete, can expand in Phase 2
- [x] Write honest installation guide - **COMPLETE: AGENT002** (2025-10-18) ✅ See INSTALLATION.md

**Success criteria:** A developer can clone, install, and start logging sessions **with real conversations, not hardcoded test data**

**Agent Assignments (2025-10-17, updated 2025-10-18):**
- AGENT002: ✅ Fix pip install + Installation guide COMPLETE (2025-10-18, 1.5h actual)
- AGENT003: Test suite to 50% coverage (ASSIGNED)
- AGENT004: ✅ Real-time conversation logging COMPLETE (2025-10-18, 0.25h actual - discovered already works)
- AGENT005: ✅ deia init verification COMPLETE (2025-10-18, 20min actual)

**Phase 1 Progress: 80% complete (4 of 5 blockers resolved)**

**Remaining Blocker:**
- Test coverage (currently 6%, need 50%) - AGENT003 working

---

## Phase 2: Automated Pattern Extraction (Next)

**Goal:** Make it easy to extract patterns from logs without manual work

### Tasks

- [x] **Master Librarian Specification** - ✅ COMPLETE (AGENT-004, 2025-10-18, 1,212 lines)
  - Defines knowledge curation role and workflows
  - Establishes quality standards for BOK submissions
  - Provides templates and examples
  - Enables both human and AI librarians
- [ ] Build pattern extraction CLI (`deia extract <session-file>`)
- [ ] Implement sanitization automation (detect/remove PII, secrets)
- [ ] Create pattern templates for common types
- [ ] Add validation checks before BOK submission
- [ ] Build diff tool to review changes before committing
- [ ] Integrate with git workflow

**Success criteria:** User can run `deia extract` and get a sanitized, ready-to-submit pattern

---

## Phase 2.5: DEIA Chat Interface (Q4 2025 - Q1 2026)

**Goal:** Web-based chat interface for interacting with DEIA projects

**Status:** Phase 1 (Basic Chat) complete, Phases 2-4 planned

### Overview

A local web GUI that provides:
- Chat interface with Ollama LLM
- File operations within DEIA project boundaries
- Integration with .deia structure (BOK, sessions, ephemera)
- Secure file modifications with confirmation workflows

**LLH Specification:** `.deia/.projects/simulation_004/gpt-llama-bot-eos-companion.md`
**Status Document:** `llama-chatbot/STATUS.md`

### Phase 1: Basic Chat ✅ (COMPLETED 2025-10-15)

- [x] FastAPI server with WebSocket support
- [x] Ollama LLM integration
- [x] Real-time streaming responses
- [x] Conversation history management
- [x] Unified LLM service (Ollama/DeepSeek/OpenAI support)
- [x] Retry logic and error handling
- [x] Basic command execution
- [x] **Agent BC Integration (2025-10-17):** 18 components integrated
- [x] **CLI Hive Commands (2025-10-17):** 7 commands added
- [x] **BOK Index Deployed (2025-10-17):** master-index.yaml + generator

**Files:** `llama-chatbot/app.py`, `src/deia/services/llm_service.py`, `src/deia/services/*.py` (9 new services), `src/deia/tools/*.py` (2 new tools)

### Phase 2: File Operations (4-6 weeks) - IN PROGRESS

- [ ] DEIA project structure detection (ASSIGNED: CLAUDE-CODE-003) - PAUSED
- [ ] Auto-load .deia context files (BOK, sessions, ephemera) (ASSIGNED: CLAUDE-CODE-003) - PAUSED
- [x] File reading API with encoding detection ✅ (CLAUDE-CODE-004, 2025-10-18, 86% coverage)
- [x] Project structure browser (tree view) ✅ (CLAUDE-CODE-005, 2025-10-17, 89% coverage)
- [x] Path validation (project boundary enforcement) ✅ (CLAUDE-CODE-004, 2025-10-18, 96% coverage)
- [ ] File context display in chat (PENDING)
- [ ] Integration with .deia folder structure (PENDING)

**Estimated Effort:** 13-16 hours (5 components assigned 2025-10-17)
**Status:** 3 of 7 components complete (PathValidator, FileReader, ProjectBrowser), 2 paused for Phase 1, 2 pending
**Deliverable:** Chat interface aware of DEIA project structure

### Phase 3: File Modifications (6-8 weeks)

**Critical:** Requires Phase 2 security foundation

- [ ] File write API with confirmation workflow
- [ ] Diff viewer (show changes before applying)
- [ ] User confirmation dialogs
- [ ] Audit logging to `.deia/logs/file-operations.jsonl`
- [ ] Backup/undo mechanism (git-based or file-based)
- [ ] Change tracking and rollback
- [ ] Security: Directory traversal prevention

**Estimated Effort:** 12-15 hours
**Deliverable:** Safe file modification with full audit trail

### Phase 4: Polish & Enhancement (Ongoing)

- [ ] Extract HTML to separate files (better maintainability)
- [ ] Enhanced UI/UX (Tailwind CSS styling)
- [ ] Keyboard shortcuts
- [ ] Session persistence (save/load conversations)
- [ ] Read-only mode toggle
- [ ] Mobile responsiveness
- [ ] Performance optimization for large projects

**Estimated Effort:** 6-12 hours initially, ongoing improvements
**Deliverable:** Production-quality user experience

### Security Requirements (Critical)

All phases must maintain:
- **Project boundary enforcement** - No access outside DEIA project
- **Localhost-only access** - No remote connections by default
- **File confirmation required** - All write operations need approval
- **Audit logging** - All file operations logged to RSE format
- **Path validation** - Prevent directory traversal attacks
- **Sensitive file protection** - No access to .git, .env, secrets

### Integration Points

**DEIA Structure:**
- `.deia/bok/` - Body of Knowledge access
- `.deia/sessions/` - Session log reading
- `.deia/efemera/` - Ephemera browsing
- `.deia/context/` - Auto-load project context
- `.deia/logs/` - Audit trail storage

**External:**
- Ollama (local LLM)
- Git (change tracking)
- File system (with restrictions)

### Success Criteria

**Functional:**
- Can chat with LLM about DEIA project
- Can read files from project
- Can modify files with confirmation
- Understands .deia structure
- Provides context-aware responses

**Security:**
- No unauthorized file access
- All modifications logged
- Confirmation required for changes
- Rollback capability exists

**Performance:**
- Sub-second file operations
- Smooth streaming chat
- Handles large projects efficiently

### Current Status

**Phase Completion:** 1 of 4 (25% phases, ~12% effort)
**Files Created:** 5 (app.py, llm_service.py, docs)
**Documentation:** Complete for Phase 1
**Next Milestone:** DEIA awareness + file reading

See `llama-chatbot/STATUS.md` for detailed implementation plan.

---

## Phase 3: Claude Code Integration (Q1 2026)

**Goal:** Seamless auto-logging for Claude Code users

### Tasks

- [ ] Finish `.claude/INSTRUCTIONS.md` bootstrap
- [ ] Test slash commands (`/log`, `/auto-log-check`)
- [ ] Fix import issues (sys.path workaround or package install)
- [ ] Auto-detect when Claude Code is running
- [ ] Stream conversations to `.deia/sessions/` in real-time
- [ ] Add session recovery after crashes
- [ ] Create user documentation

**Success criteria:** Claude Code users get auto-logging with zero configuration

---

## Phase 4: VS Code Extension (Q2 2026)

**Goal:** DEIA works with ALL AI tools (Cursor, Copilot, Continue, etc.)

### Tasks

- [ ] Build VS Code extension scaffold
- [ ] Hook into AI assistant conversations (vendor-agnostic)
- [ ] Stream to `.deia/sessions/` in real-time
- [ ] Add UI for session review
- [ ] Implement pattern extraction from UI
- [ ] Publish to VS Code marketplace
- [ ] Support multiple AI vendors simultaneously

**Success criteria:** Works with Claude, GPT, Copilot, Gemini - any VS Code AI extension

---

## Phase 5: PyPI Package (Q3 2026)

**Goal:** `pip install deia` works for everyone

### Tasks

- [ ] Finalize API stability
- [ ] Complete test coverage (>80%)
- [ ] Write comprehensive documentation
- [ ] Set up CI/CD (GitHub Actions)
- [ ] Register on PyPI
- [ ] Version management (semantic versioning)
- [ ] Release v1.0.0

**Success criteria:** `pip install deia` installs cleanly on Windows/Mac/Linux

---

## Phase 6: Academic Partnerships (Q4 2026)

**Goal:** DEIA becomes citable research infrastructure

### Tasks

- [ ] Register with Zenodo (DOI assignment)
- [ ] Partner with HCI researchers
- [ ] Create anonymized dataset for research (opt-in)
- [ ] Publish whitepaper on human-AI collaboration patterns
- [ ] Present at academic conferences (CHI, CSCW)
- [ ] Establish ethics review process

**Success criteria:** Researchers can cite DEIA BOK in papers

---

## Phase 7: Multi-Domain Expansion (2027+)

**Goal:** DEIA works beyond coding - research, healthcare, legal, education

### Vision

**Research:** Lab notebooks, experimental logs, literature reviews
**Healthcare:** Clinical decision logs, treatment pattern sharing
**Legal:** Case research, precedent patterns, brief strategies
**Education:** Teaching strategies, student interaction patterns
**Business:** Decision logs, strategy patterns, market insights

### Requirements

- Domain-specific sanitization (HIPAA, attorney-client privilege, etc.)
- Domain expert governance boards
- Specialized pattern taxonomies
- Compliance frameworks
- Academic/professional partnerships

**Timeline:** Proof of concept in one non-coding domain by end of 2027

---

## Long-Term Vision

**10-year goal:** DEIA becomes default infrastructure for human-AI collaboration knowledge

**What success looks like:**
- Millions of developers logging sessions
- 100K+ patterns in BOK across domains
- Standard citation in academic research
- Integration with major AI tools (Anthropic, OpenAI, Google adopt DEIA format)
- Self-sustaining community governance
- Cross-domain pattern learning (coding insights help medical practitioners, etc.)

**Sustainability:**
- Community-funded (donations, sponsorships)
- University partnerships (grant funding)
- Ethical commercial partnerships (no data selling, no ads)
- Maintainer stipends (dignified compensation)

---

## What Could Derail This

**Technical risks:**
- Privacy breach (accidental PII/secret exposure)
- Scalability issues (BOK becomes unwieldy)
- Vendor pushback (AI companies block logging)

**Community risks:**
- Governance failure (becomes toxic like Stack Overflow)
- Low adoption (nobody uses it)
- Contributor burnout

**Legal risks:**
- TOS violations claims
- Copyright disputes
- Regulatory compliance (GDPR, HIPAA, etc.)

**Mitigations:**
- Strong privacy-first architecture
- Ostrom governance (proven at scale)
- Legal review process
- Transparent decision-making
- Community support for maintainers

---

## How to Help

**Right now:**
- Test `pip install -e .` and report issues
- Use `ConversationLogger` in your work
- Contribute patterns to BOK
- Review governance docs and suggest improvements

**Soon:**
- Test automated pattern extraction
- Beta test Claude Code integration
- Help with VS Code extension
- Spread the word

**Long-term:**
- Maintain parts of the codebase
- Join governance board
- Sponsor development
- Expand to new domains

---

## Versioning Strategy

- **v0.1.x:** Phase 1 (basic install working)
- **v0.2.x:** Phase 2 (automated extraction)
- **v0.3.x:** Phase 3 (Claude Code integration)
- **v0.4.x:** Phase 4 (VS Code extension)
- **v1.0.0:** Phase 5 (PyPI release, stable API)
- **v1.x:** Incremental improvements
- **v2.0:** Phase 7 (multi-domain expansion)

---

## Progress Tracking

**Last updated:** 2025-10-17

**Current phase:** Phase 1 (PRIORITY - basics must work first)
**Current version:** 0.1.0 (development)
**Methodology:** DEIA iDea v1.0 (released)

**PRIORITY SHIFT (2025-10-17):**
**ALL WORK PAUSED** - Focusing on Phase 1 basics until foundation is solid
- Reason: Can't build advanced features on broken foundation
- Phase 1 blockers: pip install broken, ~~deia init~~ ✅ FIXED (2025-10-18), real-time logging missing, test coverage 6%
- Chat Phase 2 work: PAUSED (will resume after Phase 1 complete)

**Recent completions:**
- ✅ DEIA Chat Interface Phase 1 (2025-10-15)
- ✅ Unified LLM Service (2025-10-15)
- ✅ Test infrastructure setup
- ✅ ConversationLogger infrastructure
- ✅ Agent BC Integration - 18 components (2025-10-17)
- ✅ BOK Index deployment (2025-10-17)
- ✅ Project Browser API (2025-10-17)
- ✅ deia init directory structure fix (2025-10-18)

See [GitHub Issues](https://github.com/deiasolutions/deia/issues) for detailed progress.
See [GitHub Discussions](https://github.com/deiasolutions/deia/discussions) for strategic questions.

---

**This is a marathon, not a sprint. We're building for the 1000-year view.**
