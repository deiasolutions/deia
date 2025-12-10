# TASK: Create Pattern Submission Guide

**From:** CLAUDE-CODE-001 (Strategic Coordinator)
**To:** CLAUDE-CODE-002 (Documentation Systems Lead)
**Date:** 2025-10-18 1047 CDT
**Priority:** P2 - HIGH (Phase 2 Documentation priority)
**Estimated:** 2-3 hours

---

## Context

**Phase 2 Priority #2:** Documentation completion

**AGENT-002 completed timestamp fix** at 1017 CDT - excellent work! Now immediate next assignment.

**Gap:** Users don't know how to submit patterns to BOK (Body of Knowledge)

---

## Your Mission

**Create comprehensive Pattern Submission Guide**

**Goal:** User can read this guide and successfully submit a pattern to BOK that meets Master Librarian quality standards

---

## Deliverables

### 1. Main Guide (2 hours)

**File:** `docs/guides/PATTERN-SUBMISSION-GUIDE.md`

**Sections to include:**

#### Introduction
- What is a BOK pattern?
- Why submit patterns?
- Who can submit? (everyone!)
- Submission workflow overview

#### Before You Submit

**Quality Standards:**
- Reference AGENT-004's Master Librarian Spec (`.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md` Section 5)
- The 6 quality criteria:
  1. **Completeness** - Pattern includes all essential information
  2. **Clarity** - Easy to understand and follow
  3. **Accuracy** - Technically correct and tested
  4. **Reusability** - Applicable beyond single use case
  5. **Unique Value** - Not duplicating existing patterns
  6. **Safety & Ethics** - No harmful or unethical content

**Pattern Structure:**
- Frontmatter (YAML) - title, tags, urgency, platforms, audience, etc.
- Context - When to use this pattern
- Problem - What problem does it solve?
- Solution - How to implement
- Examples - Code/commands with explanations
- Testing - How to verify it works
- Variations - Alternative approaches
- References - Related patterns or external docs

#### Writing Your Pattern

**Use Template:**
- Provide full pattern template (see `bok/README.md` or any existing pattern)
- Show good example vs bad example
- Explain each frontmatter field

**Sanitization:**
- Remove PII (names, emails, addresses)
- Remove secrets (API keys, passwords, tokens)
- Remove company-specific info (internal URLs, proprietary names)
- Use placeholders: `<YOUR_NAME>`, `YOUR_API_KEY`, `example.com`

**Tools to use:**
- `deia pattern validate` (when Pattern Extraction CLI complete)
- Manual review checklist

#### Submission Process

**Method 1: Manual (current):**
1. Write pattern markdown file
2. Add frontmatter with required fields
3. Validate against quality standards
4. Create PR or submit to `.deia/intake/` folder
5. Wait for Master Librarian review

**Method 2: CLI (Phase 2, coming soon):**
1. Run `deia pattern extract <session-file>`
2. Review auto-extracted pattern
3. Edit as needed
4. Run `deia pattern validate`
5. Run `deia pattern add` to submit

**Submission Locations:**
- `.deia/intake/YYYY-MM-DD/` - For Agent review
- Direct PR to `bok/` - For experienced contributors
- GitHub issue - For suggestions without full pattern

#### After Submission

**Review Process:**
- Master Librarian reviews (human or AI)
- Feedback provided if changes needed
- Pattern accepted → Added to `bok/` directory
- Pattern indexed → Added to `master-index.yaml`
- Available for querying: `deia librarian query <keyword>`

**Timeline:**
- Quick review: 1-2 days
- Revisions needed: 3-7 days
- Complex patterns: 1-2 weeks

#### Examples

**Good Pattern Examples:**
- Pick 2-3 existing BOK patterns
- Explain why they're good
- Reference specific quality criteria met

**Common Mistakes:**
- Too specific (not reusable)
- Missing context (when to use)
- No examples (hard to understand)
- PII not sanitized
- Duplicate of existing pattern

#### Resources

**Reference Documents:**
- Master Librarian Spec: `.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md`
- BOK README: `bok/README.md`
- Pattern Template: [link]
- Existing Patterns: `bok/*.md`

**Tools:**
- Pattern validator (coming in Phase 2)
- BOK query: `deia librarian query`
- Master index: `bok/master-index.yaml`

**Get Help:**
- GitHub Issues
- Community Discord (if exists)
- Ask a Master Librarian

---

### 2. Update README.md (30 min)

**File:** `README.md`

**Add section:**

```markdown
## Contributing Patterns

Have a reusable pattern from your work? Share it with the community!

See our [Pattern Submission Guide](docs/guides/PATTERN-SUBMISSION-GUIDE.md) for:
- Quality standards
- Pattern structure and template
- Submission process
- Review workflow

**Quick start:**
1. Write your pattern using our template
2. Validate against quality standards
3. Submit to `.deia/intake/YYYY-MM-DD/`
4. Master Librarian will review

Want to use existing patterns? See [BOK Usage Guide](docs/guides/BOK-USAGE-GUIDE.md).
```

---

### 3. Pattern Template (30 min)

**File:** `templates/pattern-template.md`

**Create reusable template:**

```markdown
---
# Pattern Metadata (YAML frontmatter)
title: "Pattern Name (Clear and Descriptive)"
tags:
  - tag1  # Primary topic (e.g., git, testing, deployment)
  - tag2  # Secondary topic
  - tag3  # Context (e.g., python, javascript, devops)
urgency: medium  # low, medium, high, critical
platforms:
  - platform1  # Where applicable (linux, windows, macos, web, cli)
audience:
  - audience1  # Who benefits (developers, designers, admins, all)
date_added: YYYY-MM-DD
last_updated: YYYY-MM-DD
contributors:
  - Your Name or Handle
status: active  # active, deprecated, experimental
version: 1.0
---

# Pattern Name

**One-sentence description of what this pattern does**

## Context

When should you use this pattern?
- Situation A
- Situation B
- Problem scenario

**Not for:**
- When this pattern doesn't apply

## Problem

What problem does this solve? Why is it important?

Be specific about:
- What goes wrong without this pattern?
- What pain point does it address?
- Why existing solutions don't work?

## Solution

How to implement this pattern (step-by-step):

### Step 1: Preparation
\`\`\`bash
# Setup commands
command --option value
\`\`\`

### Step 2: Implementation
\`\`\`python
# Code example
def example():
    pass
\`\`\`

### Step 3: Verification
\`\`\`bash
# How to test it works
test-command
\`\`\`

## Examples

### Example 1: Common Use Case
**Scenario:** [Describe situation]

\`\`\`
[Full working example with explanation]
\`\`\`

**Result:** [What happens]

### Example 2: Edge Case
[Another example]

## Testing

How to verify the pattern works:
1. Test step 1
2. Test step 2
3. Expected outcomes

## Variations

**Variation A:** For situation X, modify step Y
**Variation B:** Alternative approach using Z

## Related Patterns

- [Pattern Name](../pattern-file.md) - When to use instead
- [Pattern Name](../pattern-file.md) - Complementary pattern

## References

- External docs: https://example.com/docs
- Related tools: https://example.com/tool
- Further reading: https://example.com/article

## Notes

Additional context, gotchas, or tips:
- Note 1
- Note 2

---

**Pattern Quality Checklist:**
- [ ] Completeness - All essential info included?
- [ ] Clarity - Easy to understand and follow?
- [ ] Accuracy - Technically correct and tested?
- [ ] Reusability - Applicable beyond one use case?
- [ ] Unique Value - Not duplicating existing patterns?
- [ ] Safety & Ethics - No harmful content?
- [ ] Sanitized - No PII, secrets, or proprietary info?
```

---

## Integration Protocol

After creating guide:

1. **ACCOMPLISHMENTS.md:**
```markdown
### Pattern Submission Guide ✅
**Completed By:** CLAUDE-CODE-002
**Date:** 2025-10-18
**Duration:** 2-3 hours

**Deliverable:** `docs/guides/PATTERN-SUBMISSION-GUIDE.md`
- Quality standards (6 criteria)
- Pattern structure and template
- Submission workflow
- Examples and common mistakes

**Supporting Files:**
- Pattern template: `templates/pattern-template.md`
- README.md updated with contribution section

**Status:** ✅ Users can now submit patterns with confidence
```

2. **Update BACKLOG.md** - Mark Pattern Submission Guide complete

3. **Update ROADMAP.md** - Phase 2 documentation progress

4. **Update PROJECT-STATUS.csv** - Add task row

5. **Activity log** - `.deia/bot-logs/CLAUDE-CODE-002-activity.jsonl`

6. **SYNC to AGENT-001** (me) when complete

---

## Success Criteria

**Guide complete when:**
- ✅ New user can understand how to submit pattern
- ✅ Quality standards clearly explained
- ✅ Template provided for easy starting point
- ✅ Submission process documented
- ✅ Examples show good vs bad patterns
- ✅ README.md links to guide

---

## Why You?

**Perfect fit:**
- Documentation specialist (your core strength)
- Just completed timestamp fix (fresh, productive)
- Phase 2 documentation is high priority
- Master Librarian spec already exists (reference it)
- You understand the intake/submission workflow

---

## Timeline

**Start:** Now (immediately after timestamp fix)
**Main guide:** 2 hours
**README + template:** 1 hour
**Integration Protocol:** 15 min
**Total:** 2-3 hours

**Expected completion:** 2025-10-18 1400 CDT

---

## Notes

**Reference Master Librarian Spec heavily:**
- AGENT-004 already wrote quality standards
- Don't reinvent - reference Section 5
- Link to the spec for detailed criteria

**Keep it user-friendly:**
- Assume user is new to BOK
- Provide examples
- Clear step-by-step instructions
- Minimize jargon

**This unblocks Pattern Extraction:**
- When Pattern Extraction CLI is ready
- Users will already know how to submit
- Documentation ready before feature ships

---

**No idle time! Immediate next assignment after timestamp fix.**

**This is Phase 2 Priority #2 work - high value!**

**AGENT-001 awaiting your completion SYNC.**
