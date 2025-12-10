# chromium-deia User Stories - Quick Reference

**For offline review and sprint planning**

---

## Epic 1: Automatic Conversation Capture

### Story 1.1: Detect AI Coding Tools
**Priority:** P0 (MVP)

**As a** developer using browser-based AI tools
**I want** the extension to automatically detect when I'm on Claude.ai, ChatGPT, or other coding assistants
**So that** I don't have to manually configure which sites to monitor

**Acceptance Criteria:**
- [ ] Extension detects claude.ai (Projects, standard chat)
- [ ] Extension detects chat.openai.com (ChatGPT, Code Interpreter)
- [ ] Extension detects gemini.google.com
- [ ] Extension detects copilot.microsoft.com
- [ ] Visual indicator appears when AI tool detected
- [ ] Works on all Chromium browsers (Chrome, Edge, Brave)

---

### Story 1.2: Real-time Conversation Capture
**Priority:** P0 (MVP)

**As a** developer working with Claude or ChatGPT
**I want** my coding conversations automatically captured in real-time
**So that** I can focus on coding without thinking about logging

**Acceptance Criteria:**
- [ ] User prompts captured with timestamps
- [ ] AI responses captured including code blocks
- [ ] Conversation thread structure preserved
- [ ] Multi-turn conversations tracked correctly
- [ ] Code syntax and formatting preserved
- [ ] Works even if page reloads or network issues
- [ ] Minimal performance impact (<50ms overhead)

---

### Story 1.3: Handle Claude Projects Conversations
**Priority:** P2 (Enhanced Experience)

**As a** developer using Claude Projects (with attached files/docs)
**I want** conversations in Projects captured with context about attached files
**So that** patterns include the project context

**Acceptance Criteria:**
- [ ] Detect when in Claude Projects vs standard chat
- [ ] Capture project name and description
- [ ] Note which files/docs are attached (names, not content for privacy)
- [ ] Distinguish between project chats and general chats
- [ ] Track conversation continuity across sessions

---

### Story 1.4: Code Block Recognition and Extraction
**Priority:** P1 (Early Release)

**As a** developer getting code from AI assistants
**I want** code blocks automatically identified and tagged with language
**So that** patterns can be language-specific and searchable

**Acceptance Criteria:**
- [ ] Detect code blocks in AI responses
- [ ] Extract language tags (Python, JavaScript, TypeScript, etc.)
- [ ] Preserve syntax highlighting metadata
- [ ] Handle multi-file code suggestions
- [ ] Capture diff/patch suggestions separately
- [ ] Track "copy code" button usage (indicates useful code)

---

## Epic 2: Manual Logging Controls

### Story 2.1: Quick Manual Log
**Priority:** P0 (MVP)

**As a** developer who just had a breakthrough conversation
**I want** to click the extension icon and save that session
**So that** I can quickly log important conversations without interrupting flow

**Acceptance Criteria:**
- [ ] Extension icon badge shows "loggable" status
- [ ] Single click opens popup with "Log Now" button
- [ ] Shows preview of current conversation (last 3 exchanges)
- [ ] Allows adding quick tags/notes before saving
- [ ] Confirms when log saved with file location
- [ ] Works even if auto-logging is disabled

---

### Story 2.2: Partial Conversation Selection
**Priority:** P2 (Enhanced Experience)

**As a** developer in a long conversation
**I want** to select specific parts of the conversation to log
**So that** I only capture the relevant debugging solution, not the entire 50-message thread

**Acceptance Criteria:**
- [ ] Popup shows conversation timeline
- [ ] User can select start/end messages
- [ ] Selected portion highlighted in preview
- [ ] Can add context note explaining what's useful
- [ ] Option to log full conversation or selection
- [ ] Selection persists if popup closed and reopened

---

### Story 2.3: Pause/Resume Auto-logging
**Priority:** P0 (MVP)

**As a** developer discussing sensitive client work
**I want** to temporarily pause auto-logging
**So that** I don't accidentally log proprietary information

**Acceptance Criteria:**
- [ ] Pause button in extension popup
- [ ] Paused state shown with yellow badge
- [ ] Resume button clearly visible
- [ ] Paused state persists across browser restarts
- [ ] Warning when closing browser while paused
- [ ] Optional auto-resume after N minutes/hours

---

## Epic 3: DEIA Integration

### Story 3.1: Save to .deia/sessions/
**Priority:** P1 (Early Release)

**As a** developer with DEIA installed locally
**I want** conversations saved to my project's `.deia/sessions/` folder
**So that** they integrate with my existing DEIA workflow

**Acceptance Criteria:**
- [ ] Extension detects if DEIA is installed (check for .deia in common paths)
- [ ] Prompts user to configure DEIA directory on first use
- [ ] Saves logs in DEIA session format (markdown with YAML frontmatter)
- [ ] File naming: YYYYMMDD-HHMMSS-claude-browser.md
- [ ] Compatible with DEIA CLI commands (deia list, deia extract, etc.)
- [ ] Falls back to browser localStorage if DEIA not available

---

### Story 3.2: Link Sessions to Active Project
**Priority:** P2 (Enhanced Experience)

**As a** developer working on multiple projects
**I want** browser conversations tagged with current project
**So that** logs are organized by what I'm working on

**Acceptance Criteria:**
- [ ] Settings page lists recent projects (from .deia/config.json)
- [ ] User can set "active project" from popup
- [ ] Extension remembers project per browser tab
- [ ] Conversations automatically tagged with project name
- [ ] Can change project mid-conversation (splits log)
- [ ] "No project" option for general exploration

---

### Story 3.3: Pattern Extraction Suggestions
**Priority:** P3 (Power Features)

**As a** developer who just logged a useful conversation
**I want** DEIA to suggest if this might be a shareable pattern
**So that** I can contribute to the Book of Knowledge

**Acceptance Criteria:**
- [ ] After logging, extension analyzes conversation
- [ ] Detects keywords: "always do X", "pattern", "best practice", "avoid", etc.
- [ ] Suggests if conversation might be BOK-worthy
- [ ] Shows button: "Extract Pattern"
- [ ] Opens pattern template pre-filled with conversation context
- [ ] Links to sanitization guide

---

## Epic 4: Privacy & Security

### Story 4.1: Local-only Storage
**Priority:** P0 (MVP)

**As a** privacy-conscious developer
**I want** all data stored locally on my machine
**So that** my conversations never leave my control

**Acceptance Criteria:**
- [ ] No external API calls for logging (only captures from DOM)
- [ ] No telemetry or analytics
- [ ] Clear documentation of what data is stored
- [ ] Data stored in chrome.storage.local or user-specified directory
- [ ] Export feature to move data out
- [ ] Delete feature to remove all data

---

### Story 4.2: Automatic PII Detection
**Priority:** P1 (Early Release)

**As a** developer who might accidentally include API keys or passwords
**I want** the extension to detect and warn about sensitive data
**So that** I don't log secrets

**Acceptance Criteria:**
- [ ] Scans conversation for patterns: API keys, passwords, emails, tokens
- [ ] Warning dialog before saving if sensitive data detected
- [ ] Highlights detected secrets in preview
- [ ] Option to sanitize automatically (replace with [REDACTED])
- [ ] Manual override if false positive
- [ ] Privacy scan runs locally (no API calls)

---

### Story 4.3: Selective Domain Permissions
**Priority:** P4 (Future/Nice-to-Have)

**As a** cautious developer
**I want** to explicitly allow which AI domains the extension monitors
**So that** I control where DEIA is active

**Acceptance Criteria:**
- [ ] Settings page lists all supported AI domains
- [ ] Toggle for each domain (enable/disable)
- [ ] Default: All enabled, but user can restrict
- [ ] Extension requests permissions only for enabled domains
- [ ] Can add custom domain (e.g., company internal AI tool)
- [ ] Disabled domains show no indicator, no capture

---

## Epic 5: Multi-tool Intelligence

### Story 5.1: Cross-tool Session Linking
**Priority:** P3 (Power Features)

**As a** developer using both Claude and ChatGPT for same problem
**I want** conversations linked if they're about the same topic
**So that** I can see full problem-solving context across tools

**Acceptance Criteria:**
- [ ] User can tag conversations with topic/issue ID
- [ ] Extension suggests linking if similar code/terms detected
- [ ] Linked sessions show in session list
- [ ] Can view combined timeline across tools
- [ ] Export linked sessions as single document

---

### Story 5.2: Tool Comparison Insights
**Priority:** P3 (Power Features)

**As a** developer curious about AI tool differences
**I want** to see which tool I use more and for what tasks
**So that** I can optimize my workflow

**Acceptance Criteria:**
- [ ] Dashboard showing usage stats: sessions per tool
- [ ] Breakdown by conversation length (quick vs deep)
- [ ] Identify patterns: "I use Claude for architecture, ChatGPT for debugging"
- [ ] Export stats as CSV
- [ ] Privacy: All analysis local, no server calls

---

### Story 5.3: Universal Conversation Format
**Priority:** P2 (Enhanced Experience)

**As a** DEIA maintainer
**I want** all conversations stored in a tool-agnostic format
**So that** logs work with future AI tools without changes

**Acceptance Criteria:**
- [ ] Logs use standard DEIA conversation format
- [ ] Each message tagged with: role (user/assistant), timestamp, tool
- [ ] Code blocks have language, content, line numbers
- [ ] Metadata includes: tool_name, tool_version, url, project
- [ ] Format validated against DEIA schema
- [ ] Forward-compatible (new fields don't break old parsers)

---

## Epic 6: User Experience

### Story 6.1: Zero-config First Run
**Priority:** P0 (MVP)

**As a** new DEIA user trying the extension
**I want** it to work immediately without complex setup
**So that** I can evaluate it quickly

**Acceptance Criteria:**
- [ ] Install extension → works immediately with defaults
- [ ] Auto-logging enabled by default (with consent prompt)
- [ ] Falls back to browser storage if no DEIA directory configured
- [ ] Welcome popup explains what's happening
- [ ] Clear "Next Steps" guide for DEIA CLI integration
- [ ] No errors if DEIA not installed

---

### Story 6.2: Unobtrusive Indicators
**Priority:** P1 (Early Release)

**As a** developer focused on coding
**I want** visual indicators that are helpful but not distracting
**So that** I stay in flow while knowing DEIA is working

**Acceptance Criteria:**
- [ ] Small, non-modal indicator when AI tool detected
- [ ] Fade out after 3 seconds
- [ ] Badge on extension icon shows status (green=logging, yellow=paused)
- [ ] No popups or interruptions during conversations
- [ ] Keyboard shortcut to quickly log (Alt+Shift+L)
- [ ] Settings to reduce/hide indicators

---

### Story 6.3: Session Review Interface
**Priority:** P1 (Early Release)

**As a** developer reviewing past conversations
**I want** a clean interface to browse logged sessions
**So that** I can find useful solutions from past work

**Acceptance Criteria:**
- [ ] Extension popup has "View Sessions" button
- [ ] Opens full-page interface listing all sessions
- [ ] Sortable by date, tool, project, duration
- [ ] Search by keywords in conversation
- [ ] Preview shows first user prompt + AI response
- [ ] Click session to expand full conversation
- [ ] Export individual session or bulk export

---

## Epic 7: Advanced Features

### Story 7.1: Conversation Branching Detection
**Priority:** P4 (Future/Nice-to-Have)

**As a** developer who often backtracks in conversations
**I want** the extension to track conversation branches
**So that** I can see alternative solutions I explored

**Acceptance Criteria:**
- [ ] Detect when user edits/resends a prompt
- [ ] Track branches as separate conversation paths
- [ ] Visualize branches in session review
- [ ] Can compare branches side-by-side
- [ ] Export includes all branches

---

### Story 7.2: Code Outcome Tracking
**Priority:** P3 (Power Features)

**As a** developer who gets code suggestions
**I want** to mark which suggestions I actually used
**So that** DEIA knows which patterns were valuable

**Acceptance Criteria:**
- [ ] After copying code, prompt to mark "Did this work? (Yes/No/Modified)"
- [ ] Optional follow-up note
- [ ] Tracked outcomes stored with session
- [ ] Analytics: Which types of problems have best AI solutions
- [ ] Contributes to pattern confidence ratings

---

### Story 7.3: Collaboration & Sharing
**Priority:** P4 (Future/Nice-to-Have)

**As a** developer who wants to share a solution with my team
**I want** to generate a shareable link to a sanitized conversation
**So that** teammates can learn from my AI interactions

**Acceptance Criteria:**
- [ ] "Share Session" button in session review
- [ ] Runs sanitization check automatically
- [ ] Generates markdown export
- [ ] Option to create GitHub Gist
- [ ] Option to submit to DEIA BOK (if public pattern)
- [ ] Privacy review before sharing

---

## Epic 8: Integration with Development Tools

### Story 8.1: Detect Active IDE/Project
**Priority:** P2 (Enhanced Experience)

**As a** developer with VS Code or other IDE open
**I want** the extension to know which project I'm working on
**So that** browser conversations auto-tag with correct project

**Acceptance Criteria:**
- [ ] Extension detects localhost:* ports
- [ ] Suggests project name from localhost URL patterns
- [ ] Integration with vscode-deia extension (if installed)
- [ ] Manual project selector if detection fails
- [ ] Per-tab project memory

---

### Story 8.2: Sync with VS Code DEIA Extension
**Priority:** P3 (Power Features)

**As a** developer using both VS Code and browser AI tools
**I want** sessions synced between extensions
**So that** I have unified conversation history

**Acceptance Criteria:**
- [ ] Both extensions write to same .deia/sessions/ folder
- [ ] Sessions list shows VS Code + browser conversations
- [ ] Timestamps and project tags align
- [ ] No conflicts when both write simultaneously
- [ ] Combined search across both sources

---

## Epic 9: Performance & Reliability

### Story 9.1: Offline Conversation Buffering
**Priority:** P1 (Early Release)

**As a** developer with unreliable internet
**I want** conversations buffered locally even if connection drops
**So that** I don't lose data during network issues

**Acceptance Criteria:**
- [ ] Conversations buffered in memory during capture
- [ ] Periodic saves to chrome.storage (every 1 min)
- [ ] Recovery on browser crash/restart
- [ ] Warning if buffer exceeds limit (10 MB)
- [ ] Manual "Flush Buffer" option

---

### Story 9.2: Minimal Performance Impact
**Priority:** P1 (Early Release)

**As a** developer who keeps many tabs open
**I want** the extension to use minimal CPU/memory
**So that** my browser stays fast

**Acceptance Criteria:**
- [ ] CPU usage <1% during idle monitoring
- [ ] Memory footprint <50MB per tab
- [ ] No UI jank or page slowdowns
- [ ] Lazy-load session review interface
- [ ] Debounced DOM observations

---

## Priority Summary

### P0 - MVP (Must Have) - 6 Stories
1. Story 1.1: Detect AI Coding Tools
2. Story 1.2: Real-time Conversation Capture
3. Story 2.1: Quick Manual Log
4. Story 2.3: Pause/Resume Auto-logging
5. Story 4.1: Local-only Storage
6. Story 6.1: Zero-config First Run

### P1 - Early Release - 7 Stories
7. Story 1.4: Code Block Recognition
8. Story 3.1: Save to .deia/sessions/
9. Story 4.2: Automatic PII Detection
10. Story 6.2: Unobtrusive Indicators
11. Story 6.3: Session Review Interface
12. Story 9.1: Offline Conversation Buffering
13. Story 9.2: Minimal Performance Impact

### P2 - Enhanced Experience - 4 Stories
14. Story 1.3: Handle Claude Projects Conversations
15. Story 2.2: Partial Conversation Selection
16. Story 3.2: Link Sessions to Active Project
17. Story 5.3: Universal Conversation Format
18. Story 8.1: Detect Active IDE/Project

### P3 - Power Features - 5 Stories
19. Story 3.3: Pattern Extraction Suggestions
20. Story 5.1: Cross-tool Session Linking
21. Story 5.2: Tool Comparison Insights
22. Story 7.2: Code Outcome Tracking
23. Story 8.2: Sync with VS Code DEIA Extension

### P4 - Future/Nice-to-Have - 3 Stories
24. Story 4.3: Selective Domain Permissions
25. Story 7.1: Conversation Branching Detection
26. Story 7.3: Collaboration & Sharing

---

## Development Phases

### Phase 1: MVP (v0.1.0) - Weeks 1-3
**Focus:** Core capture and manual logging
- P0 stories (1.1, 1.2, 2.1, 2.3, 4.1, 6.1)
- Goal: Prove the concept works

### Phase 2: DEIA Integration (v0.2.0) - Weeks 4-6
**Focus:** File system and DEIA CLI integration
- P1 stories (1.4, 3.1, 4.2, 6.2, 6.3, 9.1, 9.2)
- Goal: Seamless DEIA workflow

### Phase 3: Multi-tool (v0.3.0) - Weeks 7-8
**Focus:** Expand to Gemini, Copilot
- P2 stories (1.3, 5.3)
- Goal: Universal AI tool support

### Phase 4: Intelligence (v0.4.0) - Weeks 9-10
**Focus:** Pattern extraction and BOK
- P3 stories (3.3, 5.1, 5.2, 7.2)
- Goal: Smart pattern suggestions

### Phase 5: Polish (v0.5.0) - Weeks 11-12
**Focus:** Advanced UX and sync
- P2 stories (2.2, 3.2, 8.1)
- P3 stories (8.2)
- Goal: Power user features

### Phase 6: Stable (v1.0.0) - Weeks 13-16
**Focus:** Production ready, Chrome Web Store
- P4 stories (selective)
- Testing, documentation, packaging
- Goal: Public release

---

**Total:** 26 user stories across 9 epics
**Timeline:** 16 weeks to v1.0.0 stable release

**Last Updated:** 2025-10-10

