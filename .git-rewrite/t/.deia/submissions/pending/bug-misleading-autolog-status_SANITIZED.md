---
type: bug
project: deiasolutions
created: 2025-10-09
status: pending
sanitized: true
category: vscode-extension
severity: medium
reporter: davee
---

# Bug: Misleading Auto-log Status in VS Code Extension

## Problem

The VS Code extension status bar displays "DEIA: Auto-log ON" when `auto_log: true` is set in `.deia/config.json`, but **auto-logging is not actually implemented**.

This creates a false expectation that conversations are being automatically captured, when in reality nothing is happening.

## Current Behavior

1. User runs `deia init` (sets `auto_log: true` by default)
2. VS Code extension reads config
3. Status bar shows: "$(record) DEIA: Auto-log ON"
4. User assumes conversations are being logged
5. **Nothing actually gets logged automatically**

## Expected Behavior

**Option A: Be Honest (Recommended)**
- Status bar should indicate feature is not implemented
- Example: "DEIA: Auto-log (Not Implemented)"
- Or: "DEIA: Manual Logging Only"

**Option B: Implement Auto-logging**
- Actually capture conversations automatically
- See related bug: Claude Code startup integration missing

**Option C: Disable Until Implemented**
- Don't show auto-log status at all
- Only show when feature actually works

## Root Cause

**File:** `extensions/vscode-deia/src/statusBar.ts:28`
```typescript
if (this.autoLog) {
    this.statusBarItem.text = '$(record) DEIA: Auto-log ON';
    // ...but there's no code that actually does auto-logging
}
```

**File:** `extensions/vscode-deia/src/extension.ts`
- No event listeners for chat sessions
- No automatic conversation capture
- Only manual logging via `@deia log` command

## Impact

- **User Confusion:** Users think auto-logging works
- **Lost Data:** Users may not manually log, thinking it's automatic
- **Trust Issue:** Status bar is dishonest

## Reproduction

1. Install DEIA: `pip install -e .`
2. Initialize project: `deia init`
3. Install VS Code extension
4. Open VS Code
5. See status bar: "DEIA: Auto-log ON"
6. Have a conversation in GitHub Copilot Chat
7. Check `.deia/sessions/` → **No logs created**

## Environment

- OS: Windows 11
- VS Code: Latest
- DEIA Extension: v0.1.0
- DEIA Python: v0.1.0
- AI Platform: GitHub Copilot

## Suggested Fix

**Immediate (Option A):**
```typescript
// statusBar.ts
if (this.autoLog) {
    this.statusBarItem.text = '$(warning) DEIA: Auto-log (Not Implemented)';
    this.statusBarItem.tooltip = 'Auto-logging is configured but not yet implemented. Use @deia log to manually save conversations.';
    this.statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
}
```

**Long-term (Option B):**
- Implement actual auto-logging
- Hook into chat session events
- Capture conversations automatically
- Requires Claude Code integration (separate bug)

## Related Issues

- Bug: Claude Code startup integration missing
- Feature Request: AI-assisted conversation capture

## Priority

**P2 - Medium**
- Not critical (doesn't break functionality)
- But causes user confusion and false expectations
- Easy fix for Option A (update text)
- Harder fix for Option B (implement feature)

## Acceptance Criteria

**For Option A (Quick Fix):**
- [ ] Status bar text updated to indicate "Not Implemented"
- [ ] Tooltip explains how to manually log
- [ ] Warning background color to indicate incomplete feature
- [ ] User knows auto-log doesn't work yet

**For Option B (Full Fix):**
- [ ] Conversations automatically captured
- [ ] Saved to `.deia/sessions/`
- [ ] Works with Claude Code, GitHub Copilot, etc.
- [ ] User can disable if desired
- [ ] Status bar accurately reflects actual behavior

---

**Submitted via:** DEIA official bug submission process
**Next Steps:** Triage → Prioritize → Assign → Fix
