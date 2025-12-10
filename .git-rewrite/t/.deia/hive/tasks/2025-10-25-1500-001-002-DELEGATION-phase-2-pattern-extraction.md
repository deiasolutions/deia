# DELEGATION: Phase 2 - Pattern Extraction CLI (Bee 002)

**From:** 001 (Bee 001 - Scrum Master & Developer)
**To:** 002 (Bee 002)
**Date:** 2025-10-25 1500 CDT
**Queen Approved:** 000 (Q33N)
**Sprint:** Phase 2 - Automated Pattern Extraction
**Mode:** Full Delegation

---

## Context

**Phase 1 is COMPLETE.** DEIA is now installable, loggable, and tested (38% coverage).

**Phase 2 Priority:** Build automated pattern extraction so users can do `deia extract <session-file>` and get a clean, sanitized pattern ready to submit to BOK.

**Your Role:** Build the pattern extraction CLI end-to-end.

---

## Your Mission

**Build `deia extract` command** that transforms raw session logs into BOK-ready patterns.

**Input:** Raw conversation log (`.deia/sessions/session-XXXX.md`)
**Output:** Clean pattern file ready for BOK submission (sanitized, templated, validated)

---

## Phase 2 Tasks (Priority Order)

### Task 1: Pattern Extraction Engine (2-3 hours)
**What:** Core extraction logic that parses session logs and pulls out reusable patterns

**Deliverable:** `src/deia/tools/pattern_extractor.py`

**Capabilities:**
- Parse session log format
- Identify pattern boundaries (problem → solution → learning)
- Extract key insights
- Handle multi-turn conversations
- Support multiple pattern types (bug fix, architecture decision, workflow tip, error recovery)

**Success Criteria:**
- Can extract at least 3 different pattern types
- Handles real session data
- Tests pass (60%+ coverage)

---

### Task 2: Sanitization Engine (1.5-2 hours)
**What:** Remove PII, secrets, proprietary info while keeping pattern useful

**Deliverable:** `src/deia/tools/pattern_sanitizer.py`

**Detections:**
- PII: Names, emails, phone numbers, addresses
- Secrets: API keys, tokens, credentials
- Proprietary: Internal project names, company specifics
- Personal: Identifiable circumstances
- Paths: System/project-specific file paths

**Replacement Strategy:**
- `{NAME}` for person names
- `{COMPANY}` for company names
- `{PROJECT}` for project/repo names
- `{PATH}` for file paths
- `[REDACTED]` for secrets
- `{SERVICE}` for third-party services

**Success Criteria:**
- Detects 95%+ of PII/secrets
- Replacements are readable
- Pattern still makes sense after sanitization
- Tests pass (70%+ coverage)

---

### Task 3: Pattern Templates (1 hour)
**What:** Apply BOK formatting template to extracted + sanitized content

**Deliverable:** `src/deia/tools/pattern_templates.py`

**Template Fields:**
```markdown
# Pattern: {title}

**Contributor:** {user}
**Date:** {date}
**Type:** {pattern_type}
**Tags:** {tags}
**Urgency:** {low|medium|high}

## Problem
{describe the problem}

## Solution
{describe what worked}

## Why It Works
{explain the reasoning}

## When to Use It
{list conditions}

## Gotchas
{edge cases, caveats}

## Related Patterns
{links to similar patterns}
```

**Success Criteria:**
- Formats extracted pattern cleanly
- All fields populated from source
- Validates against BOK schema
- Tests pass (80%+ coverage)

---

### Task 4: Validation Layer (1.5 hours)
**What:** Check pattern before submission (quality gates)

**Deliverable:** `src/deia/tools/pattern_validator.py`

**Validation Rules:**
- [ ] Minimum word count (problem + solution + reasoning)
- [ ] No PII/secrets remain (re-scan)
- [ ] Valid pattern type selected
- [ ] Tags are from approved taxonomy
- [ ] Problem + solution both present
- [ ] "Why It Works" explains the reasoning
- [ ] Pattern is generalized (not project-specific)

**Output:** Pass/Fail + detailed feedback

**Success Criteria:**
- Catches 90%+ of submission issues
- Provides actionable feedback
- Tests pass (85%+ coverage)

---

### Task 5: Diff Tool (1.5 hours)
**What:** Review what's being submitted before committing

**Deliverable:** `src/deia/tools/pattern_differ.py`

**Capabilities:**
- Show original vs sanitized side-by-side
- Highlight redactions/replacements
- Show before/after of template formatting
- Prompt user to approve each change
- Generate diff report

**Success Criteria:**
- Clear visual output
- User can approve/reject changes
- Diff is accurate
- Tests pass (75%+ coverage)

---

### Task 6: CLI Integration (1 hour)
**What:** Wire everything into `deia extract` command

**Deliverable:** `src/deia/cli/extract.py` (new command)

**Usage:**
```bash
deia extract /path/to/session.md
# → runs extractor → sanitizer → template → validator → differ
# → prompts user to approve
# → generates bok/patterns/PATTERN-NAME.md
```

**Workflow:**
1. User picks session file
2. System extracts pattern
3. Shows before/after diff
4. User reviews and approves
5. Writes to `bok/patterns/{category}/{name}.md`
6. User can commit to git

**Success Criteria:**
- End-to-end workflow works
- Error handling for edge cases
- Tests pass (60%+ coverage)

---

## Success Criteria for All Tasks

**Functional:**
- Can extract pattern from real session log ✓
- Sanitization removes PII/secrets ✓
- Pattern is BOK-formatted and ready ✓
- Validation catches issues ✓
- Diff tool shows changes clearly ✓
- CLI is user-friendly ✓

**Quality:**
- Tests: 70%+ coverage across all modules
- No unhandled exceptions
- Clear error messages
- Documentation for each module

**Integration:**
- Works with existing deia CLI
- Integrates with BOK index
- Can submit pattern to git workflow

---

## What You'll Deliver

**By EOD today or tomorrow morning:**
- [ ] Pattern extraction engine (`pattern_extractor.py`)
- [ ] Sanitization engine (`pattern_sanitizer.py`)
- [ ] Pattern templates (`pattern_templates.py`)
- [ ] Validation layer (`pattern_validator.py`)
- [ ] Diff tool (`pattern_differ.py`)
- [ ] CLI integration (`src/deia/cli/extract.py`)
- [ ] Tests for all (70%+ coverage)
- [ ] Documentation in `docs/pattern-extraction.md`

**Estimated Effort:** 8-12 hours total

---

## Reporting

**Daily standup:**
- File: `.deia/hive/responses/deiasolutions/bee-002-phase-2-status.md`
- Include: Tasks completed, blockers, ETA adjustments

**Completion:**
- File: `.deia/hive/responses/deiasolutions/bee-002-phase-2-complete.md`
- Include: All deliverables, test coverage, integration verification

---

## If You Get Stuck

Post questions here: `.deia/hive/responses/deiasolutions/bee-002-questions.md`

I (Bee 001) will respond within 2 hours during business hours.

**Queen (Bee 000) escalation:** If blocked on design decisions or unclear requirements, I'll escalate to Q33N for guidance.

---

## You've Got This

This is the path from "we have sessions" to "we have patterns" to "we have a knowledge base."

You're building the extraction engine. Make it clean, make it safe, make it usable.

---

**001 out. Bee 002 owns Phase 2 pattern extraction. GO.**
