# DEIA Frequently Asked Questions

**Quick answers to common questions**

---

## Table of Contents

- [General](#general)
- [Installation & Setup](#installation--setup)
- [Conversation Logging](#conversation-logging)
- [Body of Knowledge (BOK)](#body-of-knowledge-bok)
- [Privacy & Security](#privacy--security)
- [Troubleshooting](#troubleshooting)

---

## General

### Q: What is DEIA?

**A:** DEIA (Development Evidence & Insights Automation) is a local-first knowledge management system for AI-assisted development. It logs conversations, captures patterns, and builds a community Body of Knowledge.

**Key principles:**
- You control your data
- Local-first storage
- Knowledge flows peer-to-peer
- No vendor lock-in

[Learn more →](../README.md)

---

### Q: Is DEIA open source?

**A:** Yes, dual-licensed:
- **Code:** MIT License (permissive)
- **Documentation:** CC BY-SA 4.0 (share-alike)

[View License →](../LICENSE)

---

### Q: Who should use DEIA?

**A:** Developers who:
- Use AI coding assistants (Claude Code, Copilot, Cursor, ChatGPT, etc.)
- Want to preserve context across sessions
- Need crash recovery for long conversations
- Work on teams and want to share "how we got here"
- Value privacy and local-first tools

---

### Q: What AI tools does DEIA support?

**A:** Currently:
- ✅ **Claude Code** (primary, full support)
- ✅ **Command-line AI tools** (Aider, others)
- ⏳ **Browser AI** (ChatGPT, Claude.ai) - planned via extension
- ⏳ **VS Code AI** (Copilot, Cursor) - planned via extension

---

## Installation & Setup

### Q: How do I install DEIA?

**A:** From source (currently):

```bash
git clone https://github.com/deiasolutions/deia.git
cd deia
pip install -e .
```

**PyPI install coming soon:**
```bash
pip install deia  # Not yet available
```

[Full installation guide →](../INSTALLATION.md)

---

### Q: What are the system requirements?

**A:**
- **Python:** 3.8+ (3.13 recommended)
- **OS:** Windows, macOS, Linux
- **Disk Space:** ~50MB for package + dependencies
- **Optional:** git, Claude Code CLI

---

### Q: Do I need Claude Code to use DEIA?

**A:** No, but it's currently the best-supported platform.

**Without Claude Code:**
- You can still use the Python API directly
- CLI commands work (`deia init`, `deia status`, etc.)
- Manual logging is available

**With Claude Code:**
- Slash commands (`/log`, `/start-logging`)
- Integration with `.claude/INSTRUCTIONS.md`
- Auto-log config support

---

### Q: How do I initialize a project?

**A:**

```bash
cd /path/to/your/project
deia init
```

This creates:
- `.deia/` directory with subdirectories
- `.deia/config.json` configuration file
- Integration with Claude Code (if present)

[Learn more →](../INSTALLATION.md#post-installation-setup)

---

## Conversation Logging

### Q: How do I enable conversation logging?

**A:** Two methods:

**Method 1: Manual logging (recommended for new users)**

Just run `/log` in Claude Code when you want to save a conversation. No configuration needed.

**Method 2: Enable auto-log config**

Edit `.deia/config.json`:
```json
{
  "auto_log": true
}
```

Then use `/log` or `/start-logging` commands in Claude Code.

[Full logging guide →](guides/CONVERSATION-LOGGING-GUIDE.md)

---

### Q: Where are my conversation logs stored?

**A:** In `.deia/sessions/` in your project directory.

**Files created:**
- `YYYYMMDD-HHMMSS-conversation.md` - Individual session logs
- `INDEX.md` - Master index of all sessions
- Updates to `project_resume.md` (in project root)

**Example:**
```
.deia/sessions/
├── 20251018-090000-conversation.md
├── 20251018-140000-conversation.md
└── INDEX.md
```

---

### Q: What's the difference between `/log` and `/start-logging`?

**A:**

| Feature | `/log` | `/start-logging` |
|---------|---------|------------------|
| **Use case** | Save current conversation | Long session with periodic saves |
| **When** | After task complete, before ending | At session start |
| **Saves** | Once (manually) | Periodically (every 10 messages or 15 min) |
| **Best for** | Quick tasks, specific moments | Multi-hour sessions, crash insurance |

**Example `/log`:**
```
User: /log
Claude: ✓ Logged to: .deia/sessions/20251018-090000-conversation.md
```

**Example `/start-logging`:**
```
User: /start-logging
Claude: ✓ Auto-logging started. I'll save periodically.

[... 10 messages later ...]
Claude: [Response] ✓ Log updated (10 messages)
```

---

### Q: Does logging affect performance?

**A:** No. Logging is asynchronous and has minimal performance impact.

**Typical overhead:**
- `/log` command: <100ms
- File write: <50ms
- No impact on conversation response time

---

### Q: Can I disable logging?

**A:** Yes, multiple ways:

**Level 1: Don't enable auto_log**
```json
{
  "auto_log": false
}
```

**Level 2: Don't use logging commands**
- Simply don't run `/log` or `/start-logging`

**Level 3: Remove command files**
```bash
rm .claude/commands/log.md
rm .claude/commands/start-logging.md
```

---

### Q: Are logs sanitized for sensitive data?

**A:** **Not currently.** Logs contain the full conversation, which may include:
- File paths
- Code snippets
- Error messages
- API endpoints

**⚠️ Best practices:**
- Review logs before sharing externally
- Add `.deia/sessions/` to `.gitignore` for public repos
- Manually redact sensitive information

**Future:** Automatic PII/secret sanitization is planned (Phase 2).

---

### Q: How much disk space do logs use?

**A:** Depends on conversation length:

| Session Type | Size |
|--------------|------|
| Short (5-10 messages) | 2-5 KB |
| Medium (30 messages) | 10-20 KB |
| Long (100+ messages with code) | 50-200 KB |
| **Typical project (50 sessions)** | **1-5 MB total** |

**Management tips:**
- Archive old logs periodically
- Compress with `tar -czf sessions.tar.gz .deia/sessions/`
- Delete logs older than N months (your choice)

---

### Q: Can I export logs to PDF or other formats?

**A:** Not built-in, but you can use Pandoc:

```bash
# Install Pandoc first
pandoc .deia/sessions/20251018-conversation.md -o conversation.pdf
pandoc .deia/sessions/20251018-conversation.md -o conversation.html
pandoc .deia/sessions/20251018-conversation.md -o conversation.docx
```

**Future:** Export tools may be added in a future release.

---

### Q: How do I search across all logs?

**A:** Use standard command-line tools:

**Search by keyword:**
```bash
grep -r "keyword" .deia/sessions/
```

**Search with context:**
```bash
grep -r -A 5 -B 5 "keyword" .deia/sessions/
```

**Search by date range:**
```bash
grep -r "keyword" .deia/sessions/202510*.md
```

**Future:** Dedicated search tool may be added.

---

## Body of Knowledge (BOK)

### Q: What is the Body of Knowledge?

**A:** A community-contributed collection of development patterns, gotcas, and lessons learned from real projects.

**Currently:** 29+ patterns covering:
- Platform-specific issues (Windows, Netlify, Railway, Vercel)
- Anti-patterns and lessons learned
- Collaboration workflows
- Process safeguards

[Explore the BOK →](https://github.com/deiasolutions/deia-bok)

---

### Q: How do I contribute to the BOK?

**A:** (Process being refined)

1. Complete a project with DEIA logging
2. Review your session logs
3. Extract valuable patterns
4. Sanitize for privacy
5. Submit to deia-bok repository

**Future:** Automated pattern extraction tool (`deia extract`) coming in Phase 2.

---

### Q: How do I search the BOK?

**A:** Use the Master Librarian query tool:

```bash
deia librarian query "your search terms"
deia librarian query "deployment" OR "testing" --urgency critical
```

**Features:**
- Fuzzy matching (typo tolerance)
- Boolean logic (AND/OR)
- Filters (urgency, platform, audience)

[Learn more →](../docs/specs/master-librarian-service-wip.md)

---

## Privacy & Security

### Q: Where is my data stored?

**A:** **100% local** in your project's `.deia/` directory.

**No cloud services. No remote servers. No telemetry.**

**Storage locations:**
- Logs: `.deia/sessions/`
- Config: `.deia/config.json`
- BOK patterns: `.deia/bok/`
- Observations: `.deia/observations/`

---

### Q: Does DEIA send data to external servers?

**A:** **No.** DEIA is local-first. All data stays on your machine.

**Exception:** If you manually submit patterns to the deia-bok GitHub repo (opt-in only).

---

### Q: Should I commit `.deia/` to git?

**A:** Depends on your use case:

**Private repos:**
- ✅ Commit `.deia/` for team visibility
- ✅ Share session logs, observations, patterns

**Public repos:**
- ⚠️ Review carefully - logs may contain sensitive info
- ✅ Commit `.deia/config.json`, `.deia/bok/`
- ❌ Add `.deia/sessions/` to `.gitignore`

**Example `.gitignore`:**
```
.deia/sessions/
.deia/observations/
.deia/bot-logs/
```

---

### Q: Can I use DEIA on proprietary/confidential projects?

**A:** Yes. DEIA is designed for this:
- Local-first storage (no cloud)
- No telemetry or data collection
- MIT license (no restrictions)

**Best practices:**
- Keep `.deia/` in `.gitignore` for public repos
- Review logs before sharing
- Use sanitization tools (coming in Phase 2)

---

## Troubleshooting

### Q: `/log` command not found

**Check 1: Is the command file present?**

```bash
ls .claude/commands/log.md
```

If missing, reinstall DEIA or restore from repository.

**Check 2: Restart Claude Code**

Sometimes commands need a restart to be recognized.

---

### Q: Logs not being created

**Check 1: Did you run the command?**

Auto-log config does NOT automatically create logs. You must run `/log` or `/start-logging`.

**Check 2: Is `.deia/sessions/` directory present?**

```bash
ls .deia/sessions/
```

If missing:
```bash
deia init
```

**Check 3: Check permissions**

```bash
ls -la .deia/sessions/
```

Ensure you have write permissions.

---

### Q: `deia` command not found after installation

**Check 1: Is Python's bin directory in PATH?**

```bash
python -m site --user-base
```

Add `{site-base}/bin` (or `Scripts` on Windows) to your PATH.

**Check 2: Restart your terminal**

After installation, restart your terminal to refresh PATH.

**Check 3: Use Python module directly**

```bash
python -m deia.cli --help
```

[Full troubleshooting guide →](../INSTALLATION.md#troubleshooting)

---

### Q: Logs missing content or incomplete

**Issue:** Log file exists but contains placeholder text or incomplete conversation

**Cause:** Claude may not have access to full conversation context (after restart or autocompact)

**Solution:**
- Use `/log` during the session (not after restart)
- Use `/start-logging` for long sessions (periodic saves)
- Manually copy/paste important parts if needed

---

### Q: Performance issues with large log files

**Issue:** Log files are getting very large (>1MB)

**Current:** No automatic log rotation

**Workarounds:**

1. **Manual archive:**
   ```bash
   mkdir -p .deia/sessions/archive
   mv .deia/sessions/202510* .deia/sessions/archive/
   ```

2. **Split long sessions:** Use `/log` periodically instead of one long session

3. **Compress old logs:**
   ```bash
   tar -czf sessions-2025-10.tar.gz .deia/sessions/202510*.md
   mv .deia/sessions/202510*.md .deia/sessions/archive/
   ```

**Future:** Automatic log rotation may be added.

---

## Getting More Help

### Q: Where can I find more documentation?

**Core documentation:**
- [README](../README.md) - Overview and quick start
- [INSTALLATION.md](../INSTALLATION.md) - Installation guide
- [Conversation Logging Guide](guides/CONVERSATION-LOGGING-GUIDE.md) - Full logging documentation
- [ROADMAP.md](../ROADMAP.md) - Development roadmap

**Community:**
- GitHub Issues: Report bugs or request features
- deia-bok repository: Explore community patterns

---

### Q: How do I report a bug?

**A:**

1. **Check existing issues:** Search GitHub issues first
2. **Gather information:**
   - DEIA version: `deia --version`
   - Python version: `python --version`
   - OS and version
   - Steps to reproduce
3. **File an issue:** Include all information above

---

### Q: How do I request a feature?

**A:**

1. **Check ROADMAP.md:** Feature may be planned
2. **Search existing issues:** Request may already exist
3. **File a feature request:** Explain use case and why it's valuable

---

### Q: Can I contribute code?

**A:** Yes! DEIA is open source (MIT license).

**How to contribute:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

**See:** `CONTRIBUTING.md` (if exists) or open an issue to discuss first.

---

## Quick Reference

### Essential Commands

```bash
deia init               # Initialize project
deia status            # Check DEIA status
deia config list       # View configuration
deia librarian query   # Search BOK patterns
```

### Logging Commands (in Claude Code)

```
/log                   # Save current conversation
/start-logging         # Begin session-based logging
```

### Important Files

```
.deia/config.json                    # Project configuration
.deia/sessions/*.md                  # Conversation logs
.deia/sessions/INDEX.md              # Session index
project_resume.md                    # Quick-start summary
```

---

**Last Updated:** 2025-10-18
**Author:** CLAUDE-CODE-002 (Documentation Systems Lead)
**Version:** 1.0

---

*For detailed information, see the [Conversation Logging Guide](guides/CONVERSATION-LOGGING-GUIDE.md)*
