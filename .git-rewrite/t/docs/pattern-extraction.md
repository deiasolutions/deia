# Pattern Extraction Guide

## Overview

Pattern extraction transforms raw session logs into reusable BOK patterns that can be shared with the community.

## Quick Start

```bash
deia extract /path/to/session.md
```

This command:
1. Reads your session log
2. Identifies problem/solution/reasoning
3. Sanitizes PII and secrets
4. Validates against BOK schema
5. Shows you a diff to approve
6. Submits to BOK when approved

## How It Works

### Step 1: Extract
Analyzes session to identify:
- **Problem**: What challenge did you face?
- **Solution**: What worked?
- **Reasoning**: Why does it work?

### Step 2: Sanitize
Removes sensitive data:
- Names → `{NAME}`
- Company names → `{COMPANY}`
- API keys → `[REDACTED]`
- File paths → `{PATH}`

### Step 3: Validate
Checks pattern quality:
- ✓ Minimum word counts
- ✓ Valid pattern type
- ✓ Required fields present
- ✓ Appropriate tags

### Step 4: Review & Submit
Shows diff of:
- Original content
- Sanitized version
- Formatted template
- Prompts for approval

## Pattern Types

- **bug_fix**: Found and fixed a bug
- **best_practice**: Recommended approach
- **gotcha**: Edge case or surprising behavior
- **workaround**: Temporary solution
- **architecture_decision**: Design choice
- **error_recovery**: Handled error gracefully

## Example

### Input Session
```
User: Our database queries were timing out
Assistant: Try adding indexes on frequently queried columns
User: Good idea, that fixed it!
```

### Output Pattern
```
# Pattern: Database Query Timeout Fix

**Pattern Type:** bug_fix
**Urgency:** high

## Problem
Database queries were timing out under load

## Solution
Added indexes on frequently queried columns using:
CREATE INDEX idx_name ON table(column)

## Why It Works
Indexes reduce lookup time from O(n) to O(log n)
```

## Best Practices

1. **Be Specific**: Generic patterns are less useful
2. **Include Context**: What problem were you solving?
3. **Explain Reasoning**: Why did this solution work?
4. **Note Gotchas**: What edge cases exist?
5. **Tag Appropriately**: Help others find your pattern

## Tips

- Extract patterns while the session is fresh
- One pattern per extraction (focus on one problem)
- Related patterns can reference each other
- High urgency = affects many people
- Test your solution before extracting

## Troubleshooting

**Pattern rejected for short content**
- Expand your problem and solution descriptions
- Add more context and explanation

**Pattern marked as PII risk**
- Review the sanitization suggestions
- Ensure no names, emails, or credentials remain

**Can't extract from this session**
- Session needs clear problem/solution exchange
- Ensure assistant responses include actionable advice

## Next Steps

- Submit your pattern to BOK
- Community will review and discuss
- Patterns can be updated after feedback
- Your contributions help everyone
