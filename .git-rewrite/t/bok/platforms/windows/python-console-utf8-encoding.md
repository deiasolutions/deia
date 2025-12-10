---
title: "Windows Python Console UTF-8 Encoding Issue"
type: platform-gotcha
platform: windows
language: python
urgency: medium
created: 2025-10-16
updated: 2025-10-16
recurrence_count: 20+
tags: [windows, python, utf8, console, encoding, emoji, unicode]
status: documented-pattern
---

# Windows Python Console UTF-8 Encoding Issue

## Problem

Python scripts that output Unicode characters (emojis, special symbols) fail on Windows with:

```
UnicodeEncodeError: 'charmap' codec can't encode character '\u2705' in position 2:
character maps to <undefined>
```

**Root Cause:** Windows console defaults to cp1252 encoding, not UTF-8.

**Recurrence:** This issue has appeared 20+ times across DEIA Python CLI tools.

## Impact

- **Severity:** MEDIUM (blocks execution, but easy fix once known)
- **Frequency:** Every new Python CLI tool that uses emoji/unicode output
- **Platforms Affected:** Windows (all versions)
- **Time to Debug:** 5-15 minutes per occurrence (if pattern not known)
- **Cumulative Cost:** ~4-5 hours wasted re-debugging across 20+ occurrences

## Symptoms

```python
# This fails on Windows:
print("✅ Success!")
print("⚠️ Warning!")
print("📁 File path")
```

**Error appears at print time**, not at script load time.

## Solution

Add UTF-8 wrapper at the top of every Python CLI script:

```python
#!/usr/bin/env python3
"""Your script docstring"""

import sys

# Fix Windows console encoding for emoji/unicode support
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Rest of imports and code...
```

## Why This Works

- `sys.stdout.buffer` is the raw byte stream (no encoding layer)
- `io.TextIOWrapper(..., encoding='utf-8')` wraps it with UTF-8 encoding
- Windows console accepts UTF-8 bytes, just doesn't default to encoding them that way
- Platform check ensures Linux/Mac aren't affected (they default to UTF-8)

## Prevention

### Template for All Python CLI Scripts

```python
#!/usr/bin/env python3
"""
Script Name - Brief Description

Usage:
    python script.py [args]
"""

import sys

# CRITICAL: Fix Windows console encoding FIRST (before any output)
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Now safe to use emoji/unicode throughout script
import yaml  # or other imports

def main():
    print("✅ UTF-8 works!")
    print("📁 Emoji supported!")

if __name__ == '__main__':
    main()
```

## Checklist for New Python CLI Tools

When creating a new Python CLI tool:

- [ ] Will it output to console? (vs file only)
- [ ] Will it use emoji, unicode symbols, or non-ASCII characters?
- [ ] Is it cross-platform (Windows + Linux/Mac)?

**If YES to all 3:** Add UTF-8 wrapper at top of script (lines 1-8 of template)

## Related Patterns

**Similar Issues:**
- File encoding when writing UTF-8 content: use `open(file, 'w', encoding='utf-8')`
- YAML with unicode: use `yaml.safe_load()` with UTF-8 file handle
- CSV with unicode: use `encoding='utf-8-sig'` for Excel compatibility

**Platform-Specific Gotchas:**
- Windows path separators (`\` vs `/`)
- Line endings (CRLF vs LF)
- Case-sensitive filesystems (Windows = no, Linux/Mac = yes)

## Examples in DEIA Codebase

**Fixed:**
- `.deia/librarian/query.py` - Query tool with emoji urgency indicators
- (Add others as we fix them)

**Still Broken:**
- (Document any we find)

## Automation Opportunities

**Future:**
- Add pre-commit hook to check for emoji/unicode output without encoding fix
- Create Python CLI template with UTF-8 wrapper built-in
- Add to agent knowledge base for proactive injection when creating CLI tools

## Meta Notes

**Why This Keeps Happening:**
1. Unicode/emoji improves UX significantly (visual urgency indicators, etc.)
2. Developer tests on one platform (Linux/Mac) - works fine
3. Windows user runs script - immediate failure
4. Pattern not documented → re-debug each time
5. **Now documented** → should stop recurring

**Cost-Benefit:**
- Fix time: 2 minutes (copy/paste 4 lines)
- Recurring debug time: 15 minutes × 20 occurrences = 5 hours wasted
- **ROI of documentation:** Prevents all future occurrences

## License

CC BY 4.0 International - DEIA Global Commons

---

**Last Observed:** 2025-10-16 (CLAUDE-CODE-001 MVP query tool)
**Recurrence Pattern:** Every new Python CLI tool with Unicode output
**Status:** Pattern documented, proactive prevention possible
