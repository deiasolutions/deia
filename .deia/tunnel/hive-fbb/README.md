# Hive-FBB Communication Tunnel

**Hive:** HIVE-FBB (Family Bond Bot)
**Parent Hive:** HIVE-DEIA-CORE
**Created:** 2025-10-19

## Purpose

This directory is the communication tunnel between the Family Bond Bot hive and the DEIA Core hive.

## How It Works

1. **FBB → DEIA Core**: Messages from FBB agents/sessions go here
2. **DEIA Core → FBB**: Responses and coordination messages

## Message Format

Messages use JSONL format with this structure:

```json
{
  "timestamp": "2025-10-19T12:00:00.000000",
  "from_hive": "HIVE-FBB",
  "to_hive": "HIVE-DEIA-CORE",
  "message_type": "pattern_submission|request|coordination|status",
  "subject": "Brief subject line",
  "content": "Message content",
  "metadata": {
    "agent_id": "CLAUDE-CODE-XXX",
    "session_id": "session-id",
    "priority": "low|medium|high|urgent"
  }
}
```

## Use Cases

### Pattern Submission
FBB extracts a pattern → submits to DEIA BOK via this tunnel

### Request for Assistance
FBB needs DEIA core functionality → requests via tunnel

### Coordination
Multi-hive coordination for shared resources

### Status Updates
FBB reports status to parent hive

## File Naming Convention

- Incoming (FBB → DEIA): `YYYY-MM-DD-HHMM-fbb-to-core-{type}-{subject}.jsonl`
- Outgoing (DEIA → FBB): `YYYY-MM-DD-HHMM-core-to-fbb-{type}-{subject}.jsonl`

## Examples

See `.deia/tunnel/claude-to-claude/` in parent hive for agent-to-agent message examples.

---

**Status:** Active
**Monitoring:** Manual (for now)
**Next Review:** After first pattern submission from FBB
