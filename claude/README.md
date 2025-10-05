# DEIA - Development Evidence & Insights Automation

**Learn from every AI-assisted development session. Build better with AI.**

> Platform-agnostic knowledge sharing for developers using Claude Code, Cursor, GitHub Copilot, and other AI coding assistants.

---

## What is DEIA?

DEIA is a methodology and toolkit for capturing, sanitizing, and sharing learnings from AI-assisted development sessions. It helps:

- **Individuals** learn from their own sessions over time
- **Teams** build institutional knowledge about effective AI collaboration
- **The community** discover patterns and anti-patterns in human-AI development

## Quick Start

### Installation

```bash
pip install deia
```

### Initialize in Your Project

```bash
cd your-project
deia init --platform claude-code
```

### Create a Session Log

```bash
deia log create --topic "refactoring-auth-service"
```

### Sanitize Before Sharing

```bash
deia sanitize devlogs/intake/your-session.md
```

### Submit to Community

```bash
deia submit devlogs/intake/your-session_SANITIZED.md
```

---

## Features

✅ **Privacy-first** - Automated sanitization removes PII, secrets, and IP
✅ **Platform-agnostic** - Works with Claude Code, Cursor, Copilot, and more
✅ **Book of Knowledge** - Searchable community wisdom
✅ **Governance framework** - Constitutional protection against misuse
✅ **Open source** - MIT licensed, community-driven

---

## Why DEIA?

### The Problem

Developers are learning valuable lessons from AI-assisted coding sessions, but this knowledge is:
- Lost when sessions auto-compact
- Siloed to individuals
- Not shared due to privacy/IP concerns
- Not systematically analyzed

### The Solution

DEIA provides:
1. **Templates** for capturing sessions systematically
2. **Automated sanitization** to protect privacy and IP
3. **Community repository** for sharing sanitized learnings
4. **Book of Knowledge** with searchable patterns

### Example Learnings Captured

From real sessions:
- "Railway edge proxy rewrites HTTPS to HTTP in redirects" → Middleware solution
- "Use `window.location.origin` for preview URL detection" → Environment-agnostic pattern
- "Never deploy to production without explicit approval" → Governance rule
- "Test URLs yourself before asking human to click" → Collaboration anti-pattern

---

## Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Sanitization Guide](SANITIZATION_GUIDE.md)
- [Contributing](CONTRIBUTING.md)
- [Constitution](DEIA_CONSTITUTION.md)
- [Security Architecture](SECURITY_ARCHITECTURE.md)

---

## Project Status

**Current:** Alpha (v0.1.0)
**Maintainer:** Dave E. ([@deiasolutions](https://github.com/deiasolutions))
**License:** MIT
**Governance:** Benevolent dictator → Foundation (planned)

---

## Governance & Sustainability

DEIA is committed to long-term sustainability:

- **Phase 1 (Now):** Maintainer-reviewed contributions, building community
- **Phase 2 (Year 1-2):** Non-profit foundation, governance board
- **Phase 3 (Year 2+):** Paid maintainers, sustainable operations

### Support DEIA

[GitHub Sponsors](https://github.com/sponsors/deiasolutions) | [OpenCollective](https://opencollective.com/deia)

Donations fund:
- Infrastructure (servers, security, CI/CD)
- Paid maintainers to review contributions
- Community events and conferences
- Documentation and whitepapers

---

## Community

- [GitHub Discussions](https://github.com/deiasolutions/deia/discussions)
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

---

## Roadmap

**v0.1.0 (Current):**
- ✅ CLI tool (`pip install deia`)
- ✅ Automated sanitization
- ✅ Template system
- ✅ Local BOK

**v0.2.0 (Next):**
- GitHub PR automation for submissions
- Enhanced PII detection (ML-based)
- BOK sync from community repo
- Platform-specific guides

**v0.3.0 (Future):**
- MCP integration for platform vendors
- Vendor collaboration framework
- Advanced analytics on BOK
- First annual DEIA conference

---

## Philosophy

> "Learn together. Protect each other. Build better."

DEIA believes:
- Knowledge should be shared, but privacy must be protected
- Community intelligence beats individual experience
- AI-assisted development is collaborative, not autonomous
- Open governance prevents capture by any single interest

---

## Contributors

Thank you to all our contributors! [See the list](CONTRIBUTORS.md)

---

## License

MIT License - see [LICENSE](LICENSE) for details

---

**Built with ❤️ by the AI-assisted development community**
