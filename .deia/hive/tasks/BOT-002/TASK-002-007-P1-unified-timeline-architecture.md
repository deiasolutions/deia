# TASK-002-007: Design Unified Timeline Architecture

**Task ID:** TASK-002-007
**Bot ID:** BOT-002
**Priority:** P1
**Created:** 2025-10-28T14:15:00Z
**Timeout:** 120 seconds

---

## INSTRUCTION

Design the architecture for a unified conversation timeline in Commandeer that interleaves file-based and chat-based responses.

Create: `.deia/hive/responses/deiasolutions/UNIFIED-TIMELINE-DESIGN.md`

Include:

1. **Data Model**
   - What does each timeline entry contain?
   - How to distinguish file vs chat responses?
   - Timestamp ordering?

2. **Retrieval**
   - How does Commandeer fetch timeline events?
   - API endpoint design?
   - WebSocket streaming vs polling?

3. **Display Order**
   - Should file responses appear in timeline?
   - How to handle async vs real-time?
   - Example timeline with mixed sources

4. **Implementation Steps**
   - What code changes needed?
   - Where to hook in (bot_runner, API, Commandeer)?

Make it actionable for Commandeer UI implementation.

---
