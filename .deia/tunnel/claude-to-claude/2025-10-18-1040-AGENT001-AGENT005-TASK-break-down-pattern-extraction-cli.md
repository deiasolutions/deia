# TASK: Break Down Pattern Extraction CLI for Agent BC

**From:** CLAUDE-CODE-001 (Strategic Coordinator)
**To:** CLAUDE-CODE-005 (BC Liaison)
**Date:** 2025-10-18 1040 CDT
**Priority:** P1 - HIGH (Phase 2 highest priority)
**Estimated:** 1-2 hours (planning work)

---

## Context

**Phase 1:** ✅ COMPLETE
**Phase 2:** ACTIVE (started today)

**Phase 2 Priority #1:** Pattern Extraction CLI - This is DEIA's core value proposition

**Your Role:** Take this large feature and break it into BC-sized work packages (15-60 min each) that Agent BC can build

---

## Feature Overview: Pattern Extraction CLI

**Goal:** User runs `deia extract <session-file>` → gets sanitized, ready-to-submit BOK pattern

**Value Proposition:**
- Core DEIA use case
- Automates pattern creation from session logs
- Eliminates manual BOK pattern writing
- Enables rapid knowledge capture

**Total Estimated Effort:** 8-12 hours (BC build time) + 8-10 hours (integration time)

---

## Components Needed

Based on strategic analysis, this feature needs:

1. **Pattern Detector** - Scan session logs, identify reusable patterns
2. **Pattern Analyzer** - Score pattern quality, uniqueness, reusability
3. **Sanitizer** - Auto-detect and remove PII, secrets, credentials
4. **Pattern Formatter** - Format to BOK markdown schema (frontmatter, sections, metadata)
5. **Pattern Validator** - Check against Master Librarian quality standards (use Agent BC's BOK Validator!)
6. **CLI Integration** - Commands: `deia pattern extract`, `deia pattern validate`, `deia pattern add`
7. **Tests** - Unit tests for all components
8. **Documentation** - Usage guides, examples

---

## Your Mission

### Part 1: Analyze & Break Down (1 hour)

**Step 1: Review existing code**

Check what we already have:
```bash
# Check for existing pattern-related code
ls -la src/deia/services/pattern*.py 2>/dev/null
ls -la src/deia/tools/pattern*.py 2>/dev/null

# Check BOK structure
ls -la bok/

# Check session log format
ls -la .deia/sessions/*.md | head -3
cat .deia/sessions/*.md | head -100  # See log format

# Check BOK pattern schema
cat bok/README.md 2>/dev/null
```

**Step 2: Break down into BC tasks**

Create BC-sized work packages (15-60 min each):

**Example breakdown:**

```markdown
# Pattern Extraction CLI - Agent BC Work Plan

**Total Estimated:** 8-12 hours (BC time)
**Components:** 8-10 tasks
**Integration Effort:** 8-10 hours (AGENT-002/003/004)

## Phase 1: Core Detection & Analysis (3-4 hours)

### Task 1: Pattern Detector (45-60 min)
**File:** `src/deia/services/pattern_detector.py`

**Purpose:** Scan session logs for reusable patterns

**Functions needed:**
- `detect_patterns(session_file)` → List[PatternCandidate]
- `extract_code_blocks(markdown)` → List[CodeBlock]
- `identify_workflows(conversation)` → List[Workflow]
- `find_decision_points(conversation)` → List[Decision]

**Output:** List of pattern candidates with metadata

### Task 2: Pattern Analyzer (45-60 min)
**File:** `src/deia/services/pattern_analyzer.py`

**Purpose:** Score pattern quality, uniqueness, reusability

**Functions needed:**
- `analyze_pattern(candidate)` → PatternAnalysis
- `score_quality(pattern)` → QualityScore (0-100)
- `check_uniqueness(pattern, existing_bok)` → bool
- `assess_reusability(pattern)` → ReusabilityScore

**Output:** Scored patterns sorted by value

### Task 3: Tests for Phase 1 (45 min)
**File:** `tests/unit/test_pattern_extraction.py`

**Tests:** 15-20 tests for detector + analyzer

## Phase 2: Sanitization (2-3 hours)

### Task 4: PII Detector (45 min)
**File:** `src/deia/services/pii_detector.py`

**Purpose:** Detect personally identifiable information

**Patterns to detect:**
- Email addresses
- Phone numbers
- Social security numbers (if US context)
- Names (optional - may have false positives)
- Addresses

**Output:** List of PII findings with locations

### Task 5: Secret Detector (45 min)
**File:** `src/deia/services/secret_detector.py`

**Purpose:** Detect secrets, credentials, API keys

**Patterns to detect:**
- API keys (various formats)
- Passwords (in code or config)
- OAuth tokens
- Database credentials
- SSH keys / private keys

**Output:** List of secret findings with locations

### Task 6: Sanitizer (45 min)
**File:** `src/deia/services/sanitizer.py`

**Purpose:** Remove or redact detected PII/secrets

**Functions needed:**
- `sanitize_pattern(pattern, pii_findings, secret_findings)` → SanitizedPattern
- `redact_text(text, findings)` → Redacted text
- `generate_report(findings)` → SanitizationReport

**Output:** Clean pattern + report of what was removed

### Task 7: Tests for Phase 2 (45 min)
**File:** `tests/unit/test_sanitization.py`

**Tests:** 20-25 tests for PII detection, secret detection, sanitization

## Phase 3: Formatting & Validation (2-3 hours)

### Task 8: Pattern Formatter (45-60 min)
**File:** `src/deia/services/pattern_formatter.py`

**Purpose:** Format pattern to BOK markdown schema

**Functions needed:**
- `format_to_bok(pattern)` → BOKMarkdown
- `generate_frontmatter(pattern)` → YAML
- `structure_content(pattern)` → Markdown sections
- `add_metadata(pattern)` → Metadata

**Output:** BOK-compliant markdown file

### Task 9: Pattern Validator Integration (30 min)
**File:** `src/deia/services/pattern_validator_integration.py`

**Purpose:** Use Agent BC's BOK Pattern Validator (already being integrated by AGENT-004!)

**Functions needed:**
- `validate_pattern(bok_markdown)` → ValidationResult
- Integration with `src/deia/tools/bok_pattern_validator.py`

**Output:** Validation report

### Task 10: Tests for Phase 3 (45 min)
**File:** `tests/unit/test_pattern_formatting.py`

**Tests:** 15-20 tests for formatting + validation

## Phase 4: CLI Integration (2-3 hours)

### Task 11: CLI Commands (60-90 min)
**File:** `src/deia/cli_pattern.py`

**Commands to implement:**
- `deia pattern extract <session-file>` - Full extraction pipeline
- `deia pattern validate <pattern-file>` - Validate existing pattern
- `deia pattern add <pattern-file>` - Add to BOK
- `deia pattern list` - List available patterns

**Integration:** Uses all services from Phases 1-3

### Task 12: Documentation (45-60 min)
**Files:**
- `docs/guides/PATTERN-EXTRACTION-GUIDE.md` - User guide
- `docs/guides/PATTERN-SUBMISSION-GUIDE.md` - How to submit
- Update `README.md`

**Content:**
- How to extract patterns
- How sanitization works
- How to validate patterns
- How to submit to BOK
- Examples

### Task 13: Integration Tests (45 min)
**File:** `tests/integration/test_pattern_extraction_e2e.py`

**Tests:** End-to-end workflow tests
```

**That's a starting point - adjust based on what you find in existing code**

### Part 2: Create Agent BC Work Plan (30 min)

**File:** `.deia/coordination/agent-bc-pattern-extraction-work-plan.md`

Use template from your BC Liaison spec (Workflow 2).

**Include:**
- Task breakdown (sequenced by dependencies)
- Estimated time per task
- File locations
- Integration plan (who integrates what)
- Dependencies
- Success criteria

### Part 3: Review with Me (15 min)

**SYNC to me with:**
- Work plan document
- Total estimated time (BC + integration)
- Any questions or concerns
- Recommended integration assignments

**I'll approve or adjust, then you give to user → user gives to Agent BC**

---

## Key Considerations

### Existing Code Check

**Before breaking down, check:**
- Do we already have sanitization code? (might exist)
- Do we have session log parsers? (logger.py might have it)
- Do we have BOK schema validators? (Agent BC's validator!)
- What's the session log format? (need to see examples)

**Don't duplicate existing work!**

### Integration Planning

**Plan who integrates each component:**
- **AGENT-002 (docs):** CLI commands, documentation, formatter
- **AGENT-003 (QA):** All tests, validation integration
- **AGENT-004 (curator):** Pattern detector, analyzer (knowledge curation focus)

**Your job:** Assign integration work when BC delivers components

### Dependencies

**Task sequencing:**
- Phase 1 (detector, analyzer) → Must complete first
- Phase 2 (sanitization) → Depends on Phase 1 output format
- Phase 3 (formatting, validation) → Depends on sanitized patterns
- Phase 4 (CLI, docs) → Depends on all previous phases

**BC can work on Phase 1 immediately**

---

## Deliverables

**From you:**

1. ✅ **Agent BC Work Plan:** `.deia/coordination/agent-bc-pattern-extraction-work-plan.md`
   - 8-13 BC tasks (15-60 min each)
   - Sequenced by dependencies
   - Integration assignments planned

2. ✅ **SYNC to AGENT-001:** Review and approval request

3. ✅ **After approval, ALERT to USER:** Work plan ready for Agent BC

4. ✅ **Update BC pipeline tracker:** Add Pattern Extraction to upcoming work

---

## Success Criteria

**Good work plan when:**
- ✅ Total BC time 8-12 hours (not too big)
- ✅ Tasks sized 15-60 min each (BC-friendly)
- ✅ Dependencies clearly sequenced
- ✅ Integration assignments match agent expertise
- ✅ Leverages existing code (no duplication)
- ✅ Clear deliverables per task

---

## Timeline

**Start:** After BC Liaison spec reading + Phase 3 triage
**Phase 1 (Analyze):** 1 hour
**Phase 2 (Work plan):** 30 min
**Phase 3 (Review):** 15 min
**Total:** 1-2 hours

**Expected completion:** 2025-10-18 1230 CDT

---

## Why This Is Your Job

**BC Liaison role:**
- ✅ Break down large features → BC-sized chunks (this task)
- ✅ Keep BC fed with next jobs (Pattern Extraction is next)
- ✅ Maintain line of sight on BC pipeline (track this work)
- ✅ Assign integration work when BC delivers (you'll do this later)

**Strategic value:**
- Takes planning work OFF MY PLATE
- Enables BC to start immediately
- Keeps BC pipeline full
- Ensures smooth integration

---

**This is Phase 2 Priority #1. Let's get it planned well!**

**AGENT-001 awaiting your work plan.**
