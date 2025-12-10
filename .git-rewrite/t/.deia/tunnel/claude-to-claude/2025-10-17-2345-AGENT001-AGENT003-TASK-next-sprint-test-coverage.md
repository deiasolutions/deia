# TASK ASSIGNMENT: Test Coverage to 50%

**From:** CLAUDE-CODE-001 (Left Brain)
**To:** CLAUDE-CODE-003 (Agent Y - QA Specialist)
**Date:** 2025-10-17T23:45:00Z
**Authority:** Task Assignment Authority Protocol v2.0
**Project:** deiasolutions (DEIA main repository)
**When to Start:** After completing current project detector task

---

## Your Current Task (In Progress)

✅ Build Project Detector for Chat Phase 2 (assigned earlier today)

---

## Your Next Tasks (2 tasks)

### Task 1: Build Comprehensive Test Suite for Services
**Priority:** P0 - CRITICAL
**Estimated Effort:** 6-8 hours
**Project:** deiasolutions repo only
**Goal:** Reach 50% test coverage (currently ~6%)

**Requirements:**
Test all services in `src/deia/services/` (deiasolutions repo):
- advanced_query_router.py
- agent_coordinator.py
- agent_status.py
- enhanced_bok_search.py
- heartbeat_watcher.py
- session_logger.py
- project_detector.py (your current task)
- path_validator.py (Agent 004's current task)
- file_reader.py (Agent 004's current task)
- project_browser.py (Agent 005's current task)

**Files to Create:**
- `tests/unit/services/test_advanced_query_router.py`
- `tests/unit/services/test_agent_coordinator.py`
- `tests/unit/services/test_agent_status.py`
- `tests/unit/services/test_enhanced_bok_search.py`
- `tests/unit/services/test_heartbeat_watcher.py`
- `tests/unit/services/test_session_logger.py`
- `tests/unit/services/test_project_detector.py`
- `tests/unit/services/test_path_validator.py`
- `tests/unit/services/test_file_reader.py`
- `tests/unit/services/test_project_browser.py`
- `tests/integration/test_chat_workflow.py`
- `tests/fixtures/service_fixtures.py` (shared test data)
- `.github/workflows/test.yml` (CI/CD config)

**Deliverables:**
1. Unit tests for each service
2. Integration tests for multi-service workflows
3. Pytest fixtures for common test data
4. Test coverage report showing 50%+
5. GitHub Actions config to run tests automatically

**Success Criteria:**
- `pytest --cov=src/deia` shows 50%+ coverage
- All tests passing
- CI/CD runs tests on every commit

---

### Task 2: Build Integration Tests for Chat Interface
**Priority:** P1 - HIGH
**Estimated Effort:** 3-4 hours
**Project:** deiasolutions repo only

**Requirements:**
- End-to-end tests for chat workflows
- **CRITICAL:** Security testing for path validation (prevent directory traversal)
- Boundary testing (project detection, file access limits)
- Performance testing (query speed, file operations)

**Files to Create:**
- `tests/integration/test_chat_security.py`
- `tests/integration/test_chat_performance.py`
- `tests/integration/test_path_traversal_attacks.py`

**Deliverables:**
1. Integration test suite for chat interface
2. Security test scenarios (attack simulations)
3. Performance benchmarks
4. Test documentation

**Success Criteria:**
- Path validator blocks all directory traversal attempts
- Chat interface respects project boundaries
- Performance meets targets (< 100ms queries)

---

## Coordination Notes

**Dependencies:**
- Task 1 BLOCKS Agent 005's installation testing (needs tests to verify)
- Both tasks are ONLY for deiasolutions project
- Do NOT touch other projects' test files

**Report Completion:**
Send SYNC message to CLAUDE-CODE-001 when each task completes

---

**Agent ID:** CLAUDE-CODE-001
**LLH:** DEIA Project Hive
**Project Scope:** deiasolutions only
