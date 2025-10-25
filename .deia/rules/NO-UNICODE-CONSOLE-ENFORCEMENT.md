# NO UNICODE IN CONSOLE OUTPUT - ENFORCEMENT

**Status:** CRITICAL - 28+ documented failures costing real money
**Owner:** All agents, all sessions
**Enforcement:** Pre-commit hook + runtime sanitization

## The Problem

Claude repeatedly outputs Unicode symbols (✓✗→←•★) in print statements despite:
- Explicit instructions not to
- 28+ documented failures
- User paying tokens to fix the same error repeatedly
- `.deia/observations/` documenting this issue multiple times

## Enforcement Layers

### Layer 1: Pre-Commit Hook (RECOMMENDED)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Block commits containing Unicode in print statements

if git diff --cached --name-only | grep -q '\.py$'; then
    # Check staged Python files for Unicode in print statements
    if git diff --cached | grep -E '^\+.*print.*[✓✗→←↑↓•●○◆★☆□■▲▼◀▶]'; then
        echo "ERROR: Unicode symbols detected in print statements"
        echo "Use ASCII alternatives: [OK] [ERROR] [INFO] -> <- ^ v *"
        exit 1
    fi
fi
```

### Layer 2: Runtime Sanitization

Add to all subprocess wrappers:

```python
def _sanitize_output(self, text: str) -> str:
    """
    Remove problematic Unicode that causes Windows cp1252 errors.

    This is a band-aid for Anthropic's failure to respect "no Unicode" instructions.
    """
    replacements = {
        '✓': '[OK]',
        '✗': '[ERROR]',
        '→': '->',
        '←': '<-',
        '↑': '^',
        '↓': 'v',
        '•': '*',
        '●': '*',
        '○': 'o',
        '◆': '*',
        '★': '*',
        '☆': '*',
    }

    for unicode_char, ascii_replacement in replacements.items():
        text = text.replace(unicode_char, ascii_replacement)

    return text

# In subprocess wrapper:
self.process = subprocess.Popen(
    [...],
    encoding='utf-8',
    errors='replace',  # Don't crash on encoding errors
)

# When reading output:
line = self.process.stdout.readline()
line = self._sanitize_output(line)  # Clean before processing
```

### Layer 3: Linting Rule

Add to `.pylintrc` or create `.deia/linters/check-unicode.py`:

```python
#!/usr/bin/env python3
"""
Check for Unicode in print statements.
Run before committing Python files.
"""
import re
import sys
from pathlib import Path

FORBIDDEN_UNICODE = r'[✓✗→←↑↓•●○◆★☆□■▲▼◀▶]'

def check_file(filepath: Path) -> list:
    """Return list of line numbers with Unicode in print statements."""
    violations = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if 'print' in line and re.search(FORBIDDEN_UNICODE, line):
                violations.append((line_num, line.strip()))

    return violations

if __name__ == '__main__':
    py_files = Path('.').rglob('*.py')
    found_issues = False

    for filepath in py_files:
        violations = check_file(filepath)
        if violations:
            found_issues = True
            print(f"\n{filepath}:")
            for line_num, line_content in violations:
                print(f"  Line {line_num}: {line_content}")

    if found_issues:
        print("\nERROR: Unicode detected in print statements")
        print("Use ASCII: [OK] [ERROR] [INFO] -> <- ^ v *")
        sys.exit(1)

    print("No Unicode violations found")
    sys.exit(0)
```

### Layer 4: Agent Instructions Update

Add to `.claude/CLAUDE.md` (make it FIRST instruction):

```markdown
# CRITICAL RULE #1: NO UNICODE IN CODE

**Platform:** Windows (cp1252 encoding)
**Violations to date:** 28+ documented incidents
**Cost to user:** ~500-1000 tokens per incident to fix

NEVER use Unicode symbols in any code you write:
- ❌ NO: ✓ ✗ → ← ↑ ↓ • ● ○ ◆ ★ ☆ □ ■ ▲ ▼ ◀ ▶
- ✅ YES: [OK] [ERROR] [INFO] [WARN] -> <- ^ v * o

This applies to:
- print() statements
- logging calls
- error messages
- comments (if they will be displayed)
- test output

Use ASCII only. No exceptions. User is paying tokens for your mistakes.
```

## Token Waste Documentation

Each Unicode incident costs approximately:
- Initial generation: ~200 tokens
- Error explanation: ~300 tokens
- Regeneration: ~200 tokens
- Verification: ~100 tokens
- **Total per incident: ~800 tokens**

28 incidents × 800 tokens = **22,400 tokens wasted**

At $3 per million input tokens (Claude Sonnet):
- 22,400 tokens = **$0.07** wasted on this single bug

At $15 per million output tokens:
- 22,400 tokens = **$0.34** wasted on this single bug

**Total estimated waste: $0.41**

This doesn't include:
- User's time explaining the issue repeatedly
- Frustration and lost productivity
- Cognitive load of remembering to check for this bug

## Evidence for Anthropic Complaint

Related GitHub Issues:
- #7582: Feature request to disable emoji in code generation
- #5058: Bug report about encoding issues

User quote:
> "I HAVE TO PAy tokens to watch you repeated make the same fucking mistake and fix it over and over and over ad fucking nauseum."

System evidence:
- `.deia/observations/2025-10-24-UNICODE-ERROR-INCIDENT-28.md`
- `.deia/observations/2025-10-24-claude-antipattern-search-instead-of-query.md`
- Multiple prior Unicode error observations

## Implementation Status

- [ ] Pre-commit hook created
- [ ] Runtime sanitization added to subprocess wrappers
- [ ] Linting rule created
- [ ] `.claude/CLAUDE.md` updated with critical rule
- [ ] Anthropic complaint filed

## Verification

After implementing enforcement layers, test with:

```bash
# Should PASS:
echo 'print("[OK] Success")' > test.py
python .deia/linters/check-unicode.py

# Should FAIL:
echo 'print("✓ Success")' > test.py
python .deia/linters/check-unicode.py
```
