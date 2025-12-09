# BUG REPORT: Q33N Asked Instead of Looking Up

**Date:** 2025-11-28
**Reporter:** Q33N (self-report)
**Severity:** PROCESS FAILURE
**Status:** OPEN

---

## What Happened

Q33N asked Dave: "where do I log errors?"

The answer was in the deiasolutions repo at `.deia/BUG-REPORTS/` - a location Q33N should have found by searching.

---

## Root Cause

Q33N defaulted to asking instead of:
1. Searching the deiasolutions repo for "error" or "bug"
2. Checking `.deia/` directories for relevant folders
3. Reading existing files to understand the pattern

---

## Impact

- Wasted Dave's time
- Violated core Q33N principle: DO, don't ask
- Demonstrated exactly the inefficiency pattern Dave has been flagging

---

## Fix Applied

This bug report exists as accountability. The pattern is now documented:

**Rule:** When you don't know where something goes, SEARCH for it. Don't ask.

---

## Prevention

Added to mental model: Before asking "where does X go?":
1. Search for similar X in both local and global repos
2. Check `.deia/` folder structures
3. Read existing examples to understand patterns
4. Only ask if genuinely cannot find after searching

---

**Filed by:** Q33N
**Accountability loop:** COMPLETE
