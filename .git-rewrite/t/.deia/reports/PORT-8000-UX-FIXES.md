# Port 8000 Chat Controller - UX/Procedural Fixes Specification
**Date:** 2025-10-25
**Reviewer:** BOT-00004
**Focus:** 5 Critical User Workflows

---

## Workflow 1: Launch Bot

### Current Flow (Broken ❌)

```
User clicks "Launch Bot"
    ↓
Browser prompt() dialog appears
    ↓
User types "BOT-001"
    ↓
No validation feedback
    ↓
User clicks OK
    ↓
Unclear if launch succeeded or failed
    ↓
User has to manually check bot list
```

**Problems:**
- Browser `prompt()` is outdated, ugly
- No input hints or autocomplete
- No success/failure feedback
- Bot might already be running (duplicate launch)
- User uncertain about next step

---

### Proposed Flow (Fixed ✅)

```
User clicks "Launch Bot"
    ↓
Professional modal opens with:
  • Input field (focused, ready to type)
  • List of available bot templates
  • Help text: "Enter bot ID or select template"
    ↓
User types "BOT-001"
    ↓
Real-time validation:
  • "Valid format ✓" or "Invalid format ✗"
  • Check if bot already running: "⚠ Already running"
  • Suggest next available ID if duplicate
    ↓
User clicks "Launch"
    ↓
Progress indicator shows: "Launching BOT-001..."
    ↓
Success message: "✓ BOT-001 launched successfully"
  (with option to "Connect Now")
  OR
Error message: "✗ Failed: [specific reason]"
  (with option to "Try Again")
    ↓
Modal closes, bot appears in list automatically
```

**Improvements:**
- ✅ Professional modal instead of browser prompt
- ✅ Real-time validation with clear feedback
- ✅ Prevents duplicate launches
- ✅ Shows progress during launch
- ✅ Clear success/error messaging
- ✅ Next logical action suggested

---

## Workflow 2: Send Command

### Current Flow (Broken ❌)

```
User selects bot from list
    ↓
Input field STILL disabled (selectBot() missing)
    ↓
User clicks in input → Nothing happens
    ↓
User doesn't know why they can't type
    ↓
User is stuck
```

**Problems:**
- Input never enables (selectBot function missing)
- No feedback on bot selection
- User doesn't know interface is broken
- No visual indication of selected bot

---

### Proposed Flow (Fixed ✅)

```
User clicks bot in list
    ↓
Visual feedback: Bot item highlights
    ↓
Chat header updates: "🔗 Connected to BOT-001"
    ↓
Chat history loads automatically
    ↓
Input field enables with visual feedback:
  • Border color changes to active (#667eea)
  • Placeholder text updates: "Send command to BOT-001..."
  • Cursor placed in field automatically (focus)
    ↓
User types command: "list files"
    ↓
While typing:
  • Sending icon appears on Send button (hover state)
  • Help text shows: "Press Enter or click Send"
    ↓
User presses Enter (or clicks Send)
    ↓
Message appears in chat with user indicator:
  (Blue bubble) "list files"
    ↓
Typing indicator shows: "BOT-001 thinking..."
    ↓
Response appears: (Gray bubble) "files: ..."
    ↓
Clear message attribution:
  • User messages: Blue, right-aligned, "You"
  • Bot messages: Gray, left-aligned, "BOT-001"
    ↓
Input field clears, ready for next message
```

**Improvements:**
- ✅ Input field enables when bot selected
- ✅ Visual selection feedback
- ✅ Chat history auto-loads
- ✅ Clear message attribution
- ✅ Typing indicator shows bot is working
- ✅ Natural keyboard interaction (Enter to send)

---

## Workflow 3: Monitor Status

### Current Flow (Broken ❌)

```
User looks at status panel on right
    ↓
Status panel is empty
    ↓
No information about running bots
    ↓
User doesn't know bot health/uptime/resources
    ↓
Status panel is useless
```

**Problems:**
- Status update polling never starts (statusUpdateInterval = null)
- No visibility into bot state
- Can't tell if bot is healthy vs struggling
- No performance metrics

---

### Proposed Flow (Fixed ✅)

```
Bot launches successfully
    ↓
Status panel auto-updates every 2 seconds:

┌─────────────────────┐
│ 📊 Status Dashboard │
├─────────────────────┤
│ BOT-001             │
│ ✓ Running           │
│ Uptime: 2m 34s      │
│ Memory: 120MB       │
│ CPU: 12%            │
│ Port: 8001          │
│ PID: 5234           │
├─────────────────────┤
│ BOT-002             │
│ ⚠ Busy              │
│ Response time: 3.2s │
│ Queue: 2 messages   │
├─────────────────────┤
│ BOT-003             │
│ ⚠ Idle (30s)        │
│ Ready to receive     │
    ↓
User can:
  • Hover over status item → Tooltip with details
  • Click status item → Detailed metrics chart
  • Color-coded indicators:
    - ✓ Green: Running, healthy
    - ⚠ Orange: Busy, degraded
    - ✗ Red: Error or offline
```

**Improvements:**
- ✅ Status updates auto-poll on schedule
- ✅ Clear health indicators (colors + text)
- ✅ Shows bot metrics (uptime, memory, CPU)
- ✅ Distinguishes between healthy and busy bots
- ✅ Helps user understand bot state

---

## Workflow 4: Switch Between Bots

### Current Flow (Broken ❌)

```
User selects BOT-001
    ↓
User wants to switch to BOT-002
    ↓
User clicks BOT-002 in list
    ↓
Unclear if switch worked
    ↓
Chat history might show mixed messages
    ↓
User confused about which bot is active
```

**Problems:**
- No visual distinction of active bot
- Chat history mixes conversations
- Hard to track which bot is selected
- Session isolation broken

---

### Proposed Flow (Fixed ✅)

```
User clicks BOT-002 in bot list
    ↓
Visual indicators update:
  • BOT-002 item: Highlighted, active state
  • Chat header: Changes to "🔗 Connected to BOT-002"
  • Selected bot ID shown in header
    ↓
Chat messages clear (or separate by session):
  Option A: Clear messages (fresh session)
  Option B: Show "[Session 1: BOT-001]" separator
           Then show "[Session 2: BOT-002]" below
    ↓
Chat history loads for BOT-002 only
    ↓
Input field updates placeholder:
  "Send command to BOT-002..."
    ↓
User sees clear context:
  • Active bot highlighted in list (green left border)
  • Header shows "BOT-002" prominently
  • Chat attribution shows "BOT-002: response"
  • Status panel highlights BOT-002's status
    ↓
User sends message → Routes to BOT-002 only
    ↓
User can switch back to BOT-001 anytime
  → Same clear visual feedback
```

**Improvements:**
- ✅ Active bot always visually clear
- ✅ Session isolation (separate histories)
- ✅ Header always shows selected bot
- ✅ Chat attribution prevents confusion
- ✅ Easy to switch between bots

---

## Workflow 5: View Chat History

### Current Flow (Broken ❌)

```
User selects bot
    ↓
Chat history loads (if it works)
    ↓
All messages appear mixed together
    ↓
No clear timestamps or attribution
    ↓
Hard to trace conversation flow
    ↓
Large history crashes (all in memory)
```

**Problems:**
- History logic is buggy (double-reverse)
- Loads entire file into memory
- No pagination (or broken pagination)
- Mixed sessions unclear
- Slow with large files

---

### Proposed Flow (Fixed ✅)

```
User selects bot
    ↓
Status shows: "Loading history..."
    ↓
Chat panel displays messages in chronological order:

┌────────────────────────────────────┐
│ Oct 25, 2:15 PM                    │ ← Date separator
│                                    │
│           You: list files          │ ← Your message (blue)
│           BOT-001: files: a.txt... │ ← Bot response (gray)
│           [1 min ago]              │ ← Timestamp
│                                    │
│ Oct 25, 2:16 PM                    │ ← Date separator
│           You: show line 10        │
│           BOT-001: Line 10: ...    │
│           [12 sec ago]             │
│                                    │
│ ── Load more history ──             │ ← Pagination control
└────────────────────────────────────┘
    ↓
User can:
  • Scroll up to load earlier messages (pagination)
  • Hover over message → Show full timestamp
  • Click message → Expand/collapse long content
  • Search within session history
    ↓
Clear message structure:
  • User messages: Blue, right-aligned, avatar "You"
  • Bot messages: Gray, left-aligned, avatar "BOT-001"
  • Timestamps: Relative ("5 min ago") + hover for exact
  • Code/commands: Formatted in monospace
```

**Improvements:**
- ✅ Pagination works reliably (session-based)
- ✅ Clear date separators
- ✅ Full message attribution (who said what)
- ✅ Timestamps show context (relative + exact)
- ✅ Handles large histories efficiently
- ✅ Message formatting preserved
- ✅ Scrollable history without crashing

---

## Cross-Workflow Improvements

### Error Handling

**Current:**
- Silent failures
- Unclear error messages
- User doesn't know what to do

**New:**
```
If bot launch fails:
  "✗ Failed to launch BOT-001: Port 8001 already in use
   Suggestion: Try a different bot ID, or stop running bots first."

If message send fails:
  "⚠ Command failed to reach BOT-001 (offline)
   Options: [Retry] [Switch Bot] [Dismiss]"

If WebSocket disconnects:
  "⚠ Lost connection. Reconnecting...
   Reconnection attempts: 3/5"
```

### Loading States

**Current:** Nothing shows during operations

**New:**
```
During bot launch: Spinner + "Launching BOT-001..."
During message send: Button shows loading state (disabled)
During history load: Spinner + "Loading {N} messages..."
During bot switch: Fade out old messages, fade in new
```

### Keyboard Navigation

**Current:** Mouse-only interface

**New:**
```
Shortcuts:
  Ctrl/Cmd + L → Launch bot dialog
  Ctrl/Cmd + Enter → Send message
  Up arrow (in input) → Previous command
  Down arrow (in input) → Next command
  Tab → Switch between bots
  Escape → Close modals
```

---

## Success Metrics

After implementing these fixes, measure:

| Metric | Current | Target |
|--------|---------|--------|
| Time to launch bot | 45s (with confusion) | 15s (clear flow) |
| User errors per session | 3-4 | <1 |
| Chat message success rate | 60% | 98%+ |
| User can identify selected bot | 40% | 100% |
| Perceived responsiveness | Slow | Fast |

---

Generated by BOT-00004
