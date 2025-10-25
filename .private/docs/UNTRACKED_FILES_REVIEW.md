# Untracked Files Review - 2025-10-10

**Total untracked:** 34 files

**Decision needed:** Which should be committed to GitHub?

---

## Root-Level Documentation (New)

### Installation/Setup Docs
- `QUICKSTART.md` - Quick installation guide
- `DEIA_INTEGRATION_GUIDE.md` - Integration guide
- `DEIA_MEMORY_SETUP.md` - Memory setup instructions
- `DEIA_MEMORY_HIERARCHY.md` - Advanced memory configuration

**Recommendation:**
- **Keep:** QUICKSTART.md (simple path)
- **Review:** Others may be redundant per REPO_INDEX notes (lines 95-101)

### Project Philosophy
- `PRINCIPLES.md` - Project principles

**Recommendation:** **Commit** - Core project philosophy should be public

---

## .claude/ Directory (Claude Code Integration)

### Core Files (Already committed)
- ✅ `.claude/INSTRUCTIONS.md` (committed)
- ✅ `.claude/REPO_INDEX.md` (committed)
- ✅ `.claude/STARTUP_CHECKLIST.md` (committed)

### Additional Files (Untracked)
- `.claude/CAPABILITIES.md` - What Claude can/can't do
- `.claude/commands/auto-log-check.md` - Auto-log check command
- `.claude/commands/doc-audit.md` - Doc audit command
- `.claude/commands/log.md` - Manual log command

**Recommendation:** **Commit all** - These are part of Claude Code integration infrastructure

---

## docs/ Directory (New Documentation)

### Process Documentation
- `docs/DEV-PRACTICES-SUMMARY.md` - Development standards quick reference
- `docs/SUBMISSION_WORKFLOW.md` - Admin review process
- `docs/SUBMISSION_WORKFLOW_AUDIT.md` - Gap analysis
- `docs/IMPLEMENTATION_PLAN.md` - Technical roadmap

**Recommendation:** **Commit** - Core project process documentation

### Dave's Workflow (Questionable)
- `docs/Dave Questions.md` - Dave's question tracking
- `docs/Dave-Questions-Dialog.md` - Q&A history

**Recommendation:** **Review with Dave** - May contain private notes/questions

### Other
- `docs/library-feedback.md` - Library feedback tracking

**Recommendation:** **Commit** - Process documentation

---

## Source Code (New)

- `src/deia/cli_utils.py` - CLI helper functions (safe_print, etc.)
- `src/deia/logger_realtime.py` - Real-time logger variant

**Recommendation:** **Commit** - Core functionality

---

## VS Code Extension (New Files)

- `extensions/vscode-deia/CHANGELOG.md`
- `extensions/vscode-deia/STATUS.md`
- `extensions/vscode-deia/TESTING.md`

**Recommendation:** **Commit** - Extension documentation

---

## Build Artifacts / Dependencies (Don't Commit)

- `extensions/vscode-deia/node_modules/` - Dependencies
- `extensions/vscode-deia/out/` - Compiled output
- `extensions/vscode-deia/deia-0.1.0.vsix` - Built extension
- `extensions/vscode-deia/package-lock.json` - Lock file
- `nul` - Temp file
- `pytest.ini` - Test config (should this be committed?)
- `tests/` - Test directory

**Recommendation:**
- **Don't commit:** node_modules, out, .vsix, nul
- **Commit:** pytest.ini, tests/ (needed for development)

---

## Other Directories

- `.github/` - GitHub workflows/templates
- `bok/patterns/documentation/` - BOK patterns
- `docs/audits/` - Audit reports
- `docs/decisions/` - Already has one file committed
- `README.md.backup` - Backup file

**Recommendation:**
- **Review:** .github/ (if workflows exist, commit them)
- **Commit:** bok/patterns/ (community contributions)
- **Don't commit:** README.md.backup (temp file)
- **Commit:** docs/audits/ if contains useful info
- **Commit:** Additional docs/decisions/ files

---

## Proposed Commit Strategy

### Commit Group 1: Core Infrastructure
```bash
git add .claude/CAPABILITIES.md .claude/commands/
git add src/deia/cli_utils.py src/deia/logger_realtime.py
git add pytest.ini tests/
git commit -m "Add core infrastructure: CLI utils, logger variants, test config, Claude commands"
```

### Commit Group 2: Documentation
```bash
git add PRINCIPLES.md QUICKSTART.md
git add docs/DEV-PRACTICES-SUMMARY.md docs/SUBMISSION_WORKFLOW*.md docs/IMPLEMENTATION_PLAN.md
git add docs/library-feedback.md
git commit -m "Add project documentation: principles, quickstart, workflows"
```

### Commit Group 3: VS Code Extension
```bash
git add extensions/vscode-deia/CHANGELOG.md extensions/vscode-deia/STATUS.md extensions/vscode-deia/TESTING.md
git commit -m "Add VS Code extension documentation"
```

### Review Separately (Ask Dave)
- `docs/Dave Questions.md` - May be private
- `docs/Dave-Questions-Dialog.md` - May be private
- `DEIA_INTEGRATION_GUIDE.md` - May be redundant
- `DEIA_MEMORY_SETUP.md` - May be redundant
- `DEIA_MEMORY_HIERARCHY.md` - May be redundant
- `.github/` - Unknown contents
- `bok/patterns/documentation/` - Unknown contents
- `docs/audits/` - Unknown contents

### Don't Commit (Cleanup)
- `extensions/vscode-deia/node_modules/`
- `extensions/vscode-deia/out/`
- `extensions/vscode-deia/deia-0.1.0.vsix`
- `extensions/vscode-deia/package-lock.json` (maybe - consider adding to .gitignore)
- `README.md.backup`
- `nul`

---

## Questions for Dave

1. **Dave's question docs** - Are `docs/Dave Questions.md` and `docs/Dave-Questions-Dialog.md` private or can they be public?

2. **Memory docs redundancy** - REPO_INDEX says INTEGRATION_GUIDE and some memory docs are redundant. Should I delete them or keep them?

3. **Extension build artifacts** - Should `package-lock.json` be in .gitignore for the extension?

4. **BOK patterns** - What's in `bok/patterns/documentation/`? Should it be committed?

5. **.github/** - What's in there? Workflows to commit?

---

## Recommendation

**Wait for Dave's input on:**
- Dave's question tracking files (private?)
- Redundant memory setup docs (delete or keep?)
- Unknown directory contents (.github/, bok/patterns/, docs/audits/)

**Then commit in 3 groups** as outlined above.

---

*This review file is private (.private/docs/) and won't be committed.*
