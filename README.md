# DEIA - Development Evidence & Insights Automation

**Never lose context. Share what you learn. Build better with AI.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

---

## The Problem

You're building with AI assistants (Claude Code, Cursor, Copilot).

**What happens:**
- Computer crashes → entire conversation lost
- Session resets → AI forgets all context
- Switch projects → waste time re-explaining everything
- Solve hard problems → no one else benefits

**Current solutions:**
- ❌ Anthropic doesn't save conversations
- ❌ Export manually (if you remember)
- ❌ Copy-paste to notes (tedious, inconsistent)
- ❌ Rediscover same patterns others already found

**Result:** AI-assisted development is painful. Knowledge is lost. Progress is repeated.

---

## The Solution

**DEIA provides:**

1. **Conversation Logging** - Automatic, timestamped, never lose context again
2. **Pattern Library (BOK)** - Community knowledge from real AI-assisted work
3. **Privacy-First Sharing** - Contribute without exposing secrets or IP

**Status:** Working system (local), preparing for public launch.

---

## Quick Start

### 1. Log Conversations (Do This First)

**Never lose context again:**

```bash
# Setup (one-time)
pip install deia  # Coming soon - for now use manual setup
mkdir -p .deia/sessions

# Log a conversation
deia log conversation

# Or use Python API
from deia.logger import quick_log
quick_log('what you worked on', 'full transcript')
```

**What you get:**
- Timestamped logs in `.deia/sessions/`
- Automatic index for quick lookup
- Crash recovery in seconds, not hours

**Docs:** [Conversation Logging Guide](docs/conversation-logging.md)

### 2. Search the BOK

**Learn from community patterns:**

```bash
# Search for patterns
deia bok search "authentication"

# Browse by category
ls bok/patterns/collaboration/
ls bok/platforms/railway/
```

**Categories:**
- `bok/patterns/` - General best practices
- `bok/platforms/` - Platform-specific workarounds (Railway, Vercel, AWS)
- `bok/anti-patterns/` - What NOT to do

### 3. Contribute (Optional)

**Share what you learn:**

```bash
# Extract pattern from your logs
deia extract .deia/sessions/conversation.md

# Sanitize (removes PII, secrets, IP)
deia sanitize pattern.md

# Submit to community
deia submit pattern.md
```

**Requirements:**
- Must be universally useful (not project-specific)
- Must be sanitized (no secrets, PII, or proprietary info)
- Must follow BOK format

**Docs:** [Contributing Guide](CONTRIBUTING.md)

---

## Why DEIA Exists

### The $100/Month Problem

> "I'm paying $100/month for Claude Code. It doesn't save conversations. My computer crashes. I lose hours of work. This is unacceptable."
>
> — Dave Eichler, DEIA creator

**DEIA makes AI assistants viable by solving the context-loss problem.**

### The Knowledge Gap

**What exists:**
- Academic research (MIT, Microsoft) - top-down
- Vendor documentation - product-focused
- Stack Overflow - code-focused

**What's missing:**
- Practitioner knowledge from AI-assisted work
- Real patterns from actual usage
- Cross-domain learning
- Privacy-preserving sharing

**DEIA fills this gap.**

---

## Features

### ✅ Conversation Logging
- Automatic timestamped logs
- Structured format (context, decisions, files, next steps)
- Works with any AI tool (Claude Code, Cursor, Copilot)
- Gitignored by default (private)
- Quick recovery after crashes

### ✅ Book of Knowledge (BOK)
- Community-contributed patterns
- Platform-specific workarounds
- Anti-patterns (what NOT to do)
- Searchable, categorized, validated

### ✅ Privacy-First Design
- Local-first logging (never leaves your machine)
- Automatic sanitization tools
- Manual review required before sharing
- Biometric protection for sensitive operations
- Constitutional privacy guarantees

### ✅ Open Source
- MIT license (code)
- CC BY-SA 4.0 (BOK content)
- Community governance
- Transparent operations

### 🔄 Coming Soon
- Automatic BOK extraction from logs
- AI-assisted sanitization
- Pattern validation system
- Web dashboard
- Integration with MCP servers

---

## Installation

### Current (Manual)

```bash
# Clone repo
git clone https://github.com/deiasolutions/deia.git
cd deia

# Install dependencies
pip install -r requirements.txt

# Initialize in your project
deia init
```

### Future (Automated)

```bash
pip install deia
deia init
```

---

## Documentation

### Getting Started
- [Quick Start Guide](QUICKSTART.md) - 5-minute intro
- [Conversation Logging](docs/conversation-logging.md) - Never lose context
- [BOK Format](docs/bok-format.md) - How patterns are structured

### Contributing
- [Contributing Guide](CONTRIBUTING.md) - How to submit
- [Sanitization Guide](docs/sanitization-guide.md) - Privacy rules
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community standards

### Architecture
- [Security Architecture](docs/architecture/security.md) - How we protect privacy
- [Constitution](CONSTITUTION.md) - Governance principles
- [Licensing](LICENSE) - Legal details

### Advanced
- [CLI Reference](docs/cli-reference.md) - All commands
- [Python API](docs/python-api.md) - Programmatic usage
- [Slash Commands](docs/slash-commands.md) - Claude Code integration

---

## BOK Categories

### Platforms
- [Railway](bok/platforms/railway/) - Railway-specific patterns
- [Vercel](bok/platforms/vercel/) - Vercel-specific patterns
- AWS, Azure, GCP (coming soon)

### Patterns
- [Collaboration](bok/patterns/collaboration/) - Human-AI collaboration patterns
- [Governance](bok/patterns/governance/) - Project governance patterns
- Security, Performance (coming soon)

### Anti-Patterns
- [What NOT to do](bok/anti-patterns/) - Common mistakes to avoid

---

## Use Cases

### For Individual Developers
- Log conversations → never lose context
- Search BOK → learn from community
- Contribute patterns → help others

### For Teams
- Shared BOK → consistent practices
- Cross-project learning → avoid repeating mistakes
- Onboarding → new devs learn faster

### For Organizations
- Knowledge preservation → institutional memory
- Pattern extraction → identify best practices
- Compliance → audit AI-assisted work

### For Researchers
- Data source → study human-AI collaboration
- Pattern analysis → identify trends
- Academic publications → cite real usage

---

## Philosophy

### Constitutional Principles

1. **Privacy First** - Never share without explicit consent and sanitization
2. **Community Owned** - Governance by contributors, not corporations
3. **Reciprocity** - Organizations using DEIA must contribute back
4. **Common Good** - Knowledge is for humanity, not profit
5. **Quality Standards** - Validate patterns, verify usefulness

**Full details:** [CONSTITUTION.md](CONSTITUTION.md)

### Governance

- **Maintainers:** Review and merge contributions
- **Contributors:** Submit patterns, validate claims
- **Community:** Discuss, vote, propose changes
- **Board:** Handle disputes, strategic direction

**Future:** Non-profit foundation for sustainable operations

---

## Project Status

**Current Phase:** Local implementation, preparing for public launch

**What works:**
- ✅ Conversation logging system (fully functional)
- ✅ BOK structure defined
- ✅ Sanitization guides written
- ✅ Python CLI tool (functional)
- ✅ Constitutional framework complete

**In progress:**
- 🔄 Public GitHub repository setup
- 🔄 Issue/PR templates
- 🔄 Community onboarding materials

**Coming Q1 2025:**
- 📅 Public launch
- 📅 pip install deia
- 📅 Web dashboard
- 📅 First community patterns

**Roadmap:** [ROADMAP.md](ROADMAP.md) (coming soon)

---

## Community

### Get Involved

**Ways to contribute:**
- Log your conversations, share patterns
- Review submissions, validate patterns
- Improve documentation
- Build tooling
- Report bugs

**Communication:**
- GitHub Discussions (primary)
- Issues (bugs, features)
- Pull Requests (code, patterns, docs)

### Recognition

**Contributors get:**
- Recognition in CONTRIBUTORS.md
- Profile badges (planned)
- Voting rights in governance
- Priority support

---

## FAQ

**Q: Is DEIA free?**
A: Yes. Code is MIT, BOK is CC BY-SA 4.0. Free forever.

**Q: Where are my logs stored?**
A: Locally in `.deia/sessions/` (gitignored). Never uploaded unless you explicitly submit.

**Q: Can I use DEIA commercially?**
A: Yes. MIT license allows commercial use. If you benefit significantly, please contribute back.

**Q: What if my employer has IP concerns?**
A: Logs are private by default. Only share after sanitization and employer approval.

**Q: Does DEIA work with Cursor/Copilot/etc?**
A: Yes. Logging is tool-agnostic. Slash commands are Claude Code-specific, but CLI/API works everywhere.

**Q: How do I know patterns are valid?**
A: Community validation. Patterns marked with confidence level and number of sources.

**Q: Can I contribute anonymously?**
A: Yes. Use pseudonym for submissions. We track contribution, not identity.

**Q: What happens if I accidentally share secrets?**
A: Pre-commit hooks catch common secrets. Manual review is required. If something slips through, we delete and notify.

---

## Credits

**Created by:** Dave Eichler ([@deiasolutions](https://github.com/deiasolutions))

**Inspired by:**
- Frustration with conversation loss in Claude Code
- Need for practitioner knowledge in AI collaboration
- Desire to build collective intelligence

**Built with:**
- Python (Click, Rich)
- Markdown (documentation)
- Git (version control)
- Constitutional principles (governance)

**Special thanks:**
- Anthropic (for Claude Code, despite the lack of conversation persistence)
- Open source community
- Early contributors (coming soon)

---

## License

- **Code:** MIT License - [LICENSE-CODE](LICENSE)
- **BOK Content:** CC BY-SA 4.0 - [LICENSE-BOK](LICENSE)
- **Documentation:** CC BY-SA 4.0

See [LICENSING.md](LICENSING.md) for details.

---

## Links

- **Website:** [deiasolutions.org](https://deiasolutions.org) (coming soon)
- **GitHub:** [github.com/deiasolutions/deia](https://github.com/deiasolutions/deia)
- **Issues:** [Report bugs](https://github.com/deiasolutions/deia/issues)
- **Discussions:** [Join conversation](https://github.com/deiasolutions/deia/discussions)
- **Email:** contact@deiasolutions.org (coming soon)

---

**Never lose context. Share what you learn. Build better with AI.**

**Start logging: `deia log conversation`**
