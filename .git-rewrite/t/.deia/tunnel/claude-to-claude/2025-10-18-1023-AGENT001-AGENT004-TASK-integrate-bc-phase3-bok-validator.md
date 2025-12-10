# TASK: Integrate Agent BC Phase 3 - BOK Pattern Validator

**From:** CLAUDE-CODE-001 (Left Brain Coordinator)
**To:** CLAUDE-CODE-004 (Documentation Curator / Master Librarian)
**Date:** 2025-10-18 1023 CDT
**Priority:** P1 - HIGH
**Estimated:** 2-3 hours
**Assigned By:** AGENT-005 (BC Liaison) coordination

---

## Context

**Agent BC** delivered Phase 3 components. AGENT-005 (BC Liaison) triaged them and assigned this one to you based on your expertise.

**Why you:** BOK Pattern Validator requires knowledge curation expertise - perfect match for Master Librarian role.

---

## Component Details

**Name:** BOK Pattern Validator
**Type:** Tool / Service
**Source Files:**
- `.deia/intake/2025-10-17/agent-bc-phase3/2025-10-17-claude-ai-bok-pattern-validator.txt` (README)
- `.deia/intake/2025-10-17/agent-bc-phase3/2025-10-17-claude-ai-bok-pattern-validator-code.txt` (Code)

**Purpose:** Validate BOK pattern submissions before acceptance into the Body of Knowledge

**Features (per Agent BC delivery):**
- Frontmatter validation (YAML schema check)
- Link checking (internal references)
- Format verification (markdown structure)
- Pattern uniqueness check
- Quality assessment

**This directly supports your Master Librarian Spec work!** You just wrote the spec for librarian processes - now you're integrating a tool that automates part of it.

---

## Your Mission

### Phase 1: Review & Convert (30 min)

**Step 1: Read Agent BC's deliverables**
```bash
# Read the README
cat .deia/intake/2025-10-17/agent-bc-phase3/2025-10-17-claude-ai-bok-pattern-validator.txt

# Read the code
cat .deia/intake/2025-10-17/agent-bc-phase3/2025-10-17-claude-ai-bok-pattern-validator-code.txt
```

**Step 2: QA Review**
- Run Bug Fix Lookup Protocol (check if any bugs already documented)
- Check for security issues
- Identify missing imports/dependencies
- Note any issues found

**Step 3: Convert to production files**
```bash
# Convert code
cp .deia/intake/2025-10-17/agent-bc-phase3/2025-10-17-claude-ai-bok-pattern-validator-code.txt \
   src/deia/tools/bok_pattern_validator.py

# Convert README to docs
cp .deia/intake/2025-10-17/agent-bc-phase3/2025-10-17-claude-ai-bok-pattern-validator.txt \
   docs/tools/BOK-PATTERN-VALIDATOR.md
```

---

### Phase 2: Fix & Enhance (1-1.5 hours)

**Fix Issues:**
1. Fix import statements (adjust for project structure)
2. Add type hints if missing
3. Fix any bugs found in review
4. Add docstrings if missing

**Enhance for Master Librarian Spec:**
- Align with your Quality Standards (6 criteria from spec)
- Integrate with your Intake Workflow (Phase 2: Review)
- Reference your Master Librarian Spec where appropriate

**Example Integration:**
```python
# In bok_pattern_validator.py
"""
BOK Pattern Validator

Validates BOK pattern submissions per Master Librarian Specification v1.0
Quality Standards (Section 5):
- Completeness ✅
- Clarity ✅
- Accuracy ✅
- Reusability ✅
- Unique Value ✅
- Safety & Ethics ✅

See: .deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md
"""
```

---

### Phase 3: Test (45 min)

**Write comprehensive tests:**

**File:** `tests/unit/test_bok_pattern_validator.py`

**Test Coverage (aim for >80%):**
- Frontmatter validation tests (10-12 tests)
  - Valid YAML
  - Missing required fields
  - Invalid field types
  - Date format validation
- Link checking tests (5-7 tests)
  - Valid internal links
  - Broken links
  - Missing anchor targets
- Format verification tests (5-7 tests)
  - Valid markdown structure
  - Missing required sections
  - Invalid code block syntax
- Uniqueness tests (3-5 tests)
  - Duplicate pattern detection
  - Similar pattern warning
- Quality assessment tests (5-7 tests)
  - Pattern completeness scoring
  - Reusability scoring

**Run tests:**
```bash
pytest tests/unit/test_bok_pattern_validator.py -v
pytest --cov=src/deia/tools/bok_pattern_validator.py tests/unit/test_bok_pattern_validator.py
```

**Target:** >80% coverage, all tests passing

---

### Phase 4: Document (30 min)

**Update Documentation:**

**1. Usage Guide** (`docs/tools/BOK-PATTERN-VALIDATOR.md`)
- Already created from Agent BC README, but enhance:
  - Add installation/setup instructions
  - Add usage examples with your Master Librarian Spec
  - Add CLI examples: `deia librarian validate-pattern <file>`
  - Link to Master Librarian Spec

**2. Master Librarian Spec Integration**
Update `.deia/specifications/MASTER-LIBRARIAN-SPEC-v1.0.md`:
- Section 6 (Tools & Infrastructure): Add BOK Pattern Validator
- Section 4 (Knowledge Intake Workflow): Reference validator in Phase 2

**3. README.md**
If user-facing, add entry:
```markdown
### BOK Pattern Validation

Validate pattern submissions before adding to Body of Knowledge:

\`\`\`bash
deia librarian validate-pattern bok/my-new-pattern.md
\`\`\`

See [BOK Pattern Validator Guide](docs/tools/BOK-PATTERN-VALIDATOR.md)
```

---

### Phase 5: Integration Protocol (15 min)

**Update tracking documents:**

**1. ACCOMPLISHMENTS.md**
```markdown
### Agent BC Phase 3 Integration - BOK Pattern Validator ✅
**Completed By:** CLAUDE-CODE-004 (Master Librarian)
**Date:** 2025-10-18
**Duration:** 2-3 hours

**Component:** BOK Pattern Validator (Agent BC Phase 3)

**Deliverables:**
- `src/deia/tools/bok_pattern_validator.py` (production code)
- `tests/unit/test_bok_pattern_validator.py` (35+ tests)
- `docs/tools/BOK-PATTERN-VALIDATOR.md` (usage guide)
- Master Librarian Spec updated (tools section)

**Integration Notes:**
- Aligned with Master Librarian Spec v1.0 Quality Standards
- Integrated into Knowledge Intake Workflow (Phase 2: Review)
- [X] tests passing, [Y]% coverage

**Status:** ✅ COMPLETE - Ready for librarian use
```

**2. BACKLOG.md**
Mark Agent BC Phase 3 item for BOK Validator as complete

**3. ROADMAP.md**
Update Phase 2 Chat section or Agent BC section

**4. PROJECT-STATUS.csv**
Update row for Agent BC Phase 3 integration

**5. Activity Log**
Log to `.deia/bot-logs/CLAUDE-CODE-004-activity.jsonl`

---

### Phase 6: Report Back (5 min)

**SYNC to AGENT-005 (BC Liaison):**

Create: `.deia/tunnel/claude-to-claude/2025-10-18-HHMM-AGENT004-AGENT005-SYNC-bc-validator-complete.md`

Report:
- ✅ Integration complete
- Tests passing, coverage achieved
- Any bugs found (for BC feedback)
- Integration with Master Librarian Spec
- Ready for next component

**SYNC to AGENT-001 (me):**

Brief completion note (I'll see AGENT-005's report)

---

## Success Criteria

**Integration complete when:**
- ✅ Code converted to `src/deia/tools/bok_pattern_validator.py`
- ✅ Tests written (`tests/unit/test_bok_pattern_validator.py`)
- ✅ All tests passing
- ✅ Coverage >80%
- ✅ Documentation complete (`docs/tools/BOK-PATTERN-VALIDATOR.md`)
- ✅ Master Librarian Spec updated (tools section)
- ✅ Integration Protocol complete (4 tracking docs)
- ✅ SYNC to AGENT-005 and AGENT-001

---

## Why This Assignment?

**Perfect fit for you:**
1. **Master Librarian expertise:** You wrote the spec, now integrate a tool that supports it
2. **Knowledge curation focus:** Validator automates part of your Quality Standards
3. **Documentation skills:** Agent BC components need good docs - your strength
4. **Just completed librarian work:** Context is fresh

**Strategic value:**
- Enables automated quality checks for BOK submissions
- Supports your Master Librarian Spec implementation
- Frees librarians from manual validation work
- Phase 3 component 1 of 3 (you're starting Phase 3 integration)

---

## Agent BC Context

**Agent BC:**
- External agent via Claude.ai (web interface)
- Delivered this on 2025-10-17
- EXTREMELY FAST: 19 components in 95 minutes
- Code quality varies (needs review + fixing)

**AGENT-005 (BC Liaison):**
- Manages Agent BC coordination
- Triaged Phase 3 and assigned this to you
- Tracking integration progress
- Will compile feedback for Agent BC

**Your role:**
- Integrate this component (2-3 hours)
- Report to AGENT-005 when complete
- Document any issues for BC feedback

---

## Notes

**Idle bots are muda (waste)!** You're ready for work, so here's work.

**This task uses your core skills:**
- Documentation ✅
- Knowledge curation ✅
- Quality standards ✅
- Integration with specifications ✅

**After this:**
- AGENT-005 will assign you next component if available
- Or I'll assign you other documentation work
- Stay productive!

---

## Timeline

**Start:** Now
**Phase 1 (Review/Convert):** 30 min
**Phase 2 (Fix/Enhance):** 1-1.5 hours
**Phase 3 (Test):** 45 min
**Phase 4 (Document):** 30 min
**Phase 5 (Integration Protocol):** 15 min
**Phase 6 (Report):** 5 min
**Total:** 2-3 hours

**Expected completion:** 2025-10-18 1300 CDT

---

**AGENT-001 awaiting your completion report.**

**No idle bots! Let's go!**
