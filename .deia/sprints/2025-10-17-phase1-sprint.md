# Sprint: Phase 1 Basics (2025-10-17)

**Sprint Goal:** Fix the foundation - make DEIA installable and usable
**Priority:** P0 - CRITICAL
**Started:** 2025-10-17
**Expected Duration:** 2-3 sessions
**Status:** 🚨 ACTIVE

---

## Why This Sprint

**Problem:** We've been building advanced features (Chat Phase 2) on a broken foundation.

**Reality Check:**
- Developer CANNOT install DEIA (`pip install -e .` broken)
- Developer CANNOT verify `deia init` works
- Developer CANNOT log real conversations (no real-time capture)
- We have 11,359 lines of code with only 6% test coverage

**Decision:** STOP everything. Fix Phase 1 first.

---

## Sprint Tasks

### Task 1: Fix pip install + Installation Guide
**Assigned:** CLAUDE-CODE-002
**Priority:** P0 - CRITICAL
**Status:** Not started

**Deliverables:**
- [ ] Working `pip install -e .` from clean environment
- [ ] Fixed pyproject.toml (if needed)
- [ ] Installation test results
- [ ] Installation guide (docs/INSTALLATION.md)

**Success Criteria:**
```bash
git clone repo
cd deiasolutions
pip install -e .
deia --help  # works
```

---

### Task 2: Test Suite to 50% Coverage
**Assigned:** CLAUDE-CODE-003
**Priority:** P0 - CRITICAL
**Status:** Not started

**Current Coverage:** 6%
**Target Coverage:** 50%

**Deliverables:**
- [ ] Unit tests for core modules (cli, init, logger)
- [ ] Integration tests for workflows
- [ ] Coverage report showing 50%+
- [ ] All tests passing
- [ ] CI/CD config

**Success Criteria:**
```bash
pytest --cov=src/deia
# Shows 50%+ coverage
```

---

### Task 3: Real-Time Conversation Logging
**Assigned:** CLAUDE-CODE-004
**Priority:** P0 - CRITICAL
**Status:** Not started

**Deliverables:**
- [ ] Conversation capture mechanism
- [ ] Integration with Claude Code
- [ ] Real-time streaming to .deia/sessions/
- [ ] End-to-end test with real conversation

**Success Criteria:**
Have real Claude Code conversation → check .deia/sessions/ → log file exists with actual content

---

### Task 4: Verify & Fix deia init
**Assigned:** CLAUDE-CODE-005
**Priority:** P0 - CRITICAL
**Status:** Not started

**Deliverables:**
- [ ] Working `deia init` command
- [ ] All required directories created
- [ ] Tests proving it works
- [ ] Bug report if issues found

**Success Criteria:**
```bash
mkdir test-project
cd test-project
deia init
ls -la .deia/  # shows all required directories
```

---

## Definition of Done

**Sprint Complete When:**
1. ✅ `pip install -e .` works on clean environment
2. ✅ `deia init` creates valid .deia/ structure
3. ✅ Real-time conversation logging captures actual conversations
4. ✅ Test coverage ≥ 50%
5. ✅ Installation guide exists and is tested
6. ✅ All tests passing

**Phase 1 Success Criteria Met:**
"A developer can clone, install, and start logging sessions with real conversations"

---

## Dependencies

**None between tasks** - all can work in parallel

**Blocks:**
- Everything else (Chat Phase 2, Phase 2, etc.)

---

## Sprint Tracking

**Daily Updates:**
- Agents report progress via SYNC messages
- Coordinator (CLAUDE-CODE-001) monitors activity logs
- Blockers escalated immediately

**Completion Estimates:**
- Each task: 1 session
- Total sprint: 2-3 sessions

---

## What Happens Next

**After Sprint Complete:**
- Phase 1 success criteria met ✅
- Resume Chat Phase 2 work
- Resume advanced features
- Build on solid foundation

**Until Sprint Complete:**
- No new feature work
- No advanced features
- Foundation only

---

**Sprint Master:** CLAUDE-CODE-001 (Left Brain)
**LLH:** DEIA Project Hive
**Last Updated:** 2025-10-17T00:10:00Z
