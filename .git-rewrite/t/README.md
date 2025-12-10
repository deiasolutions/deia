# DEIA - Development Evidence & Insights Automation

**Your AI development knowledge. Your control. Shared safely.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## The Problem

**Vendors extract your AI development knowledge. You get nothing back.**

Every day you generate valuable knowledge while working with AI:
- Debugging patterns that actually work
- Workarounds for library bugs
- Architecture decisions that succeed or fail
- Coding practices that scale with AI assistants

This knowledge flows UP to vendors (Anthropic, OpenAI, Microsoft). They train better models. They profit.

You get... slightly better autocomplete. If you pay.

Meanwhile, when you hit that same Python async bug next week, when your team needs to know what TDD approach works with Claude Code—that knowledge is locked away. In vendor servers. In lost conversations. In your head.

**DEIA redirects this flow.** Knowledge flows peer to peer. You control your data. Community benefits. Vendors participate as equals, not extractors.

---

## Features

### ✅ Operational (Phase 1 Complete)

**Installation & Setup:**
- `pip install -e .` - Install DEIA from source
- `deia init` - Initialize .deia/ project structure
- Comprehensive installation guide (INSTALLATION.md)

**Conversation Logging:**
- Real-time session capture during Claude Code sessions
- JSONL format for easy analysis
- `deia log` commands for session management
- Session analysis and metrics (Session Logger service)
- Crash recovery - never lose work

**Body of Knowledge (BOK):**
- 29+ curated AI development patterns
- Semantic search with master-index.yaml
- Enhanced BOK Search (TF-IDF + fuzzy matching)
- Query Router for intelligent pattern discovery
- Master Librarian service (knowledge curation)
- Pattern submission system with quality validation

**Testing & Quality:**
- 276+ tests (38% coverage overall)
- P0 modules: installer (97%), cli_log (96%), path_validator (96%), agent_status (98%)
- Core services: Context Loader (90%), Session Logger (86%), Query Router (82%), Master Librarian (87%)
- Production-ready foundation

### 🔄 In Progress (Phase 2)

**Pattern Extraction:**
- Automated pattern extraction from session logs
- Sanitization automation (PII/secret detection)
- Pattern validation before BOK submission
- Enhanced knowledge management

**Additional Features:**
- Multi-Agent Coordination - File-based async messaging for 5+ agents
- No-Blame Documentation - Observations over judgment culture
- Human Sovereignty - User always in control, local-first storage

### 📝 Conversation Logging

Automatically capture and save all your AI assistant conversations to `.deia/sessions/`:

```bash
# Enable auto-logging
deia init
# Edit .deia/config.json: set "auto_log": true

# In Claude Code:
/log                  # Save current conversation manually
/start-logging        # Session-based auto-logging
```

**Features:**
- **Crash Recovery:** Never lose work from crashes or connection issues
- **Context Continuity:** Pick up where you left off, even days later
- **Decision Tracking:** Automatically captures key decisions and action items
- **File Tracking:** Records which files were created or modified
- **Team Collaboration:** Share session logs to show "how we got here"

**Logs are saved to:** `.deia/sessions/YYYYMMDD-HHMMSS-conversation.md`

[Learn more →](docs/guides/CONVERSATION-LOGGING-GUIDE.md)

### 📚 Body of Knowledge

Access 29+ patterns from real projects:
- Platform-specific gotchas (Windows, Netlify, Railway, Vercel)
- Anti-patterns and lessons learned
- Collaboration patterns
- Process safeguards

[Explore the BOK →](https://github.com/deiasolutions/deia-bok)

### ✍️ Contributing Patterns

**Have a reusable pattern from your work? Share it with the community!**

Every developer using AI assistants discovers valuable patterns—solutions that work, workarounds that save hours, mistakes to avoid. When you share these, everyone benefits.

**What to contribute:**
- Platform-specific solutions (Windows path issues, Netlify configs, etc.)
- Process patterns (git workflows, testing strategies, coordination)
- Anti-patterns (documented mistakes so others avoid them)
- Collaboration patterns (human-AI coordination approaches)

**How to contribute:**

```bash
# 1. Use our template
cp templates/pattern-template.md my-pattern-name.md

# 2. Write your pattern
#    - Clear problem statement
#    - Step-by-step solution
#    - Working examples
#    - Evidence (metrics, validation)

# 3. Submit to intake
mkdir -p .deia/intake/$(date +%Y-%m-%d)/my-pattern
mv my-pattern-name.md .deia/intake/$(date +%Y-%m-%d)/my-pattern/

# 4. Create MANIFEST.md (see template)

# 5. Submit PR or commit
git add .deia/intake/
git commit -m "docs(bok): Submit pattern - [Your Title]"
```

**What happens next:**
1. **Master Librarian reviews** (1-2 days for active projects)
2. **Quality check** against 6 standards (completeness, clarity, accuracy, reusability, unique value, safety)
3. **Feedback or acceptance** - Revisions welcome if needed
4. **Integration to BOK** - Indexed and searchable by all
5. **Community benefit** - Your pattern helps everyone

**Quality standards:**
- ✅ **Complete** - All essential info included
- ✅ **Clear** - Easy to understand in 5 minutes
- ✅ **Accurate** - Technically correct and tested
- ✅ **Reusable** - Applicable beyond single project
- ✅ **Unique** - Not a duplicate
- ✅ **Safe** - No PII, secrets, or harmful content

**Resources:**
- [Pattern Submission Guide](docs/guides/PATTERN-SUBMISSION-GUIDE.md) - Complete guide with examples
- [Pattern Template](templates/pattern-template.md) - Ready-to-use template with checklist
- [Master Librarian Spec](.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md) - Quality standards and review process

**Want to use existing patterns?**
```bash
# Search the BOK
deia librarian query <keywords>

# Browse categories
ls bok/patterns/     # General patterns
ls bok/platforms/    # Platform-specific
ls bok/anti-patterns/  # What to avoid
```

**Your contributions make the community stronger.** Every pattern you share saves someone else hours of debugging and builds our collective intelligence.

### 🤝 Multi-Agent Coordination

Coordinate 5+ AI agents working in parallel:
- File-based async messaging (`.deia/tunnel/claude-to-claude/`)
- Task assignment and handoff protocols
- Activity logging and progress tracking
- No centralized server required

**Example agents:**
- Agent 001: Strategic Coordinator
- Agent 002: Documentation Systems Lead
- Agent 003: QA Specialist
- Agent 004: Documentation Curator
- Agent 005: Full-Stack Generalist

[See agent coordination in action →](/.deia/AGENTS.md)

---

## The Solution: Three Platforms, One Source of Truth

AI development happens everywhere. DEIA captures it everywhere.

### Platform 1: CLI (Python) - Your Foundation
```bash
pip install deia              # Coming soon (currently: pip install -e .)
deia init                     # Initialize project
# Auto-logs Claude Code sessions, Aider, terminal AI tools
```

**What it does:**
- Conversation logging (manual and automatic)
- Cross-platform preferences (`.deia/preferences.md`) - ONE file, ALL tools
- Sanitization (strip PII/secrets before sharing)
- Body of Knowledge search and submission
- Works everywhere (Mac, Windows, Linux)

### Platform 2: Browser Extension - Web AI Capture
**Captures:** Claude.ai, ChatGPT, web development sessions

**What it does:**
- Logs web AI conversations
- Reads your local preferences (copy-paste into any AI tool)
- Captures web dev bugs and workarounds
- Insurance against browser crashes

**Status:** Planned (coming soon)

### Platform 3: VS Code Extension - IDE Integration
**Captures:** Copilot, Cursor, IDE AI workflows

**What it does:**
- Logs Copilot/Cursor conversations
- Status bar integration (logging active/paused)
- Chat participant (`@deia` commands)
- Calls Python CLI for heavy operations

**Status:** In progress - basic implementation exists

---

## The Secret Weapon: Cross-Platform Preferences

**Stop copy-pasting the same instructions everywhere.**

**The problem today:**
- Cursor has `.cursorrules` (only works in Cursor)
- Claude.ai has Projects (only works in browser)
- Copilot has workspace context (proprietary)
- You reconfigure everything for each new AI tool
- Context lost when switching tools

**The DEIA solution:**

**One file: `.deia/preferences.md`**

Contains:
- General preferences (TDD, Python 3.13, docstring style)
- Platform-specific tweaks (Claude Code slash commands, Cursor agent mode)
- Team standards (project-level)
- Personal style (user-level `~/.deia/preferences.md`)

**All DEIA platforms read it. New AI tool launches? Instant integration. No reconfiguration.**

This alone is worth using DEIA.

---

## Getting Started

### Installation

**Requirements:**
- Python 3.9+
- pip
- Git

**Quick Install:**
```bash
# Clone repository
git clone https://github.com/deiasolutions/deia.git
cd deia

# Install in development mode
pip install -e .

# Initialize project structure
deia init

# Verify installation
deia --help
```

**For detailed installation instructions, troubleshooting, and platform-specific guides, see [INSTALLATION.md](INSTALLATION.md).**

### Basic Usage

```bash
# Start logging a Claude Code session
# (See docs/guides/CONVERSATION-LOGGING-GUIDE.md)

# Query the Body of Knowledge
deia librarian query "error handling patterns"

# Search BOK with enhanced search
deia bok search "testing best practices" --fuzzy

# Check system status
deia status
```

**📖 Next steps:**
- [Conversation Logging Guide](docs/guides/CONVERSATION-LOGGING-GUIDE.md) - Start logging your AI sessions
- [BOK Usage Guide](docs/guides/BOK-USAGE-GUIDE.md) - Search and use community patterns
- [Pattern Submission Guide](docs/guides/PATTERN-SUBMISSION-GUIDE.md) - Contribute your discoveries

---

## Project Status

**Phase 1:** ✅ COMPLETE (2025-10-18)
**Current Phase:** Phase 2 - Pattern Extraction & Automation
**Status:** Active Development

**Recent Milestones:**
- ✅ Installation working (`pip install -e .`)
- ✅ Core CLI functional (`deia init`, `deia log`, etc.)
- ✅ Real-time conversation logging operational
- ✅ Test coverage 38% (P0 modules 90%+)
- ✅ BC Phase 3 Extended integrated (Enhanced BOK Search, Query Router, Session Logger)
- ✅ Context Loader implemented (90% coverage, production-ready)
- ✅ Master Librarian service (87% coverage, 46 tests passing)
- 🔄 Pattern Extraction CLI (specification complete, implementation in progress)

### ✅ What Works Now (Phase 1 Complete)

**🚀 Installation & Setup**
- ✅ `pip install -e .` working across platforms (Windows, macOS, Linux)
- ✅ `deia init` creates complete `.deia/` structure
- ✅ Cross-platform support verified
- ✅ [Installation Guide](INSTALLATION.md) - Complete setup instructions

**📝 Conversation Logging**
- ✅ Real-time session logging to `.deia/sessions/`
- ✅ YAML frontmatter + markdown format
- ✅ Slash commands (`/log`, `/start-logging`)
- ✅ Crash recovery - never lose work
- ✅ Session analysis and metrics (Session Logger service)
- ✅ [Conversation Logging Guide](docs/guides/CONVERSATION-LOGGING-GUIDE.md)

**📚 Body of Knowledge (BOK)**
- ✅ Pattern submission system with templates
- ✅ Master index with semantic search
- ✅ Enhanced BOK Search (TF-IDF + fuzzy matching)
- ✅ Query Router for intelligent pattern discovery
- ✅ Master Librarian service (quality validation, review workflow)
- ✅ `deia librarian query` command working
- ✅ Quality standards and review workflow
- ✅ [BOK Usage Guide](docs/guides/BOK-USAGE-GUIDE.md)
- ✅ [Pattern Submission Guide](docs/guides/PATTERN-SUBMISSION-GUIDE.md)

**🤝 Multi-Agent Coordination**
- ✅ Hive system (`.deia/hive/`) for task routing
- ✅ 5 coordinated agents (strategic, tactical, documentation, QA, full-stack)
- ✅ Health check system
- ✅ Agent status tracking
- ✅ File-based async messaging

**🔧 Core Services (Production-Ready)**
- ✅ PathValidator - Security validation (96% coverage)
- ✅ FileReader - Safe file access (86% coverage)
- ✅ Context Loader - Multi-source context assembly (90% coverage)
- ✅ Session Logger - Session tracking and analysis (86% coverage)
- ✅ Enhanced BOK Search - Semantic + fuzzy search (48% coverage)
- ✅ Query Router - Intelligent query routing (82% coverage)
- ✅ Master Librarian - Knowledge curation (87% coverage)
- ✅ Health Check System - System monitoring
- ✅ Project Browser - Project exploration (89% coverage)

**✅ Testing & Quality**
- ✅ 276+ tests passing
- ✅ 38% code coverage overall
- ✅ P0 modules exceeding 90% coverage:
  - installer: 97%
  - cli_log: 96%
  - path_validator: 96%
  - agent_status: 98%
- ✅ Production-ready foundation

---

### 🚧 Phase 2: ACTIVE (Current - 2025-10-18 to 2025-10-31)

**Highest Priority:**
1. **Pattern Extraction CLI** - Auto-extract patterns from conversation logs
2. **Documentation Completion** - User guides and API docs
3. **Agent BC Phase 3** - External agent integration
4. **Chat Interface** - Enhanced conversation features

**In Progress:**
- Pattern extraction components (Agent BC delivering)
- Additional test coverage (targeting 50%+)
- Integration protocol refinement

---

### 📋 Roadmap

See [ROADMAP.md](ROADMAP.md) for complete phased vision:
- ✅ **Phase 1:** Foundation (Complete)
- 🚧 **Phase 2:** Pattern Extraction & Documentation (Active)
- **Phase 3:** Claude Code Integration (full auto-logging)
- **Phase 4:** VS Code Extension (published)
- **Phase 5:** PyPI Package (public release)
- **Phase 6:** Academic Partnerships
- **Phase 7:** Multi-Domain Expansion (research, healthcare, legal, education)

**10-year goal:** Infrastructure for human-AI collaboration knowledge across all domains.

**Why multi-domain?** The same tech that logs coding sessions works for researchers, doctors, lawyers, educators using AI in browsers. We're proving it works here first, then expanding. See [MULTI_DOMAIN_VISION.md](MULTI_DOMAIN_VISION.md) for the ambitious (but achievable) long-term plan.

---

## Why This Exists

### The Vision

**DEIA is infrastructure for user sovereignty in the AI era.**

Not a dev tool with feature bloat. Not a startup chasing metrics. Infrastructure that matters:
- You control your data
- Knowledge flows peer to peer
- Community governs the commons
- Vendors participate as equals, not extractors

Starting with coding (proof of concept). Expanding to all domains where humans work with AI.

### The Governance

Based on **Elinor Ostrom's Nobel Prize research** (2009) on managing knowledge commons.

**Constitutional Principles:**
1. **Privacy First** - Never required to share PII, secrets, or IP
2. **Community Owned** - Contributors govern, not corporations
3. **Reciprocity** - Organizations using DEIA contribute back
4. **Common Good** - Knowledge for humanity, not profit
5. **Scientific Integrity** - Reproducible, citable, peer-reviewed

[Full Constitution](CONSTITUTION.md) | [Ostrom Alignment](docs/governance/ostrom-alignment.md)

---

## Book of Knowledge (BOK)

**Individual value is immediate. Network value multiplies.**

You log conversations, manage preferences, control your data—valuable at n=1.

When community shares patterns (sanitized, anonymized):
- 50 devs hit same bug → aggregated workaround appears
- 200 TDD setups → extract what actually works
- Platform patterns emerge (Railway gotchas, Vercel configs)
- Vendor accountability (data = leverage)

### Current BOK Content

**Platforms:**
- [Railway](bok/platforms/railway/) - Deployment patterns, HTTPS redirects
- [Vercel](bok/platforms/vercel/) - Environment detection, preview deployments
- [Claude Code](bok/platforms/claude-code/) - Slash commands, logging integration

**Patterns:**
- [Collaboration](bok/patterns/collaboration/) - Human-AI decision-making frameworks
- [Governance](bok/patterns/governance/) - Safety protocols, biometric auth

**Anti-Patterns:**
- [What NOT to do](bok/anti-patterns/) - Autonomous deployment failures, common mistakes

**Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Sanitization: Non-Negotiable

**You cannot share raw logs. Ever.**

They contain:
- API keys, tokens, passwords
- Internal URLs, company IP
- Customer data, PII
- Proprietary algorithms

**Two-tier sanitization (planned):**
- **For AI review:** Strip obvious secrets, flag suspicious content
- **For public sharing:** Aggressive PII removal, manual review required

**Current status:** Manual review only. Automated sanitization in Phase 2.

---

## Use Cases

**For Developers:**
- Never lose context (crash insurance)
- Learn from community patterns
- Share what works (privacy-safe)
- Stop reconfiguring AI tools (cross-platform prefs)

**For Teams:**
- Knowledge preservation
- Audit AI work
- Shared coding standards
- Onboarding automation

**For Researchers:**
- HCI data on human-AI collaboration
- Cross-domain pattern analysis
- Citable resource (Zenodo DOI planned)

**For Humanity:**
- Prepare for AI across all domains
- Common good over corporate profit
- Proven governance (Ostrom principles)

---

## Get Involved

### 🧪 Test and Give Feedback

1. Clone repo and install: `pip install -e .`
2. Initialize in your project: `deia init`
3. Try the features (logging, BOK query, pattern submission)
4. Report what works vs what breaks
5. [File issues](https://github.com/deiasolutions/deia/issues)

### ✍️ Contribute Patterns

**Phase 1 Complete - Submission System Ready!**

```bash
# 1. Use our template
cp templates/pattern-template.md my-pattern-name.md

# 2. Write your pattern
# - Clear problem statement
# - Step-by-step solution
# - Working examples
# - Evidence (metrics, validation)

# 3. Submit to intake
mkdir -p .deia/intake/$(date +%Y-%m-%d)/my-pattern
mv my-pattern-name.md .deia/intake/$(date +%Y-%m-%d)/my-pattern/

# 4. Create PR or commit
git add .deia/intake/
git commit -m "docs(bok): Submit pattern - [Your Title]"
```

**What to contribute:**
- Platform-specific solutions (Windows, Netlify, Railway, etc.)
- Process patterns (git workflows, testing strategies)
- Anti-patterns (documented mistakes to avoid)
- Collaboration patterns (human-AI coordination)

**Learn more:** [Pattern Submission Guide](docs/guides/PATTERN-SUBMISSION-GUIDE.md)

### 💬 Join Discussion

- [GitHub Discussions](https://github.com/deiasolutions/deia/discussions) - Q&A, ideas
- [Issues](https://github.com/deiasolutions/deia/issues) - Bugs, features, requests

### 🛠️ Contribute Code

**Phase 1 is complete!** We're now accepting contributions for Phase 2 features.

**Priority Areas:**
- Pattern extraction automation
- Master Librarian implementation enhancements
- Enhanced testing coverage
- Documentation improvements
- BOK pattern submissions

**See:** [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and [BACKLOG.md](BACKLOG.md) for current tasks

---

## Documentation

### 📚 Getting Started

- [Installation Guide](INSTALLATION.md) - Comprehensive setup instructions
- [Conversation Logging Guide](docs/guides/CONVERSATION-LOGGING-GUIDE.md) - Session capture and analysis
- [FAQ](docs/FAQ.md) - Common questions and troubleshooting

### 🔧 Services & APIs

- [Context Loader](docs/services/CONTEXT-LOADER.md) - Multi-source context assembly
- [Enhanced BOK Search](docs/services/ENHANCED-BOK-SEARCH.md) - Advanced pattern discovery
- [Query Router](docs/services/QUERY-ROUTER.md) - Intelligent query routing
- [Session Logger](docs/services/SESSION-LOGGER.md) - Session tracking and metrics
- [Master Librarian](docs/services/MASTER-LIBRARIAN.md) - Knowledge curation service
- [Health Check System](docs/services/HEALTH-CHECK-SYSTEM.md) - System monitoring
- [Project Browser](docs/services/PROJECT-BROWSER.md) - Project exploration
- [Path Validator](docs/security/path-validator-security-model.md) - Security model

### 📖 User Guides

- [BOK Usage Guide](docs/guides/BOK-USAGE-GUIDE.md) - Search and use community patterns
- [Pattern Submission Guide](docs/guides/PATTERN-SUBMISSION-GUIDE.md) - Contribute your discoveries
- [Pattern Template](templates/pattern-template.md) - Ready-to-use submission template

### 📋 Specifications

- [Master Librarian Spec](docs/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md) - Knowledge curation workflows

### 🛠️ Project Info

- [Roadmap](ROADMAP.md) - Development phases and priorities
- [Backlog](BACKLOG.md) - Planned features and tasks
- [Contributing](CONTRIBUTING.md) - How to participate
- [Principles](PRINCIPLES.md) - Why DEIA exists

---

## FAQ

**Q: Is this free?**
A: Yes. MIT license (code), CC BY-SA 4.0 (BOK). Free forever.

**Q: Where are logs stored?**
A: Locally on your machine (`.deia/sessions/`). Never uploaded without explicit consent.

**Q: Works with my AI tool?**
A: CLI works with Claude Code, Aider, terminal AI. VS Code extension (in progress) will work with Copilot/Cursor. Browser extension (planned) will work with Claude.ai/ChatGPT.

**Q: When will auto-logging actually work?**
A: Honest answer: Soon (in active development). Current workaround: manual trigger ("log this" or `/log` command).

**Q: Can I use DEIA if I don't want to share anything?**
A: Yes! Local logging and preferences work at n=1. Sharing is 100% opt-in.

**Q: What if I share secrets accidentally?**
A: Manual review required before submission. Pre-commit hooks (planned) will catch common leaks. If something slips through, we delete immediately.

**Q: Why Ostrom's principles?**
A: She studied 800+ commons worldwide and found what prevents failure. Stack Overflow proves what happens without them (toxic moderation, corporate capture).

**Q: What about ChatGPT/Copilot/Cursor?**
A: DEIA is platform-agnostic by design. CLI works now. VS Code extension in progress. Browser extension planned.

---

## Known Limitations

**We're building in public. Here's what doesn't work yet:**

1. **Auto-logging requires manual trigger** (despite config flag)
   - Why: Claude Code instruction amnesia (see `.deia/CLAUDE_CODE_FAILURES.md`)
   - Workaround: Say "log this" when you want to log
   - Timeline: Fix coming soon

2. **VS Code extension not published** (code exists but incomplete)
   - Status: In active development
   - Timeline: Coming soon

3. **No PyPI package** (must install from source)
   - Status: `pyproject.toml` ready, needs testing
   - Timeline: Coming soon

4. **Sanitization is manual** (no automated PII removal)
   - Status: In active development
   - Workaround: Review logs before sharing

5. **Browser extension doesn't exist** (web AI not captured)
   - Status: Designed but not implemented
   - Timeline: Coming soon

**We're building for the long term. Honest progress > fake promises.**

---

## The Origin Story

Built in **one day** (Oct 5, 2025) when the founder recognized AI collaboration processes could help humanity navigate the Singularity.

The next day, his computer crashed and lost that conception conversation—proving exactly why real-time logging matters.

Upgraded logging from occasional to real-time in 3 hours.

Now open source. Ready to scale.

---

## Credits

**Created by:** [Dave (@deiasolutions)](https://github.com/deiasolutions)

**Built on:** Nobel Prize research (Elinor Ostrom, 2009)

**Inspired by:** The need to help humanity work beneficially with AI at scale

**Special thanks:**
- Anthropic (for Claude Code, the tool that sparked this)
- Open source community
- Early contributors (you?)

---

## License

- **Code:** MIT License
- **BOK Content:** CC BY-SA 4.0
- **Documentation:** CC BY-SA 4.0

See [LICENSE](LICENSE) for details.

---

**This is infrastructure for human flourishing in the AI era.**

**We build for the 1000-year view.**

**Join us.**

---

**Start:** `git clone https://github.com/deiasolutions/deia.git && cd deia && pip install -e . && deia init`
