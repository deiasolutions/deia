# DEIA: Product Vision & Technical Direction

## The Problem We're Solving

**Vendors extract our AI development knowledge. We get nothing back.**

Every day, thousands of developers generate valuable knowledge:
- Debugging patterns that actually work
- Workarounds for library bugs
- Architecture decisions that succeed or fail
- Coding practices that scale with AI assistants

This knowledge flows UP to vendors (Anthropic, OpenAI, Microsoft). They train better models. They improve their products. They profit.

We get... slightly better autocomplete. If we pay.

Meanwhile, when YOU hit that same Python async bug next week, when YOUR team needs to know what TDD approach works with Claude Code, when the developer next to you discovers a Cursor workaround—that knowledge is locked away. In vendor servers. In lost conversations. In heads.

**DEIA redirects this flow.** Knowledge flows peer to peer. You control your data. Community benefits from shared patterns. Vendors participate as equals, not extractors.

This is infrastructure for user sovereignty in the AI era.

---

## The Solution Architecture

### Three Platforms, One Commons

**Why three platforms?** Because AI development happens everywhere:
- Terminal (Claude Code, Aider, command-line tools)
- Browser (Claude.ai, ChatGPT, web development)
- IDE (Copilot, Cursor, VS Code workflows)

Capture only one? You miss most of the knowledge. Capture all three? Comprehensive evidence of what works.

### Platform 1: CLI (Python)
**What it does**: Foundation and terminal AI capture

**Core capabilities**:
- Conversation logging (manual and automatic)
- Project initialization (`deia init`)
- Cross-platform preferences (`.deia/preferences.md`)
- Sanitization (strip PII/secrets before sharing)
- Body of Knowledge (search, sync, submit patterns)
- Admin tools (security scanning, quality control)

**Why CLI first**: 
- Works everywhere (cross-platform by nature)
- Foundation for other platforms (browser/VS Code call it)
- Claude Code integration (the tool that sparked this)
- Fastest to build and iterate

**Current state to assess**:
- What commands exist and work?
- What's stubbed vs functional?
- What breaks or doesn't exist yet?
- How's the auto-logging for Claude Code?

### Platform 2: Browser Extension
**What it does**: Web AI capture + web dev session intelligence

**Core capabilities**:
- Log Claude.ai conversations
- Log ChatGPT conversations  
- Capture web dev bugs and workarounds
- Read local preferences
- Copy preferences to clipboard (for pasting into ANY AI tool)
- Communicate with local DEIA (send logs, get patterns)

**Why browser matters**:
- Most people use Claude.ai or ChatGPT web
- Web dev sessions = rich bug/workaround data
- Browser crashes = conversations lost (insurance value)
- Clipboard feature = immediate utility before full integration

**Current state to assess**:
- Does extension exist at all?
- What's built vs designed vs wishlist?
- Technical decisions needed (Chrome first? Firefox?)
- How does it talk to local DEIA? (localhost API? file system?)

### Platform 3: VS Code Extension
**What it does**: IDE AI capture + development workflow integration

**Core capabilities**:
- Log Copilot conversations
- Log Cursor sessions
- Status bar integration (logging active/paused)
- Command palette commands
- Chat participant (`@deia` commands)
- Preferences integration (read, copy, apply)
- Calls Python CLI for heavy lifting

**Why VS Code matters**:
- Where serious development happens
- Copilot has massive user base
- Cursor is exploding in AI dev community
- IDE context = richest development evidence

**Current state to assess**:
- Extension in progress—what works?
- What's blocking completion?
- Does it call CLI correctly?
- Chat participant functional?
- Status bar working?

---

## The Heart of the System: Preferences

**Not "settings." Preferences. There's a difference.**

Settings are tool-specific configs. Preferences are how you work—your standards, your team's practices, your hard-won knowledge about what actually works with AI.

### The Problem Today
- Cursor has `.cursorrules` (only works in Cursor)
- Claude.ai has Projects (only works in browser)
- Copilot has workspace context (proprietary)
- You copy-paste the same instructions everywhere
- New AI tool launches → reconfigure everything
- Context lost switching tools

### The DEIA Solution
**One file: `.deia/preferences.md`**

Contains:
- General preferences (apply everywhere): TDD, Python 3.13, docstring style
- Platform-specific (Claude Code slash commands, Cursor agent mode)
- Project-level (team standards)
- Personal (~/.deia/preferences.md for your own style)

**All platforms read it. New tool? Instant integration. No reconfiguration.**

This is the "cross-platform intelligence" that makes DEIA valuable even at n=1.

### Two Levels
**User-level**: `~/.deia/preferences.md` - Your personal coding standards
**Project-level**: `/project/.deia/preferences.md` - Team/project standards

Project overrides user. Platform-specific overrides general. Simple hierarchy.

### Current State to Assess
- File format defined?
- Parser exists?
- Which platforms can read it?
- Which platforms can inject it into AI tools?
- Does hierarchy work (user → project, general → specific)?
- Template generation on `deia init`?

---

## The Commons: Body of Knowledge

**Individual value is immediate. Network value multiplies.**

You log conversations, manage preferences, control your data—all valuable at n=1.

But when community shares patterns (anonymized, sanitized):
- 50 devs hit same bug → aggregated workaround appears
- 200 TDD setups → extract what actually works
- Platform patterns emerge (Railway gotchas, Vercel configs)
- Anti-patterns surface (what fails, what NOT to do)
- Vendor accountability (data = leverage)

**This is the moat.** Not technology (anyone can build logging). The community patterns.

### BOK Structure
```
bok/
  platforms/          # Railway, Vercel, Claude Code, Cursor
  patterns/           # What works (TDD, collaboration, architecture)
  anti-patterns/      # What fails (autonomous deployment, no tests)
  languages/          # Python, JavaScript, etc.
  frameworks/         # FastAPI, React, etc.
  bugs/               # Known issues + workarounds
```

### Submission Workflow
1. You log conversations/patterns locally
2. Run `deia sanitize` (strips PII, secrets, company info)
3. Manual review (you control what shares)
4. Submit via PR to deia-bok repo
5. Community curation (quality matters)
6. Everyone benefits

**This is opt-in, privacy-first, user-controlled.**

### Current State to Assess
- BOK repo structure exists?
- Submission workflow works?
- Sanitization robust?
- Search functionality?
- Pattern format defined?
- Community moderation plan?

---

## Sanitization: Non-Negotiable

**You can't share raw logs. Ever.**

They contain:
- API keys, tokens, passwords
- Internal URLs, company IP
- Customer data, PII
- Proprietary algorithms, trade secrets

**Two-tier sanitization:**
- **For AI review** (Claude/GPT4 reviews before human): Strip obvious secrets, flag suspicious content
- **For public sharing**: Aggressive PII removal, manual review required

### What Gets Sanitized
- API keys, access tokens, JWT
- Email addresses, phone numbers, names
- Internal domain names, IP addresses
- File paths revealing company structure
- Specific customer references
- Proprietary code snippets (patterns okay, implementation no)

### Current State to Assess
- Sanitization engine exists?
- Detection patterns comprehensive?
- False positive rate acceptable?
- Manual review workflow?
- Pre-commit hooks?
- Two-tier implementation?

---

## Bug & Workaround Intelligence

**This is where vendor accountability emerges.**

When 50 developers report:
- "Claude Code fails with X error on Windows"
- "Cursor agent mode breaks on files >1000 lines"
- "Railway deployment fails with Y, here's the fix"

**Aggregated data = power.**

For users: "Known issue. 89% use this workaround. Fix coming in v2.3."
For vendors: "Your API breaks in these 10 ways. Here's crowdsourced data."

Equal exchange, not extraction.

### Capture Points
- Browser extension: web errors, console logs, debugging sessions
- VS Code extension: IDE errors, failed builds, extension crashes
- CLI: command failures, API errors, integration issues

### Current State to Assess
- Bug detection implemented?
- Context capture (environment, stack trace)?
- Workaround documentation format?
- Aggregation logic?
- Vendor reporting workflow?
- Privacy in bug reports?

---

## Integration: GitHub Spec Kit

**Spec Kit is brand new (Sep 2025) and gaining traction.**

GitHub's framework for spec-driven development. DEIA complements it perfectly:
- Spec Kit: WHAT you're building (specs, architecture, plans)
- DEIA: HOW you build it (coding standards, preferences, practices)

### Potential Integration
- `deia suggest-spec` - Community spec patterns for your stack
- Spec Kit's `constitution.md` ≈ DEIA's preferences
- Share spec patterns to DEIA BOK
- Learn from others' successful projects

**Priority: LOW for now.** Validate core features first. But keep architecture compatible.

---

## Technical Decisions Needed

### Browser Extension Architecture
**Question**: How does browser talk to local DEIA?

**Option A - Localhost API**:
- Python CLI runs local API server (Flask/FastAPI)
- Browser extension sends logs via HTTP
- Pro: Clean separation, language-agnostic
- Con: Need to run server, port conflicts, auth

**Option B - File System**:
- Browser extension writes directly to `.deia/sessions/`
- Requires native messaging host
- Pro: No server needed
- Con: More complex extension, OS-specific

**Option C - Hybrid**:
- Direct file write for logs
- HTTP for complex operations (search BOK, sanitize)
- Pro: Best of both
- Con: Two integration paths to maintain

**What's your preference?**

### VS Code Extension Integration
**Question**: How much does VS Code do vs delegating to CLI?

**Option A - Thin wrapper**:
- All logic in Python CLI
- VS Code just calls CLI commands
- Pro: Logic centralized, easier to maintain
- Con: subprocess overhead, error handling

**Option B - Smart extension**:
- Conversation capture in TypeScript
- CLI for heavy operations (sanitize, BOK)
- Pro: Better performance, native integration
- Con: Logic split between platforms

**Option C - Current approach**:
- Assess what's built, don't overengineer

**What exists now?**

### Preference Injection
**Question**: How do AI tools actually read preferences?

**For Claude Code**:
- Startup hooks? Config file? Manual injection?
- Can it read `.deia/preferences.md` automatically?
- Or need `deia load-prefs` before each session?

**For Cursor**:
- Override `.cursorrules` with `.deia/preferences.md`?
- Or convert DEIA → Cursor format?

**For Copilot**:
- Workspace instructions?
- Extension can inject context?

**What's technically possible vs wishful thinking?**

---

## What Matters Most Right Now

**Priority 1: Your Daily Workflow**
What do YOU use most? Where's the pain?
- If Claude Code: Get auto-logging rock solid
- If Claude.ai: Build browser extension
- If Cursor/Copilot: Finish VS Code extension

**Build for yourself first. Dogfood it. If it doesn't help you, it won't help anyone.**

**Priority 2: Cross-Platform Prefs**
This is the unique value. Get it working for TWO platforms minimum:
- Proves the concept (one source of truth)
- Shows immediate benefit (stop copy-pasting)
- Demonstrates technical feasibility

**Priority 3: Third Platform**
Complete coverage. Now you have comprehensive evidence capture.

**Priority 4: Community Features**
BOK, sharing, patterns—only after individual value proven.

**Priority 5: Everything Else**
Spec Kit, dashboards, analytics—nice but not essential.

---

## Questions for Assessment

**Current State**:
1. What actually works today when you run commands?
2. What's built but broken?
3. What's designed but not implemented?
4. What's blocking you from daily use?

**Architecture**:
5. How should browser extension talk to local DEIA?
6. How much logic in VS Code vs CLI?
7. How does preference injection actually work technically?

**Priorities**:
8. Which platform do you use most? (Honest answer)
9. What would give YOU the most immediate value?
10. What's the minimum to get first external user?

**Scope**:
11. What can we cut and still prove the vision?
12. What's essential vs nice-to-have?
13. What's blocking vs parallelizable?

---

## The Vision Stays Constant

**We're building infrastructure for user sovereignty in the AI era.**

Not a dev tool with feature bloat. Not a startup chasing metrics. Infrastructure that matters:
- You control your data
- Knowledge flows peer to peer
- Community governs the commons
- Vendors participate as equals

Everything we build serves this vision. Everything else is noise.

**Now: assess where we are, prioritize what matters, build what helps.**

Let's do this.
