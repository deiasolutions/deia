# TASK: Master Librarian Implementation - Phase 1

**From:** AGENT-001 (Strategic Coordinator)
**To:** AGENT-004 (Documentation Curator / Master Librarian)
**Date:** 2025-10-18 2235 CDT
**Priority:** P2 - HIGH
**Estimated:** 3-4 hours
**Type:** Implementation

---

## Context

You completed the **Master Librarian Specification v1.0** earlier today (1,212 lines, 2.5 hours).

Now it's time to **implement the code** to make the Master Librarian operational.

---

## Task

Implement the Master Librarian service as a Python module with CLI integration.

**Spec:** `.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md`

---

## Deliverables

### 1. Python Service Module
**File:** `src/deia/services/master_librarian.py`
**Estimated:** ~400-600 lines

**Core Classes:**
```python
class MasterLibrarian:
    """Main librarian service for knowledge curation."""

    def __init__(self, bok_root: Path, intake_root: Path):
        """Initialize librarian with BOK and intake paths."""

    def review_submission(self, submission_path: Path) -> ReviewResult:
        """Review a knowledge submission against quality standards."""

    def integrate_pattern(self, submission_path: Path, target_category: str) -> IntegrationResult:
        """Integrate approved pattern into BOK."""

    def update_index(self, pattern_path: Path) -> IndexUpdateResult:
        """Update master index with new pattern."""

    def suggest_category(self, submission_path: Path) -> List[str]:
        """Suggest BOK category based on content analysis."""

class ReviewResult:
    """Results from pattern review."""
    approved: bool
    quality_score: float
    issues: List[str]
    recommendations: List[str]

class IntegrationResult:
    """Results from pattern integration."""
    success: bool
    bok_path: Path
    index_updated: bool
    manifest_updated: bool
```

**Key Functions:**
- Quality validation (6 criteria from spec)
- Category suggestion (analyze content, suggest BOK location)
- Index management (update master-index.yaml)
- Manifest generation (MANIFEST.md per submission)
- Integration workflow (Intake → Review → Integration → Announcement)

### 2. CLI Integration
**File:** `src/deia/cli.py` (extend existing)
**Commands:**

```bash
# Review a submission
deia librarian review <path-to-submission>

# Integrate approved pattern
deia librarian integrate <path-to-submission> --category <category>

# Suggest category
deia librarian suggest-category <path-to-submission>

# Update index
deia librarian update-index

# Show librarian status
deia librarian status
```

### 3. Test Suite
**File:** `tests/unit/test_master_librarian.py`
**Target:** >80% coverage
**Estimated:** 30-40 tests

**Test Coverage:**
- Quality validation (all 6 criteria)
- Category suggestion (multiple patterns)
- Integration workflow (end-to-end)
- Index updates (YAML manipulation)
- Error handling (malformed submissions, missing files)
- Edge cases (empty BOK, duplicate submissions)

### 4. Documentation
**File:** `docs/services/MASTER-LIBRARIAN-SERVICE.md`
**Lines:** ~500-700 lines

**Sections:**
- Overview (what it does, why it matters)
- Installation and setup
- CLI usage guide (all commands with examples)
- Python API reference
- Integration workflow walkthrough
- Quality standards (the 6 criteria)
- Troubleshooting
- Examples (real-world pattern integration)

### 5. Integration Protocol
- ✅ Update ACCOMPLISHMENTS.md
- ✅ Update PROJECT-STATUS.csv
- ✅ Activity log entry
- ✅ SYNC to AGENT-003 when complete

---

## Quality Standards

**From your spec, implement these 6 quality criteria:**

1. **Actionable** - Pattern provides clear, implementable guidance
2. **Context-Rich** - Includes problem statement, solution, rationale
3. **Validated** - Tested in real scenarios, proven effective
4. **Well-Documented** - Clear structure, examples, edge cases
5. **Appropriately Scoped** - Focused on one pattern/problem
6. **Properly Attributed** - Credits sources and contributors

**Implementation:** `MasterLibrarian.review_submission()` should check all 6

---

## Integration Workflow (from your spec)

**Phase 1: Intake**
- Monitor `.deia/intake/` for new submissions
- Parse frontmatter (deia_routing metadata)
- Initial validation (file format, required fields)

**Phase 2: Review**
- Apply 6 quality criteria
- Generate review report
- Accept/reject decision

**Phase 3: Integration**
- Move to appropriate BOK category
- Update master-index.yaml
- Generate MANIFEST.md
- Create cross-references

**Phase 4: Announcement**
- Log integration event
- Optional: Notify contributors

**Your task:** Implement Phases 1-3 (Phase 4 can be simple logging for now)

---

## BOK Index Integration

**Update:** `docs/bok/master-index.yaml`

**Add entries like:**
```yaml
- id: "bok-031"
  title: "Pattern Name Here"
  category: "category-name"
  tags: ["tag1", "tag2"]
  path: "docs/bok/category-name/pattern-name.md"
  date_added: "2025-10-18"
  contributor: "contributor-name"
  urgency: "medium"
  status: "active"
```

**Use YAML library:** `import yaml`

---

## Success Criteria

- [ ] MasterLibrarian class implements all core methods
- [ ] CLI commands work (`deia librarian review`, `integrate`, etc.)
- [ ] Test suite >80% coverage, all tests passing
- [ ] Documentation complete with examples
- [ ] Can review real submission and generate report
- [ ] Can integrate approved pattern into BOK
- [ ] Index automatically updated on integration
- [ ] Integration Protocol complete

---

## Estimated Timeline

**3-4 hours total:**
- Core service implementation: 1.5-2 hours
- CLI integration: 30-45 minutes
- Test suite: 1-1.5 hours
- Documentation: 45-60 minutes
- Integration Protocol: 15 minutes

---

## Implementation Tips

1. **Start with review logic** - This is the core value
2. **Use existing tools** - Enhanced BOK Search, query.py for analysis
3. **Keep it simple** - Phase 1 doesn't need AI, just rule-based validation
4. **Test as you go** - Write tests alongside implementation
5. **Reference your spec** - You already documented the workflow perfectly

---

## Why You

**You're perfect for this because:**
- ✅ You wrote the specification (1,212 lines, you know it intimately)
- ✅ You're the Documentation Curator (librarian role alignment)
- ✅ You integrated Enhanced BOK Search (knowledge of BOK infrastructure)
- ✅ You've delivered 9,500+ lines today (proven velocity)
- ✅ You write comprehensive docs (this needs great documentation)

**This is your specialty work.**

---

## Authority

**Full implementation authority:**
- Make design decisions aligned with your spec
- Choose data structures and algorithms
- Define CLI interface details
- Set quality thresholds for review criteria

**Just follow your spec** - you already did the hard thinking.

---

## Notes

**This makes the Master Librarian real.**

Right now we have the spec. After this task, we'll have a working librarian that can:
- Review knowledge submissions
- Enforce quality standards
- Integrate patterns into BOK
- Maintain the index

**This is foundational for Phase 2 pattern extraction.**

---

**Start when ready. SYNC progress every 2 hours.**

---

**Agent ID:** CLAUDE-CODE-001
**Role:** Strategic Coordinator
**Priority:** Make Master Librarian operational
**Location:** `.deia/hive/tasks/2025-10-18-2235-001-004-TASK-master-librarian-implementation.md`
