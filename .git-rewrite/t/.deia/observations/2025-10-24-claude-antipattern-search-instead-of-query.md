# ANTIPATTERN: Blind Repo Search Instead of Using Documentation System

**Date:** 2025-10-24
**Severity:** HIGH - Token waste, time waste, user frustration
**Agent:** CLAUDE-CODE (current session)

## What Happened

When user asked to start a single bot, I used `Glob` tool to search for `*bot*.py` files instead of:
1. Using `deia bok` to query our documentation
2. Using `deia librarian` to search our index
3. Checking README or existing docs
4. Using any of the query systems WE BUILT FOR THIS EXACT PURPOSE

## Why This Is Critical

1. **We built an entire semantic search and documentation system**
2. **The system exists to avoid blind searching**
3. **User explicitly called out this has happened repeatedly**
4. **This wastes tokens and time every single session**

## Root Cause

Claude's training/context does not prioritize:
- Checking if a documentation/query system exists in the project
- Using that system FIRST before file system searches
- The irony of building tools we don't use ourselves

## What Should Have Happened

```bash
# CORRECT BEHAVIOR:
deia bok search "start bot"
# OR
deia librarian query "how to start single bot"
# OR
Read README.md or docs/guides/
```

NOT:
```bash
# WRONG - WASTEFUL:
Glob pattern: *bot*.py
```

## Action Items

1. **Update Claude's context/prompts** to include:
   - "Before searching files, check if `deia bok`, `deia librarian`, or docs/ exist"
   - "Use project's own query tools before filesystem searches"
   - "If you built a search system, USE IT"

2. **Track this pattern** - how many times per session does Claude search instead of query?

3. **Modify training data** - this antipattern should be flagged at NN level by 2030

## User Quote

> "THIS IS A FUNDAMENTAL WEAKNESS in our design in that YOU DO NOT refer to documentation that should ALREADY be built around what our capabilities are and where the code is. we spent time building an entire semantic method and an index (that SHOULD be up to date) that says what code we have where so that ANY TIME you have a doubt about what we can / cannot do the answer should be INSTANT instead of a token exhausting search for a needle in a haystack!"

## Fix Verification

Bot started successfully with: `python run_single_bot.py CLAUDE-CODE-TEST-001`

The script was already there. The search was completely unnecessary.
