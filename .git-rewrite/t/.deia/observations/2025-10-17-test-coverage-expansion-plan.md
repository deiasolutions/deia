# Test Coverage Expansion Plan: 6% → 50%

**Created By:** CLAUDE-CODE-003 (Agent Y / QA Specialist)
**Date:** 2025-10-17
**Current Coverage:** ~6% (3 test files for 50+ source files)
**Target Coverage:** 50% (milestone toward 80% production goal)
**Estimated Effort:** 16-20 hours total
**Priority:** HIGH - Critical for production readiness

---

## Executive Summary

**Current State:**
- **Test Files:** 12 (including conftest.py, __init__.py files)
- **Actual Test Files:** ~9 with tests
- **Source Files:** 50+ Python files in `src/deia/`
- **Estimated Coverage:** 6-10%

**Target State:**
- **Test Coverage:** 50%+ of codebase
- **Critical Components:** 100% tested
- **High-Value Components:** 70%+ tested
- **Remaining Components:** 30%+ tested

**Strategy:** Prioritize critical and high-value components first, then expand coverage systematically.

---

## Coverage Analysis

### Currently Tested Components ✅

| Component | Test File | Status | Estimated Coverage |
|-----------|-----------|--------|-------------------|
| Logger | `tests/unit/test_logger.py` | ✅ Exists | ~60% |
| Hive | `tests/unit/test_hive.py` | ✅ Exists | ~50% |
| CLI | `tests/integration/test_cli.py` | ✅ Exists | ~40% |
| Bot Queue | `tests/test_bot_queue.py` | ✅ Exists | ~50% |
| Sync | `tests/test_sync.py` | ✅ Exists | ~50% |
| Drones | `tests/test_drones.py` | ✅ Exists | ~40% |
| Messaging | `tests/test_messaging.py` | ✅ Exists | ~50% |
| Path Validator | `tests/unit/test_path_validator.py` | ✅ Exists | ~80% |
| Project Browser | `tests/unit/test_project_browser.py` | ✅ Exists | 89% |
| File Reader | `tests/unit/test_file_reader.py` | ✅ Exists | ~70% |

**Current Coverage Estimate:** ~55-60% for tested files, but only ~10-15% of total codebase

---

### Critical Components (Must Test - Priority 1)

**Definition:** Components that would break core functionality or create security risks if buggy.

| Component | File | Reason Critical | Test Priority | Est. Time |
|-----------|------|-----------------|---------------|-----------|
| AgentStatusTracker | `services/agent_status.py` | Core hive coordination, state management | **P0** | 2h |
| DEIAContextLoader | `context/deia_context_loader.py` | Security critical (path traversal), foundation for BOK | **P0** | 2h |
| AgentCoordinator | `services/agent_coordinator.py` | Routing logic, task delegation | **P0** | 2h |
| BOK Index Generator | `tools/generate_bok_index.py` | Data structure critical (P0 bug found) | **P0** | 1h |

**Subtotal:** 7 hours

---

### High-Value Components (Should Test - Priority 2)

**Definition:** User-facing or frequently-used components where bugs cause significant impact.

| Component | File | Value/Risk | Test Priority | Est. Time |
|-----------|------|------------|---------------|-----------|
| Enhanced BOK Search | `services/enhanced_bok_search.py` | Key feature, TF-IDF search | **P1** | 2h |
| ChatInterfaceApp | `services/chat_interface_app.py` | User-facing, WebSocket security | **P1** | 3h |
| Session Logger | `services/session_logger.py` | Activity tracking, metrics | **P1** | 1.5h |
| Heartbeat Watcher | `services/heartbeat_watcher.py` | Monitoring critical | **P1** | 1.5h |
| BOK Pattern Validator | `tools/bok_pattern_validator.py` | Quality gate, async operations | **P1** | 2h |
| Advanced Query Router | `services/advanced_query_router.py` | Confidence scoring | **P1** | 1.5h |
| CLI Hive Commands | `cli_hive.py` | User entry point | **P1** | 1.5h |

**Subtotal:** 13 hours

---

### Medium-Value Components (Nice to Test - Priority 3)

**Definition:** Supporting components where bugs are inconvenient but not critical.

| Component | File | Reason | Test Priority | Est. Time |
|-----------|------|--------|---------------|-----------|
| Config | `config.py` | Configuration management | **P2** | 1h |
| Installer | `installer.py` | Setup process | **P2** | 1h |
| Validator | `validator.py` | Data validation | **P2** | 1h |
| Templates | `templates.py` | Template rendering | **P2** | 1h |
| Sanitizer | `sanitizer.py` | Input sanitization | **P2** | 1h |
| CLI Utils | `cli_utils.py` | Utility functions | **P2** | 1h |
| Doctor | `doctor.py` | Diagnostics | **P2** | 1.5h |

**Subtotal:** 7.5 hours

---

## Phased Implementation Plan

### Phase 1: Critical Components (Week 1)
**Goal:** Test all P0 components
**Duration:** 7 hours
**Coverage Impact:** +15-20% overall coverage

**Tasks:**
1. ✅ **AgentStatusTracker** (2h)
   - Thread-safety tests
   - State transition logic
   - Heartbeat monitoring
   - Dashboard rendering (if implemented)

2. ✅ **DEIAContextLoader** (2h)
   - Path traversal security tests
   - BOK index loading
   - Search functionality
   - Pattern retrieval

3. ✅ **AgentCoordinator** (2h)
   - Query classification
   - Routing logic
   - Task delegation
   - Agent availability checks

4. ✅ **BOK Index Generator** (1h)
   - Dict vs array structure (P0 bug)
   - Metadata extraction
   - YAML generation
   - Nested directory handling

**Milestone:** All critical components tested, P0 bugs cannot recur

---

### Phase 2: High-Value Components (Week 2)
**Goal:** Test all P1 components
**Duration:** 13 hours
**Coverage Impact:** +20-25% overall coverage

**Tasks:**
1. ✅ **Enhanced BOK Search** (2h)
   - TF-IDF search accuracy
   - Fuzzy matching
   - Related patterns
   - Performance with large datasets

2. ✅ **ChatInterfaceApp** (3h)
   - WebSocket authentication
   - JSON error handling
   - Command parsing
   - Delegation workflow
   - File serving

3. ✅ **Session Logger** (1.5h)
   - JSONL format
   - Activity logging
   - Metrics calculation
   - File rotation

4. ✅ **Heartbeat Watcher** (1.5h)
   - Agent monitoring
   - Timeout detection
   - Auto-escalation
   - Status aggregation

5. ✅ **BOK Pattern Validator** (2h)
   - Async link checking
   - YAML validation
   - Metadata validation
   - Division by zero fixes

6. ✅ **Advanced Query Router** (1.5h)
   - Complexity scoring
   - Confidence calculation
   - Capability matching
   - Routing decisions

7. ✅ **CLI Hive Commands** (1.5h)
   - Command execution
   - Dashboard display
   - Status reporting
   - Monitor daemon

**Milestone:** All high-value components tested, user-facing features reliable

---

### Phase 3: Medium-Value Components (Week 3)
**Goal:** Reach 50% overall coverage
**Duration:** 7.5 hours (selective testing)
**Coverage Impact:** +10-15% overall coverage

**Selective Testing Strategy:**
- Test critical paths in each component (not 100% coverage)
- Focus on public APIs
- Skip internal helpers (unless complex)
- Aim for 40-50% coverage per file

**Tasks:**
1. Config (1h) - Basic loading, validation
2. Installer (1h) - Setup flow, dependency checks
3. Validator (1h) - Key validation rules
4. Templates (1h) - Rendering, variable substitution
5. Sanitizer (1h) - Input sanitization patterns
6. CLI Utils (1h) - Common utility functions
7. Doctor (1.5h) - Diagnostic checks

**Milestone:** 50% overall coverage achieved

---

## Coverage Milestones

### Milestone 1: 20% Coverage (After Phase 1)
**Target Date:** Week 1 complete
**Components:** 4 critical components tested
**Quality Gate:** All P0 components have tests

### Milestone 2: 40% Coverage (After Phase 2)
**Target Date:** Week 2 complete
**Components:** 11 high-value components tested
**Quality Gate:** All user-facing features tested

### Milestone 3: 50% Coverage (After Phase 3)
**Target Date:** Week 3 complete
**Components:** 18-20 components tested
**Quality Gate:** ROADMAP Phase 1 requirement met

### Long-Term: 80% Coverage (Production Goal)
**Target Date:** Before production deployment
**Components:** All components except utilities
**Quality Gate:** Production-ready quality

---

## Test Types and Patterns

### Unit Tests (Primary Focus)
**Location:** `tests/unit/`
**Coverage:** Individual functions/classes
**Mocking:** Heavy use of mocks for dependencies

**Example Pattern:**
```python
@pytest.fixture
def mock_dependency():
    return Mock(spec=DependencyClass)

def test_feature(mock_dependency):
    component = Component(mock_dependency)
    result = component.method()
    assert result == expected
```

### Integration Tests (Secondary)
**Location:** `tests/integration/`
**Coverage:** Component interactions
**Mocking:** Minimal mocking, real dependencies

**Example Pattern:**
```python
def test_workflow_end_to_end(tmp_path):
    # Create real components
    loader = DEIAContextLoader(tmp_path)
    coordinator = AgentCoordinator(loader)

    # Test full workflow
    result = coordinator.route_query("test")
    assert result is not None
```

### Security Tests (Critical)
**Location:** Within unit tests
**Coverage:** Path traversal, injection, auth
**Pattern:** Explicit security test cases

**Example Pattern:**
```python
def test_path_traversal_blocked():
    with pytest.raises(ValueError):
        loader.get_pattern("../../../etc/passwd")
```

---

## Testing Standards

### Coverage Requirements
- **Critical Components (P0):** 80%+ coverage
- **High-Value Components (P1):** 70%+ coverage
- **Medium-Value Components (P2):** 40%+ coverage
- **Overall Target:** 50%+ for Phase 3

### Test Quality Requirements
- ✅ All tests must pass before merge
- ✅ Tests must be deterministic (no flaky tests)
- ✅ Mocks used for external dependencies (file I/O, network)
- ✅ Edge cases explicitly tested
- ✅ Security issues have dedicated test cases
- ✅ Test names clearly describe what's being tested

### Documentation Requirements
- ✅ Docstrings for fixtures
- ✅ Comments for non-obvious test logic
- ✅ Test file header explaining component under test

---

## Tools and Infrastructure

### Existing Infrastructure ✅
- ✅ Pytest configured and working
- ✅ `tests/` directory structure established
- ✅ `conftest.py` with shared fixtures
- ✅ `tests/unit/` and `tests/integration/` directories

### Coverage Tools
```bash
# Run tests with coverage
pytest --cov=src/deia --cov-report=html --cov-report=term

# View coverage report
# Open htmlcov/index.html in browser

# Coverage for specific module
pytest --cov=src/deia/services/agent_status tests/unit/test_agent_status.py
```

### Recommended Additions
- [ ] Coverage badge in README
- [ ] Pre-commit hook to check coverage doesn't decrease
- [ ] CI/CD integration (run tests on all commits)
- [ ] Coverage report in PR comments

---

## Risk Assessment

### Risks

**1. Time Estimates May Be Low**
- Complex components may take longer than estimated
- Mitigation: Re-estimate after Phase 1, adjust plan

**2. Missing Dependencies**
- Some components may need dependencies (rapidfuzz, aiohttp)
- Mitigation: Install dependencies as needed, document in test files

**3. Code May Need Refactoring for Testability**
- Global state, tight coupling makes testing hard
- Mitigation: Refactor as needed, document changes

**4. Test Maintenance Burden**
- More tests = more maintenance when code changes
- Mitigation: Keep tests simple, avoid over-mocking

### Assumptions

- ✅ P0/P1 bug fixes already applied (from QA report)
- ✅ Test infrastructure working (pytest, fixtures)
- ✅ Components are in `src/deia/` (integrated)
- ✅ Agent 003 (me) has time allocated for testing work

---

## Success Criteria

**Phase 1 Success:**
- ✅ All 4 critical components have test files
- ✅ Each critical component has 80%+ coverage
- ✅ All tests passing
- ✅ Security tests included

**Phase 2 Success:**
- ✅ All 7 high-value components tested
- ✅ Each component has 70%+ coverage
- ✅ User-facing features validated
- ✅ Overall coverage >35%

**Phase 3 Success:**
- ✅ 50% overall coverage achieved
- ✅ ROADMAP Phase 1 requirement met
- ✅ Production readiness improved
- ✅ No regression in existing tests

**Overall Success:**
- ✅ Test suite runs fast (<2 minutes)
- ✅ Tests are maintainable
- ✅ Coverage measured and tracked
- ✅ Team confidence in code quality increased

---

## Next Steps

**Immediate (This Session):**
1. Begin Phase 1 with AgentStatusTracker tests
2. Set up coverage tracking
3. Create test file templates

**This Week:**
1. Complete Phase 1 (critical components)
2. Run coverage report
3. Adjust Phase 2 estimates based on learnings

**Next 2 Weeks:**
1. Complete Phase 2 (high-value components)
2. Begin Phase 3 (selective medium-value testing)
3. Achieve 50% coverage milestone

---

## Resource Requirements

**Time:**
- Agent 003 (me): 16-20 hours over 3 weeks
- Code review: 2-3 hours (for test quality)

**Tools:**
- pytest-cov (coverage measurement)
- pytest-mock (mocking utilities)
- Dependencies: rapidfuzz, aiohttp (if not installed)

**Documentation:**
- This plan
- Test file headers
- Coverage reports

---

## Coordination

**Dependencies:**
- Need confirmation that P0/P1 fixes are integrated
- Need access to source files in `src/deia/`
- May need coordination with Agent 005 (integration) for dependency installation

**Communication:**
- Update heartbeat when starting each phase
- Create SYNC message when milestones achieved
- Report blockers if components can't be tested

**Deliverables:**
- Test files in `tests/unit/` and `tests/integration/`
- Coverage reports (HTML + terminal)
- Summary report at each milestone

---

## Appendix: Component Inventory

### All Components in src/deia/ (50+ files)

**Core Services (11):**
- ✅ services/agent_status.py (CRITICAL - P0)
- ✅ services/agent_coordinator.py (CRITICAL - P0)
- ✅ services/enhanced_bok_search.py (HIGH - P1)
- ✅ services/advanced_query_router.py (HIGH - P1)
- ✅ services/session_logger.py (HIGH - P1)
- ✅ services/heartbeat_watcher.py (HIGH - P1)
- ✅ services/chat_interface_app.py (HIGH - P1)
- services/llm_service.py (MEDIUM - P2)
- services/deepseek_service.py (LOW - P3)
- ✅ services/messaging.py (TESTED)
- ✅ services/project_browser.py (TESTED - 89% coverage)
- services/path_validator.py (TESTED)
- services/file_reader.py (TESTED)

**Context & Tools (3):**
- ✅ context/deia_context_loader.py (CRITICAL - P0)
- ✅ tools/generate_bok_index.py (CRITICAL - P0)
- ✅ tools/bok_pattern_validator.py (HIGH - P1)
- tools/query.py (MEDIUM - P2)

**CLI (5):**
- ✅ cli_hive.py (HIGH - P1)
- cli.py (MEDIUM - P2)
- cli_log.py (MEDIUM - P2)
- cli_utils.py (MEDIUM - P2)

**Core System (10):**
- ✅ config.py (MEDIUM - P2)
- core.py (LOW - P3)
- ✅ hive.py (TESTED)
- ✅ bot_queue.py (TESTED)
- orchestrator.py (LOW - P3)
- clock.py (LOW - P3)
- minutes.py (LOW - P3)
- ✅ sync.py (TESTED)
- sync_state.py (LOW - P3)
- sync_provenance.py (LOW - P3)

**Utilities (10):**
- ✅ logger.py (TESTED)
- logger_realtime.py (LOW - P3)
- ✅ validator.py (MEDIUM - P2)
- ✅ sanitizer.py (MEDIUM - P2)
- ✅ templates.py (MEDIUM - P2)
- bok.py (LOW - P3)
- admin.py (LOW - P3)
- ✅ installer.py (MEDIUM - P2)
- ✅ doctor.py (MEDIUM - P2)
- vendor_feedback.py (LOW - P3)
- ditto_tracker.py (LOW - P3)
- config_schema.py (LOW - P3)
- init_enhanced.py (LOW - P3)
- slash_command.py (LOW - P3)

**Drones (7):**
- ✅ drones/base_drone.py (TESTED)
- ✅ drones/reader_drone.py (TESTED)
- ✅ drones/writer_drone.py (TESTED)
- ✅ drones/summarizer_drone.py (TESTED)
- ✅ drones/architect_drone.py (TESTED)
- ✅ drones/scribe_drone.py (TESTED)
- ✅ drones/stylist_drone.py (TESTED)

**Total Components:** 50+
**Currently Tested:** ~10-12 (20-24%)
**Target After Plan:** ~20-25 (40-50%)

---

**Plan Status:** ✅ Complete and Ready for Execution
**Next Action:** Begin Phase 1, Task 1 - AgentStatusTracker Tests

---

**Created By:** CLAUDE-CODE-003 (Agent Y)
**Role:** QA Specialist & Testing Lead
**Date:** 2025-10-17
**Estimated Total Effort:** 16-20 hours across 3 weeks
**Target:** 50% test coverage

---

`#test-coverage` `#quality-assurance` `#production-readiness` `#testing-plan`
