# UAT Script: Auto-Logging Feature

**Version:** 0.1.0
**Date:** 2025-10-10
**Tester:** Dave
**Duration:** ~15 minutes

---

## Pre-Test Setup

### 1. Launch Extension Development Host

```bash
# In VS Code, open extension directory
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\extensions\vscode-deia

# Press F5 (or Run > Start Debugging)
# This opens a new VS Code window with extension loaded
```

**Expected:** New "Extension Development Host" window opens

---

### 2. Open Test Project

In the Extension Development Host window:

```bash
File > Open Folder
Navigate to: C:\Users\davee\deia-test
Click "Select Folder"
```

**Expected:**
- Test project opens
- Status bar (bottom right) shows: `$(save) DEIA: Manual` OR `$(record) DEIA: Auto-log ON`

**Checkpoint:** Status bar visible? ☐ Yes ☐ No

---

## Test Suite

### Test 1: Check DEIA Status

**Steps:**
1. Open Command Palette (`Ctrl+Shift+P`)
2. Type: `DEIA: Check Status`
3. Press Enter

**Expected Output:**
```
DEIA Status

Project: deia-test
User: dave
Auto-log: ON (or OFF)
Version: 0.1.0

Sessions: C:\Users\davee\deia-test\.deia\sessions
```

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 2: View Monitor Status (Baseline)

**Steps:**
1. Command Palette (`Ctrl+Shift+P`)
2. Type: `DEIA: Show Monitor Status`
3. Press Enter

**Expected Output:**
```
Auto-Logging Monitor

Status: ⚫ Inactive (or 🟢 Active)
Buffer: 0 messages
Session Duration: 0m 0s

Enable auto-log to start monitoring. (or "Monitoring AI conversations...")
```

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 3: Enable Auto-Logging

**Steps:**
1. Command Palette
2. Type: `DEIA: Toggle Auto-Logging`
3. Press Enter

**Expected:**
- Notification: "DEIA auto-logging enabled"
- Status bar changes to: `$(record) DEIA: Auto-log ON` (orange/yellow background)
- Console log (Help > Toggle Developer Tools): "[DEIA] Auto-logging enabled, monitoring started"

**Verification:**
4. Open file: `C:\Users\davee\deia-test\.deia\config.json`
5. Check: `"auto_log": true`

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 4: Simulate Activity - File Changes

**Steps:**
1. In test project, create new file: `test.txt`
2. Type some content: "Testing DEIA auto-logging"
3. Save file (`Ctrl+S`)
4. Wait 2 seconds
5. Run: `DEIA: Show Monitor Status`

**Expected:**
```
Status: 🟢 Active
Buffer: 0 messages (file changes don't add messages, just reset timer)
Session Duration: 0m 5s (approximate)
```

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 5: Chat with @deia (Message Capture)

**Steps:**
1. Open chat panel (icon in left sidebar, or `Ctrl+Alt+I` if available)
2. Type: `@deia help`
3. Wait for response
4. Run: `DEIA: Show Monitor Status`

**Expected:**
```
Status: 🟢 Active
Buffer: 2 messages (1 user, 1 assistant)
Session Duration: 1m 15s (approximate)
```

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 6: Add More Messages

**Steps:**
1. In chat, type: `@deia status`
2. Wait for response
3. Run: `DEIA: Show Monitor Status`

**Expected:**
```
Buffer: 4 messages (or more)
```

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 7: Manual Save Buffer

**Steps:**
1. Command Palette
2. Type: `DEIA: Save Conversation Buffer Now`
3. Press Enter
4. When prompted "Describe what you were working on":
   - Type: `UAT testing auto-logging feature`
   - Press Enter

**Expected:**
- Notification: "Saved X messages to DEIA" (where X is your buffer count)
- Button: [View Log]
- Click [View Log] - should open the session file

**Verification:**
5. Check file opened: `.deia/sessions/YYYYMMDD-HHMMSS-conversation.md`
6. File should contain:
   - Your context: "UAT testing auto-logging feature"
   - Full transcript with all messages
   - Timestamp

7. Check: `.deia/sessions/INDEX.md`
   - New entry added

8. Check: `project_resume.md`
   - New session listed at top

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 8: Verify Buffer Cleared After Save

**Steps:**
1. Run: `DEIA: Show Monitor Status`

**Expected:**
```
Buffer: 0 messages (cleared after successful save)
Session Duration: 2m 30s (continuing)
```

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 9: Add New Messages and Check Status

**Steps:**
1. In chat: `@deia help` again
2. Wait for response
3. Run: `DEIA: Show Monitor Status`

**Expected:**
```
Buffer: 2 messages (new conversation started)
Session Duration: 3m 0s (continuing)
```

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 10: Disable Auto-Logging

**Steps:**
1. Command Palette
2. Type: `DEIA: Toggle Auto-Logging`
3. Press Enter

**Expected:**
- If buffer has messages: Saves them first
- Notification: "DEIA auto-logging disabled"
- Status bar changes to: `$(save) DEIA: Manual`
- Console log: "[DEIA] Auto-logging disabled, monitoring stopped"

**Verification:**
4. Check `.deia/config.json`: `"auto_log": false`
5. Run: `DEIA: Show Monitor Status`

**Expected:**
```
Status: ⚫ Inactive
Buffer: 0 messages
```

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 11: Re-enable and Test Persistence

**Steps:**
1. Toggle auto-logging ON again
2. Chat with `@deia` (2-3 messages)
3. Close Extension Development Host window (without saving buffer)
4. Press F5 again to relaunch
5. Open test project
6. Run: `DEIA: Show Monitor Status`

**Expected:**
- Status: 🟢 Active (auto-restarts because config has auto_log: true)
- Buffer: 0 messages (previous buffer lost - expected behavior, not persisted across restarts)

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 12: Edge Case - Save Empty Buffer

**Steps:**
1. Ensure buffer is empty (check status)
2. Run: `DEIA: Save Conversation Buffer Now`

**Expected:**
- Notification: "No conversation messages in buffer."
- No prompt for context

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

### Test 13: Error Handling - No DEIA CLI

**Setup:**
```bash
# Temporarily rename deia CLI to simulate missing
# (Skip if you want to avoid breaking things)
```

**Steps:**
1. Have messages in buffer
2. Try to save manually

**Expected:**
- Error notification: "DEIA CLI not found. Install DEIA: pip install -e /path/to/deia"

**Result:** ☐ Skip ☐ Pass ☐ Fail
**Notes:**

---

### Test 14: Inactivity Auto-Save

**Note:** This test requires 5 minutes of waiting. You can skip if time-constrained.

**Steps:**
1. Enable auto-logging
2. Chat with `@deia` (add 2-3 messages to buffer)
3. Run: `DEIA: Show Monitor Status` - note buffer count
4. **Do NOT interact with VS Code for 5 minutes**
5. After 5 minutes, check for auto-save notification

**Expected:**
- After 5min: Notification appears: "DEIA: Conversation auto-logged (X messages)"
- Button: [View Log]
- Buffer cleared automatically

**Result:** ☐ Skip ☐ Pass ☐ Fail
**Notes:**

---

### Test 15: Status Bar Integration

**Steps:**
1. Toggle auto-logging ON
2. Observe status bar

**Expected:**
- Icon: `$(record)`
- Text: "DEIA: Auto-log ON"
- Background: Orange/warning color
- Tooltip (hover): "DEIA auto-logging is enabled. Click for status."

**Steps:**
3. Click status bar item

**Expected:**
- Opens DEIA status dialog (same as running Check Status command)

**Result:** ☐ Pass ☐ Fail
**Notes:**

---

## Post-Test Cleanup

### 1. Review Session Logs

```bash
# Open folder
C:\Users\davee\deia-test\.deia\sessions\

# Should see:
- INDEX.md (updated)
- Multiple conversation log files (*.md)
```

**Verification:**
- Each log has proper format
- Timestamps are correct
- Transcripts captured

**Result:** ☐ Pass ☐ Fail

---

### 2. Check project_resume.md

```bash
# Open file
C:\Users\davee\deia-test\project_resume.md
```

**Expected:**
- Latest session listed at top
- Context matches what you entered
- Link to session log file

**Result:** ☐ Pass ☐ Fail

---

### 3. Developer Console Check

**Steps:**
1. In Extension Development Host: `Help > Toggle Developer Tools`
2. Click "Console" tab
3. Filter for: `DEIA`

**Expected Log Messages:**
```
[DEIA] Extension activating...
[DEIA] Starting conversation monitoring...
[DEIA] Monitoring started
[DEIA] Added user message (buffer: 1 messages)
[DEIA] Added assistant message (buffer: 2 messages)
[DEIA] Saving X messages...
[DEIA] Conversation saved: <path>
```

**Result:** ☐ Pass ☐ Fail
**Errors Found:**

---

## Test Summary

### Counts

- **Total Tests:** 15
- **Passed:** ___
- **Failed:** ___
- **Skipped:** ___

### Critical Issues Found

1.
2.
3.

### Minor Issues Found

1.
2.
3.

### Suggestions for Improvement

1.
2.
3.

---

## Sign-Off

**Tester:** __________________
**Date:** __________________
**Overall Result:** ☐ Pass ☐ Pass with Issues ☐ Fail

**Recommendation:**
☐ Ready for release
☐ Ready with documentation updates
☐ Needs fixes before release

**Notes:**

---

## Quick Test (5-Minute Version)

If you're short on time, run these essential tests:

1. **Test 3:** Enable auto-logging ✓
2. **Test 5:** Chat with @deia ✓
3. **Test 7:** Manual save buffer ✓
4. **Test 8:** Verify buffer cleared ✓
5. **Test 10:** Disable auto-logging ✓

**Quick Pass Criteria:** All 5 tests pass = Feature works!

---

## Troubleshooting Guide

### Issue: Status bar not showing

**Fix:**
1. Check setting: `deia.showStatusBar` (should be true)
2. Check `.deia/` directory exists in project
3. Reload window (`Ctrl+R`)

### Issue: Monitor not starting

**Fix:**
1. Check console for errors
2. Verify `.deia/config.json` has `"auto_log": true`
3. Try toggling off and on again

### Issue: Messages not being captured

**Fix:**
1. Ensure you're using `@deia` participant (not other AI assistants)
2. Check monitor is active: `DEIA: Show Monitor Status`
3. Check console for errors

### Issue: DEIA CLI not found

**Fix:**
```bash
# Install DEIA Python package
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions
pip install -e .

# Verify
deia --version
```

---

**End of UAT Script**
