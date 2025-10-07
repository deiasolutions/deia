# DEIA + SpecKit Integration

**Bridge conversation logging with spec-driven development.**

## Overview

The DEIA VSCode extension now integrates with [GitHub SpecKit](https://github.com/github/spec-kit) to automatically convert logged AI conversations into formal specifications and project principles.

## What This Solves

### Problem
- Conversations with AI contain valuable requirements, decisions, and architecture discussions
- This knowledge gets lost or stays buried in logs
- SpecKit needs specifications, but writing them manually is time-consuming

### Solution
- DEIA logs conversations automatically
- Extension extracts structured knowledge from logs
- One-click conversion to SpecKit specs and constitution updates

## Features

### 1. Conversation → Specification
**Command:** `DEIA: Create SpecKit Spec from Conversation`

**What it does:**
- Analyzes a DEIA conversation log
- Extracts:
  - Requirements mentioned
  - Technical decisions made
  - Architecture discussions
  - Implementation notes
- Generates a SpecKit-compatible markdown specification
- Saves to `specs/` directory

**Workflow:**
```
User has conversation with AI → DEIA logs it → User runs command →
Picks conversation log → Names spec → Spec created in specs/
```

### 2. Decisions → Constitution
**Command:** `DEIA: Add Decisions to SpecKit Constitution`

**What it does:**
- Extracts key decisions from conversation log
- Formats them as project principles
- Adds to `.specify/memory/constitution.md`
- Preserves SpecKit constitution format

**Workflow:**
```
Conversation contains decisions → Run command → Pick log →
Preview extracted principles → Confirm → Added to constitution
```

## Example Workflow

### Scenario: Building Authentication System

1. **Have conversation with AI:**
   ```
   User: I need to build authentication for my app
   AI: Let's use JWT tokens with refresh tokens...
   [Discussion about password hashing, session management, etc.]
   ```

2. **DEIA automatically logs it** (if auto-log enabled)
   - Saved to `.deia/sessions/2025-10-07_auth-discussion.md`

3. **Create specification:**
   - Run: `DEIA: Create SpecKit Spec from Conversation`
   - Select: `2025-10-07_auth-discussion.md`
   - Name: `authentication-spec`
   - Result: `specs/authentication-spec.md` created

4. **Update constitution:**
   - Run: `DEIA: Add Decisions to SpecKit Constitution`
   - Select: same conversation
   - Preview shows:
     ```markdown
     ## Project Principles (from conversation 2025-10-07)

     - Use JWT tokens for stateless authentication
     - Implement refresh token rotation for security
     - Hash passwords with bcrypt (cost factor 12)
     - Store sessions in Redis for scalability
     ```
   - Click "Add" → Constitution updated

5. **Continue with SpecKit workflow:**
   - Use `/speckit.plan` with the generated spec
   - Use `/speckit.tasks` to break down implementation
   - Constitution guides AI assistant behavior

## How It Works

### Extraction Algorithm

The extension parses DEIA log markdown structure:

```markdown
## What We Worked On
[Extracts as requirements]

## Key Decisions
- Decision 1
- Decision 2
[Extracts as decisions]

## Full Transcript
User: ...architecture discussion...
AI: ...pattern recommendation...
[Scans for architecture keywords]
```

### Output Format

**Specification:**
```markdown
# authentication-spec

**Generated from DEIA conversation log**
**Date:** 2025-10-07

---

## Requirements

Building authentication system with JWT tokens and refresh token rotation.

## Technical Decisions

- Use JWT tokens for stateless authentication
- Implement refresh token rotation
- Hash passwords with bcrypt

## Architecture Notes

- Store sessions in Redis for scalability
- Implement rate limiting on login endpoints

---

*This specification was extracted from a DEIA conversation log and may need refinement.*
```

## Requirements

1. **DEIA CLI installed and configured**
   ```bash
   pip install -e /path/to/deia
   deia init
   ```

2. **SpecKit CLI installed** (optional, for spec workflow)
   ```bash
   uv tool install github-spec-kit
   ```

3. **SpecKit initialized in project** (for constitution updates)
   ```bash
   specify init
   ```

## Benefits

### For Individual Developers
- Never lose architectural decisions
- Conversations automatically become documentation
- Spec-driven development without manual spec writing

### For Teams
- Shared constitution reflects actual decisions
- Conversation history → formal specifications
- Onboarding: new devs can read specs generated from conversations

### For Open Source
- Contributors can see decision history
- Specs stay synchronized with development
- Transparent decision-making process

## Limitations

### Current Limitations
- Extraction is keyword-based (may miss context)
- Generated specs need human review
- Works best with structured conversations
- Requires DEIA conversation logs to exist first

### Future Improvements
- AI-powered extraction (better context understanding)
- Automatic spec refinement suggestions
- Integration with `/speckit.specify` command
- Bidirectional sync (specs → DEIA knowledge base)

## Integration Points

### SpecKit → DEIA
- Specs created from conversations
- Constitution updated from decisions
- One-way flow (conversation → spec)

### Future: DEIA → SpecKit Workflow
1. User has conversation with AI
2. DEIA logs + auto-generates spec draft
3. User runs `/speckit.specify` with DEIA context
4. SpecKit plan references conversation logs
5. Full traceability: conversation → spec → plan → implementation

## Architecture

```
┌──────────────────┐
│ AI Conversation  │
└────────┬─────────┘
         │ (DEIA logs)
         ▼
┌──────────────────┐
│ .deia/sessions/  │
│ conversation.md  │
└────────┬─────────┘
         │ (Extract)
         ▼
┌──────────────────┐      ┌──────────────────┐
│ SpecExtraction   │──────│ specs/           │
│ - requirements   │      │ new-spec.md      │
│ - decisions      │      └──────────────────┘
│ - architecture   │
└────────┬─────────┘
         │ (Format)
         ▼
┌──────────────────┐
│ .specify/memory/ │
│ constitution.md  │
└──────────────────┘
```

## Commands Reference

### Create Specification
```
Command Palette → DEIA: Create SpecKit Spec from Conversation
↓
Pick conversation log
↓
Name the spec
↓
specs/[name].md created
```

### Update Constitution
```
Command Palette → DEIA: Add Decisions to SpecKit Constitution
↓
Pick conversation log
↓
Preview extracted decisions
↓
Confirm addition
↓
.specify/memory/constitution.md updated
```

## Best Practices

### 1. Structure Your Conversations
Ask AI to explicitly state decisions:
```
User: What are the key decisions we just made?
AI: We decided to:
1. Use PostgreSQL for persistence
2. Implement CQRS pattern
3. Use Redis for caching
```

### 2. Log Regularly
Enable auto-logging or manually log after important conversations.

### 3. Review Generated Specs
Always review and refine AI-generated specifications before using them.

### 4. Keep Constitution Clean
Periodically review constitution to remove outdated principles.

## Comparison: Manual vs. DEIA+SpecKit

### Manual SpecKit Workflow
1. Have conversation with AI
2. Manually write specification in markdown
3. Manually update constitution
4. Lose conversation context over time
5. **Time:** 30-60 minutes per spec

### DEIA+SpecKit Workflow
1. Have conversation with AI → auto-logged
2. Run command → spec generated
3. Run command → constitution updated
4. Full conversation preserved forever
5. **Time:** 2 minutes per spec

**10-30x faster** with better traceability.

## Related Resources

- [GitHub SpecKit](https://github.com/github/spec-kit)
- [DEIA Documentation](https://github.com/deiasolutions/deia)
- [Spec-Driven Development Blog Post](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/)

## Contributing

Have ideas for better extraction algorithms or additional SpecKit integrations? See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

**Built for humanity. Privacy-first. Community-owned.**
