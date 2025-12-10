# DEIA VS Code Extension Specification

**Status:** Design document for future implementation
**Priority:** High (enables non-Claude Code users)

---

## Overview

VS Code extension to enable DEIA conversation logging and BOK submission for:
- GitHub Copilot users
- Other AI coding assistants (Tabnine, Codeium, etc.)
- Manual coding sessions

**Key feature:** Works with ANY AI assistant in VS Code, not just Claude Code.

---

## Core Features

### 1. Conversation Logging

**Auto-detect AI interactions:**
- GitHub Copilot suggestions
- Chat conversations (if available via API)
- Code completions with context

**Manual logging:**
- Command palette: "DEIA: Log Current Session"
- Keyboard shortcut: `Ctrl+Shift+D L`
- Status bar button: "Log Session"

**What gets logged:**
- Timestamp
- Files modified
- AI suggestions accepted/rejected
- Chat conversations (if accessible)
- Code changes with context

### 2. Pattern Extraction

**Smart detection:**
- Identify repetitive patterns
- Suggest pattern extraction
- Show notification: "This looks like a shareable pattern. Extract to DEIA?"

**Manual extraction:**
- Select code/comments
- Right-click → "Extract DEIA Pattern"
- Opens pattern template with context pre-filled

### 3. Auto-Submission (Opt-in)

**Configuration:**
```json
{
  "deia.autoSubmit": false,
  "deia.autoAnonymize": true,
  "deia.trustedSubmitter": false,
  "deia.githubUsername": "your-username",
  "deia.reviewBeforeSubmit": true
}
```

**Workflow:**
1. Pattern extracted
2. Auto-anonymized (if enabled)
3. If `reviewBeforeSubmit`: Show diff, ask for confirmation
4. If trusted submitter: Auto-create PR to DEIA
5. If not trusted: Save to local intake for manual submission

### 4. BOK Search

**Inline search:**
- Command: "DEIA: Search BOK"
- Search community patterns
- Insert pattern into code with attribution

**Contextual suggestions:**
- "Working on authentication? Check these DEIA patterns..."
- Shown in sidebar when relevant

---

## UI Components

### Status Bar Item

```
[DEIA] 🟢 Logging • 3 patterns ready
```

Click actions:
- Log current session
- View patterns in intake
- Open DEIA settings

### Sidebar Panel

```
DEIA
├── 📊 Session Logs (5)
│   ├── 2025-10-06 14:30 - Feature: Auth
│   └── 2025-10-06 09:15 - Bugfix: Database
├── 📥 Intake (3)
│   ├── pattern-auth-flow.md ⚠️ Needs review
│   ├── pattern-error-handling.md ✓ Ready
│   └── pattern-db-migration.md ⚠️ Needs anonymization
├── 🔍 Search BOK
└── ⚙️ Settings
```

### Webview Panel (Pattern Editor)

```
┌─────────────────────────────────────────────┐
│ Extract Pattern                             │
├─────────────────────────────────────────────┤
│                                             │
│ Pattern Name: [Authentication Flow_____]    │
│                                             │
│ Category: ○ Platform-specific              │
│           ● General pattern                │
│           ○ Anti-pattern                   │
│                                             │
│ Description:                                │
│ ┌─────────────────────────────────────────┐ │
│ │ [Fill in pattern description]          │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Code Example: [Extracted from selection]   │
│                                             │
│ ⚠️ PII Detected: 2 items                   │
│   • Email on line 15                       │
│   • API key on line 42                     │
│   [Auto-fix] [Review Manually]             │
│                                             │
│ [Cancel] [Save to Intake] [Submit to DEIA] │
└─────────────────────────────────────────────┘
```

---

## Technical Architecture

### Extension Structure

```
vscode-deia/
├── package.json              # Extension manifest
├── src/
│   ├── extension.ts          # Entry point
│   ├── logger.ts             # Conversation logger
│   ├── pattern-extractor.ts  # Pattern extraction
│   ├── anonymizer.ts         # PII detection and removal
│   ├── submitter.ts          # GitHub PR creation
│   ├── bok-search.ts         # BOK search and retrieval
│   ├── ui/
│   │   ├── sidebar.ts        # Sidebar panel
│   │   ├── statusbar.ts      # Status bar item
│   │   └── webview.ts        # Pattern editor webview
│   └── config.ts             # Configuration management
├── media/                    # Icons, CSS
└── test/                     # Tests
```

### Key APIs

**VS Code APIs used:**
- `vscode.window` - UI components
- `vscode.workspace` - File system access
- `vscode.commands` - Command registration
- `vscode.extensions` - Detect other extensions
- `vscode.TextEditor` - Code modification tracking

**External APIs:**
- GitHub API - PR creation
- DEIA public API (future) - BOK search, pattern submission

### Data Storage

**Local:**
- `.deia/` directory (created by extension)
- `sessions/` - Conversation logs (JSON + markdown)
- `intake/` - Patterns ready for submission
- `config.json` - User preferences

**Remote:**
- GitHub repo - Public DEIA BOK
- Optional: DEIA API service (future)

---

## User Workflows

### Workflow 1: Auto-Logging (GitHub Copilot)

```
1. User writes code with Copilot
2. DEIA extension monitors:
   - Files modified
   - Copilot suggestions accepted
   - Time spent on each file
3. Every 30 minutes: Auto-save session snapshot
4. On session end: Create final log in .deia/sessions/
5. User can review log later
```

### Workflow 2: Manual Pattern Extraction

```
1. User writes useful code pattern
2. User selects code + comments
3. Right-click → "Extract DEIA Pattern"
4. Webview opens with:
   - Pattern name (auto-suggested)
   - Category (auto-detected)
   - Code example (pre-filled)
5. User fills in description
6. Extension scans for PII
7. User reviews and corrects
8. Click "Save to Intake"
9. Pattern saved to .deia/intake/
```

### Workflow 3: Trusted Submitter (Dave's Workflow)

```
1. Dave works with ANY AI assistant
2. Extension logs session automatically
3. Dave extracts pattern
4. Pattern auto-anonymized
5. If Dave is trusted submitter:
   - Auto-create branch in DEIA repo
   - Auto-commit pattern to bok/
   - Auto-create PR
   - DEIA admin (also Dave) auto-accepts (CFRL)
6. Pattern live in public BOK within minutes
```

### Workflow 4: End-User Submission

```
1. User extracts pattern
2. Extension saves to .deia/intake/
3. User reviews, ensures PII removed
4. Command: "DEIA: Submit Pattern"
5. Extension:
   - Forks DEIA repo (if not already)
   - Creates branch
   - Commits pattern
   - Creates PR
6. DEIA maintainer reviews
7. If approved: Pattern added to BOK
```

---

## Configuration Options

```json
{
  // Auto-logging
  "deia.autoLog.enabled": true,
  "deia.autoLog.interval": 30,  // minutes
  "deia.autoLog.onSessionEnd": true,

  // Pattern extraction
  "deia.patterns.autoSuggest": true,
  "deia.patterns.minCodeLines": 5,  // Minimum lines for pattern suggestion

  // Anonymization
  "deia.anonymize.auto": true,
  "deia.anonymize.strictMode": false,  // If true, block submission if PII detected

  // Submission
  "deia.submission.autoSubmit": false,
  "deia.submission.reviewRequired": true,
  "deia.submission.trustedSubmitter": false,

  // GitHub integration
  "deia.github.username": "",
  "deia.github.email": "",
  "deia.github.personalAccessToken": "",  // Stored securely

  // BOK search
  "deia.bok.autoSuggest": true,
  "deia.bok.searchOnError": true,  // Search BOK when error occurs

  // UI
  "deia.statusBar.visible": true,
  "deia.sidebar.autoOpen": false,
  "deia.notifications.enabled": true
}
```

---

## Security Considerations

### PII Detection

**Regex patterns for:**
- Email addresses
- API keys (common formats)
- Passwords (flagged keywords)
- URLs with credentials
- IP addresses (optionally)
- Names (harder, use ML?)

**ML-based detection:**
- Microsoft Presidio (optional dependency)
- Detect PII with higher accuracy
- Can be disabled for performance

### Secrets Management

**GitHub token:**
- Stored in VS Code SecretStorage API
- Never logged or transmitted except to GitHub API
- Can be rotated by user

**Pattern submission:**
- Always review before submit (unless trusted + CFRL)
- Show diff of what will be committed
- Require confirmation

---

## Implementation Phases

### Phase 1: MVP (Core Logging)

- ✅ Extension scaffolding
- ✅ `.deia/` initialization (like `deia init`)
- ✅ Manual session logging
- ✅ Basic status bar
- ✅ Configuration UI

### Phase 2: Pattern Extraction

- ✅ Code selection → Extract pattern
- ✅ Pattern template editor
- ✅ Basic PII detection (regex)
- ✅ Save to intake

### Phase 3: Submission

- ✅ GitHub integration
- ✅ Fork + branch + commit + PR workflow
- ✅ Trusted submitter mode (CFRL)
- ✅ Review UI before submission

### Phase 4: BOK Search

- ✅ Search command
- ✅ Sidebar with results
- ✅ Insert pattern into code
- ✅ Contextual suggestions

### Phase 5: Auto-Logging

- ✅ Monitor file changes
- ✅ Detect AI assistant usage (if API available)
- ✅ Auto-save session snapshots
- ✅ Session end detection

### Phase 6: Advanced

- ✅ ML-based PII detection (Presidio)
- ✅ Pattern suggestion AI
- ✅ DEIA API integration
- ✅ Multi-language support

---

## Marketplace Listing

**Name:** DEIA - AI Development Intelligence

**Description:**
Never lose context. Share what you learn. Build better with AI.

DEIA automatically logs your AI-assisted coding sessions and helps you share valuable patterns with the community while protecting your privacy.

**Features:**
- 🔐 Automatic conversation logging (insurance against crashes)
- 📚 Extract and share coding patterns
- 🔍 Search community Book of Knowledge
- 🤖 Works with GitHub Copilot, Claude, and other AI assistants
- 🛡️ Privacy-first (auto-anonymization, PII detection)
- 🚀 Trusted submitter mode for rapid pattern sharing

**Compatible with:**
- GitHub Copilot
- Claude Code (enhanced integration)
- Cursor (if using VS Code)
- Any AI coding assistant

---

## Open Questions

1. **Can we access GitHub Copilot suggestions programmatically?**
   - May need to use VS Code's proposed API
   - Or monitor `textDocument/didChange` events

2. **How to detect which AI assistant is being used?**
   - Check installed extensions
   - Monitor specific file patterns
   - User self-reports in config

3. **Should we build DEIA API service or use GitHub directly?**
   - GitHub API: Simple, no infrastructure
   - DEIA API: Better control, analytics, validation

4. **How to handle pattern versioning?**
   - BOK entries evolve over time
   - Need versioning strategy
   - Extension should fetch latest

---

## Resources Needed

**Development:**
- TypeScript developers (VS Code extension)
- UI/UX design for webviews
- Testing on multiple AI assistants

**Infrastructure:**
- GitHub Actions for extension publishing
- Optional: DEIA API service (Node.js/Python)
- Optional: ML model hosting (for PII detection)

**Timeline:**
- Phase 1 (MVP): 2-3 weeks
- Phase 2-3 (Full features): 4-6 weeks
- Phase 4-6 (Advanced): 8-12 weeks

---

## Success Metrics

**Adoption:**
- Number of installs
- Active users
- Sessions logged per day

**Engagement:**
- Patterns extracted per user
- Submission rate
- BOK search queries

**Quality:**
- PII detection accuracy
- False positive rate on pattern suggestions
- User satisfaction (ratings)

---

**This extension makes DEIA accessible to ALL VS Code users, not just Claude Code.**

**Estimated reach: 10M+ VS Code users with AI assistants**
