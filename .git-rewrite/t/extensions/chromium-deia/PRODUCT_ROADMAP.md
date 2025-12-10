# chromium-deia Product Roadmap

**Quick reference for development priorities**

---

## MVP Release (v0.1.0) - 2-3 weeks

**Goal:** Basic conversation capture with manual logging

### Must-Have Features
1. **Auto-detect Claude/ChatGPT** pages ✓ (foundation exists)
2. **Capture conversations** from DOM in real-time
3. **Manual "Log Now"** button in popup
4. **Pause/resume** auto-logging
5. **Local storage** in browser (chrome.storage.local)
6. **Privacy-first** - no external calls

### Success Criteria
- Works on claude.ai and chat.openai.com
- Can capture and save 10+ message conversation
- Visual indicator shows when active
- Users can pause if discussing sensitive topics

### Technical Tasks
- [ ] Implement MutationObserver for Claude DOM
- [ ] Implement MutationObserver for ChatGPT DOM
- [ ] Build conversation parser for each tool
- [ ] Create storage schema (JSON format)
- [ ] Test with long conversations (50+ messages)

---

## v0.2.0 - DEIA Integration (4-6 weeks)

**Goal:** Integrate with DEIA CLI and local file system

### Features
1. **Save to .deia/sessions/** folder (File System Access API)
2. **DEIA-compatible format** (markdown + YAML frontmatter)
3. **Project tagging** - link sessions to active project
4. **PII detection** - warn before logging secrets
5. **Code block extraction** - identify and tag code snippets

### Success Criteria
- Works seamlessly with DEIA CLI (`deia list`, `deia extract`)
- Sessions appear in vscode-deia timeline
- 90%+ accuracy on PII detection
- Code blocks tagged with correct language

### Technical Tasks
- [ ] File System Access API integration
- [ ] DEIA format writer (match ConversationLogger)
- [ ] PII regex patterns (API keys, passwords, emails)
- [ ] Code block parser with language detection

---

## v0.3.0 - Multi-tool Support (6-8 weeks)

**Goal:** Expand beyond Claude and ChatGPT

### Features
1. **Gemini support** (gemini.google.com)
2. **Copilot support** (copilot.microsoft.com)
3. **Claude Projects** special handling
4. **Universal conversation format** (tool-agnostic)
5. **Tool comparison dashboard**

### Success Criteria
- Works on 4+ AI tools
- Unified session format across tools
- Users can see which tool they prefer for what tasks

### Technical Tasks
- [ ] Gemini DOM parser
- [ ] Copilot DOM parser
- [ ] Claude Projects detection and context capture
- [ ] Schema v2 with tool metadata
- [ ] Usage analytics (local only)

---

## v0.4.0 - Pattern Intelligence (8-10 weeks)

**Goal:** Smart pattern extraction and BOK integration

### Features
1. **Pattern suggestions** - AI detects potential BOK patterns
2. **Code outcome tracking** - "Did this solution work?"
3. **Cross-tool session linking** - link related conversations
4. **Sanitization wizard** - guided PII removal for sharing
5. **BOK submission** - one-click pattern contribution

### Success Criteria
- 10+ patterns submitted from browser sessions
- User feedback: "This saved me time documenting solutions"
- Sanitization catches 99%+ of sensitive data

### Technical Tasks
- [ ] Pattern detection heuristics (keywords, structure)
- [ ] Outcome tracking UI (thumbs up/down on code)
- [ ] Session linking by tags or similarity
- [ ] Sanitization workflow with preview
- [ ] BOK submission GitHub integration

---

## v0.5.0 - Advanced UX (10-12 weeks)

**Goal:** Power user features and polish

### Features
1. **Session review interface** - browse all past conversations
2. **Partial conversation selection** - log only relevant parts
3. **Conversation branching** - track when user backtracks
4. **Keyboard shortcuts** - fast logging without mouse
5. **Sync with vscode-deia** - unified session history

### Success Criteria
- Session review loads <500ms with 100+ sessions
- Power users adopt keyboard shortcuts
- VS Code + browser sessions show in single timeline

### Technical Tasks
- [ ] Full-page session browser UI
- [ ] Selection interface for partial logs
- [ ] Branch detection in conversation flow
- [ ] Keyboard shortcut system
- [ ] Shared .deia/sessions/ with file watching

---

## v1.0.0 - Stable Release (12-16 weeks)

**Goal:** Production-ready, Chrome Web Store launch

### Features
1. **Onboarding flow** - welcome tour for new users
2. **Settings import/export** - backup configuration
3. **Chrome Web Store listing** - public availability
4. **Documentation site** - usage guides and FAQs
5. **Community feedback loop** - in-app feature voting

### Success Criteria
- 500+ users in first month after store launch
- <10 critical bugs reported
- 4+ star rating on Chrome Web Store
- Active community discussions

### Technical Tasks
- [ ] Chrome Web Store packaging and submission
- [ ] Onboarding tutorial (interactive)
- [ ] Settings backup/restore
- [ ] Documentation site (GitHub Pages or similar)
- [ ] Telemetry (opt-in, privacy-respecting)

---

## Future Releases (Post-1.0)

### v1.1 - Enterprise Features
- Team session sharing (private repos)
- Custom domain support (internal AI tools)
- LDAP/SSO integration for team auth
- Admin dashboard for team usage

### v1.2 - Cross-browser Support
- Firefox port (WebExtensions API)
- Safari port (if feasible)
- Edge-specific optimizations

### v1.3 - Advanced Analytics
- Local LLM for pattern analysis (privacy-first)
- Conversation quality scoring
- Learning path recommendations
- Time-to-solution metrics

### v2.0 - Ecosystem Integration
- Direct API integrations (if vendors allow)
- Real-time collaboration on sessions
- Pattern marketplace (optional)
- Research partnerships (academic access)

---

## Risk Mitigation

### Technical Risks
**Risk:** AI tools change DOM structure frequently
**Mitigation:**
- Abstract scraping logic into tool-specific adapters
- Version detection and fallback strategies
- Community contributions for tool updates

**Risk:** File System Access API limited on some browsers
**Mitigation:**
- Fallback to chrome.storage.local
- Export to downloads folder as alternative

**Risk:** Performance impact on browser
**Mitigation:**
- Lazy loading, debouncing, throttling
- Performance testing with long conversations
- User-configurable performance mode

### Product Risks
**Risk:** Low adoption due to setup complexity
**Mitigation:**
- Zero-config first run experience
- Progressive enhancement (works standalone, better with DEIA CLI)
- Clear value proposition in onboarding

**Risk:** Privacy concerns about conversation capture
**Mitigation:**
- Transparent documentation of what's captured
- Open source for auditability
- Local-only storage (no servers)
- Easy data export and deletion

---

## Development Principles

1. **Privacy-first** - No data leaves user's machine without explicit action
2. **Unobtrusive** - Never interrupt developer flow
3. **Tool-agnostic** - Support all major AI coding assistants
4. **DEIA-compatible** - Seamless integration with CLI and VS Code
5. **Community-driven** - Open source, accept contributions
6. **Performance-conscious** - <50ms overhead on page interactions

---

## Resources Needed

### Development
- 1-2 developers (Dave + contributors)
- Chrome extension expertise
- DEIA core library integration
- UI/UX design for session review interface

### Testing
- Test accounts for all AI tools
- Multiple browsers (Chrome, Edge, Brave)
- Performance testing tools
- Community beta testers

### Infrastructure
- GitHub repository (✓ exists)
- Chrome Web Store account
- Documentation hosting (GitHub Pages)
- Community discussion forum (GitHub Discussions)

---

## Success Metrics (KPIs)

### Adoption Metrics
- Weekly active users (WAU)
- Sessions logged per user per week
- Retention rate (30-day, 90-day)

### Quality Metrics
- Crash rate (<1%)
- PII detection accuracy (>95%)
- Performance impact (<50ms)
- User-reported bugs per week

### Value Metrics
- Patterns submitted to BOK
- GitHub stars on repo
- Community contributions (PRs, issues)
- User testimonials and case studies

---

**Last Updated:** 2025-10-10
**Owner:** Dave Eichler
**Contributors:** DEIA Community

