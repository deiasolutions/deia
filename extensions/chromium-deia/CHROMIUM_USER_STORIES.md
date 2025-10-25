# chromium-deia User Stories

**Target Users:** Developers coding with browser-based AI tools (Claude, ChatGPT, Gemini, etc.)

**Core Value Proposition:** Automatically capture coding conversations and patterns without disrupting flow, building collective knowledge commons.

---

## Epic 1: Automatic Conversation Capture

### Story 1.1: Detect AI Coding Tools
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

**Technical Notes:**
- Content script monitors URL patterns
- Check for common AI coding elements (code blocks, conversation threads)
- Lightweight detection to avoid performance impact

---

### Story 1.2: Real-time Conversation Capture
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

**Technical Notes:**
- MutationObserver for DOM changes
- Tool-specific selectors (each AI tool has different HTML structure)
- Local buffer in case of network issues
- Debounced capture to avoid excessive writes

---

### Story 1.3: Handle Claude Projects Conversations
**As a** developer using Claude Projects (with attached files/docs)
**I want** conversations in Projects captured with context about attached files
**So that** patterns include the project context

**Acceptance Criteria:**
- [ ] Detect when in Claude Projects vs standard chat
- [ ] Capture project name and description
- [ ] Note which files/docs are attached (names, not content for privacy)
- [ ] Distinguish between project chats and general chats
- [ ] Track conversation continuity across sessions

**Technical Notes:**
- Projects have different DOM structure than standard chat
- Need to identify project context from page metadata
- Privacy: Only capture file names, not content (unless user opts in)

---

### Story 1.4: Code Block Recognition and Extraction
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

**Technical Notes:**
- Most AI tools use markdown-style code blocks with language tags
- Could track which code blocks user copies (engagement signal)
- Store code blocks with start/end line numbers in conversation

---

## Epic 2: Manual Logging Controls

### Story 2.1: Quick Manual Log
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

**Technical Notes:**
- Badge color indicates if conversation detected (green) or not (gray)
- Popup loads quickly (<200ms)
- Preview shows user prompt + AI response snippets

---

### Story 2.2: Partial Conversation Selection
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

**Technical Notes:**
- UI shows compact message list (user/AI icons + first line)
- Drag to select range, or click start + click end
- Store selection in sessionStorage temporarily

---

### Story 2.3: Pause/Resume Auto-logging
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

**Technical Notes:**
- Store pause state in chrome.storage.local
- MutationObserver stops when paused
- Badge shows pause icon (⏸)

---

## Epic 3: DEIA Integration

### Story 3.1: Save to .deia/sessions/
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

**Technical Notes:**
- Need File System Access API (Chrome 86+)
- User must grant permission to write to directory
- Format matches ConversationLogger output from Python library
- Include metadata: tool (claude/chatgpt), url, duration, message_count

---

### Story 3.2: Link Sessions to Active Project
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

**Technical Notes:**
- Store project mapping in chrome.storage.local
- Tab ID → project name mapping
- When saving, write to project-specific .deia/sessions/

---

### Story 3.3: Pattern Extraction Suggestions
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

**Technical Notes:**
- Simple keyword/heuristic analysis (no AI call needed)
- Patterns to detect: troubleshooting, architecture decisions, tool workflows
- Integration with `deia extract` command (if DEIA CLI available)

---

## Epic 4: Privacy & Security

### Story 4.1: Local-only Storage
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

**Technical Notes:**
- Open source for auditability
- No third-party libraries that phone home
- Storage location clearly documented

---

### Story 4.2: Automatic PII Detection
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

**Technical Notes:**
- Regex patterns for common secrets (GitHub tokens, AWS keys, etc.)
- Check against patterns from .gitignore-style rules
- Use DEIA sanitization patterns from core library

---

### Story 4.3: Selective Domain Permissions
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

**Technical Notes:**
- Use chrome.permissions API for runtime permissions
- Custom domains: user provides URL pattern + CSS selectors for messages

---

## Epic 5: Multi-tool Intelligence

### Story 5.1: Cross-tool Session Linking
**As a** developer using both Claude and ChatGPT for same problem
**I want** conversations linked if they're about the same topic
**So that** I can see full problem-solving context across tools

**Acceptance Criteria:**
- [ ] User can tag conversations with topic/issue ID
- [ ] Extension suggests linking if similar code/terms detected
- [ ] Linked sessions show in session list
- [ ] Can view combined timeline across tools
- [ ] Export linked sessions as single document

**Technical Notes:**
- Simple tagging: user provides ID (e.g., "bug-auth-flow")
- Keyword similarity detection (TF-IDF or simpler)
- Linked sessions stored with relationship metadata

---

### Story 5.2: Tool Comparison Insights
**As a** developer curious about AI tool differences
**I want** to see which tool I use more and for what tasks
**So that** I can optimize my workflow

**Acceptance Criteria:**
- [ ] Dashboard showing usage stats: sessions per tool
- [ ] Breakdown by conversation length (quick vs deep)
- [ ] Identify patterns: "I use Claude for architecture, ChatGPT for debugging"
- [ ] Export stats as CSV
- [ ] Privacy: All analysis local, no server calls

**Technical Notes:**
- Aggregate data from logged sessions
- Simple categorization by keywords
- Visualizations: charts in settings page (Chart.js or similar)

---

### Story 5.3: Universal Conversation Format
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

**Technical Notes:**
- JSON or YAML frontmatter + markdown body
- Schema versioning (v1, v2, etc.)
- Matches ConversationLogger format from Python library

---

## Epic 6: User Experience

### Story 6.1: Zero-config First Run
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

**Technical Notes:**
- First run: show onboarding popup
- Defaults: auto-log ON, all tools enabled, browser storage
- Progressive enhancement: better with DEIA CLI, but works without

---

### Story 6.2: Unobtrusive Indicators
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

**Technical Notes:**
- Subtle toast notification (bottom-right corner)
- CSS animations for smooth fade
- Respect user's reduced-motion preferences

---

### Story 6.3: Session Review Interface
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

**Technical Notes:**
- Full-page UI (separate HTML page opened in new tab)
- Load sessions from chrome.storage or .deia/sessions/
- Search uses simple string matching (could enhance with fuse.js)

---

## Epic 7: Advanced Features

### Story 7.1: Conversation Branching Detection
**As a** developer who often backtracks in conversations
**I want** the extension to track conversation branches
**So that** I can see alternative solutions I explored

**Acceptance Criteria:**
- [ ] Detect when user edits/resends a prompt
- [ ] Track branches as separate conversation paths
- [ ] Visualize branches in session review
- [ ] Can compare branches side-by-side
- [ ] Export includes all branches

**Technical Notes:**
- Claude Projects shows edit history (detect DOM changes)
- ChatGPT shows regenerate button usage
- Store branches as tree structure

---

### Story 7.2: Code Outcome Tracking
**As a** developer who gets code suggestions
**I want** to mark which suggestions I actually used
**So that** DEIA knows which patterns were valuable

**Acceptance Criteria:**
- [ ] After copying code, prompt to mark "Did this work? (Yes/No/Modified)"
- [ ] Optional follow-up note
- [ ] Tracked outcomes stored with session
- [ ] Analytics: Which types of problems have best AI solutions
- [ ] Contributes to pattern confidence ratings

**Technical Notes:**
- Detect copy events on code blocks
- Show unobtrusive prompt after paste detected in another tab (tricky)
- Or simpler: Manual "Mark Outcome" in session review

---

### Story 7.3: Collaboration & Sharing
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

**Technical Notes:**
- Uses DEIA sanitization patterns
- GitHub Gist creation via API (requires auth)
- BOK submission follows CONTRIBUTING.md workflow

---

## Epic 8: Integration with Development Tools

### Story 8.1: Detect Active IDE/Project
**As a** developer with VS Code or other IDE open
**I want** the extension to know which project I'm working on
**So that** browser conversations auto-tag with correct project

**Acceptance Criteria:**
- [ ] Extension detects localhost:* ports
- [ ] Suggests project name from localhost URL patterns
- [ ] Integration with vscode-deia extension (if installed)
- [ ] Manual project selector if detection fails
- [ ] Per-tab project memory

**Technical Notes:**
- Check for localhost:3000, localhost:8080, etc.
- Could use local storage sync between vscode-deia and chromium-deia
- Simple heuristics: common dev server ports

---

### Story 8.2: Sync with VS Code DEIA Extension
**As a** developer using both VS Code and browser AI tools
**I want** sessions synced between extensions
**So that** I have unified conversation history

**Acceptance Criteria:**
- [ ] Both extensions write to same .deia/sessions/ folder
- [ ] Sessions list shows VS Code + browser conversations
- [ ] Timestamps and project tags align
- [ ] No conflicts when both write simultaneously
- [ ] Combined search across both sources

**Technical Notes:**
- Shared file system via File System Access API
- File naming prevents conflicts (include source: vscode/browser)
- Watch for file changes (chrome.fileSystem API)

---

## Epic 9: Performance & Reliability

### Story 9.1: Offline Conversation Buffering
**As a** developer with unreliable internet
**I want** conversations buffered locally even if connection drops
**So that** I don't lose data during network issues

**Acceptance Criteria:**
- [ ] Conversations buffered in memory during capture
- [ ] Periodic saves to chrome.storage (every 1 min)
- [ ] Recovery on browser crash/restart
- [ ] Warning if buffer exceeds limit (10 MB)
- [ ] Manual "Flush Buffer" option

**Technical Notes:**
- IndexedDB for large buffer storage
- Service worker persists across page reloads
- chrome.storage.local for smaller metadata

---

### Story 9.2: Minimal Performance Impact
**As a** developer who keeps many tabs open
**I want** the extension to use minimal CPU/memory
**So that** my browser stays fast

**Acceptance Criteria:**
- [ ] CPU usage <1% during idle monitoring
- [ ] Memory footprint <50MB per tab
- [ ] No UI jank or page slowdowns
- [ ] Lazy-load session review interface
- [ ] Debounced DOM observations

**Technical Notes:**
- Use IntersectionObserver for efficient DOM watching
- Throttle MutationObserver callbacks
- Offload heavy processing to service worker

---

## Priority Matrix

### P0 (MVP - Must Have)
- Story 1.1: Detect AI Coding Tools
- Story 1.2: Real-time Conversation Capture
- Story 2.1: Quick Manual Log
- Story 2.3: Pause/Resume Auto-logging
- Story 4.1: Local-only Storage
- Story 6.1: Zero-config First Run

### P1 (Early Release)
- Story 1.4: Code Block Recognition
- Story 3.1: Save to .deia/sessions/
- Story 4.2: Automatic PII Detection
- Story 6.2: Unobtrusive Indicators
- Story 6.3: Session Review Interface

### P2 (Enhanced Experience)
- Story 1.3: Handle Claude Projects Conversations
- Story 2.2: Partial Conversation Selection
- Story 3.2: Link Sessions to Active Project
- Story 5.3: Universal Conversation Format
- Story 8.1: Detect Active IDE/Project

### P3 (Power Features)
- Story 3.3: Pattern Extraction Suggestions
- Story 5.1: Cross-tool Session Linking
- Story 5.2: Tool Comparison Insights
- Story 7.2: Code Outcome Tracking
- Story 8.2: Sync with VS Code DEIA Extension

### P4 (Future/Nice-to-Have)
- Story 7.1: Conversation Branching Detection
- Story 7.3: Collaboration & Sharing
- Story 4.3: Selective Domain Permissions

---

## Success Metrics

**Adoption:**
- 100+ active users in first month
- 50% of users enable auto-logging
- 20+ sessions logged per user per week

**Quality:**
- <1% false positives in PII detection
- <5 GitHub issues per week
- 90%+ uptime (no crashes)

**Value:**
- 10+ patterns submitted to BOK from browser sessions
- 5+ users integrate with DEIA CLI
- Positive feedback from early adopters

---

## Technical Constraints

1. **Chrome Manifest V3** - Service workers, no background pages
2. **No remote servers** - All processing local (privacy-first)
3. **File System Access** - Requires user permission (Chrome 86+)
4. **Cross-origin restrictions** - Can't access all site data without permissions
5. **Tool-specific scraping** - Each AI tool has different DOM structure

---

## Open Questions

1. How to handle very long conversations (100+ messages)? Chunking strategy?
2. Should we support Firefox (different extension API)? Separate project?
3. How to detect if user copies code to IDE vs just reads it?
4. Best way to sync with vscode-deia without conflicts?
5. Should we build a local LLM integration for pattern extraction? (Privacy-first analysis)

---

**Version:** 1.0
**Last Updated:** 2025-10-10
**Contributors:** Dave, Claude Code

