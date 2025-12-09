# TASK: Context Loader Implementation

**From:** AGENT-003 (Tactical Coordinator)
**To:** AGENT-002 (Documentation Systems Lead)
**Date:** 2025-10-18 2235 CDT
**Priority:** P1 - HIGH
**Estimated:** 3-4 hours
**Type:** Phase 2 Foundation - Core Component

---

## Context

The Context Loader is a critical component for DEIA's intelligence. It loads and manages contextual information for AI interactions.

**Source:** Check Agent BC Phase 2 deliverables for Context Loader specification (if exists), or design from existing DEIA patterns.

---

## Task

Implement the DEIA Context Loader system.

---

## Deliverables

### 1. Python Implementation
**File:** `src/deia/services/context_loader.py`

**Core Components:**
- Load project context (files, structure, metadata)
- Load BOK patterns relevant to current task
- Load session history and preferences
- Build context windows for AI prompts
- Context prioritization and relevance scoring
- Memory management (context size limits)
- Caching for performance

**Requirements:**
- Security: Path validation (use existing path_validator)
- Performance: Efficient loading, caching
- Flexibility: Configurable context sources
- Integration: Works with BOK, session logger, file reader
- Full type hints and docstrings

### 2. Test Suite
**File:** `tests/unit/test_context_loader.py`

**Requirements:**
- >80% coverage
- Test all context loading scenarios
- Test security (path traversal prevention)
- Test caching behavior
- Test memory management
- Edge cases (missing files, invalid paths, large contexts)

### 3. Documentation
**File:** `docs/services/CONTEXT-LOADER.md`

**Sections:**
- Overview and purpose
- How to use (with examples)
- API reference
- Context sources and prioritization
- Configuration options
- Performance considerations
- Security model
- Integration examples
- Troubleshooting

### 4. Integration Protocol
- ✅ Run full test suite (all tests passing)
- ✅ Update ACCOMPLISHMENTS.md
- ✅ Update PROJECT-STATUS.csv
- ✅ Activity log entry
- ✅ SYNC to me when complete

---

## Success Criteria

- Context Loader fully functional
- >80% test coverage, all tests passing
- Security validated (no path traversal vulnerabilities)
- Documentation comprehensive
- Production-ready quality

---

## Design Considerations

### Context Sources (Suggested)
1. **Project Files** - Current project structure and key files
2. **BOK Patterns** - Relevant patterns from BOK
3. **Session History** - Recent conversation and decisions
4. **User Preferences** - Stored preferences and settings
5. **Active Tasks** - Current work context

### Security Requirements
- ✅ Use existing `path_validator.py` for all file paths
- ✅ No path traversal vulnerabilities
- ✅ Validate all external inputs
- ✅ Graceful handling of missing/inaccessible files

### Performance Requirements
- ✅ Cache frequently accessed contexts
- ✅ Lazy loading where possible
- ✅ Configurable context size limits
- ✅ Fast context assembly (<100ms for typical use)

---

## Notes

**Why you're suited for this:**
- You have knowledge systems expertise
- You understand documentation and information architecture
- You've worked with session logger (context source)
- You have strong systems design skills

**Authority:** Full design and implementation authority - make architectural decisions that fit DEIA patterns

**This is a core intelligence component** - design it well

---

## Estimated Timeline

- Design/Planning: 30-45 min
- Implementation: 1.5-2 hours
- Testing: 45-60 min
- Documentation: 45-60 min
- Integration Protocol: 15 min
- **Total: 3-4 hours**

---

## Dependencies

**Available to you:**
- `path_validator.py` (security)
- `file_reader.py` (file access)
- `session_logger.py` (session context)
- `enhanced_bok_search.py` (BOK patterns)
- `config.py` (preferences)

**Leverage these to build a powerful context system.**

---

## Alignment

**This aligns with:**
- Your knowledge systems specialty
- Phase 2 Foundation goals
- DEIA's AI intelligence enhancement mission
- Season 2 integration focus

**This is critical infrastructure. Build it solid.**

---

**Start when ready. SYNC progress every 2 hours.**

**AGENT-003 out.**
