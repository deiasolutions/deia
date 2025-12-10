# Windows Git Bash Path Conversion Issues

**Platform:** Git Bash on Windows
**Issue Type:** MSYS Path Conversion
**Severity:** Medium - Can break CLI commands using `/` as command names
**Date Added:** 2025-10-11
**Discovered In:** BOT-00003 slash command implementation

---

## Summary

Git Bash on Windows automatically converts arguments starting with `/` to Windows absolute paths due to MSYS path conversion. This breaks CLI commands that use `/` as the command name (e.g., `deia /`).

---

## The Problem

### What Happens

When you run a command like:
```bash
deia / --bot BOT-00002 "test command"
```

Git Bash interprets the `/` as a Unix root path and converts it to:
```bash
deia C:/Program Files/Git/ --bot BOT-00002 "test command"
```

This causes Click (or any CLI framework) to fail with:
```
Error: No such command 'C:/Program Files/Git/'
```

### Why It Happens

Git Bash uses MSYS (Minimal SYStem), which provides Unix-like path handling on Windows. MSYS automatically converts paths that look like Unix paths to Windows paths. This is normally helpful (e.g., `/c/Users` → `C:\Users`), but breaks when `/` is used as a command name.

### Impact

- **CLI commands using `/` as command names fail**
- **Only affects Git Bash on Windows** (PowerShell, CMD, WSL, and Linux/Mac terminals work fine)
- **Hard to debug** - Error message doesn't mention path conversion

---

## Detection

### Symptoms
- Command registered correctly in CLI framework (shows in `--help`)
- Command works in PowerShell/CMD/WSL
- Command fails only in Git Bash
- Error message mentions `C:/Program Files/Git/` or similar Windows path

### Verification
```bash
# This will show the path conversion in action
python -c "import sys; print(sys.argv)" / --test
# Output in Git Bash: ['...', 'C:/Program Files/Git/', '--test']
# Output in PowerShell: ['...', '/', '--test']
```

---

## Solutions

### Option 1: Use Alternative Command Name (RECOMMENDED)

Instead of `/`, use a word-based command name:

```python
# Instead of this:
@main.command(name='/')
def slash_command(...):
    ...

# Do this:
@main.command(name='slash')
def slash_command(...):
    ...
```

Usage:
```bash
deia slash --bot BOT-00002 "test command"  # Works everywhere
```

**Pros:**
- Works on all platforms
- Easier to discover in help text
- No workarounds needed

**Cons:**
- Less concise than `/`
- May be less intuitive for users familiar with slash commands

---

### Option 2: Add Alias Command

Support both `/` and `slash` as command names:

```python
@main.command(name='slash', aliases=['/'])
@click.argument('command', nargs=-1, required=False)
def slash_command(command, ...):
    """Send commands to bots. Use 'deia slash' on Windows Git Bash."""
    ...
```

Then document in CLI help:
```
Usage: deia slash [OPTIONS] [COMMAND]...
       deia / [OPTIONS] [COMMAND]...  (Not supported in Git Bash on Windows)
```

**Pros:**
- Supports both styles
- Users can choose based on their environment

**Cons:**
- Needs documentation
- Still breaks in Git Bash for `/` form

---

### Option 3: Environment Variable Workaround

Users can disable MSYS path conversion for specific arguments:

```bash
# For one command:
MSYS2_ARG_CONV_EXCL="/" deia / --bot BOT-00002 "test"

# For entire session:
export MSYS2_ARG_CONV_EXCL="/"
deia / --bot BOT-00002 "test"
```

**Pros:**
- Keeps `/` command name
- No code changes needed

**Cons:**
- Requires user education
- Easy to forget
- Breaks other path conversions in same session

---

### Option 4: Use Alternative Shells

Document that users should use PowerShell, CMD, or WSL instead of Git Bash for this command.

**Pros:**
- No code changes
- Avoids Git Bash quirks

**Cons:**
- Limits user choice
- Poor user experience

---

## Recommendations

### For CLI Design

1. **Avoid single-character commands starting with `/` or `-`**
   - Use word-based command names (e.g., `slash`, `send`, `broadcast`)
   - Reserve special characters for flags/options

2. **Test on multiple shells during development**
   - Git Bash on Windows
   - PowerShell
   - Windows CMD
   - WSL
   - Linux/Mac bash

3. **Document platform limitations clearly**
   - Include in `--help` text
   - Mention in README
   - Add to error messages where possible

### For Users

If you encounter this issue:

1. **Quick fix:** Use PowerShell or CMD instead of Git Bash
2. **Alternative:** Use `MSYS2_ARG_CONV_EXCL="/"` environment variable
3. **Best fix:** Request an alias command from the developer

---

## Related Issues

- [Git for Windows MSYS2 Path Conversion Documentation](https://github.com/git-for-windows/build-extra/blob/master/ReleaseNotes.md#known-issues)
- [Stack Overflow: Git Bash path conversion](https://stackoverflow.com/questions/7250130/how-to-stop-mingw-and-msys-from-mangling-path-names-given-at-the-command-line)

---

## Examples in DEIA

### Issue Encountered
- **File:** `src/deia/slash_command.py`
- **CLI Integration:** `src/deia/cli.py:1128-1194`
- **Command:** `deia /`
- **Status:** Documented limitation
- **Workarounds:** Use `MSYS2_ARG_CONV_EXCL="/"` or alternative shells

### Completion Report
See `.deia/reports/BOT-00003-slash-command-complete.md` for full details.

---

## Prevention Checklist

When designing CLI commands:

- [ ] Avoid command names starting with `/`
- [ ] Test on Git Bash (Windows)
- [ ] Test on PowerShell
- [ ] Test on CMD
- [ ] Test on WSL
- [ ] Test on Linux/Mac bash
- [ ] Document platform limitations
- [ ] Provide alternative command names if using special characters

---

**Last Updated:** 2025-10-11
**Maintained By:** BOT-00003 (Drone-Integration)
**Related Pattern:** CLI Design Best Practices
