# DEIA - Development Evidence & Insights Automation

**Knowledge commons for human-AI collaboration. Built for humanity.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## The Mission

As AI reaches every domain of human activity—coding, research, healthcare, legal work, education, business—we need shared knowledge about what works in human-AI collaboration.

**DEIA is that infrastructure.**

Privacy-first. Community-owned. Grounded in [Nobel Prize research](https://en.wikipedia.org/wiki/Elinor_Ostrom) on governing knowledge commons. For the common good.

**Built in one day** to help humanity navigate the Singularity.

---

## What DEIA Does

### 1. Never Lose Context

Computer crashes. AI forgets. You start over.

**DEIA logs everything locally:**
- Real-time conversation logging
- Timestamped sessions in `.deia/sessions/`
- Auto-recovery in seconds, not hours
- Works with Claude Code, Cursor, Copilot, any AI tool

### 2. Learn From the Community

Same problems solved repeatedly. Knowledge stays siloed.

**DEIA shares patterns privacy-safely:**
- Community Book of Knowledge → **[deia-bok](https://github.com/deiasolutions/deia-bok)**
- Platform-specific solutions (Railway, Vercel, AWS)
- Human-AI collaboration patterns
- Anti-patterns (what NOT to do)

### 3. Contribute Without Exposing Secrets

Can't share raw logs (PII, IP, secrets).

**DEIA sanitizes first:**
- Local-first architecture
- Manual review required
- Opt-in sharing only
- Privacy guaranteed by [Constitution](CONSTITUTION.md)

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/deiasolutions/deia.git
cd deia
pip install -e .

# Install globally (one-time setup)
deia install

# Initialize in your project
cd /path/to/your/project
deia init

# Follow the instructions to set up Claude Code memory
# Then start using DEIA - it will auto-log your sessions!
```

**Full guide:** [Conversation Logging Quickstart](CONVERSATION_LOGGING_QUICKSTART.md)

---

## Why This Exists

### The Real Problem

AI collaboration knowledge is lost or siloed:
- Crashes lose entire conversations ($100/month tools don't save)
- Solutions rediscovered repeatedly
- No cross-domain learning (research ≠ coding ≠ healthcare)
- Privacy concerns prevent sharing

### The Real Solution

Knowledge commons with proven governance:
- **Ostrom's 8 principles** (Nobel Prize, 2009) prevent commons failure
- **Privacy-first** architecture (local logging, opt-in sharing)
- **Multi-domain** vision (coding, research, healthcare, legal, education, business)
- **Community-owned** (not corporate controlled)

---

## What Makes DEIA Different

| Other Approaches | DEIA |
|-----------------|------|
| Stack Overflow (toxic moderation) | Ostrom governance (proven at scale) |
| Vendor docs (product-focused) | Practitioner knowledge (real usage) |
| Academic research (top-down) | Community patterns (bottom-up) |
| Central data storage (breach risk) | Local-first (you own your data) |
| One domain only | All domains (cross-learning) |

---

## Philosophy

**Constitutional Principles:**

1. **Privacy First** - Never required to share PII, secrets, or IP
2. **Community Owned** - Contributors govern, not corporations
3. **Reciprocity** - Organizations using DEIA contribute back
4. **Common Good** - Knowledge for humanity, not profit
5. **Scientific Integrity** - Reproducible, citable, peer-reviewed

**Governance:** Based on Elinor Ostrom's research on sustainable commons management. [Full Constitution](CONSTITUTION.md)

**Multi-Domain Vision:** Starting with coding (proof of concept), expanding to research, healthcare, legal, education, business.

---

## Book of Knowledge (BOK)

Community-contributed patterns from real AI-assisted work.

### Platforms
- [Railway](bok/platforms/railway/) - Deployment patterns, HTTPS redirects
- [Vercel](bok/platforms/vercel/) - Environment detection, preview deployments
- [Claude Code](bok/platforms/claude-code/) - Slash commands, logging integration
- More platforms as community contributes

### Patterns
- [Collaboration](bok/patterns/collaboration/) - Human-AI decision-making frameworks
- [Governance](bok/patterns/governance/) - Biometric authentication, safety protocols
- More categories emerging from community

### Anti-Patterns
- [What NOT to do](bok/anti-patterns/) - Autonomous production deployment, common mistakes

**Want to contribute?** See [Contributing Guide](CONTRIBUTING.md)

---

## Use Cases

**For Developers:** Never lose context. Learn from community. Share what works.

**For Researchers:** HCI data. Cross-domain patterns. Citable resource.

**For Organizations:** Knowledge preservation. Audit AI work. Compliance.

**For Humanity:** Prepare for AI across all domains. Common good over corporate profit.

---

## Current Status

### ✅ What Works Now

- Conversation logging **infrastructure** (`ConversationLogger` class with file I/O)
- CLI commands: `deia init`, `deia doctor`, `deia status`, `deia config`, `deia admin`
- BOK structure with initial community patterns (separate repo: deia-bok)
- Privacy-first architecture (local storage)
- Governance framework (Constitution, Principles)
- VSCode extension (basic implementation, not published)

### ⚠️ What's Infrastructure-Only (Not Production Ready)

- **Conversation capture**: Logger can *write* files but can't *capture* live conversations yet
  - Manual API calls work: `ConversationLogger().create_session_log(...)`
  - `python -m deia.logger` creates test data only
  - Missing: Real-time capture from Claude Code/Cursor/other AI tools
- **Auto-logging**: Config flag exists but no mechanism to auto-capture conversations

### 🚧 In Active Development

- `pip install -e .` setup (pyproject.toml ready, needs testing)
- `deia init` command (code exists, needs validation)
- Claude Code integration (slash commands drafted)

### 📋 Roadmap

See [ROADMAP.md](ROADMAP.md) for phased vision:
- **Phase 1:** Get basic install working
- **Phase 2:** Automated pattern extraction
- **Phase 3:** VS Code extension
- **Phase 4:** Multi-domain expansion

---

## Get Involved

**Contribute patterns:**
1. Use DEIA in your work
2. Extract useful patterns
3. Sanitize (remove PII/secrets)
4. Submit via PR

**Join discussion:**
- [GitHub Discussions](https://github.com/deiasolutions/deia/discussions) - Q&A, ideas
- [Issues](https://github.com/deiasolutions/deia/issues) - Bugs, features

**Support the mission:**
- Star this repo
- Share with your community
- Contribute patterns
- [Sponsor development](https://github.com/sponsors/deiasolutions) (coming soon)

---

## Installation

```bash
# Current (manual setup)
git clone https://github.com/deiasolutions/deia.git
cd deia
pip install -r requirements.txt

# Initialize in your project
python -m deia.logger

# Future (automated)
pip install deia
deia init
```

---

## Documentation

**Getting Started:**
- [Conversation Logging Guide](docs/conversation-logging.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Sanitization Guide](docs/sanitization-guide.md)

**Architecture:**
- [Constitution](CONSTITUTION.md) - Governance principles
- [Security Architecture](docs/architecture/security.md)
- [Ostrom Alignment](docs/governance/ostrom-alignment.md)

---

## The Origin Story

Built in **one day** (Oct 5, 2025) when the founder recognized AI collaboration processes could help humanity navigate the Singularity.

The next day, his computer crashed and lost that conception conversation—proving exactly why real-time logging matters.

Upgraded logging from occasional to real-time in 3 hours.

**Now public.** Ready to scale.

---

## FAQ

**Q: Is this free?**
A: Yes. MIT license (code), CC BY-SA 4.0 (BOK). Free forever.

**Q: Where are logs stored?**
A: Locally on your machine (`.deia/sessions/`). Never uploaded without your explicit consent.

**Q: Works with my AI tool?**
A: Yes. Logging works with Claude Code, Cursor, Copilot, any AI assistant.

**Q: Can I contribute anonymously?**
A: Yes. Use a pseudonym. We track contributions, not identity.

**Q: What if I share secrets accidentally?**
A: Manual review required before submission. Pre-commit hooks catch common leaks. If something slips through, we delete immediately.

**Q: Why Ostrom's principles?**
A: She studied 800+ commons worldwide and found 8 design principles that prevent failure. Stack Overflow and Wikipedia show what happens without them.

---

## Credits

**Created by:** [Dave Eichler](https://github.com/deiasolutions)

**Built on:** Nobel Prize research (Elinor Ostrom, 2009)

**Inspired by:** The need to help humanity work beneficially with AI at scale

**Special thanks:**
- Anthropic (for Claude Code)
- Open source community
- Early contributors (you?)

---

## License

- **Code:** MIT License
- **BOK Content:** CC BY-SA 4.0
- **Documentation:** CC BY-SA 4.0

See [LICENSE](LICENSE) for details.

---

**This is infrastructure for human flourishing. Join us.**

**Start: `python -m deia.logger`**
