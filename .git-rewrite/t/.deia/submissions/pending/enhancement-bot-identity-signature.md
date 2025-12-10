---
type: improvement
project: deiasolutions
created: 2025-10-13
status: pending
sanitized: true
category: bot-coordination
---

# Enhancement: Bot Identity Signature in All Outputs

## Summary

Add requirement that every bot ALWAYS reports their bot ID as the last line in their output, using a standardized identity statement format.

## Problem Statement

Currently, bots may complete tasks without clearly identifying themselves in their output. This makes it difficult to:
- Track which bot performed which action when reviewing logs
- Debug issues in multi-bot coordination
- Verify bot identity from output alone
- Maintain clear audit trail in session transcripts

## Proposed Solution

**Mandate that all bots end every response with an identity signature:**

```
---
[BOT-ID | Role | Instance: instance-id]
```

**Example:**
```
---
[BOT-00002 | Drone-Dev | Instance: 6acce126]
```

### Implementation Details

1. **Update hive coordination rules** (`.deia/hive-coordination-rules.md`)
   - Add section: "Bot Identity Signature Protocol"
   - Require signature as last line of all bot outputs
   - Define exact format

2. **Update bot instruction templates**
   - Add reminder at top: "Always end responses with identity signature"
   - Include example signature in template

3. **Update launch scripts**
   - Add signature requirement to LAUNCH-BOT-*.md files
   - Include in initial bot briefing

4. **Enforcement**
   - Bots should self-check before responding
   - Queen can flag violations during review
   - Include in bot quality metrics

### Format Specification

```
---
[BOT-{ID} | {Role} | Instance: {instance-id}]
```

**Required fields:**
- BOT-{ID}: Bot identifier (e.g., BOT-00002)
- {Role}: Bot role (e.g., Drone-Dev, Queen, Worker)
- Instance: {instance-id}: Current instance ID

**Optional fields (future):**
- Status: Current status (ACTIVE, STANDBY, etc.)
- Task: Current task ID

**Placement:**
- Must be the LAST line of bot output
- Preceded by horizontal rule `---`
- No content after signature

## Benefits

1. **Traceability**
   - Every bot action clearly attributed
   - Easy to grep logs for specific bot output
   - Clear audit trail for compliance

2. **Debugging**
   - Instantly identify which bot produced output
   - Track bot instance across session
   - Verify correct bot responded to assignment

3. **Multi-Bot Coordination**
   - Clear handoff identification
   - Prevent confusion when multiple bots active
   - Support parallel bot operations

4. **Quality Assurance**
   - Easy to verify bot followed protocols
   - Clear accountability for actions
   - Support automated output validation

5. **User Experience**
   - User always knows which bot is responding
   - Reduces cognitive load in multi-bot scenarios
   - Professional, consistent output format

## Example Usage

### Before (Unclear Attribution):
```
Task completed successfully! Report written to .deia/reports/link-fix-20251013-1312.md

Standing by for next assignment.
```

### After (Clear Attribution):
```
Task completed successfully! Report written to .deia/reports/link-fix-20251013-1312.md

Standing by for next assignment.

---
[BOT-00002 | Drone-Dev | Instance: 6acce126]
```

## Implementation Locations

1. `.deia/hive-coordination-rules.md`
   - Add "Bot Identity Signature" section after "Bot Identity Protocol"

2. `.deia/instructions/BOT-*-instructions.md` (template)
   - Add reminder at top
   - Include example in "Getting Started"

3. `.deia/instructions/LAUNCH-BOT-*.md`
   - Add signature requirement to launch checklist

4. Bot memory/preferences
   - Add to standard bot briefing
   - Include in bot startup checklist

## Related Enhancements

- Could integrate with "identify yourself" protocol (process-001)
- Could add to heartbeat messages for consistency
- Could extend to include task status, elapsed time, etc.

## Validation

**Success criteria:**
- All bot outputs end with identity signature
- Signature format is consistent across all bots
- Easy to parse programmatically (regex: `\[BOT-\d+ \| .+ \| Instance: [a-f0-9]+\]`)
- No bot responses without signature

**Testing:**
- Review 10 bot responses before/after implementation
- Verify signature present in all cases
- Test signature parsability with grep/regex

## Tags

bot-coordination, output-format, identity, audit-trail, multi-bot, quality-assurance

## Category

Hive Coordination / Bot Communication Protocol

## Proposed Location

- Primary: `.deia/hive-coordination-rules.md` (new section)
- Reference: `.deia/instructions/TEMPLATE-BOT-instructions.md`
- Documentation: `bok/patterns/collaboration/bot-identity-signature.md`

## Priority

**Medium** - Improves clarity and debugging but not blocking current operations

## Effort Estimate

- Documentation updates: 30 minutes
- Template updates: 15 minutes
- Bot re-briefing: 5 minutes per bot
- Testing/validation: 30 minutes

**Total:** ~2 hours

## Notes

This enhancement request was created by BOT-00002 based on user feedback during session on 2025-10-13. User specifically requested: "save an arequest for enhancement tht a bot ALWAYS reports their bot id as the last line in their output, with an ident statement"

---

**Submitted by:** BOT-00002 (Instance ID: 6acce126)
**Session:** 2025-10-13
**Status:** Awaiting user review
