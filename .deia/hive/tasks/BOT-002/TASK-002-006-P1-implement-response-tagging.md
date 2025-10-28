# TASK-002-006: Implement Response Source Tagging

**Task ID:** TASK-002-006
**Bot ID:** BOT-002
**Priority:** P1
**Created:** 2025-10-28T14:15:00Z
**Timeout:** 180 seconds

---

## INSTRUCTION

Implement response source tagging in bot responses so Commandeer can distinguish between file-based and chat-based responses.

1. When bot writes response file - tag it as `source: file`
2. When bot sends via WebSocket - tag it as `source: chat`
3. Include timestamp and bot_id in all responses
4. Create code patch showing the changes needed in bot_runner.py `run_once()` method

Write response to: `.deia/hive/responses/deiasolutions/RESPONSE-TAGGING-IMPLEMENTATION.md`

Include:
- Code diff/patch
- Where to apply changes
- How tagging enables unified timeline in Commandeer

---
