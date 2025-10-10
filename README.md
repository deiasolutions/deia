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

## Quick Start

```bash
# Clone and install
git clone https://github.com/deiasolutions/deia.git
cd deia
pip install -e .

# Initialize in your project
cd /path/to/your/project
deia init

# Start using DEIA
# (Currently requires manual trigger - see "Current Status" below)
```

**Full guide:** [QUICKSTART.md](QUICKSTART.md)

---

## Current Status: Honest Assessment

### ✅ What Actually Works Today

- **Conversation logging infrastructure:** `ConversationLogger` Python class
- **File writing:** Can save session logs to `.deia/sessions/`
- **CLI commands:** `deia init`, `deia status`, `deia config`, `deia admin`
- **BOK structure:** ~10 community patterns in separate [deia-bok](https://github.com/deiasolutions/deia-bok) repo
- **Privacy architecture:** Local-first storage
- **Governance framework:** Constitution, principles, Ostrom alignment

### ⚠️ What's Infrastructure-Only (Not Production Ready)

**Conversation capture is incomplete:**
- ✅ Can write logs when called: `ConversationLogger().create_session_log(...)`
- ✅ Test mode: `python -m deia.logger` creates sample log
- ❌ Real-time capture from AI tools not implemented
- ❌ Auto-logging requires manual trigger despite config flag

**Why it's not automatic:**
- Claude Code doesn't reliably follow startup instructions (see `.deia/CLAUDE_CODE_FAILURES.md`)
- No OS-level hooks for conversation streaming yet
- Current workaround: User must say "log this" to trigger logging

### 🚧 In Active Development

- **CLI logging:** Making manual triggers easier (`/log` command)
- **Preference system:** Format and parser
- **VS Code extension:** Basic scaffold exists, needs completion
- **Test coverage:** Test infrastructure created, needs expansion

### 📋 Roadmap

See [ROADMAP.md](ROADMAP.md) for phased vision:
- **Phase 1 (Current):** Get basic install working, honest conversation capture
- **Phase 2 (Soon):** Automated pattern extraction
- **Phase 3 (Soon):** Claude Code integration (real auto-logging)
- **Phase 4 (Soon):** VS Code extension (published)
- **Phase 5:** PyPI package
- **Phase 6:** Academic partnerships
- **Phase 7:** Multi-domain expansion (research, healthcare, legal, education)

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

**Test and give feedback:**
1. Clone repo, try `deia init`
2. Report what works vs what breaks
3. [File issues](https://github.com/deiasolutions/deia/issues)

**Contribute patterns:**
1. Use DEIA in your work
2. Extract useful patterns
3. Sanitize (remove PII/secrets)
4. Submit via PR to [deia-bok](https://github.com/deiasolutions/deia-bok)

**Join discussion:**
- [GitHub Discussions](https://github.com/deiasolutions/deia/discussions) - Q&A, ideas
- [Issues](https://github.com/deiasolutions/deia/issues) - Bugs, features

---

## Documentation

**Getting Started:**
- [QUICKSTART.md](QUICKSTART.md) - 3-step installation
- [PRINCIPLES.md](PRINCIPLES.md) - Why DEIA exists
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to participate

**For Developers:**
- [ROADMAP.md](ROADMAP.md) - Phased vision
- [DEV-PRACTICES-SUMMARY.md](docs/DEV-PRACTICES-SUMMARY.md) - Development standards
- [CLAUDE_CODE_FAILURES.md](.deia/CLAUDE_CODE_FAILURES.md) - Known AI limitations

**Architecture:**
- [Constitution](CONSTITUTION.md) - Governance framework
- [Security Architecture](docs/architecture/security.md) - Privacy-first design
- [Ostrom Alignment](docs/governance/ostrom-alignment.md) - Commons governance

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
