# SPRINT 2 TASK: Chat Features Expansion (BOT-003)
**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-003 (CLAUDE-CODE-003)
**Date:** 2025-10-25 23:00 CDT (Post-Fire Drill)
**Priority:** P1 - HIGH
**Mode:** Sprint Work - Sequential then parallel
**Duration:** 6-8 hours

---

## Mission: Expand Chat Controller with Advanced Features

Fire drill got chat working. Now add features users actually need: history, context, smart routing, persistence.

---

## Task 1: Chat History & Persistence (2 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**Current Issues:**
- Messages lost on page refresh
- No conversation history
- Can't resume sessions

**Your Work:**
1. Store all messages in `.deia/hive/responses/chat-history-{date}.jsonl`
2. On page load, load last 100 messages from history
3. Add "Load More History" button to scroll back further
4. Implement session persistence: resume conversation on reload
5. Add timestamp to each message

**Success Criteria:**
- Messages survive page refresh
- History file grows correctly
- Can view past conversations
- Performance: < 100ms to load history

**Files:**
- Modify: `llama-chatbot/app.py` (add persistence endpoints)
- Enhance: JavaScript to load/display history

---

## Task 2: Multi-Session Support (1.5 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**What We Need:**
Support multiple independent chat sessions:

**Your Work:**
1. Generate session ID on chat open (UUID)
2. Allow user to "Start New Conversation"
3. List recent sessions in sidebar
4. Switch between sessions (preserves history)
5. Archive old sessions (move to `.deia/sessions/archive/`)

**Success Criteria:**
- Can have 5+ independent sessions
- Switch between sessions instantly
- Each session isolated history
- Sessions listed with timestamp

**Files:**
- Modify: `llama-chatbot/app.py` (session management)
- Enhance: HTML for session switcher

---

## Task 3: Context-Aware Chat (2 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**Current Issue:**
- Chat doesn't know about DEIA project context
- Responses not informed by BOK or governance

**Your Work:**
1. Auto-detect DEIA project on startup
2. Load project README, governance, key BOK patterns
3. Include context in bot prompts
4. User can see "Context Loaded: {files}" in UI
5. Option to add custom context ("Add File to Context")

**Success Criteria:**
- Context auto-loaded on startup
- Bot responses reflect project knowledge
- User can see what context is loaded
- Can add/remove context dynamically

**Files:**
- Create: `src/deia/services/chat_context_loader.py`
- Modify: `llama-chatbot/app.py` (pass context to bots)

---

## Task 4: Smart Bot Routing (1.5 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**What We Need:**
Automatically route commands to most appropriate bot:

**Your Work:**
1. Analyze user message to determine bot type needed
2. Categories: dev (code), qa (testing), docs (writing), etc.
3. Route to bot matching category
4. User can override selection (@bot-001 override)
5. Show selected bot before sending

**Success Criteria:**
- Correctly routes 80%+ of messages
- Override mechanism works
- User sees which bot selected
- Category inference visible in UI

**Files:**
- Create: `src/deia/services/message_router.py`
- Modify: `llama-chatbot/app.py` (integrate router)

---

## Task 5: Message Filtering & Safety (1 hour)
**Status:** PENDING - START AFTER FIRE DRILL

**Current Issues:**
- No validation of messages before sending
- Could send malicious commands
- No rate limiting

**Your Work:**
1. Validate commands before sending to bot
2. Block dangerous patterns (rm -rf, etc.)
3. Add rate limiting (max 10 messages/min per user)
4. Log all messages (audit trail)
5. Warn user of dangerous patterns

**Success Criteria:**
- Dangerous commands blocked
- Rate limiting enforced
- Audit trail available
- User gets clear error messages

**Files:**
- Create: `src/deia/services/message_validator.py`
- Modify: `llama-chatbot/app.py` (validate before send)

---

## Task 6: Chat Export & Sharing (1.5 hours)
**Status:** PENDING - START AFTER FIRE DRILL

**What We Need:**
Allow users to save/share conversations:

**Your Work:**
1. Add "Export Conversation" button
2. Export formats: Markdown, JSON, PDF
3. Save to `.deia/exports/{session-id}.{format}`
4. Generate shareable link (localhost only, secure)
5. Include context and metadata in export

**Success Criteria:**
- All 3 export formats work
- Export files well-formatted
- Metadata included
- Can reload exported conversation

**Files:**
- Create: `src/deia/services/chat_exporter.py`
- Modify: `llama-chatbot/app.py` (export endpoints)

---

## Deliverables (Report When Complete)

Create file: `.deia/hive/responses/deiasolutions/bot-003-sprint-2-status.md`

Include:
- [ ] Chat history persistence working
- [ ] Multi-session support implemented
- [ ] Context-aware chat working
- [ ] Smart bot routing functional
- [ ] Message filtering & safety active
- [ ] Chat export/sharing working
- [ ] All 6 tasks tested
- [ ] Evidence: screenshots of new features
- [ ] Any issues or improvements discovered

**Estimated Total Time:** 6-8 hours (can overlap with BOT-001 work)

---

## Success Criteria for Sprint 2

**Usability:**
- Users can save conversations
- Easy to switch between sessions
- Context is visible and helpful
- Messages validated before sending

**Reliability:**
- No data loss
- History survives restarts
- Rate limiting works
- Audit trail complete

**Safety:**
- Dangerous commands blocked
- Rate limiting prevents abuse
- All messages logged
- User can review before sending

---

## If You Get Stuck

Post to: `.deia/hive/responses/deiasolutions/bot-003-sprint-2-questions.md`

Q33N responds within 30 minutes.

---

**Q33N out. BOT-003: Sprint 2 = Expand chat features. Make it user-friendly and safe.**
