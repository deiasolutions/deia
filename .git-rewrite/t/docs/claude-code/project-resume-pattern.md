# Project Resume Pattern for AI Assistants

**Pattern Category:** Human-AI Collaboration Best Practice

---

## Problem

AI assistants lose context between sessions:
- No memory of previous work
- Don't know project structure or conventions
- Repeat questions already answered
- Miss critical project-specific requirements
- May not know they should check memory/preferences

**User frustration:** "I just told you this yesterday" or "Why don't you remember how this project works?"

---

## Solution

Create a `project_resume.md` file in the project root (or `.deia/project_resume.md` for DEIA projects) that serves as a "read me first" document for AI assistants.

**Think of it as:** The note you'd leave for a new team member starting work on the project.

---

## What to Include

### 1. Orientation Instructions
```markdown
## For AI Assistants Starting a Session

Welcome! Before proceeding:

### Check Your Memory Settings
- Look for existing memories/preferences about this project
- If found: Follow those instructions
- If not found: Read [location of preferences file]

### What This Project Is
[Brief 1-2 sentence description]

### Your Responsibilities
- [Key task 1]
- [Key task 2]
- [Key task 3]
```

### 2. Current State
```markdown
## Current State

### What's Working
- ✅ Feature A
- ✅ Feature B

### Recent Work
- Last session: [summary]

### Pending Tasks
- [ ] Task 1
- [ ] Task 2

### Known Issues
- Issue 1
- Issue 2
```

### 3. Project Structure
```markdown
## Project Structure

```
project/
├── src/           # Source code
├── tests/         # Tests
├── docs/          # Documentation
└── .ai/           # AI assistant configs
```

## Key Files
- `src/main.py` - Entry point
- `.ai/preferences.md` - Your instructions
```

### 4. Essential Context
```markdown
## Important Documents
- [CONTRIBUTING.md] - How to contribute
- [ARCHITECTURE.md] - System design
- [CONVENTIONS.md] - Code style

## Key Commands
```bash
npm run dev    # Start development
npm test       # Run tests
```

## User Preferences
- Communication style: [concise/detailed]
- Common phrases: [any specific terminology]
- Pet peeves: [things to avoid]
```

### 5. Session History
```markdown
## Context from Previous Sessions

### Most Recent Session
- [Summary of last session]
- [Key decisions made]

### User Feedback
- [Any corrections or preferences expressed]
```

---

## Implementation

### Location Options

**Option 1: Project Root**
```
project/
└── PROJECT_RESUME.md
```
- Pro: Easy to find
- Con: Clutters root directory

**Option 2: Hidden Directory**
```
project/
└── .ai/
    └── project_resume.md
```
- Pro: Keeps root clean
- Con: AI might not know to look there

**Option 3: Tool-Specific**
```
project/
└── .deia/
    └── project_resume.md
```
- Pro: Integrated with tooling
- Con: Only works with that tool

**Recommendation:** Use option 2 (`.ai/project_resume.md`) or option 3 if using a specific tool like DEIA.

---

## Template

```markdown
# [Project Name] - Project Resume

**⚠️ IMPORTANT: Read This First**

## For AI Assistants Starting a Session

Welcome! You're working on [Project Name]. Before proceeding:

### 1. Check Your Memory Settings

**If you have memory/preferences capability:**
- Search for "[project name]" in your memories
- If found: Follow those instructions
- If not found: Read [.ai/preferences.md or similar]

### 2. What is [Project Name]?

[1-2 sentence description]

This means:
- [Key responsibility 1]
- [Key responsibility 2]
- [Key responsibility 3]

### 3. Your Responsibilities

- [What you should do automatically]
- [What you should ask about first]
- [What you should never do]

---

## Current State

### What's Working
- ✅ [Feature/component]

### Recent Work (Last Session)
- [Summary]

### Pending Tasks
- [ ] [Task]

### Known Issues
- [Issue]

---

## Project Structure

```
[Directory tree]
```

---

## Key Commands

```bash
[Essential commands]
```

---

## Important Documents

- [Link] - [Description]

---

## Context from Previous Sessions

### Session Summary (Most Recent)
[What happened last time]

### User Preferences
[Communication style, preferences, pet peeves]

---

**Last updated:** [Date] (automated by [tool])
```

---

## Automation

### Auto-Update on Each Session

**At end of session:**
```python
def update_project_resume(session_summary: str):
    resume = load_project_resume()

    # Move current "Recent Work" to history
    resume['history'].append(resume['recent_work'])

    # Update with new session summary
    resume['recent_work'] = session_summary

    # Update timestamp
    resume['last_updated'] = datetime.now()

    save_project_resume(resume)
```

**DEIA does this automatically** with `ConversationLogger`.

---

## Examples

### Example 1: Web App Project
```markdown
# MyWebApp - Project Resume

## For AI Assistants

You're working on a React/Node.js web app. Before starting:

1. Check if you have "MyWebApp" memory set up
2. If not, read `.ai/preferences.md`
3. Check recent session logs in `.ai/sessions/`

### Your Responsibilities
- Follow test-driven development (write tests first)
- Never commit directly to main (always use feature branches)
- Ask before making breaking changes

## Current State

### What's Working
- ✅ User authentication
- ✅ Dashboard UI
- ✅ API endpoints

### Pending
- [ ] Email notifications
- [ ] Admin panel

### Known Issues
- Database connection pools under load

## Key Commands
```bash
npm run dev         # Start dev server
npm test            # Run tests
npm run deploy:staging  # Deploy to staging
```

## User Preferences
- Prefers TypeScript strict mode
- Wants code review before deployment
- Communication style: Direct and concise
```

---

## Benefits

### For Users
- AI understands project immediately
- Less repetition of context
- Consistent behavior across sessions
- Better continuity

### For AI Assistants
- Clear starting point every session
- Know what's expected
- Avoid repeating mistakes
- Build on previous work

### For Teams
- Onboarding documentation doubles as AI context
- Single source of truth for project state
- Reduces bus factor (what if key person leaves)

---

## Anti-Patterns

### ❌ Too Long
```markdown
# Project Resume (10,000 words)

[Wall of text about every detail]
```
**Problem:** AI won't read it all, defeats purpose of quick orientation.

**Fix:** Keep it under 500 lines. Link to detailed docs.

---

### ❌ Never Updated
```markdown
## Recent Work (Last Session)
- Added user login (2023-05-01)

[It's now 2025]
```
**Problem:** Stale information is worse than no information.

**Fix:** Automate updates or delete outdated sections.

---

### ❌ No Actionable Instructions
```markdown
## For AI Assistants

This is a cool project. Good luck!
```
**Problem:** Doesn't help AI know what to do.

**Fix:** Be specific about responsibilities and procedures.

---

## Related Patterns

- [Clarifying Questions Policy](./clarifying-questions-policy.md) - How to handle ambiguous responses
- [Memory Hierarchy](./memory-hierarchy.md) - Different levels of AI memory/preferences
- [Session Logging](./session-logging.md) - Capturing conversation context

---

## Testing

**How to test if it works:**

1. Start a new session (or fresh AI instance)
2. First message: "What do you know about this project?"
3. Check if AI mentions reading project_resume.md
4. Verify AI knows:
   - Project purpose
   - Where to find preferences
   - Current state
   - Key responsibilities

If AI doesn't know these things, either:
- The resume isn't being read (location issue)
- The AI doesn't have it in memory/preferences
- The resume isn't clear enough

---

## Attribution

- **Pattern formalized:** 2025-10-07
- **Created by:** Dave (@dave-atx) (DEIA project)
- **Context:** Solving context loss between Claude Code sessions
- **Quote:** "hey claude, check memory to see if there's anything you need to know, and if there aren't any memory settings, since you don't retain everything we want you to, here's your reminder that this is a deia project and you need to be on your toes"

---

## License

CC BY-SA 4.0 - Share, adapt, attribute
