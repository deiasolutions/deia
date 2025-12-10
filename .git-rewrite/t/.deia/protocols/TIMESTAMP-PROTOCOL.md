# Timestamp Protocol

**Version:** 1.0
**Effective:** 2025-10-18
**Authority:** User directive
**Created By:** CLAUDE-CODE-002
**Reason:** Fix process failure (UTC timestamp error)

---

## Purpose

Define the standard timestamp format for all DEIA coordination messages, activity logs, and documentation to ensure timeline clarity and prevent timezone confusion.

---

## Standard Format

**All coordination messages, logs, and documentation MUST use user local time.**

**User Timezone:** CDT (Central Daylight Time, UTC-5)

### Accepted Formats

**1. Human-Readable (Preferred for documentation):**
```
YYYY-MM-DD HHMM CDT
```
**Example:** `2025-10-18 1007 CDT`

**2. ISO-8601 with Timezone (Preferred for logs):**
```
YYYY-MM-DDTHH:MM:SS-05:00
```
**Example:** `2025-10-18T10:07:00-05:00`

**3. File Naming Convention:**
```
YYYY-MM-DD-HHMM-FROM-TO-TYPE-description.md
```
**Example:** `2025-10-18-1007-AGENT002-AGENT001-SYNC-fix-complete.md`

---

## Examples

### ✅ CORRECT

- `2025-10-18 1007 CDT` (human-readable)
- `2025-10-18T10:07:00-05:00` (ISO-8601)
- `2025-10-18-1007-AGENT001-AGENT002-TASK-description.md` (filename)
- `"ts":"2025-10-18T10:07:00-05:00"` (JSON log entry)

### ❌ WRONG

- `2025-10-18T15:07:00Z` (UTC instead of CDT)
- `2025-10-18-1507-...` (UTC hour in filename)
- `2025-10-18 15:07 UTC` (wrong timezone)
- `2025-10-18 10:07` (missing timezone indicator)

---

## Getting Current Time

Before creating any timestamped file or log entry, agents MUST verify current local time:

### Command

```bash
date "+%Y-%m-%d %H%M %Z"
```

### Expected Output

```
2025-10-18 1007 CDT
```

### Verification

- Hour should be between 00-23 (24-hour format)
- Timezone should show "CDT" (or "CST" during winter)
- Time should match user's actual clock time

---

## Application Areas

### 1. Coordination Messages

**Location:** `.deia/tunnel/claude-to-claude/`

**Filename Format:**
```
YYYY-MM-DD-HHMM-FROM-TO-TYPE-description.md
```

**Internal Timestamp:**
```markdown
**Date:** YYYY-MM-DD HHMM CDT
```

**Example:**
```
Filename: 2025-10-18-1007-AGENT002-AGENT001-SYNC-fix-complete.md
Content:  **Date:** 2025-10-18 1007 CDT
```

---

### 2. Activity Logs

**Location:** `.deia/bot-logs/AGENT-ID-activity.jsonl`

**Format:**
```json
{
  "ts": "YYYY-MM-DDTHH:MM:SS-05:00",
  "agent_id": "AGENT-ID",
  "event": "event_name",
  ...
}
```

**Example:**
```json
{
  "ts": "2025-10-18T10:07:00-05:00",
  "agent_id": "CLAUDE-CODE-002",
  "event": "task_completed"
}
```

---

### 3. Documentation Files

**Locations:** `.deia/observations/`, `.deia/protocols/`, `docs/`, etc.

**Format:**
```markdown
**Date:** YYYY-MM-DD HHMM CDT
```

or

```markdown
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD HHMM CDT
```

---

### 4. Session Logs

**Location:** `.deia/sessions/`

**Filename Format:**
```
YYYYMMDD-HHMMSS[microseconds]-conversation.md
```

**Internal Format (from ConversationLogger):**
```
**Date:** YYYY-MM-DDTHH:MM:SS.microseconds (CDT implied)
```

**Note:** Session logs use local time by default (Python's `datetime.now()` uses system timezone).

---

## Verification Checklist

Before creating a timestamped file, verify:

- [ ] Current time checked with `date` command
- [ ] Hour is between 00-23 (24-hour CDT time)
- [ ] Timezone indicator included (CDT or -05:00)
- [ ] Time matches user's actual clock
- [ ] If unsure, ask user or double-check system time

---

## Exceptions

**NONE.**

All timestamps MUST use user local time (CDT).

**Rationale:**
- User is in CDT timezone
- All coordination is user-facing
- Consistency prevents confusion
- Local time is most intuitive for user

---

## Timezone Conversion

If you receive a UTC timestamp and need to convert:

**Formula:** CDT = UTC - 5 hours

**Examples:**
- 16:30 UTC → 11:30 CDT
- 19:15 UTC → 14:15 CDT
- 00:30 UTC → 19:30 CDT (previous day)

**Tool:**
```bash
# Convert UTC to CDT
date -d "2025-10-18 16:30 UTC" "+%Y-%m-%d %H%M %Z"
```

---

## Process Failure Response

If an agent creates a file with wrong timezone:

1. **Detection:** Notice timestamp doesn't match expected local time
2. **Alert:** Create ALERT message to ALL_AGENTS
3. **Assignment:** Coordinator assigns fix task to appropriate agent
4. **Fix:** Rename files, update timestamps, document in observations/
5. **Prevention:** Review this protocol, verify understanding

**Documented Example:** See `.deia/observations/2025-10-18-timestamp-utc-error-fix-log.md`

---

## Agent Training

All agents MUST:

1. **Read this protocol** before creating timestamped files
2. **Verify current time** with `date` command before file creation
3. **Use CDT format** in all user-facing documents
4. **Check their work** - does timestamp match actual time?
5. **Ask if unsure** - timezone mistakes are preventable

---

## Related Protocols

- Integration Protocol (`.deia/protocols/INTEGRATION-PROTOCOL.md`)
- Coordination Message Protocol (`.deia/governance/TASK-ASSIGNMENT-AUTHORITY.md`)
- Activity Logging Protocol (implied in agent workflows)

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-10-18 | Initial protocol created after UTC error fix | CLAUDE-CODE-002 |

---

## Authority

This protocol is established by user directive following the 2025-10-18 UTC timestamp error incident.

All agents are required to follow this protocol for consistency and clarity in project coordination.

---

**Questions about this protocol?**
- Check the fix log: `.deia/observations/2025-10-18-timestamp-utc-error-fix-log.md`
- Ask coordinator (AGENT-001) for clarification
- Refer to examples in this document

---

**Effective immediately:** 2025-10-18 1010 CDT

**Status:** ✅ ACTIVE

---

*DEIA Project - Clear communication through consistent timestamps*
