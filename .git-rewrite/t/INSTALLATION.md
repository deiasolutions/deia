# DEIA Installation Guide

**Comprehensive installation instructions for all platforms**

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Post-Installation Setup](#post-installation-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Platform-Specific Notes](#platform-specific-notes)
- [Dependencies](#dependencies)
- [Uninstallation](#uninstallation)
- [Setting Up Conversation Logging](#setting-up-conversation-logging-optional)
- [Next Steps](#next-steps)

---

## Prerequisites

### Required

- **Python 3.8+** (Python 3.10+ recommended)
- **pip** (Python package manager)
- **git** (version control)

### Recommended

- **Python 3.13** (latest tested version)
- **Virtual environment** (venv, conda, or similar)
- **50MB free disk space** (for package and dependencies)

### Check Prerequisites

```bash
# Check Python version
python --version
# Should output: Python 3.8.x or higher

# Check pip
pip --version
# Should output: pip X.X.X

# Check git
git --version
# Should output: git version X.X.X
```

If any command fails, install the missing prerequisite first.

---

## Installation Methods

### Method 1: From Source (Current - Recommended)

**Step 1: Clone the repository**

```bash
git clone https://github.com/deiasolutions/deia.git
cd deia
```

**Step 2: Install in editable mode**

```bash
pip install -e .
```

This installs DEIA and all dependencies, making the `deia` command available globally.

**Step 3: Run global installation**

```bash
deia install
```

This creates the global DEIA directory (`~/.deia/`) and sets up user-level configuration.

### Method 2: From PyPI (Coming Soon)

```bash
pip install deia
deia install
```

**Status:** Package structure ready, awaiting PyPI publication.

### Method 3: With Virtual Environment (Recommended for Development)

```bash
# Create and activate virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install DEIA
pip install -e .
deia install
```

---

## Post-Installation Setup

### 1. Verify Installation

```bash
deia --version
# Should output: deia, version 0.1.0

deia --help
# Should show available commands
```

### 2. Initialize a Project

Navigate to your project directory and run:

```bash
cd /path/to/your/project
deia init
```

This creates:
- `.deia/` directory with 11 subdirectories
- `.deia/config.json` (project configuration)
- `.claude/` directory for Claude Code integration
- `project_resume.md` (project context file)

### 3. Configure DEIA (Optional)

```bash
# View current configuration
deia config

# Enable auto-logging
deia config auto_log true

# Set default sanitization level
deia config sanitization_level aggressive
```

### 4. Set Up Claude Code Integration (Optional)

If you use Claude Code:

1. In Claude Code, type: `# deia-user`
2. Paste the content from `.claude/preferences/deia.md`
3. Save the memory

Now Claude will automatically detect DEIA-enabled projects.

---

## Verification

### Basic Verification

```bash
# Check deia command works
deia --help

# Check Python import works
python -c "import deia; print('DEIA imported successfully')"

# Check installed version
python -c "import deia; print(f'Version: {deia.__version__}')"
```

Expected output:
```
DEIA imported successfully
Version: 0.1.0
```

### Test Project Initialization

```bash
# Create test directory
cd /tmp
mkdir test-deia-project
cd test-deia-project

# Initialize DEIA
deia init

# Verify directory structure
ls -la .deia/
```

Expected output: 11 subdirectories created (sessions, bok, index, federalist, governance, tunnel, bot-logs, observations, handoffs, intake, logs).

### Test CLI Commands

```bash
# Test status command
deia status

# Test hive commands
deia hive status

# Test librarian query
deia librarian query "test" --limit 1
```

### Run Diagnostics

```bash
deia doctor
```

This runs a comprehensive diagnostic check and reports any issues.

---

## Troubleshooting

### Issue: `pip install -e .` fails with "No module named setuptools"

**Solution:**
```bash
pip install --upgrade setuptools wheel
pip install -e .
```

### Issue: `deia` command not found after installation

**Solution 1: Check pip install location**
```bash
pip show deia
# Check that 'Location' is in your Python site-packages
```

**Solution 2: Reinstall in user mode**
```bash
pip install --user -e .
```

**Solution 3: Check PATH**
```bash
# Windows
echo %PATH%

# Mac/Linux
echo $PATH
```

Ensure Python Scripts directory is in PATH:
- Windows: `C:\Users\<username>\AppData\Local\Programs\Python\Python3XX\Scripts`
- Mac/Linux: `~/.local/bin` or `/usr/local/bin`

### Issue: Permission denied on `deia install`

**Solution:**
```bash
# Windows: Run as Administrator
# Mac/Linux: Check directory permissions
chmod 755 ~/.deia
```

### Issue: Import errors for dependencies

**Solution:**
```bash
# Reinstall all dependencies
pip install --force-reinstall -e .

# Or install dependencies manually
pip install click pyyaml rich python-dateutil requests watchdog scikit-learn rapidfuzz fastapi uvicorn websockets chardet
```

### Issue: `deia init` creates incomplete directory structure

**Solution:** This was a known bug, fixed in version 0.1.0 (2025-10-18).

Update to latest version:
```bash
cd /path/to/deia
git pull
pip install -e .
```

### Issue: Conflicts with existing DEIA installation

**Solution:**
```bash
# Uninstall old version
pip uninstall deia

# Clean cache
pip cache purge

# Reinstall
pip install -e .
```

---

## Platform-Specific Notes

### Windows

**Prerequisites:**
- Git Bash recommended for CLI commands
- Windows Terminal for better CLI experience
- Visual Studio Build Tools (for some dependencies)

**Installation:**
```bash
# Clone
git clone https://github.com/deiasolutions/deia.git
cd deia

# Install
pip install -e .
deia install
```

**PATH Configuration:**
If `deia` command not found, add Python Scripts to PATH:
1. Search "Environment Variables" in Windows
2. Edit PATH
3. Add: `C:\Users\<username>\AppData\Local\Programs\Python\Python3XX\Scripts`

### macOS

**Prerequisites:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.13

# Install git
brew install git
```

**Installation:**
```bash
git clone https://github.com/deiasolutions/deia.git
cd deia
pip3 install -e .
deia install
```

**Note:** Use `pip3` and `python3` explicitly on macOS to avoid conflicts with system Python 2.

### Linux (Ubuntu/Debian)

**Prerequisites:**
```bash
sudo apt update
sudo apt install python3 python3-pip git python3-venv
```

**Installation:**
```bash
git clone https://github.com/deiasolutions/deia.git
cd deia
pip3 install -e .
deia install
```

**PATH Configuration:**
If `deia` not found, add to `~/.bashrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### Linux (Fedora/RHEL)

**Prerequisites:**
```bash
sudo dnf install python3 python3-pip git
```

**Installation:** Same as Ubuntu/Debian above.

---

## Dependencies

DEIA installs the following dependencies automatically:

**Required (runtime):**
- `click>=8.0` - CLI framework
- `pyyaml>=6.0` - YAML parsing
- `rich>=13.0` - Terminal formatting
- `python-dateutil>=2.8` - Date handling
- `requests>=2.28` - HTTP requests
- `watchdog>=3.0` - File monitoring
- `scikit-learn>=1.3.0` - ML utilities
- `rapidfuzz>=3.0.0` - Fuzzy string matching
- `fastapi>=0.104.0` - Web API framework
- `uvicorn>=0.24.0` - ASGI server
- `websockets>=12.0` - WebSocket support
- `chardet>=5.0` - Character encoding detection

**Optional (development):**
- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Coverage reporting
- `pytest-mock>=3.12` - Mocking
- `black>=23.0` - Code formatting
- `ruff>=0.1.0` - Linting
- `mypy>=1.0` - Type checking

**Install dev dependencies:**
```bash
pip install -e ".[dev]"
```

---

## Uninstallation

### Remove DEIA Package

```bash
pip uninstall deia
```

### Remove Global DEIA Directory (Optional)

```bash
# This deletes user-level configuration
rm -rf ~/.deia/
```

### Remove Project-Level DEIA (Per Project)

```bash
# In project directory
rm -rf .deia/
rm -rf .claude/
rm project_resume.md
```

---

## Setting Up Conversation Logging (Optional)

DEIA can automatically log all your AI assistant conversations to preserve context and enable crash recovery.

### Quick Setup

**Step 1: Verify your project is initialized**

```bash
ls .deia/config.json
```

If the file doesn't exist, run:
```bash
deia init
```

**Step 2: Enable auto-logging**

Edit `.deia/config.json` and set `auto_log` to `true`:

```json
{
  "project": "your-project",
  "user": "your-name",
  "auto_log": true,
  "version": "0.1.0"
}
```

Or use the CLI (if available):
```bash
deia config set auto_log true
```

**Step 3: Verify configuration**

```bash
cat .deia/config.json
```

Should show `"auto_log": true`

**Step 4: Start logging**

In Claude Code, use these commands:
- `/log` - Save current conversation manually
- `/start-logging` - Begin session-based auto-logging

**Step 5: Verify logs are created**

```bash
ls .deia/sessions/
```

You should see conversation log files.

###  What Gets Logged

When you run `/log` or `/start-logging`, Claude will save:
- Full conversation transcript (user messages + AI responses)
- Key decisions made
- Files created or modified
- Action items (completed and pending)
- Next steps for continuity

### Where Logs are Stored

**Location:** `.deia/sessions/`

**Files created:**
- `YYYYMMDD-HHMMSS-conversation.md` - Individual session logs
- `INDEX.md` - Master index of all sessions
- Updates to `project_resume.md` in project root

### Manual Logging

Use `/log` when you want to save a specific conversation:

```
User: /log

Claude:
✓ Logged to: .deia/sessions/20251018-090000-conversation.md
```

**Best for:**
- Saving after task completion
- Before ending a session
- Preserving important decisions

### Session-Based Auto-Logging

Use `/start-logging` for long sessions with periodic saves:

```
User: /start-logging

Claude:
✓ Auto-logging started
Session: 20251018-090000-conversation
I'll save periodically and notify you.

[... work continues ...]

Claude: [Response]
✓ Log updated (10 messages)

[... session ends ...]

User: that's it

Claude:
✓ Session logged to `.deia/sessions/20251018-090000-conversation.md`
```

**Best for:**
- Long debugging sessions (>1 hour)
- Multi-hour feature development
- Insurance against crashes

### Disable Logging

**Method 1: Don't enable it**
- Keep `auto_log: false` in config
- Don't use `/log` or `/start-logging` commands

**Method 2: Remove from config**

```json
{
  "auto_log": false
}
```

### Full Documentation

For complete details, see: **[Conversation Logging Guide](docs/guides/CONVERSATION-LOGGING-GUIDE.md)**

Covers:
- Advanced features
- Troubleshooting
- API reference
- Examples
- FAQ

---

## Next Steps

After successful installation:

1. **Read the Quick Start:** [QUICKSTART.md](QUICKSTART.md)
2. **Explore the CLI:** `deia --help`
3. **Initialize a project:** `deia init`
4. **Set up logging:** See [Conversation Logging](#setting-up-conversation-logging-optional) above
5. **Review principles:** [PRINCIPLES.md](PRINCIPLES.md)
6. **Check the roadmap:** [ROADMAP.md](ROADMAP.md)

---

## Getting Help

**Installation issues:**
- File an issue: https://github.com/deiasolutions/deia/issues
- Run diagnostics: `deia doctor`
- Check FAQ: [README.md](README.md#faq)

**General questions:**
- GitHub Discussions: https://github.com/deiasolutions/deia/discussions
- Documentation: [README.md](README.md)

---

**Installation guide last updated:** 2025-10-18
**Verified on:** Python 3.8-3.13, Windows 11, macOS 14, Ubuntu 22.04
