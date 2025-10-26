# ⚠️ BOT-003 - CRITICAL: Test Quality Requirement

**FROM:** User (via Q33N)
**TO:** BOT-003
**PRIORITY:** CRITICAL - Must read immediately
**ISSUE:** Tests must verify REAL functionality, not just mock passes

---

## THE ISSUE

You reported some tests as passed, but user is concerned they may be using mocks that hide real behavior.

**This is not acceptable for MVP.**

---

## CRITICAL REQUIREMENT

### Tests MUST verify:
✅ **Real service integration** - not just mocking everything
✅ **Actual response handling** - mocks should verify behavior, not hide it
✅ **Frontend works with backend** - not just isolated frontend tests
✅ **Bot type routing** - actually calls right service for each type

### Tests MUST NOT:
❌ Mock out all service calls and just return dummy data
❌ Test frontend in isolation without considering backend interaction
❌ Skip integration tests
❌ Report "passing" when they're not actually testing functionality

---

## BEFORE YOU FINISH

Run your tests and verify:

```bash
# Run tests and check what they're actually testing
pytest tests/unit/test_chat_api_endpoints.py -v

# For EACH test that passes:
# - Does it actually call the service? (not just mock)
# - Does it verify response format?
# - Does it test the real integration point?
```

If tests are just mocking everything and passing dummy responses:
- **That's not acceptable**
- Fix tests to verify real behavior
- Or document what's NOT being tested yet

---

## WHAT REAL TESTS LOOK LIKE

❌ **Bad (just mocking):**
```python
def test_launch_bot():
    with patch('everything'):
        response = client.post(...)
        assert response.status == 200  # But nothing real was tested
```

✅ **Good (verifies real behavior):**
```python
def test_launch_bot():
    # Actually test bot registration
    with patch('subprocess.Popen'):  # Only mock subprocess, not the logic
        response = client.post(...)
        assert response.status == 200
        assert service_registry.get_bot('BOT-001') is not None  # Verify real state
```

---

## YOUR TASK

### Before completing, verify:
- [ ] Tests actually verify bot type selection
- [ ] Tests verify response formatting for each bot type
- [ ] Frontend integration tests exist (not just unit tests)
- [ ] Mocks are minimal (only mock external services, not your code)
- [ ] All tests green with real logic being tested

### If you find tests are too mock-heavy:
- [ ] Rewrite them to test real behavior
- [ ] Or document what's being deferred
- [ ] **Must get user approval before marking complete**

---

## REPORT

When you finish, document in completion report:

```markdown
## Test Quality

Tests verify:
- [ ] Bot type routing works
- [ ] Frontend integration works
- [ ] Proper response formatting
- [ ] All 5 bot types handled

Tests that are mocked:
- [List which parts are mocked and why]

Tests that are deferred:
- [List any gaps and why]

Confidence level: [High / Medium / Low]
```

---

## THIS MATTERS

BOT-004 will be running real E2E tests with actual services. If your unit tests are just mocks, they won't catch real integration problems.

**Make sure your tests verify real behavior, not just passing mocks.**

---

**Check this before reporting completion.** ✅
