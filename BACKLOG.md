# DEIA Development Backlog

## In Progress

### Downloads Monitor - Phase 1: Safe Temp Staging
**Status:** In Progress
**Priority:** High
**Assigned:** Bot 1 (Architect)
**Started:** 2025-10-11

**Goal:** Implement safe file processing with temp staging and no auto-delete.

**Tasks:**
- [x] Basic monitor with file watching
- [x] YAML frontmatter parsing
- [x] Routing logic
- [x] Startup scanning and state tracking
- [ ] **Temp staging implementation (current)**
- [ ] Test with sample files
- [ ] Update documentation
- [ ] Commit to repo

**Security Requirements:**
- Never delete files until git commit confirmed
- Handle privacy markings appropriately
- Keep temp files for recovery

---

## Backlog

### Master Librarian Service - Phase 1: Enhanced Query Tool
**Priority:** Medium
**Estimated Effort:** Small (1-2 sessions)
**Dependencies:** Query tool MVP (✅ complete), Master index YAML (✅ complete)
**Spec:** `docs/specs/master-librarian-service-wip.md`

**Goal:** Extend MVP query tool with advanced search and usage tracking.

**Context:**
During Q33N deployment session (2025-10-16), we realized: "we now have more info than one AI can ingest and hold in context." Built foundation (master-index.yaml, query.py MVP, taxonomy). Now need proactive knowledge management service.

**Tasks:**
- [ ] Add fuzzy matching (typo tolerance)
- [ ] Multi-keyword AND/OR logic
- [ ] Filter by urgency/platform/audience
- [ ] Usage tracking (log all queries)
- [ ] Integrate as `deia librarian query` command
- [ ] Test with real session queries

**Success Metrics:**
- Zero-result rate drops (better discovery)
- Query time < 100ms (performance)
- Usage logs capture patterns (analytics foundation)

**Next Phases:**
- Phase 2: Proactive injection (detect patterns, inject docs before mistakes)
- Phase 3: Index maintenance & curation
- Phase 4: MCP server + Claude Code hooks

---

### Downloads Monitor - Phase 2: Git-Aware Cleanup
**Priority:** High
**Estimated Effort:** Medium
**Dependencies:** Phase 1 complete

**Goal:** Automatically clean up temp files after confirming git commit.

**Tasks:**
- [ ] Implement git status checking
- [ ] Monitor routed files for commits
- [ ] Delete temp only after commit confirmed
- [ ] Archive on timeout (24h)
- [ ] Handle .gitignore detection
- [ ] Testing with real git workflows

**Security Considerations:**
- Verify file is tracked AND committed before delete
- If ignored → assume sensitive → archive
- Timeout safety net (archive, don't delete)

---

### Downloads Monitor - Phase 3: Privacy Handling
**Priority:** Medium
**Estimated Effort:** Large
**Dependencies:** Phase 2 complete

**Goal:** Advanced privacy controls and encryption for sensitive files.

**Tasks:**
- [ ] Parse privacy markings from YAML
- [ ] Implement privacy levels (public/internal/private)
- [ ] Encrypt archived files for internal/private
- [ ] Alert if private file → public repo
- [ ] Block routing on privacy violations
- [ ] Audit log for privacy-marked files

**Security Requirements:**
- Encryption at rest for private/internal files
- Never commit private files to public repos
- Audit trail for compliance

---

### Downloads Monitor - Phase 4: Local User Settings
**Priority:** Low
**Estimated Effort:** Small
**Dependencies:** Phase 1 complete

**Goal:** Per-user configuration overrides.

**Tasks:**
- [ ] Support `~/.deia/downloads-monitor/local-config.json`
- [ ] Override cleanup policies per-user
- [ ] Override privacy defaults
- [ ] Document local settings format

---

### CLI Command: `deia monitor`
**Priority:** Medium
**Estimated Effort:** Small
**Dependencies:** Phase 1 complete

**Goal:** Integrate downloads monitor into DEIA CLI.

**Tasks:**
- [ ] Add `deia monitor start` command
- [ ] Add `deia monitor stop` command
- [ ] Add `deia monitor status` command
- [ ] Add `deia monitor config` (edit config)
- [ ] System service integration (systemd/launchd)

---

### Pattern Extraction: Safe File Processing
**Priority:** Low
**Estimated Effort:** Small
**Dependencies:** Phase 2 validated

**Goal:** Extract BOK pattern from this work.

**Tasks:**
- [ ] Extract pattern from this session
- [ ] Sanitize (remove paths, names, etc)
- [ ] Format as BOK pattern
- [ ] Submit to bok/patterns/security/

**Pattern Name:** "Never Delete Until Persisted"

---

## Done

### Downloads Monitor - Initial Implementation
**Completed:** 2025-10-11
**Summary:** Basic file monitoring with YAML routing and startup scanning.

**Delivered:**
- File watching with watchdog
- YAML frontmatter parsing
- Project-based routing
- Startup scan with state tracking
- Error handling and logging

---

## Notes

**Development Location:**
- Tool installed: `~/.deia/downloads-monitor/` (user config)
- Source code: `extensions/downloads-monitor/` (in repo, coming)
- Documentation: `docs/downloads-monitor.md` (coming)

**Auto-Logging:**
- ✅ This session is being logged
- ✅ Auto-log enabled in deiasolutions repo
- ✅ Private sessions in `.deia/sessions/`
- Review later for pattern extraction

**Security Notes:**
- Keep all dev logs private until sanitized
- Review for PII before any public sharing
- Extract patterns, not implementation details

- [Future Egg] PlayerBot-Train-v0: expose GameAPI, add scripted baseline policy, then ML/NN agent. Also apply to FlappyBird scaffold.
