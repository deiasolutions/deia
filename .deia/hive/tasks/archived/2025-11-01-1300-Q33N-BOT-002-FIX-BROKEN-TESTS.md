# Task Assignment: BOT-002 - Fix Broken Test Files

**Assigned to:** BOT-002
**Assigned by:** Q33N
**Priority:** P0 - CRITICAL BLOCKER
**Deadline:** 2025-11-01 18:00 CDT
**Scope:** FamilyBondBot Backend Test Suite

---

## Task

The test suite cannot run because 3 test files contain syntax errors. Your job is to fix these errors so all tests can be collected and executed.

**Broken Files:**
1. `backend/tests/contract/test_coaching_messages_post.py` - Line 38
2. `backend/tests/integration/test_chatgpt_integration.py` - Line 238
3. `backend/tests/integration/test_coaching_flow.py` - Line 60

---

## Success Criteria

- [ ] All 3 files have syntax corrected
- [ ] `pytest --collect-only` runs without errors (all 168+ tests collected)
- [ ] All previously passing tests still pass
- [ ] Code follows existing test patterns in the repo
- [ ] No new warnings or deprecation errors introduced

---

## Locations to Check

**Working Directory:**
```
C:\Users\davee\onedrive\documents\github\familybondbot\fbb
```

**Broken Files:**
1. `backend/tests/contract/test_coaching_messages_post.py`
2. `backend/tests/integration/test_chatgpt_integration.py`
3. `backend/tests/integration/test_coaching_flow.py`

**Reference for correct patterns:**
- `backend/tests/contract/test_experiments_api.py` (PASSING - use as model)
- `backend/tests/contract/test_auth_login.py` (PASSING - use as model)

---

## How to Execute

### Step 1: Examine Broken File #1
```bash
cd C:\Users\davee\onedrive\documents\github\familybondbot\fbb
cat backend/tests/contract/test_coaching_messages_post.py | head -50
```
Look at line 38. You'll see invalid JSON literal `{,` with no fields. Fix by:
- Either completing the object with proper fields (see test_experiments_api.py for safety_assessment format)
- Or removing empty object if not needed

### Step 2: Examine Broken File #2
```bash
cat backend/tests/integration/test_chatgpt_integration.py | sed -n '235,240p'
```
Look at line 238. You'll see indentation error. Fix by:
- Checking surrounding context (lines 235-240)
- Re-indenting the assert statement to match the code block

### Step 3: Examine Broken File #3
```bash
cat backend/tests/integration/test_coaching_flow.py | sed -n '55,65p'
```
Look at line 60. Same issue as file #1 - invalid JSON `{,`. Fix by:
- Completing the object or removing it

### Step 4: Validate All Tests Collect
```bash
cd backend
python -m pytest --collect-only -q
```
Expected output: Should show "168 tests collected" or similar (no errors)

### Step 5: Run Tests to Verify No Regressions
```bash
python -m pytest backend/tests/contract/ -v --tb=short
```
All previously passing contract tests should still pass.

---

## Rules

1. **Do not modify test logic** - Only fix syntax errors
2. **Preserve test intent** - If a test checks something, keep that check
3. **Match existing patterns** - Look at passing tests for format consistency
4. **No new dependencies** - Don't add imports or external libraries
5. **No changes to fixtures** - Only fix the broken syntax

---

## Deliverable Format

Create a response file at:
```
C:\Users\davee\onedrive\documents\github\deiasolutions\.deia\hive\responses\bot-002-FIX-BROKEN-TESTS-complete.md
```

Include:
- [x] Status: COMPLETE or BLOCKED
- Description of fixes applied to each file
- Test collection output (pytest --collect-only)
- Summary of passing tests
- Any issues encountered
- Time spent

---

## Notes

- These 3 files appear to be recently edited with incomplete fixture objects
- Fixing them unblocks the entire test suite
- After this is complete, BOT-003 and BOT-004 can proceed with encryption work
- This is the critical path item for beta launch

---

**Questions?** Check test_experiments_api.py and test_health_endpoints.py for passing test patterns.
