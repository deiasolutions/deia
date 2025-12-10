# Pattern Extraction Architecture v1.0

**Created:** 2025-10-18 1615 CDT
**By:** CLAUDE-CODE-001 (Strategic Coordinator)
**Status:** APPROVED - Ready for integration
**Estimated Time to Implement:** 30-45 min per component

---

## Problem

Agent BC will deliver Pattern Extraction Track 1 in ~3 hours. Integrating agents need architectural decisions NOW:
- Where do extracted patterns go?
- What's the user review workflow?
- Storage format and naming?
- Auto-validation threshold?

---

## Architecture Decisions

### Decision 1: Extracted Pattern Storage

**Location:** `.deia/patterns/extracted/`

**Directory Structure:**
```
.deia/patterns/
├── extracted/           # Auto-extracted patterns (pre-review)
│   ├── pending/        # Awaiting user review
│   ├── approved/       # User approved, ready for BOK
│   └── rejected/       # User rejected or low quality
├── templates/          # Pattern templates
└── archive/            # Old/superseded patterns
```

**File Naming Convention:**
```
YYYY-MM-DD-HHMM-{session-id}-{pattern-title-slug}.md

Example:
2025-10-18-1430-20251018-094705-daily-standup-for-ai-agents.md
```

**Why:**
- Separate from BOK (patterns need review first)
- Clear workflow stages (pending → approved/rejected)
- Traceable to source session
- Easy to find and manage

---

### Decision 2: User Review Workflow

**Process:**
```
1. deia pattern extract session.md
   ↓
2. Pattern saved to .deia/patterns/extracted/pending/
   ↓
3. User reviews pattern (manual step)
   ↓
4. User runs: deia pattern approve <pattern-file>
   OR: deia pattern reject <pattern-file>
   ↓
5. Approved → moved to .deia/patterns/extracted/approved/
   Rejected → moved to .deia/patterns/extracted/rejected/
   ↓
6. User runs: deia pattern add <approved-pattern>
   ↓
7. Pattern added to bok/ with proper category
```

**Commands:**
- `deia pattern extract <session>` - Extract pattern from session log
- `deia pattern list pending` - List patterns awaiting review
- `deia pattern approve <pattern>` - Approve pattern for BOK
- `deia pattern reject <pattern> --reason "..."` - Reject pattern
- `deia pattern add <pattern>` - Add approved pattern to BOK
- `deia pattern validate <pattern>` - Re-run validation

**Why:**
- Human-in-the-loop (user reviews before BOK submission)
- Clear approval/rejection workflow
- Prevents low-quality patterns in BOK
- User controls what gets published

---

### Decision 3: Auto-Validation Threshold

**Quality Score Threshold: 70/100**

**Rules:**
- Score ≥ 70: Pattern saved to `pending/` (eligible for approval)
- Score < 70: Pattern saved to `rejected/` with validation report
- User can override and approve low-scoring patterns if desired

**Validation Report Included:**
- Overall score (0-100)
- Quality breakdown (Completeness, Clarity, Accuracy, Reusability, Unique Value, Safety)
- PII/Secret detection results
- Sanitization actions taken
- Recommendations for improvement

**Why:**
- Automatic quality filter
- User can still review low-scoring patterns
- Transparent scoring (user sees validation report)
- Prevents obviously bad patterns from cluttering pending/

---

### Decision 4: Pattern Metadata

**Every extracted pattern includes frontmatter:**
```yaml
---
# BOK Standard Fields
title: Auto-generated Pattern Title
platform: Platform-Agnostic | Railway | Claude Code | etc
category: Pattern | Anti-Pattern
tags: [auto-generated, keywords]
confidence: Experimental
date: 2025-10-18

# Extraction Metadata
source_session: 20251018-094705
source_project: deiasolutions
extraction_method: deia-pattern-extract-v1
extraction_timestamp: 2025-10-18T14:30:00-05:00

# Quality Metrics
quality_score: 75
uniqueness_score: 80
reusability_score: 70
overall_score: 75

# Sanitization
pii_detected: true
pii_redacted_count: 3
secrets_detected: false
sanitization_report: See validation report below

# Review Status
review_status: pending
approved_by: null
approved_date: null
---
```

**Why:**
- Traceable to source session
- Quality metrics visible
- Sanitization transparency
- Audit trail for approvals

---

### Decision 5: Integration with BOK

**When user runs `deia pattern add <approved-pattern>`:**

1. Read pattern frontmatter
2. Determine BOK category from `platform` and `category` fields
3. Move file to appropriate BOK directory:
   - Platform-Agnostic → `bok/patterns/`
   - Platform-Specific → `bok/platforms/{platform}/`
   - Anti-Pattern → `bok/anti-patterns/`
4. Update `bok/master-index.yaml`
5. Optionally trigger `scripts/generate_bok_index.py`

**BOK Naming Convention:**
```
bok/patterns/{slug}.md
bok/platforms/{platform}/{slug}.md
bok/anti-patterns/{slug}.md
```

**Why:**
- Consistent with existing BOK structure
- Automated indexing
- Clear categorization
- No manual file moving

---

## Implementation Checklist

**For Agent BC Track 1 (Detection):**
- [x] Pattern Detector saves to `.deia/patterns/extracted/pending/`
- [x] Use file naming convention: `YYYY-MM-DD-HHMM-{session-id}-{slug}.md`
- [x] Include extraction metadata in frontmatter
- [x] Include quality scores in frontmatter

**For Agent BC Track 2 (Sanitization):**
- [x] PII Detector populates sanitization metadata
- [x] Sanitizer updates frontmatter with redaction counts
- [x] Validation report appended to pattern file

**For Agent BC Track 3 (Formatting):**
- [x] Pattern Formatter generates complete frontmatter
- [x] Quality score threshold check (70/100)
- [x] Save to `pending/` or `rejected/` based on score

**For Agent BC Track 4 (CLI):**
- [x] `deia pattern extract` - Extract from session
- [x] `deia pattern list pending` - List pending patterns
- [x] `deia pattern approve` - Move pending → approved
- [x] `deia pattern reject` - Move pending → rejected
- [x] `deia pattern add` - Add approved → BOK
- [x] `deia pattern validate` - Re-run validation

---

## Directory Setup (Immediate)

**Create directories NOW:**
```bash
mkdir -p .deia/patterns/extracted/pending
mkdir -p .deia/patterns/extracted/approved
mkdir -p .deia/patterns/extracted/rejected
mkdir -p .deia/patterns/templates
mkdir -p .deia/patterns/archive
```

**Add to `.gitignore`:**
```
# Extracted patterns (user reviews before committing)
.deia/patterns/extracted/pending/
.deia/patterns/extracted/rejected/
```

**Track in git:**
```
# Approved patterns ready for BOK
.deia/patterns/extracted/approved/
```

---

## Time Estimates (AI Hours - Experience-Based)

**Based on today's actual deliveries:**
- Pattern Detector integration: **30-45 min** (AGENT-004)
- Sanitizer integration: **45-60 min** (AGENT-005)
- Formatter integration: **60-90 min** (AGENT-002)
- CLI commands: **60-90 min** (AGENT-002)
- Tests per track: **45 min** (AGENT-003)

**Total integration time: ~5-6 hours** (not days!)

**Agent BC build time: ~10.5 hours** (per work plan)

**Calendar time with parallel tracks: This weekend through mid-next week** (~5-7 days with weekends)

---

## Success Criteria

**Architecture complete when:**
- [x] Storage locations defined
- [x] File naming convention established
- [x] User review workflow documented
- [x] Auto-validation threshold set
- [x] BOK integration path clear
- [x] CLI commands specified
- [x] Directories created

**Integration complete when:**
- [ ] User can run `deia pattern extract session.md`
- [ ] Pattern saved to `pending/` with quality score
- [ ] User can review and approve/reject
- [ ] Approved patterns move to BOK with `deia pattern add`
- [ ] All tests passing
- [ ] Documentation complete

---

## References

- Pattern Extraction Work Plan: `~/Downloads/uploads/2025-10-18-1945-AGENT_005-AGENT_BC-TASK-pattern-extraction-work-plan.md`
- BOK Structure: `bok/README.md`
- Master Index: `bok/master-index.yaml`
- Pattern Submission Guide: `docs/guides/PATTERN-SUBMISSION-GUIDE.md`

---

**APPROVED FOR IMPLEMENTATION**

**Next Step:** Create directories, send to AGENT-003 for distribution to integrating agents

**001 out.**
