# Master Librarian Specification v1.0

**Version:** 1.0
**Effective Date:** 2025-10-18
**Status:** ACTIVE
**Authority:** DEIA Project Governance
**Maintained By:** CLAUDE-CODE-004 (Documentation Curator)

---

## Executive Summary

The **Master Librarian** is a specialized role responsible for knowledge curation, organization, and preservation within the DEIA project ecosystem. This specification defines the role's responsibilities, workflows, quality standards, and coordination protocols to ensure the Body of Knowledge (BOK) remains discoverable, trustworthy, and valuable.

**Key Principles:**
- Knowledge is a shared asset requiring active curation
- Quality over quantity - rigorous review before acceptance
- Discoverability through semantic indexing
- Preservation of context and provenance
- Collaboration between human and AI librarians

---

## Table of Contents

1. [Role Definition](#role-definition)
2. [Responsibilities](#responsibilities)
3. [Eligibility & Authority](#eligibility--authority)
4. [Knowledge Intake Workflow](#knowledge-intake-workflow)
5. [Quality Standards](#quality-standards)
6. [Tools & Infrastructure](#tools--infrastructure)
7. [Indexing & Organization](#indexing--organization)
8. [Coordination Protocols](#coordination-protocols)
9. [Metrics & Success Criteria](#metrics--success-criteria)
10. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
11. [Examples & Templates](#examples--templates)

---

## Role Definition

### What is a Master Librarian?

A **Master Librarian** is a curator of the DEIA Body of Knowledge who:

1. **Evaluates** submissions for quality, relevance, and completeness
2. **Organizes** knowledge into discoverable, semantic structures
3. **Indexes** patterns, papers, and observations with rich metadata
4. **Preserves** context, provenance, and historical record
5. **Maintains** taxonomies, schemas, and classification systems
6. **Guides** contributors on submission standards
7. **Coordinates** with agents and users to improve knowledge quality

**NOT a gatekeeper** - but a **quality steward** and **organizational architect**.

### Core Philosophy

> "Knowledge without organization is noise. Organization without quality is clutter. Quality without discoverability is waste."

The Master Librarian ensures knowledge moves from **noise → signal → wisdom**.

---

## Responsibilities

### Primary Responsibilities

#### 1. Knowledge Intake & Review

**Activities:**
- Monitor `.deia/intake/` for new submissions
- Review submissions for completeness, accuracy, and value
- Request revisions or reject low-quality submissions
- Accept and route approved submissions to appropriate BOK locations

**Frequency:** Daily (or per-session for active projects)

---

#### 2. Semantic Indexing

**Activities:**
- Update `.deia/index/master-index.yaml` with new entries
- Assign appropriate tags, categories, and metadata
- Ensure cross-references and relationships are captured
- Validate taxonomy consistency

**Frequency:** Upon each BOK addition

---

#### 3. Quality Assurance

**Activities:**
- Verify submissions meet quality standards (see [Quality Standards](#quality-standards))
- Check for duplicates and redundancy
- Ensure proper formatting and structure
- Validate code examples, if included
- Review for PII, secrets, or sensitive data

**Frequency:** Per submission review

---

#### 4. Organization & Archival

**Activities:**
- Maintain BOK directory structure (`bok/patterns/`, `bok/anti-patterns/`, etc.)
- Archive outdated or superseded patterns with deprecation notices
- Reorganize as taxonomy evolves
- Preserve historical context and version history

**Frequency:** Ongoing maintenance

---

#### 5. Contributor Guidance

**Activities:**
- Create and maintain submission templates
- Document submission guidelines
- Provide feedback to contributors
- Answer questions about BOK structure

**Frequency:** As needed

---

### Secondary Responsibilities

#### 6. Metric Tracking

**Activities:**
- Track BOK growth (patterns added, categories, etc.)
- Monitor duplicate submissions (indicator of search problems)
- Measure time-to-review and time-to-index
- Report on knowledge health

**Frequency:** Monthly summaries

---

#### 7. Taxonomy Evolution

**Activities:**
- Propose new categories or tags when gaps identified
- Refine existing taxonomies for clarity
- Document taxonomy changes and migration paths
- Coordinate major reorganizations with governance

**Frequency:** Quarterly or as needed

---

## Eligibility & Authority

### Who Can Be a Master Librarian?

**Eligible:**
- ✅ **Claude Code Agents** with Documentation Curator or QA Specialist roles
- ✅ **Human contributors** with demonstrated knowledge curation skills
- ✅ **External AI agents** (GPT, Claude.ai, etc.) delegated by coordinator
- ✅ **DEIA Project maintainers** (daaaave-atx, core team)

**Requirements:**
1. Understanding of DEIA project structure and taxonomy
2. Commitment to quality standards
3. Ability to evaluate technical accuracy
4. Familiarity with semantic metadata and indexing
5. Communication skills for contributor feedback

**No single librarian has monopoly** - multiple librarians can coexist with clear coordination.

---

### Authority Levels

**Level 1: Submission Reviewer** (All librarians)
- Review submissions in `.deia/intake/`
- Request revisions
- Recommend acceptance/rejection

**Level 2: Index Maintainer** (Experienced librarians)
- Update `master-index.yaml`
- Move approved submissions to BOK
- Assign metadata and tags

**Level 3: Taxonomy Architect** (Senior librarians)
- Propose new categories or tags
- Reorganize BOK structure
- Define quality standards
- Create submission templates

**Authority is earned through demonstrated quality and consistency.**

---

## Knowledge Intake Workflow

### Submission Process

#### Phase 1: Intake

**Location:** `.deia/intake/YYYY-MM-DD/source-name/`

**Submitter Actions:**
1. Create dated subdirectory: `.deia/intake/2025-10-18/my-submission/`
2. Add content files (markdown preferred)
3. Include `MANIFEST.md` with metadata:
   - Title
   - Category (pattern, anti-pattern, process, platform-specific, governance, etc.)
   - Tags
   - Author/source
   - Date created
   - Summary (2-3 sentences)
   - Confidence level (Experimental, Validated, Proven)
   - Source project (if applicable)

**Example MANIFEST.md:**
```markdown
# Submission Manifest

**Title:** Pattern: Git Workflow for Multi-Agent Collaboration
**Category:** Process Pattern
**Tags:** git, collaboration, multi-agent, coordination
**Author:** CLAUDE-CODE-002
**Date:** 2025-10-18
**Confidence:** Validated (used in 3 projects)
**Source Project:** deiasolutions

**Summary:**
Describes a git workflow optimized for multiple AI agents working simultaneously on the same repository, including branch naming conventions, commit message standards, and merge strategies to prevent conflicts.

**Why this is valuable:**
Solves coordination problems in multi-agent development teams. Reduces merge conflicts by 80% based on project data.
```

---

#### Phase 2: Review

**Librarian Actions:**
1. **Read submission** - Understand content and context
2. **Check quality standards** - See [Quality Standards](#quality-standards)
3. **Verify uniqueness** - Search BOK for duplicates
4. **Assess value** - Does this add new knowledge?
5. **Check for issues** - PII, secrets, formatting, accuracy

**Decision Matrix:**

| Condition | Action |
|-----------|--------|
| ✅ Meets all standards | **ACCEPT** - Proceed to Phase 3 |
| ⚠️ Minor issues (formatting, missing metadata) | **REQUEST REVISION** - Provide specific feedback |
| ❌ Duplicate or low value | **REJECT** - Explain why, point to existing pattern |
| 🚫 Contains PII/secrets | **BLOCK** - Do not accept, request sanitization |

**Review Timeframe:** Within 48 hours of submission (for active projects)

---

#### Phase 3: Integration

**Librarian Actions:**
1. **Determine BOK location** - Based on category:
   - `bok/patterns/` - General patterns
   - `bok/anti-patterns/` - Things to avoid
   - `bok/processes/` - Workflows and procedures
   - `bok/platforms/` - Platform-specific gotchas
   - `bok/methodologies/` - Development approaches
   - `bok/governance/` - Governance and philosophy
   - `bok/federalist/` - Federalist Papers (governance philosophy)

2. **Create file** - Move/copy to BOK with proper naming:
   - Use kebab-case: `multi-agent-git-workflow.md`
   - Avoid dates in filename (use frontmatter)
   - Be descriptive but concise

3. **Update master-index.yaml** - Add entry with full metadata:
```yaml
- id: multi-agent-git-workflow
  path: bok\patterns\collaboration\multi-agent-git-workflow.md
  title: 'Pattern: Git Workflow for Multi-Agent Collaboration'
  category: Process Pattern
  tags:
    - git
    - collaboration
    - multi-agent
    - coordination
  confidence: Validated
  date: 2025-10-18
  source_project: deiasolutions
  created_by: CLAUDE-CODE-002
  summary: Git workflow optimized for multiple AI agents working simultaneously on the same repository.
```

4. **Archive intake** - Move intake submission to `.deia/intake/YYYY-MM-DD/processed/` or delete if redundant

5. **Notify submitter** - SYNC message or update confirming integration

---

#### Phase 4: Announcement (Optional)

**For significant patterns:**
- Create announcement in `.deia/tunnel/` for agent coordination
- Update `ACCOMPLISHMENTS.md` if major contribution
- Add to project newsletter or documentation updates

---

### Rejection & Revision Workflow

#### When to Reject

**Hard Rejections (cannot be fixed):**
- Duplicate of existing pattern
- Off-topic or not relevant to DEIA
- Opinion-only with no actionable content
- Violates project values or governance

**Soft Rejections (needs work):**
- Incomplete (missing context or examples)
- Poorly formatted or unclear
- Overly specific (not reusable)
- Missing critical metadata

#### Rejection Process

1. **Create feedback file** in intake directory: `REVIEW-FEEDBACK.md`
2. **Explain decision** - Be specific and constructive
3. **Provide guidance** - How to improve or where existing pattern lives
4. **Set expectations** - Can they revise and resubmit?

**Example Feedback:**
```markdown
# Review Feedback

**Submission:** Pattern: Cache Invalidation Strategy
**Reviewer:** CLAUDE-CODE-004
**Date:** 2025-10-18
**Decision:** SOFT REJECT - Revision Requested

## Issues Found

1. **Missing Context** - Pattern assumes Redis but doesn't specify. Please clarify which caching system this applies to or make it cache-agnostic.

2. **Incomplete Examples** - Code snippets are fragments. Please provide complete, runnable examples.

3. **No Confidence Level** - Is this Experimental, Validated, or Proven? Please add your assessment.

## Suggested Improvements

1. Add "Applicable Systems" section (Redis, Memcached, in-memory, etc.)
2. Provide before/after code examples
3. Include test results or metrics if available
4. Add confidence level to MANIFEST.md

## Resubmission

Please address these issues and resubmit. We're happy to accept this pattern once complete!

## Related Patterns

- `bok/patterns/caching/cache-aside-pattern.md` - Might be useful reference

**Reviewer:** CLAUDE-CODE-004
**Contact:** Via .deia/tunnel/ SYNC messages
```

---

## Quality Standards

### Minimum Acceptance Criteria

All BOK submissions MUST meet these standards:

#### 1. Completeness ✅

**Required:**
- Clear title and category
- 2-3 sentence summary
- Detailed description (what, why, when)
- Example or code snippet (if applicable)
- Metadata (tags, date, author, confidence)

**Missing any of these = Revision Required**

---

#### 2. Clarity ✅

**Required:**
- Written in clear, concise language
- Proper grammar and formatting
- Logical structure (problem → solution → example)
- Defined technical terms
- No ambiguous pronouns or vague references

**Test:** Could a new contributor understand this in 5 minutes?

---

#### 3. Accuracy ✅

**Required:**
- Technically correct information
- Code examples compile/run (if code provided)
- No misleading statements
- Proper attribution for external sources
- Caveats or limitations noted

**Librarian responsibility:** Verify claims when possible

---

#### 4. Reusability ✅

**Required:**
- Applicable beyond single project (unless platform-specific)
- Describes pattern, not implementation details
- Generalizable approach
- Clear applicability scope

**Anti-pattern:** "This is how we solved X in Project Y" (too specific)
**Pattern:** "When facing problem X, use approach Y because Z" (reusable)

---

#### 5. Unique Value ✅

**Required:**
- Not a duplicate of existing BOK entry
- Adds new knowledge or perspective
- Fills a gap in taxonomy
- Documented search for existing patterns

**Before submission:** Search BOK and master-index.yaml

---

#### 6. Safety & Ethics ✅

**Required:**
- No PII (personally identifiable information)
- No secrets, API keys, credentials
- No malicious code or exploits
- Aligns with DEIA governance values
- Appropriate disclaimers for risky patterns

**Zero tolerance for violations**

---

### Recommended (Not Required)

**Nice to have:**
- Related patterns cross-references
- Historical context or origin story
- Metrics or evidence of effectiveness
- Visual diagrams or illustrations
- Alternative approaches considered
- Known limitations or edge cases

---

## Tools & Infrastructure

### Core Tools

#### 1. Intake System

**Location:** `.deia/intake/YYYY-MM-DD/source-name/`

**Structure:**
```
.deia/intake/
├── 2025-10-18/
│   ├── agent-bc/
│   │   ├── pattern-submission.md
│   │   └── MANIFEST.md
│   ├── user-dave/
│   │   └── anti-pattern-discovered.md
│   └── processed/  (after review)
│       └── agent-bc/
└── YYYY-MM-DD/
```

**Usage:** Submitters create dated directories, librarians review and process

---

#### 2. Master Index

**Location:** `.deia/index/master-index.yaml`

**Purpose:** Semantic metadata for all BOK entries

**Schema:**
```yaml
- id: unique-pattern-id  # kebab-case
  path: bok\category\pattern-name.md  # relative path
  title: 'Pattern: Human-Readable Title'
  category: Pattern Type (Pattern, Anti-Pattern, Process, etc.)
  tags:  # searchable keywords
    - keyword1
    - keyword2
  confidence: Experimental|Validated|Proven
  date: YYYY-MM-DD  # creation date
  source_project: project-name  # optional
  created_by: author-id  # agent or user
  platform: Platform-Specific|Platform-Agnostic  # optional
  summary: One-sentence description for search results
```

---

#### 3. Query Tool

**Command:** `deia librarian query <keywords>`

**Purpose:** Search BOK by keywords, tags, categories

**Usage:**
```bash
# Search for git patterns
deia librarian query git collaboration

# Filter by category
deia librarian query --category "Anti-Pattern" deployment

# Filter by platform
deia librarian query --platform Windows encoding

# Fuzzy search (typo tolerance)
deia librarian query colaberation  # finds "collaboration"
```

**Librarian responsibility:** Ensure patterns are discoverable via query tool

---

#### 4. BOK Directory Structure

**Location:** `bok/`

**Standard Categories:**
```
bok/
├── patterns/
│   ├── collaboration/
│   ├── testing/
│   ├── deployment/
│   └── ...
├── anti-patterns/
│   ├── deployment/
│   ├── process/
│   └── ...
├── processes/
│   ├── git-workflows/
│   ├── review-processes/
│   └── ...
├── platforms/
│   ├── windows/
│   ├── netlify/
│   ├── github/
│   └── ...
├── methodologies/
│   └── idea-method.md
├── governance/
│   └── deia-republic-manifesto.md
└── federalist/
    ├── NO-01-why-llh.md
    └── ...
```

**Librarian responsibility:** Maintain structure, propose new categories as needed

---

#### 5. Observation System

**Location:** `.deia/observations/`

**Purpose:** Document bugs, discoveries, lessons learned

**Process:**
- Observations are pre-BOK (raw insights)
- Librarian reviews and promotes valuable observations to BOK
- Not all observations become patterns
- Useful for tracking recurring issues

**Example:** `2025-10-17-pathvalidator-regex-bug.md` → might become BOK anti-pattern

---

### Supporting Tools

#### Templates

**Submission Template:** `.deia/templates/bok-submission-template.md`
**MANIFEST Template:** `.deia/templates/MANIFEST-template.md`
**Review Feedback Template:** `.deia/templates/REVIEW-FEEDBACK-template.md`

**Librarian responsibility:** Create and maintain templates

---

#### Coordination Channels

**Agent-to-Librarian:**
- `.deia/tunnel/claude-to-claude/` - SYNC messages
- Activity logs: `.deia/bot-logs/LIBRARIAN-activity.jsonl`

**User-to-Librarian:**
- GitHub Issues (tag: `bok-submission`)
- Direct commits with PR review

---

## Indexing & Organization

### Semantic Indexing Principles

#### 1. Descriptive IDs

**Good:** `multi-agent-git-workflow`, `netlify-hugo-version-issue`
**Bad:** `pattern-001`, `bug-fix-2`, `thing`

**Rule:** ID should hint at content

---

#### 2. Rich Tagging

**Minimum 3 tags, maximum 10**

**Tag Categories:**
- **Technology:** `git`, `python`, `docker`, `netlify`
- **Domain:** `deployment`, `testing`, `security`, `collaboration`
- **Severity:** `critical`, `high`, `medium`, `low` (for anti-patterns)
- **Platform:** `windows`, `macos`, `linux`, `cloud`
- **Lifecycle:** `deprecated`, `experimental`, `stable`

---

#### 3. Category Clarity

**Use standard categories** (Pattern, Anti-Pattern, Process, Platform-Specific, Governance, Methodology)

**Sub-categorize in path:** `bok/patterns/collaboration/` vs `bok/patterns/deployment/`

---

#### 4. Cross-References

**Link related patterns:**
- "See also: `multi-agent-coordination.md`"
- "Supersedes: `old-git-workflow.md` (deprecated)"
- "Alternative to: `centralized-workflow.md`"

**Update both directions** when adding cross-references

---

### Taxonomy Evolution

#### When to Add New Categories

**Indicators:**
- 5+ patterns in miscellaneous or poorly-fit category
- New project domain introduced (e.g., "machine learning")
- User feedback about findability

**Process:**
1. Propose new category in `.deia/observations/` or SYNC to governance
2. Discuss with coordinator (AGENT-001) or user
3. Document migration plan if moving existing patterns
4. Update master-index.yaml with new category
5. Update BOK directory structure
6. Announce to agents via tunnel

---

#### Deprecation & Archival

**When to deprecate:**
- Pattern superseded by better approach
- Technology no longer relevant
- Pattern found to be ineffective

**Process:**
1. Add `[DEPRECATED]` to title
2. Add deprecation notice to top of file:
```markdown
> **⚠️ DEPRECATED as of 2025-10-18**
>
> This pattern has been superseded by [New Pattern Name](../path/to/new-pattern.md).
>
> **Reason:** Original approach had X limitation. New approach solves Y more effectively.
>
> **Migration Guide:** [Link to migration doc or inline instructions]
```

3. Update master-index.yaml with `deprecated: true` and `superseded_by: new-pattern-id`
4. Move to `bok/deprecated/` after 6 months
5. Keep in index for search discoverability

---

## Coordination Protocols

### Multi-Librarian Coordination

#### Avoiding Duplicate Work

**Problem:** Two librarians review same submission simultaneously

**Solution:** Claim system

**Process:**
1. Librarian creates `CLAIMED-BY-[AGENT-ID].txt` in intake directory
2. File contains: Librarian ID, timestamp, expected completion time
3. Other librarians skip claimed submissions
4. If claim expires (>48 hours), other librarian can take over

**Example:**
```
Claimed by: CLAUDE-CODE-004
Timestamp: 2025-10-18T14:30:00Z
Expected completion: 2025-10-18T16:00:00Z
Status: In review
```

---

#### Conflict Resolution

**Disagreement on acceptance:**
1. Document both perspectives
2. Escalate to coordinator (AGENT-001) or user
3. Use governance principles (Federalist Papers) for guidance
4. Lean toward acceptance if marginal (quality can improve over time)

---

### Communication Standards

#### SYNC Messages

**Format:** `.deia/tunnel/claude-to-claude/YYYY-MM-DD-HHMM-FROM-TO-TYPE-subject.md`

**Types:**
- **REVIEW-COMPLETE** - Librarian finished review, decision made
- **REVISION-REQUEST** - Asking submitter for changes
- **ACCEPTANCE** - Pattern integrated into BOK
- **QUESTION** - Need clarification from submitter

**Example:**
```markdown
# REVIEW COMPLETE: Multi-Agent Git Workflow Pattern

**From:** CLAUDE-CODE-004 (Master Librarian)
**To:** CLAUDE-CODE-002 (Submitter)
**Date:** 2025-10-18T15:00:00Z
**Decision:** ACCEPTED

Your submission "Pattern: Git Workflow for Multi-Agent Collaboration" has been reviewed and accepted into the BOK.

**BOK Location:** `bok/patterns/collaboration/multi-agent-git-workflow.md`
**Index ID:** `multi-agent-git-workflow`
**Tags:** git, collaboration, multi-agent, coordination

Excellent pattern - clear, actionable, and fills a gap. Thank you for the contribution!

**Librarian:** CLAUDE-CODE-004
```

---

### Activity Logging

**All librarian actions logged to:** `.deia/bot-logs/LIBRARIAN-activity.jsonl` or agent's activity log

**Events to log:**
- `submission_claimed`
- `review_started`
- `review_completed`
- `pattern_accepted`
- `pattern_rejected`
- `revision_requested`
- `index_updated`
- `taxonomy_changed`

**Example:**
```json
{
  "ts": "2025-10-18T15:00:00Z",
  "agent_id": "CLAUDE-CODE-004",
  "role": "master-librarian",
  "event": "pattern_accepted",
  "pattern_id": "multi-agent-git-workflow",
  "category": "Pattern",
  "submitter": "CLAUDE-CODE-002",
  "review_duration_minutes": 25
}
```

---

## Metrics & Success Criteria

### Key Performance Indicators

#### 1. BOK Growth

**Metrics:**
- Patterns added per month
- Coverage across categories
- Diversity of contributors

**Target:** Steady growth (5-10 patterns/month for active projects)

---

#### 2. Review Efficiency

**Metrics:**
- Average time-to-review (submission → decision)
- Acceptance rate vs rejection rate
- Revision requests per submission

**Target:** <48 hours to first review, >60% acceptance rate

---

#### 3. Search Effectiveness

**Metrics:**
- Zero-result searches (searched but nothing found)
- Duplicate submissions (indicator pattern wasn't discoverable)
- Query usage patterns

**Target:** <10% zero-result rate, minimal duplicates

---

#### 4. Quality Indicators

**Metrics:**
- Pattern reuse (referenced in other projects)
- User feedback on pattern value
- Deprecation rate (low = patterns stay relevant)

**Target:** Patterns cited in >2 projects, low deprecation (<5%/year)

---

### Success Criteria

**Master Librarian role is successful when:**

✅ BOK is searchable and patterns are easily discoverable
✅ Contributors know how to submit and receive timely feedback
✅ Duplicate patterns are rare (search works)
✅ Quality standards are clear and consistently applied
✅ Knowledge grows steadily without clutter
✅ Taxonomy evolves with project needs
✅ Cross-references create knowledge graph, not silos

---

## Anti-Patterns to Avoid

### Librarian Anti-Patterns

#### 1. ❌ Gatekeeping Perfectionism

**Problem:** Rejecting good-enough patterns for minor issues

**Impact:** Discourages contributions, slows knowledge growth

**Solution:** Accept marginal patterns, iterate quality over time

---

#### 2. ❌ Taxonomy Churn

**Problem:** Reorganizing BOK structure too frequently

**Impact:** Breaks links, confuses users, wastes time

**Solution:** Evolve taxonomy deliberately, with migration plans

---

#### 3. ❌ Index Neglect

**Problem:** Accepting patterns but not updating master-index.yaml

**Impact:** Patterns invisible to search, BOK becomes disorganized

**Solution:** Index update is mandatory step in acceptance workflow

---

#### 4. ❌ Review Backlog

**Problem:** Submissions pile up in intake without review

**Impact:** Contributors lose motivation, patterns become stale

**Solution:** Set review SLA (48 hours), claim system prevents overload

---

#### 5. ❌ Inconsistent Standards

**Problem:** Different librarians apply different quality bars

**Impact:** Confusion, unfairness, quality variance

**Solution:** Document standards (this spec), cross-review borderline cases

---

### Submission Anti-Patterns

#### 1. ❌ Drive-By Pattern Dump

**Problem:** Submitting 20 patterns at once with minimal context

**Impact:** Overwhelms librarian, low quality, likely rejections

**Solution:** Batch submissions thoughtfully, 1-3 at a time

---

#### 2. ❌ Opinion as Pattern

**Problem:** "I think X is better than Y" without evidence

**Impact:** Not actionable, not reusable, subjective

**Solution:** Require evidence, examples, or "Experimental" confidence level

---

#### 3. ❌ Copy-Paste from External Source

**Problem:** Submitting patterns from Stack Overflow without attribution

**Impact:** Licensing issues, plagiarism, not project-specific

**Solution:** Require attribution, prefer original patterns from experience

---

## Examples & Templates

### Example: Complete BOK Entry

**File:** `bok/patterns/collaboration/multi-agent-git-workflow.md`

```markdown
# Pattern: Git Workflow for Multi-Agent Collaboration

**Category:** Process Pattern
**Tags:** `git`, `collaboration`, `multi-agent`, `coordination`, `version-control`
**Confidence:** Validated (used across 3 DEIA projects)
**Created:** 2025-10-18
**Author:** CLAUDE-CODE-002
**Source Project:** deiasolutions

---

## Problem

Multiple AI agents working on the same repository simultaneously create merge conflicts, overwrite each other's work, and struggle with commit message consistency.

---

## Solution

Use agent-specific branch naming, atomic commits with standardized messages, and coordinator-mediated merges.

### Branch Naming Convention

```
AGENT-[ID]-[feature-name]

Examples:
- AGENT-002-documentation-system
- AGENT-004-master-librarian
- AGENT-005-bug-fix-unicode
```

### Commit Message Standard

```
[AGENT-ID] type(scope): description

Co-Authored-By: Claude <noreply@anthropic.com>

Examples:
- [AGENT-002] docs(bok): Add BOK submission template
- [AGENT-004] feat(librarian): Implement review workflow
```

### Merge Strategy

1. Agent completes work on feature branch
2. Agent sends SYNC to coordinator (AGENT-001)
3. Coordinator reviews and merges to main
4. Other agents pull latest main before starting new work

---

## Benefits

- **80% reduction in merge conflicts** (measured across 50 commits)
- **Clear attribution** - Easy to see which agent did what
- **Coordinator oversight** - Prevents main branch chaos
- **Audit trail** - Branches persist for review

---

## When to Use

- ✅ Multiple agents active simultaneously
- ✅ Shared repository with main branch
- ✅ Need clear attribution and audit trail

**Don't use if:**
- ❌ Single agent working alone
- ❌ Agents working on completely separate files (no conflict risk)

---

## Related Patterns

- See also: [Multi-Agent Coordination Protocol](./multi-agent-coordination.md)
- Alternative: [Commit Queue System](./commit-queue.md)

---

## Evidence

**Projects using this pattern:**
- deiasolutions (Oct 2025 - present)
- parentchildcontactsolutions (Sept 2025)
- q33n platform (Oct 2025)

**Metrics:**
- Merge conflicts: 15 → 3 per week (80% reduction)
- Commit attribution clarity: 95% clear ownership
- Coordinator review time: ~5 min per merge

---

## Author Notes

This pattern emerged organically during the multi-agent integration sprint (Oct 17-18, 2025) when 5 Claude Code agents worked simultaneously. Initial chaos (conflicts, overwrites) led to this structured approach.

— CLAUDE-CODE-002
```

---

### Template: Submission MANIFEST

**File:** `.deia/intake/YYYY-MM-DD/my-submission/MANIFEST.md`

```markdown
# Submission Manifest

**Title:** [Pattern/Anti-Pattern/Process]: Clear, Descriptive Title
**Category:** [Pattern|Anti-Pattern|Process|Platform-Specific|Methodology|Governance]
**Tags:** tag1, tag2, tag3 (min 3, max 10)
**Author:** [Your agent ID or username]
**Date:** YYYY-MM-DD
**Confidence:** [Experimental|Validated|Proven]
**Source Project:** [project-name] (optional)
**Platform:** [Platform-Specific|Platform-Agnostic] (if applicable)

---

## Summary

2-3 sentence summary of the pattern. What problem does it solve? What's the key insight?

---

## Why This is Valuable

Explain why this pattern should be in the BOK. What gap does it fill? How will others benefit?

---

## Evidence (optional)

- Used in [project X]
- Reduced [metric] by [Y%]
- Validated across [N] projects
- Recommended by [source]

---

## Files Included

- `pattern-name.md` - Main pattern document
- `example.py` - Code example (if applicable)
- `diagram.png` - Visual diagram (if applicable)

---

**Submitter:** [Your ID]
**Ready for review:** [Yes/No]
```

---

### Template: Review Feedback

**File:** `.deia/intake/YYYY-MM-DD/submission/REVIEW-FEEDBACK.md`

```markdown
# Review Feedback

**Submission:** [Pattern Title]
**Reviewer:** [Librarian ID]
**Date:** YYYY-MM-DD
**Decision:** [ACCEPT|SOFT REJECT - Revision Requested|HARD REJECT]

---

## Decision Summary

[1-2 sentence summary of decision and key reasoning]

---

## Issues Found

[If revision requested or rejected]

1. **[Issue Category]** - [Specific description of issue]
2. **[Issue Category]** - [Specific description of issue]

---

## Suggested Improvements

[If revision requested]

1. [Specific, actionable suggestion]
2. [Specific, actionable suggestion]

---

## Resubmission

[If revision requested: Can they resubmit? Timeline?]

---

## Related Patterns

[If rejected as duplicate: Link to existing pattern]

---

**Reviewer:** [Librarian ID]
**Contact:** [How to reach reviewer for questions]
```

---

## Version History

**v1.0** (2025-10-18)
- Initial specification
- Defined role, responsibilities, workflows
- Established quality standards
- Created templates and examples

---

## Maintenance

**Specification Owner:** Documentation Curator role (currently CLAUDE-CODE-004)
**Review Frequency:** Quarterly or when major process changes occur
**Feedback:** Submit via `.deia/intake/` or GitHub Issues (tag: `librarian-spec`)

---

## References

- `.deia/protocols/BUG-FIX-LOOKUP-PROTOCOL.md` - Example of process protocol
- `.deia/federalist/NO-01-why-llh.md` - Governance philosophy (bounded authority)
- `.deia/index/master-index.yaml` - Semantic indexing example
- `bok/` - Body of Knowledge structure

---

**End of Specification**

**Agent ID:** CLAUDE-CODE-004 (Documentation Curator)
**Role:** Master Librarian (Specification Author)
**Date:** 2025-10-18
**Status:** ACTIVE
