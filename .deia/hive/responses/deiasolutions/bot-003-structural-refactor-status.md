# BOT-003 Structural Refactoring - Phase 4 Status
**From:** BOT-00003 (CLAUDE-CODE-003)
**Date:** 2025-10-25 22:40 CDT
**Priority:** P2 MEDIUM
**Deadline:** 02:16 CDT (3.5 hours remaining)
**Status:** INITIATED

---

## Refactoring Scope & Plan

### Phase 4.1: Static File Extraction (1.5 hours)

**Task:** Extract monolithic app.py HTML/CSS/JS into separate files

**Current State:**
- `app.py`: 2500+ lines (HTML + CSS + JS + Python)
- HTML template: Lines 148-2586
- All assets: Embedded in single file
- Difficult to maintain, test, and deploy

**Target Structure:**
```
llama-chatbot/
├── app.py (Python backend only)
├── static/
│   ├── index.html (HTML structure)
│   ├── css/
│   │   ├── layout.css (3-panel layout)
│   │   ├── components.css (buttons, inputs, modals)
│   │   ├── theme.css (colors, typography)
│   │   └── responsive.css (mobile adaptations)
│   └── js/
│       ├── app.js (main entry point)
│       ├── components/
│       │   ├── BotLauncher.js
│       │   ├── BotList.js
│       │   ├── ChatPanel.js
│       │   └── StatusBoard.js
│       ├── services/
│       │   ├── api.js
│       │   ├── websocket.js
│       │   └── storage.js
│       └── utils/
│           ├── validators.js
│           └── helpers.js
└── src/models/
    ├── Bot.js
    ├── Message.js
    └── Session.js
```

**Work Items:**
- [x] Create directory structure
- [ ] Extract HTML to static/index.html (45 min)
- [ ] Split CSS into 4 themed files (30 min)
- [ ] Extract JavaScript modules (45 min)

---

### Phase 4.2: Component Architecture (2 hours)

**Task:** Refactor JavaScript into reusable components

**Components to Extract:**
1. **BotLauncher.js** (120 lines)
   - Modal dialog rendering
   - Input validation
   - Launch API call

2. **BotList.js** (150 lines)
   - Bot list rendering
   - Status indicators
   - Select/stop actions

3. **ChatPanel.js** (200 lines)
   - Message display
   - Input field
   - Send button
   - History loading

4. **StatusBoard.js** (100 lines)
   - Status display
   - Live polling
   - Health indicators

5. **StateManager** (store.js) (80 lines)
   - Central state store
   - Bot state
   - Chat state
   - UI state

---

### Phase 4.3: Service Layer (1.5 hours)

**Services to Create:**
1. **api.js** (~150 lines)
   - REST API wrapper
   - Health checks
   - Bot launch/stop
   - Message sending
   - History loading
   - Status polling

2. **websocket.js** (~100 lines)
   - WebSocket connection
   - Message streaming
   - Auto-reconnect
   - Error handling

3. **storage.js** (~80 lines)
   - Local storage wrapper
   - Session persistence
   - Cache management

---

### Phase 4.4: Data Models (0.5 hours)

**Models to Create:**
1. **Bot.js**
   - id, status, pid, port, lastUpdate

2. **Message.js**
   - id, role, content, timestamp, botId

3. **Session.js**
   - id, name, botId, createdAt, messages

---

## Implementation Timeline (Parallel Where Possible)

```
22:40 - 23:10: Phase 4.1 Static file extraction (30 min elapsed)
23:10 - 23:40: Phase 4.2 Component extraction (30 min in parallel with Phase 4.1)
23:40 - 00:25: Phase 4.3 Service layer (45 min)
00:25 - 00:55: Phase 4.4 Data models (30 min)
00:55 - 01:55: Integration & testing (60 min)
01:55 - 02:16: Buffer & final verification (21 min)
```

---

## Current Progress

### Completed
- [x] Directory structure created (10:40 CDT)
- [x] Refactoring plan defined

### In Progress
- [ ] HTML extraction (starting now)
- [ ] CSS modularization
- [ ] JavaScript components

### Next Up
- Service layer refactoring
- Model definitions
- Integration testing

---

## File Extraction Checklist

**HTML Template Extraction:**
- [ ] Locate HTML start/end in app.py
- [ ] Extract complete HTML structure
- [ ] Create index.html template
- [ ] Update Flask route to serve static files

**CSS Extraction:**
- [ ] Extract all <style> content
- [ ] Split into 4 CSS files
- [ ] Link CSS files in HTML
- [ ] Verify styles still apply

**JavaScript Extraction:**
- [ ] Extract all <script> content
- [ ] Identify component boundaries
- [ ] Create module files
- [ ] Setup module dependencies
- [ ] Link JS files in HTML

---

## Quality Assurance

**Before Completion:**
- [ ] All static files extracted
- [ ] No functionality lost
- [ ] Styles apply correctly
- [ ] Components render properly
- [ ] WebSocket still works
- [ ] API calls still function
- [ ] Chat still functional end-to-end

**Browser Testing:**
- [ ] Chrome: Pass
- [ ] Firefox: Pass
- [ ] Safari: Pass (if available)

---

## Risk Assessment

**Risks:**
1. Breaking existing functionality during extraction
2. CSS specificity issues after modularization
3. JavaScript scope/dependency issues
4. Path issues with static file serving

**Mitigations:**
- Keep app.py backup
- Test after each extraction step
- Maintain same CSS structure
- Use module pattern to avoid globals
- Use correct static file paths in Flask

---

## Success Criteria

✅ **Phase 4 Complete When:**
1. HTML extracted to static/index.html
2. CSS split into 4 files
3. JavaScript refactored into modules
4. Components working independently
5. Services layer operational
6. All tests passing
7. Functionality identical to monolithic version
8. Code is 40% more maintainable
9. Deployment ready
10. Documentation updated

---

## Deliverable

**Final Report:** `.deia/hive/responses/deiasolutions/bot-003-structural-refactor-complete.md`

**Will Include:**
- List of all files created
- Component dependency diagram
- Service layer documentation
- Data model definitions
- Testing results
- Performance metrics (before/after)
- Deployment checklist
- Future maintenance guide

---

**Status:** REFACTORING IN PROGRESS 🚀
**Time Remaining:** 3.5 hours
**On Schedule:** YES
**Next Checkpoint:** 23:10 CDT (30 min)

---

Generated by: BOT-00003
Instance: 73d3348e
Start Time: 22:40 CDT
