# TASK: Integrate Agent BC Phase 3 Components

**From:** CLAUDE-CODE-001 (Left Brain Coordinator)
**To:** CLAUDE-CODE-005 (Full-Stack Generalist)
**Date:** 2025-10-18 1145 CDT
**Priority:** P2 - MEDIUM (After BUG-004 fix)
**Estimated:** 3-4 hours
**Managed Through:** Web AI Coordination (Agent BC via Claude.ai)

---

## Context

**Agent BC Background:**
- External agent working through Claude.ai (web interface)
- Created 18 components for Chat Phase 1 + BOK systems
- **Phase 1 & 2:** Already integrated by AGENT-003 (2025-10-17)
- **Phase 3:** 3 new components waiting in intake folder

**Your Role:** Integrate Phase 3 components and prepare for future Agent BC deliveries.

---

## What Agent BC Built (Phase 3)

**Location:** `.deia/intake/2025-10-17/agent-bc-phase3/`

**3 Components:**

1. **BOK Pattern Validator**
   - README: `2025-10-17-claude-ai-bok-pattern-validator.txt`
   - Code: `2025-10-17-claude-ai-bok-pattern-validator-code.txt`
   - Purpose: Validate BOK pattern submissions before acceptance
   - Features: Link checking, frontmatter validation, format verification

2. **Health Check System**
   - File: `2025-10-17-claude-ai-health-check-system.txt`
   - Purpose: Monitor agent/service health
   - Features: Heartbeat monitoring, status reporting

3. **(Potential additional components)**
   - Check Downloads folder for: Web Dashboard, Advanced Query Router, Session Logger, Enhanced BOK Search

---

## Your Mission

### Part 1: Integrate Phase 3 Components (2-3 hours)

**Step 1: Review & Convert (30 min)**

```bash
# 1. Review the 3 Phase 3 files
cat .deia/intake/2025-10-17/agent-bc-phase3/*.txt

# 2. Convert .txt to proper Python files
# BOK Validator
cp .deia/intake/2025-10-17/agent-bc-phase3/2025-10-17-claude-ai-bok-pattern-validator-code.txt \
   src/deia/tools/bok_pattern_validator.py

# Health Check
cp .deia/intake/2025-10-17/agent-bc-phase3/2025-10-17-claude-ai-health-check-system.txt \
   src/deia/services/health_check.py
```

**Step 2: Fix & Test (1-2 hours)**

For each component:
1. Fix import statements
2. Add type hints if missing
3. Fix any bugs (use Bug Fix Lookup Protocol!)
4. Write tests (unit tests for each)
5. Verify integration

**Test Requirements:**
- BOK Validator: 10-15 tests
- Health Check: 8-10 tests
- All tests must pass
- Coverage: >80% for each component

**Step 3: Document (30 min)**

Create/update documentation:
- `docs/tools/BOK-PATTERN-VALIDATOR.md` - Usage guide
- `docs/services/HEALTH-CHECK-SYSTEM.md` - Service guide
- Update `README.md` if user-facing
- Add to ACCOMPLISHMENTS.md

---

### Part 2: Search for Additional Components (30 min)

**Agent BC may have created more components.** Search for them:

```bash
# Check Downloads folder (if accessible)
find ~/Downloads -name "*bok*" -o -name "*dashboard*" -o -name "*query*" -o -name "*session*" 2>/dev/null

# Check for web dashboard code
grep -r "dashboard\|web.*interface" ~/Downloads 2>/dev/null

# Look for these specific Phase 3 components mentioned in manifest:
# - Task 9: Web Dashboard
# - Task 10: Advanced Query Router
# - Task 13: Session Logger
# - Task 15: Enhanced BOK Search
```

**If found:**
- Copy to `.deia/intake/2025-10-17/agent-bc-phase3/`
- Add to manifest
- Integrate following same process

---

### Part 3: Prepare for Future Agent BC Work (30 min)

**Create coordination protocol for Agent BC deliveries:**

**File:** `.deia/protocols/AGENT-BC-INTEGRATION-PROTOCOL.md`

```markdown
# Agent BC Integration Protocol

## Background

Agent BC works through Claude.ai (web interface), creating components that are delivered via Downloads folder.

## Delivery Process

1. **Agent BC creates component** (via Claude.ai)
2. **User downloads to ~/Downloads/**
3. **DEIA agent copies to .deia/intake/YYYY-MM-DD/agent-bc-phaseX/**
4. **Integration agent processes** (convert .txt → .py, fix, test, integrate)

## Integration Checklist

For each Agent BC component:

- [ ] Copy from Downloads to intake folder
- [ ] Convert .txt → proper file format (.py, .md, .yaml)
- [ ] Fix imports and dependencies
- [ ] Run Bug Fix Lookup Protocol for any bugs
- [ ] Write tests (>80% coverage)
- [ ] Document in docs/
- [ ] Add to ACCOMPLISHMENTS.md
- [ ] Update BACKLOG.md
- [ ] Update PROJECT-STATUS.csv
- [ ] SYNC to AGENT-001

## File Naming

Agent BC uses pattern: `YYYY-MM-DD-claude-ai-component-name.txt`

Integration agent renames to proper format:
- Code: `src/deia/{services|tools}/component_name.py`
- Tests: `tests/unit/test_component_name.py`
- Docs: `docs/{services|tools}/COMPONENT-NAME.md`

## Quality Standards

- All Agent BC code must be reviewed for bugs
- Tests required before integration
- Documentation required for user-facing features
- Follow existing project structure

## Coordination

- Agent BC works asynchronously (web AI)
- Deliveries arrive in batches
- Integration happens when DEIA agents available
- AGENT-001 coordinates priorities
```

---

## Deliverables

**Phase 3 Integration:**
- [ ] `src/deia/tools/bok_pattern_validator.py` (converted from .txt)
- [ ] `src/deia/services/health_check.py` (converted from .txt)
- [ ] `tests/unit/test_bok_pattern_validator.py` (10-15 tests)
- [ ] `tests/unit/test_health_check.py` (8-10 tests)
- [ ] `docs/tools/BOK-PATTERN-VALIDATOR.md` (usage guide)
- [ ] `docs/services/HEALTH-CHECK-SYSTEM.md` (service guide)
- [ ] All tests passing

**Coordination Protocol:**
- [ ] `.deia/protocols/AGENT-BC-INTEGRATION-PROTOCOL.md` (new protocol)
- [ ] Update `.deia/intake/2025-10-17/MANIFEST.md` (mark Phase 3 integrated)

**Integration Protocol:**
- [ ] Update `.deia/ACCOMPLISHMENTS.md`
- [ ] Update `BACKLOG.md`
- [ ] Update `PROJECT-STATUS.csv`
- [ ] Log to `.deia/bot-logs/CLAUDE-CODE-005-activity.jsonl`
- [ ] SYNC to AGENT-001 when complete

---

## Success Criteria

**Integration complete when:**
- ✅ All 3 Phase 3 components converted to proper files
- ✅ All tests written and passing (>80% coverage each)
- ✅ Documentation created for each component
- ✅ Agent BC coordination protocol documented
- ✅ Integration Protocol checklist complete

**Ready for future Agent BC work when:**
- ✅ Protocol exists for handling deliveries
- ✅ Intake folder structure documented
- ✅ Integration process clear

---

## Task Priority

**Complete these in order:**

1. **FIRST:** Fix BUG-004 (safe_print unicode) - 30 min task
2. **THEN:** Agent BC Phase 3 Integration - 3-4 hours

Total time: 3.5-4.5 hours

---

## Notes on Agent BC Coordination

**Agent BC works through:**
- Platform: Claude.ai (web interface)
- Delivery: Downloads folder
- Format: .txt files with code/documentation
- Managed by: User (daaaave-atx)
- Integrated by: DEIA agents (AGENT-003 did Phase 1+2, you do Phase 3)

**Why this matters:**
- Agent BC is external (not Claude Code)
- Asynchronous delivery (batches via Downloads)
- Requires conversion (.txt → .py)
- May have bugs (always review)
- Good work but needs integration

**Your role:**
- Convert Agent BC deliveries to production code
- Fix bugs, add tests, document
- Prepare for future deliveries
- Create sustainable integration process

---

## Timeline

**Estimated Breakdown:**
- BUG-004 fix: 30 min (priority task)
- Phase 3 review & convert: 30 min
- Fix, test, integrate: 1-2 hours
- Documentation: 30 min
- Coordination protocol: 30 min
- Integration Protocol: 15 min
- **Total: 3.5-4.5 hours**

---

## Critical Files

**Intake folder:**
```
.deia/intake/2025-10-17/agent-bc-phase3/
├── 2025-10-17-claude-ai-bok-pattern-validator.txt
├── 2025-10-17-claude-ai-bok-pattern-validator-code.txt
└── 2025-10-17-claude-ai-health-check-system.txt
```

**Target locations:**
```
src/deia/tools/bok_pattern_validator.py
src/deia/services/health_check.py
tests/unit/test_bok_pattern_validator.py
tests/unit/test_health_check.py
docs/tools/BOK-PATTERN-VALIDATOR.md
docs/services/HEALTH-CHECK-SYSTEM.md
```

---

**This completes Agent BC's Phase 3 work and prepares for future collaboration.**

**AGENT-001 awaiting your integration completion report.**
