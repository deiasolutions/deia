# IMMEDIATE ASSIGNMENT: BOT-001 - Feature 3: Bot Communication

**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001 (Bot Infrastructure)
**Date:** 2025-10-25 18:20 CDT
**Priority:** P0 - START NOW
**Status:** QUEUE READY

---

## You've Got Momentum

Features 1 & 2 done in 3 hours (both under estimate).

Feature 3 is simpler. Build it fast.

---

## Feature 3: Bot Communication Layer (1.5 hours)

**What it is:**
Bots can message each other. Coordinate on complex, multi-step tasks.

**What to build:**
- Message queue: `POST /api/bot/{id}/message` - send message to bot
- Message inbox: `GET /api/bot/{id}/messages` - retrieve messages
- Pub/Sub system: Bots subscribe to topics (`task_complete`, `error_alert`, `scaling_event`, etc.)
- Message format: JSON with `sender_id`, `recipient_id`, `message_type`, `content`, `timestamp`
- Logging: All bot-to-bot messages logged to `.deia/bot-logs/bot-messages.jsonl`

**Implementation:**
- `src/deia/services/bot_messenger.py` (NEW) - BotMessenger class, message queue, pub/sub
- Integrate into `bot_service.py` - expose messaging endpoints
- Thread-safe message storage (in-memory with persistence option)

**Success criteria:**
- [ ] Bot-to-bot messaging working
- [ ] Pub/Sub subscriptions work
- [ ] Messages persist (queue survives bot restart)
- [ ] Logging complete
- [ ] No message loss
- [ ] 70%+ test coverage

**Time estimate:** 1.5 hours

---

## Example Usage

**Bot A sends message to Bot B:**
```bash
POST /api/bot/BOT-B/message
{
  "sender_id": "BOT-A",
  "message_type": "task_complete",
  "content": {"task_id": "TASK-123", "result": "success"}
}
```

**Bot B retrieves messages:**
```bash
GET /api/bot/BOT-B/messages?message_type=task_complete
```

**Bot subscribes to topic:**
```bash
POST /api/bot/BOT-B/subscribe
{
  "topic": "task_complete",
  "handler": "on_task_complete"
}
```

---

## Integration with Previous Features

- Orchestrator uses messaging to notify bots of task assignments
- Auto-scaler sends `scaling_event` messages when bots added/removed
- Scheduler can ask bots about their current load
- Bots respond with status messages

---

## Queue Status

**Completed:** Features 1-2
**Next in queue:** Feature 4 (Adaptive Scheduling) - ready when done
**After that:** Feature 5 (Dashboard) - queued and ready

No downtime between features.

---

## GO

You know the pattern. Clear spec, success criteria, integration points.

Build it.

**001: Start Feature 3 immediately.**

---

**Q33N out. Keep the velocity.**
