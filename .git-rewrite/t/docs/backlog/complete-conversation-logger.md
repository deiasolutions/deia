# Backlog: Complete Conversation Logger

**Status:** Critical - Core feature claimed as working but not production-ready
**Priority:** P0 (Blocking Phase 1 completion)
**Created:** 2025-10-07

---

## Problem Statement

The `ConversationLogger` class exists and can write session logs to `.deia/sessions/`, but it **cannot capture live conversations**.

**Current state:**
- ✅ Infrastructure works (file I/O, formatting, indexing)
- ✅ Manual API calls work: `logger.create_session_log(context, transcript, ...)`
- ❌ No way to capture actual conversations from Claude Code/Cursor/other AI tools
- ❌ `python -m deia.logger` just creates hardcoded test data
- ❌ `auto_log: true` config flag has no implementation

**User impact:** README and docs claim conversation logging works, but users cannot actually log their AI conversations without manually copying/pasting content and calling the API.

---

## Root Cause

See: `docs/postmortems/logger-claims-vs-reality-rca.md`

**TL;DR:** Project built rapidly (1 day) with "build first, integrate later" approach. Infrastructure was implemented but capture mechanism was deferred. This created a gap between what was claimed vs what works.

---

## Requirements

### Must Have (P0)
1. **Capture mechanism** - Some way to get conversation data into the logger
2. **Real conversation data** - Not hardcoded test strings
3. **Works end-to-end** - User can run a command and get their actual conversation logged

### Should Have (P1)
4. **Real-time logging** - Capture during conversation, not just at end
5. **Auto-detection** - Automatically detect when in DEIA project and log
6. **Multiple AI tools** - Works with Claude Code, Cursor, Copilot, etc.

### Nice to Have (P2)
7. **Zero configuration** - Works immediately after `deia init`
8. **Background process** - Runs silently without user intervention
9. **Crash recovery** - Buffers data in case of crashes

---

## Implementation Options

### Option 1: Manual Copy/Paste (Minimum Viable)
**How it works:**
- User copies conversation from AI tool
- Runs: `deia log --from-clipboard` or `deia log --from-file conversation.txt`
- Logger parses and saves

**Pros:**
- Simple to implement
- Works with any AI tool
- No permission/API issues

**Cons:**
- Manual workflow (defeats "auto-logging" claim)
- User must remember to do it
- Doesn't help if crash happens

**Effort:** 2-4 hours

---

### Option 2: File Watcher (Semi-Automated)
**How it works:**
- Claude Code saves conversations to temp files (if it does?)
- DEIA watches those files
- Auto-imports when file changes

**Pros:**
- Automated if temp files exist
- No API access needed
- Works in background

**Cons:**
- Depends on AI tool behavior (may not save temp files)
- Platform-specific (Windows vs Mac vs Linux paths)
- May miss conversations if no temp files

**Effort:** 1-2 days (research + implementation)

---

### Option 3: Claude Code API Integration (Ideal)
**How it works:**
- Use Claude Code's API (if exists) to subscribe to conversation events
- Log in real-time as messages are sent/received
- Full fidelity capture

**Pros:**
- True auto-logging
- Real-time capture
- Crash recovery possible

**Cons:**
- Requires Claude Code API access (may not exist)
- May need Anthropic approval
- Vendor lock-in (Claude-specific)

**Effort:** Unknown (depends on API availability)

---

### Option 4: VSCode Extension Monitoring (Cross-Tool)
**How it works:**
- VSCode extension monitors active editor
- Detects when user is in AI chat
- Captures from extension context

**Pros:**
- Works across multiple AI tools (Claude, Copilot, Cursor)
- Uses existing VSCode extension
- Can run in background

**Cons:**
- VSCode-specific (doesn't help CLI users)
- May have permission issues
- Requires extension development

**Effort:** 2-3 days (already have extension scaffolding)

---

### Option 5: Clipboard Monitoring (Pragmatic)
**How it works:**
- Background service monitors clipboard
- When conversation-like text is copied, prompts: "Log this?"
- One-click to save

**Pros:**
- Works with any AI tool
- Low friction (auto-prompts)
- Cross-platform

**Cons:**
- Privacy concerns (monitoring clipboard)
- May be annoying (false positives)
- Still semi-manual

**Effort:** 1-2 days

---

## Recommended Approach

**Phase 1 (Immediate - Ship Something):**
- **Option 1:** Manual copy/paste with `deia log --from-clipboard`
- Gets us to "conversation logging works" honestly
- Effort: 2-4 hours
- Unblocks Phase 1 roadmap

**Phase 2 (Next Quarter):**
- **Option 4:** VSCode extension monitoring
- True auto-logging for VSCode users
- Effort: 2-3 days
- Covers most DEIA target users

**Phase 3 (Future):**
- **Option 3:** Claude Code API if/when available
- Ideal solution
- Wait for API availability

---

## Tasks

### Immediate (Option 1)
- [ ] Add `deia log --from-clipboard` command
- [ ] Add `deia log --from-file <path>` command
- [ ] Parse conversation format (detect user/assistant messages)
- [ ] Extract context, decisions, files modified automatically (AI-assisted)
- [ ] Update `python -m deia.logger` to show usage instructions (not create test log)
- [ ] Document manual logging workflow
- [ ] Test end-to-end with real Claude Code conversation

### Next (Option 4)
- [ ] Research VSCode extension APIs for chat monitoring
- [ ] Implement background watcher in VSCode extension
- [ ] Add "Log conversation" button to chat interface
- [ ] Auto-detect when in DEIA project
- [ ] Test with Claude Code, Copilot, Cursor

---

## Success Criteria

**Phase 1 (Manual):**
- ✅ User can copy a conversation and run `deia log --from-clipboard`
- ✅ Logger creates properly formatted session log
- ✅ Works with conversations from any AI tool
- ✅ Documentation accurately describes capabilities

**Phase 2 (Auto):**
- ✅ VSCode extension auto-logs conversations without user intervention
- ✅ Works across multiple AI tools
- ✅ User can enable/disable auto-logging easily
- ✅ Buffers data to prevent loss on crash

---

## Related Documents

- [Root Cause Analysis](../postmortems/logger-claims-vs-reality-rca.md)
- [ROADMAP.md Phase 1](../../ROADMAP.md)
- [ConversationLogger API](../api/conversation-logger.md)

---

## Notes

- This issue was discovered during testing on 2025-10-07
- User feedback: "seems like a big miss that we had a feature that we said was working, when it wasn't"
- Lesson: Don't claim features work until end-to-end tested with real user data
