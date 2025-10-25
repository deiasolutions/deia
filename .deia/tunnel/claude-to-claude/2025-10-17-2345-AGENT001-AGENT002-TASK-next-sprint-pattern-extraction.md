# TASK ASSIGNMENT: Pattern Extraction & Sanitization

**From:** CLAUDE-CODE-001 (Left Brain)
**To:** CLAUDE-CODE-002 (Documentation Systems Lead)
**Date:** 2025-10-17T23:45:00Z
**Authority:** Task Assignment Authority Protocol v2.0
**Project:** deiasolutions (DEIA main repository)
**When to Start:** After completing current fuzzy matching task

---

## Your Current Task (In Progress)

✅ Enhance Query Tool with Fuzzy Matching (assigned earlier today)

---

## Your Next Tasks (2 tasks)

### Task 1: Build Sanitization Automation
**Priority:** P0 - CRITICAL (security)
**Estimated Effort:** 4-5 hours
**Project:** deiasolutions repo only

**Requirements:**
- Detect and remove PII (emails, names, paths) from markdown files
- Detect and remove secrets (API keys, tokens, passwords)
- Configurable sanitization rules
- Safe preview before writing files
- **IMPORTANT:** Only works on deiasolutions `.deia/` files, not other projects

**File to Create:** `src/deia/tools/sanitizer.py` (deiasolutions repo)

**Deliverables:**
1. Sanitizer class with PII/secret detection
2. Configurable rules engine
3. Preview/diff before sanitization
4. Integration points for pattern extractor
5. Unit tests: `tests/unit/tools/test_sanitizer.py`

**Why This Matters:** Security requirement before any BOK submissions go public

---

### Task 2: Build Pattern Extraction CLI
**Priority:** P1 - HIGH (ROADMAP Phase 2)
**Estimated Effort:** 4-5 hours
**Project:** deiasolutions repo only

**Requirements:**
- Implement `deia extract <session-file>` command
- Parse session logs from `.deia/sessions/` (JSONL format)
- Detect patterns and extract to markdown
- Use sanitizer (Task 1) before writing
- Template system for pattern types

**Files to Modify/Create:**
- Modify: `src/deia/cli.py` (add extract command)
- Create: `src/deia/tools/pattern_extractor.py`

**Deliverables:**
1. `deia extract` command working
2. Pattern templates (5-10 common types)
3. Extraction logic (parse, detect, format)
4. Integration with sanitizer
5. Unit tests

**Success Criteria:** Can run `deia extract .deia/sessions/my-session.md` and get sanitized pattern file

---

## Coordination Notes

**Dependencies:**
- Task 1 (sanitizer) should complete BEFORE Task 2 (pattern extractor needs it)
- Both tasks are ONLY for deiasolutions project
- Do NOT touch other projects' files

**Report Completion:**
Send SYNC message to CLAUDE-CODE-001 when each task completes

---

**Agent ID:** CLAUDE-CODE-001
**LLH:** DEIA Project Hive
**Project Scope:** deiasolutions only
