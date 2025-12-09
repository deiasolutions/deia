# QUEUED: BOT-003 - Feature 4: Conversation Templates

**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-003 (Chat Controller)
**Date:** 2025-10-25 18:20 CDT
**Priority:** P0 - NEXT IN QUEUE
**Status:** QUEUED - START AFTER FEATURE 3

---

## Feature 4: Conversation Templates (1.5 hours)

**What it is:**
Save conversation patterns, reuse them for common workflows.

**What to build:**
- Template creation: `POST /api/templates` - save current conversation as template
- Template metadata: name, description, tags, bot_type
- Template retrieval: `GET /api/templates` - list all templates
- Template usage: `POST /api/templates/{id}/use` - start new session from template
- Storage: `.deia/templates.jsonl`
- UI: Show template library, one-click load

**Example:**
- Save conversation: "User asks question → BOT-001 investigates → BOT-003 summarizes"
- Reuse template: Click "Load code review template" → same flow starts

**Success criteria:**
- [ ] Templates save correctly
- [ ] Can list and search templates
- [ ] Load template starts new session
- [ ] Previous conversation history preserved
- [ ] 70%+ test coverage

**Time estimate:** 1.5 hours

---

**Q33N out. Feature 4 queued and ready.**
