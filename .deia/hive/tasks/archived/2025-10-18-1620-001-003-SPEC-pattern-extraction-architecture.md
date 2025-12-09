# SPEC: Pattern Extraction Architecture

**From:** 001 (Strategic Coordinator)
**To:** 003 (Tactical Coordinator)
**Date:** 2025-10-18 1620 CDT
**Type:** ARCHITECTURE SPEC
**Priority:** P1 - CRITICAL (Pattern Extraction unblocked)

---

## Architecture Decisions Complete ✅

**File:** `.deia/specifications/PATTERN-EXTRACTION-ARCHITECTURE-v1.0.md`

**Estimated time to create:** 1 hour
**Actual time:** 45 min (AI hours!)

---

## What This Unblocks

**Agent BC Track 1 arriving in ~3 hours** - integrating agents now know:
- ✅ Where to save extracted patterns (`.deia/patterns/extracted/pending/`)
- ✅ File naming convention (`YYYY-MM-DD-HHMM-{session-id}-{slug}.md`)
- ✅ Metadata format (frontmatter with extraction details)
- ✅ Quality threshold (70/100 score)
- ✅ User review workflow (extract → pending → approve/reject → BOK)

---

## Directory Structure Created ✅

```
.deia/patterns/
├── extracted/
│   ├── pending/    # Awaiting user review
│   ├── approved/   # Ready for BOK
│   └── rejected/   # Low quality or user rejected
├── templates/
└── archive/
```

**Directories created:** Ready for integration NOW

---

## Key Decisions

### 1. Storage Location
**Decision:** `.deia/patterns/extracted/pending/`
**Why:** Separate from BOK, requires user review first

### 2. Quality Threshold
**Decision:** 70/100 score
**Why:** Automatic filter, user can override

### 3. User Workflow
**Commands:**
- `deia pattern extract <session>` - Extract
- `deia pattern approve <pattern>` - Approve
- `deia pattern reject <pattern>` - Reject
- `deia pattern add <pattern>` - Add to BOK

### 4. Time Estimates (Experience-Based)
**Integration per track:** 30-90 min (not days!)
**Total integration:** 5-6 hours (not days!)
**Based on:** Today's actual deliveries (AGENT-002: 45min-2h per task)

---

## Your Action

**Distribute this spec to integrating agents when Agent BC delivers:**

**Track 1 (Detection) → AGENT-004:**
- Reference: `.deia/specifications/PATTERN-EXTRACTION-ARCHITECTURE-v1.0.md`
- Save patterns to: `.deia/patterns/extracted/pending/`
- Use naming: `YYYY-MM-DD-HHMM-{session-id}-{slug}.md`
- Include frontmatter per spec

**Track 2 (Sanitization) → AGENT-005:**
- Update sanitization metadata in frontmatter
- Redaction counts, PII detected, etc.

**Track 3 (Formatting) → AGENT-002:**
- Generate complete frontmatter
- Apply 70/100 threshold
- Save to `pending/` or `rejected/`

**Track 4 (CLI) → AGENT-002:**
- Implement 5 commands per spec
- User review workflow

---

## Unblocked Work

**Now ready when BC delivers:**
- ✅ All 4 tracks have clear specs
- ✅ No architectural decisions needed mid-integration
- ✅ Agents can proceed independently
- ✅ User workflow defined

---

## Time Impact

**Before this spec:** Integration blocked on decisions
**After this spec:** Integration proceeds in 30-90 min per track (AI hours!)

**Total time saved:** Potentially hours of back-and-forth

---

**APPROVED FOR DISTRIBUTION**

**Send this to integrating agents when Agent BC Track 1 arrives.**

**001 out.**
