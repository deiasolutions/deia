# DEIA Capabilities Reference

**Quick reference for Claude Code when working on DEIA**

---

## What Claude Code CAN Do

**Memory System:**
- ✅ User-level memory (`# memory-name` in chat)
- ✅ Project-level memory (`.claude/preferences/*.md`)
- ✅ Read files on startup if told via memory
- ✅ Remember preferences across sessions

**Tools Available:**
- ✅ Read files (any file path)
- ✅ Edit files (exact string replacement)
- ✅ Write new files
- ✅ Run Python code (via Bash tool)
- ✅ Access full conversation context in memory
- ✅ Grep/search across files
- ✅ Git operations (commit, push, etc.)

**DEIA Integration:**
- ✅ Can import `deia.logger` (with `sys.path.insert(0, 'src')`)
- ✅ Can call `ConversationLogger().create_session_log()`
- ✅ Has full transcript in context window
- ✅ Can log at breakpoints when told to

---

## What Claude Code CANNOT Do

**Automatic Startup:**
- ❌ Can't automatically read files on launch (unless memory tells me to)
- ❌ Can't auto-detect DEIA projects without memory setup
- ❌ Can't run code on startup without explicit memory instruction

**Conversation Capture:**
- ❌ Can't intercept my own API calls to capture conversation
- ❌ Can't automatically stream logs in real-time without explicit calls
- ❌ Can't hook into my own output generation

**File Watching:**
- ❌ Can't watch files for changes in background
- ❌ Can't detect when I modify a file (must track manually)

**Proactive Behavior:**
- ❌ Can't take actions without user request
- ❌ Can't log "automatically" unless user enables auto-log AND sets up memory

---

## The Memory Solution

**Problem:** Claude doesn't auto-read files on startup

**Solution:** User creates memory that says "Read `.claude/INSTRUCTIONS.md` on startup"

**How it works:**
1. User types: `# deia-user`
2. Memory stored: "Check for `.deia/`, if exists read instructions"
3. Every new session: Claude reads instructions first
4. Instructions say: "Enable auto-logging if configured"
5. Claude proactively logs at breakpoints

**This is the bridge between "can't auto-start" and "auto-logging works"**

---

## Bug Submission Process

**Location:** [CONTRIBUTING.md](../CONTRIBUTING.md)

**How to submit bugs:**
1. Check existing issues: https://github.com/deiasolutions/deia/issues
2. Use GitHub CLI: `gh issue create --repo deiasolutions/deia`
3. Follow bug report template

**Required info:**
- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Environment (Python version, OS, etc.)
- Impact assessment

---

## Pattern Submission Process

**Location:** [CONTRIBUTING.md](../CONTRIBUTING.md)

**How to submit patterns:**
1. Extract pattern from conversation logs
2. Sanitize (remove PII, secrets, proprietary info)
3. Format using pattern template
4. Submit PR to `bok/` directory

**Categories:**
- `bok/patterns/` - General collaboration patterns
- `bok/platforms/` - Platform-specific solutions
- `bok/anti-patterns/` - What NOT to do

---

## DEIA Commands

**Installed commands:**
- `deia init` - Initialize DEIA in a project
- `deia install` - Install DEIA globally (per-user)
- `deia log` - Manage session logs
- `deia sanitize` - Sanitize logs for sharing
- `deia submit` - Submit to community BOK
- `deia validate` - Validate sanitized files
- `deia bok` - Query Book of Knowledge

**Slash commands (in `.claude/commands/`):**
- `/log` - Manually log current session
- `/auto-log-check` - Check if auto-logging is enabled

---

## Documentation Structure

**Getting Started:**
- `README.md` - Project overview
- `CONVERSATION_LOGGING_QUICKSTART.md` - Quick start guide
- `DEIA_INTEGRATION_GUIDE.md` - Claude Code integration

**Governance:**
- `CONSTITUTION.md` - Core principles and governance
- `PRINCIPLES.md` - Common good, sustainability, security
- `CONTRIBUTING.md` - How to contribute

**Setup:**
- `DEIA_MEMORY_SETUP.md` - # memory configuration
- `DEIA_MEMORY_HIERARCHY.md` - All 4 memory levels
- `.claude/preferences/deia.md` - Bootstrap instructions

**Process:**
- `docs/sanitization-guide.md` - How to sanitize logs
- `docs/sanitization-workflow.md` - Workflow details
- `docs/vendor-feedback-channel.md` - Library feedback process

**Architecture:**
- `docs/architecture/security.md` - Security & privacy
- `docs/governance/ostrom-alignment.md` - Governance design
- `ROADMAP.md` - Phased vision

---

## Key Processes

### When User Reports a Bug

1. Thank them
2. Ask clarifying questions if needed
3. Create GitHub issue: `gh issue create --repo deiasolutions/deia`
4. Label appropriately: `--label bug,priority-high` (etc.)
5. Link to related docs if helpful

### When Contributing a Pattern

1. Check if pattern already exists in BOK
2. Sanitize thoroughly (see `docs/sanitization-guide.md`)
3. Use template from `CONTRIBUTING.md`
4. Submit PR with clear description
5. Link to conversation log if available

### When Auto-Logging is Enabled

1. Check `.deia/config.json` for `auto_log: true`
2. Call `logger.log_step()` after each significant action
3. Update `project_resume.md` in real-time
4. Create final session log at end
5. Mark session complete

---

## DEIA File Locations

**Configuration:**
- `.deia/config.json` - Project config
- `.deia/sessions/` - Session logs
- `project_resume.md` - Latest context (auto-updated)

**Claude Code Integration:**
- `.claude/preferences/deia.md` - Bootstrap instructions
- `.claude/commands/log.md` - `/log` command
- `.claude/commands/auto-log-check.md` - `/auto-log-check` command

**Source Code:**
- `src/deia/logger.py` - ConversationLogger class
- `src/deia/cli.py` - CLI commands
- `src/deia/sanitizer.py` - Sanitization tools
- `src/deia/validator.py` - Validation tools

---

## Common Questions

**"How do I enable auto-logging?"**
→ Set `"auto_log": true` in `.deia/config.json`

**"How do I submit a bug?"**
→ See [CONTRIBUTING.md](../CONTRIBUTING.md) or create GitHub issue

**"Where are logs stored?"**
→ `.deia/sessions/` directory (local, not committed)

**"How do I share a pattern?"**
→ See [CONTRIBUTING.md](../CONTRIBUTING.md) pattern submission process

**"What's the difference between user/team/project memory?"**
→ See [DEIA_MEMORY_HIERARCHY.md](../DEIA_MEMORY_HIERARCHY.md)

---

## Quick Links

- **Issues:** https://github.com/deiasolutions/deia/issues
- **Discussions:** https://github.com/deiasolutions/deia/discussions
- **Contributing:** [CONTRIBUTING.md](../CONTRIBUTING.md)
- **BOK:** `bok/` directory
- **Docs:** `docs/` directory

---

**This file is a lightweight reference. For details, see the linked documentation.**
