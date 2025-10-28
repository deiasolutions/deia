# TASK-002-008: Design Hybrid Mode Coordination Logic

**Task ID:** TASK-002-008
**Bot ID:** BOT-002
**Priority:** P2
**Created:** 2025-10-28T14:15:00Z
**Timeout:** 120 seconds

---

## INSTRUCTION

Design the logic for Mode 3 (Hybrid) bots that handle both file queue AND WebSocket input simultaneously.

Create: `.deia/hive/responses/deiasolutions/HYBRID-MODE-DESIGN.md`

Include:

1. **Priority Handling**
   - If both file task AND WebSocket prompt arrive at same time, which executes first?
   - How to queue/defer the other?
   - Timeout for pending tasks?

2. **Response Routing**
   - File-based task response → write to `.deia/hive/responses/`
   - WebSocket prompt response → stream to chat AND write file?
   - Both versions in timeline?

3. **State Management**
   - What state must bot track?
   - How to handle interrupts mid-task?
   - Recovery if WebSocket disconnects?

4. **Code Changes Needed**
   - Modifications to `run_once()` method?
   - WebSocket handler additions?
   - Task polling loop changes?

Make recommendations on implementation approach.

---
