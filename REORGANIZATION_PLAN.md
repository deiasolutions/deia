# DEIA Repository Reorganization Plan

**Created:** 2025-10-05
**Status:** DRAFT - Awaiting Dave's approval
**Purpose:** Separate DEIA product (public) from Dave's local instance (private)

---

## Problem Statement

Current `claude/` directory conflates:
1. **DEIA product design** (Constitution, CLI tool, BOK format)
2. **Dave's local DEIA usage** (session logs, working decisions, resume instructions)
3. **Community BOK entries** (mixed with Dave's logs)
4. **Platform-specific knowledge** (Railway, Vercel) not organized by vendor
5. **Cross-project instructions** (for parentchildcontactsolutions)

**Result:** Unclear what's DEIA design vs Dave's personal workflow. Doesn't scale.

---

## Core Distinction

### DEIA Product (Public Repository)
What everyone who uses DEIA will need:
- How DEIA works
- How to contribute
- BOK format and structure
- CLI tool
- Constitution template
- Sanitization guide

### Dave's DEIA Instance (Local, Gitignored)
Dave's personal use of DEIA:
- His session logs
- His working decisions
- His ideas and notes
- His project-specific patterns
- His resume instructions

---

## Proposed Structure

```
deiasolutions/
│
├── README.md                    # Main project README (DEIA product overview)
├── CONSTITUTION.md              # DEIA project's own constitution
├── CONTRIBUTING.md              # How to contribute BOK entries
├── LICENSE                      # CC0-1.0 for BOK, other for code
│
├── docs/                        # DEIA product documentation
│   ├── getting-started.md
│   ├── constitution-template.md      # Template for other projects
│   ├── sanitization-guide.md
│   ├── bok-format-spec.md           # How to write BOK entries
│   ├── architecture/
│   │   ├── security.md
│   │   └── privacy.md
│   └── governance/
│       ├── ostrom-alignment.md
│       └── rotg.md                  # DEIA's own Rules of the Game
│
├── bok/                         # Community Book of Knowledge (PUBLIC)
│   ├── README.md                # How BOK is organized
│   ├── platforms/               # Platform-specific workarounds
│   │   ├── railway/
│   │   │   ├── README.md        # Railway-specific issues index
│   │   │   └── https-redirect-middleware.md
│   │   ├── vercel/
│   │   │   ├── README.md        # Vercel-specific issues index
│   │   │   └── environment-auto-detection.md
│   │   └── aws/                 # Future: AWS patterns
│   │
│   ├── patterns/                # General patterns (platform-agnostic)
│   │   ├── collaboration/
│   │   │   ├── README.md
│   │   │   ├── ai-decision-making-framework.md
│   │   │   └── test-before-asking-human.md
│   │   ├── governance/
│   │   │   ├── README.md
│   │   │   └── biometric-authentication.md
│   │   ├── security/
│   │   └── performance/
│   │
│   ├── anti-patterns/           # What NOT to do
│   │   ├── README.md
│   │   └── autonomous-production-deployment.md
│   │
│   └── domains/                 # Future: Domain-specific (research, writing, etc.)
│
├── src/                         # DEIA CLI tool and libraries
│   └── deia/
│       ├── __init__.py
│       ├── cli.py
│       ├── core.py
│       └── ...
│
├── .deia/                       # Dave's LOCAL instance (GITIGNORED)
│   ├── README.md                # "This is Dave's local DEIA workspace"
│   ├── sessions/                # Dave's session logs from this project
│   ├── intake/                  # Incoming logs from other projects
│   ├── reviewed/                # Dave's reviews of sessions
│   ├── working/                 # Dave's working documents
│   │   ├── ideas.md
│   │   ├── decisions.md
│   │   └── resume-instructions.md
│   └── projects/                # Project-specific instructions
│       └── parentchildcontactsolutions/
│           ├── instructions.md
│           └── questions.md
│
├── .claude/                     # Claude Code config (Dave's local)
│   └── commands/
│       ├── save-session.md
│       └── extract-bok.md
│
└── .gitignore                   # Ignore .deia/ directory
```

---

## Migration Steps

### Phase 1: Create New Structure (No Breaking Changes)

**Step 1.1: Create new directories**
```bash
mkdir -p docs/architecture
mkdir -p docs/governance
mkdir -p bok/platforms/railway
mkdir -p bok/platforms/vercel
mkdir -p bok/patterns/collaboration
mkdir -p bok/patterns/governance
mkdir -p bok/anti-patterns
mkdir -p .deia/sessions
mkdir -p .deia/intake
mkdir -p .deia/reviewed
mkdir -p .deia/working
mkdir -p .deia/projects/parentchildcontactsolutions
```

**Step 1.2: Update .gitignore**
```
# Add to .gitignore
.deia/
```

### Phase 2: Move Files to Correct Locations

**Step 2.1: Move DEIA Product Documentation**

| Current Location | New Location | Type |
|-----------------|--------------|------|
| `claude/DEIA_CONSTITUTION.md` | `CONSTITUTION.md` | DEIA's own constitution |
| `claude/SECURITY_ARCHITECTURE.md` | `docs/architecture/security.md` | Product docs |
| `claude/SANITIZATION_GUIDE.md` | `docs/sanitization-guide.md` | Product docs |
| `claude/SANITIZATION_WORKFLOW.md` | `docs/sanitization-workflow.md` | Product docs |
| `claude/META_ROTG.md` | `docs/governance/rotg.md` | Product docs |
| `claude/OSTROM_ALIGNMENT.md` | `docs/governance/ostrom-alignment.md` | Product docs |
| `claude/CONSTITUTION_V2_DRAFT.md` | `docs/governance/constitution-v2-draft.md` | Product docs (pending) |

**Step 2.2: Move BOK Entries to Organized Structure**

| Current Location | New Location | Category |
|-----------------|--------------|----------|
| `claude/devlogs/bok/railway-https-redirect-middleware.md` | `bok/platforms/railway/https-redirect-middleware.md` | Platform-specific |
| `claude/devlogs/bok/frontend-environment-auto-detection.md` | `bok/platforms/vercel/environment-auto-detection.md` | Platform-specific |
| `claude/devlogs/bok/ai-decision-making-framework.md` | `bok/patterns/collaboration/ai-decision-making-framework.md` | General pattern |
| `claude/devlogs/bok/test-before-asking-human-to-test.md` | `bok/patterns/collaboration/test-before-asking-human.md` | General pattern |
| `claude/devlogs/bok/biometric-constitutional-authentication.md` | `bok/patterns/governance/biometric-authentication.md` | Governance pattern |
| `claude/devlogs/bok/anti-pattern-autonomous-production-deployment.md` | `bok/anti-patterns/autonomous-production-deployment.md` | Anti-pattern |

**Step 2.3: Move Dave's Local Files**

| Current Location | New Location | Type |
|-----------------|--------------|------|
| `claude/RESUME_INSTRUCTIONS.md` | `.deia/working/resume-instructions.md` | Dave's local |
| `claude/IDEAS_CAPTURE.md` | `.deia/working/ideas.md` | Dave's local |
| `claude/WORKING_DECISIONS.md` | `.deia/working/decisions.md` | Dave's local |
| `claude/devlogs/intake/*` | `.deia/intake/` | Dave's local |
| `claude/devlogs/raw/*` | `.deia/reviewed/` | Dave's local |
| `claude/devlogs/intake/deia_session_*.md` | `.deia/sessions/` | Dave's sessions |
| `claude/INSTRUCTIONS_FOR_PARENTCHILDCONTACTSOLUTIONS.md` | `.deia/projects/parentchildcontactsolutions/instructions.md` | Project-specific |
| `claude/devlogs/intake/parentchildcontactsolutions_questions-from-the-field_*.md` | `.deia/projects/parentchildcontactsolutions/questions.md` | Project-specific |

**Step 2.4: Move/Archive Other Files**

| Current Location | Action | Reason |
|-----------------|--------|--------|
| `claude/DAVE_REVIEW_SUMMARY.md` | Move to `.deia/working/` | Dave's review notes |
| `claude/DEFERRED_AMENDMENTS.md` | Move to `docs/governance/` | Product governance |
| `claude/DRAFT_ANTHROPIC_EMAIL.md` | Move to `.deia/working/` | Dave's personal draft |
| `claude/HOW_TO_SAVE_LOGS_FROM_OTHER_PROJECTS.md` | Move to `docs/` | Product docs |
| `claude/devlogs/` | Delete empty dirs after migration | Cleanup |

### Phase 3: Create README Files

**Step 3.1: Create README.md files for organization**

Files to create:
- `bok/README.md` - How BOK is organized
- `bok/platforms/README.md` - Platform-specific patterns index
- `bok/platforms/railway/README.md` - Railway-specific issues
- `bok/platforms/vercel/README.md` - Vercel-specific issues
- `bok/patterns/README.md` - General patterns index
- `bok/patterns/collaboration/README.md` - Collaboration patterns
- `bok/patterns/governance/README.md` - Governance patterns
- `bok/anti-patterns/README.md` - Anti-patterns to avoid
- `.deia/README.md` - "This is Dave's local workspace"
- `docs/README.md` - Documentation index

**Step 3.2: Update main README.md**

Update root README.md to explain:
- What DEIA is
- How to use it
- How to contribute
- Link to docs/ and bok/

### Phase 4: Update References

**Step 4.1: Update internal links**

Files that reference old paths:
- `src/deia/bok.py` (BOK search path)
- `.claude/commands/*.md` (session save paths)
- Any documentation cross-references

**Step 4.2: Update resume instructions**

New resume instructions location: `.deia/working/resume-instructions.md`

Tell Claude in next session:
- Read `.deia/working/resume-instructions.md` (not `claude/RESUME_INSTRUCTIONS.md`)
- BOK is now in `bok/` (not `claude/devlogs/bok/`)
- Docs are in `docs/` (not `claude/`)

### Phase 5: Clean Up

**Step 5.1: Remove empty directories**
```bash
# After all files moved
find claude/ -type d -empty -delete
```

**Step 5.2: Remove `claude/` directory if empty**

**Step 5.3: Update .gitignore**
```
# Ensure .deia/ is ignored
.deia/
```

---

## Verification Checklist

After reorganization:

- [ ] All BOK entries have YAML frontmatter
- [ ] All BOK entries are categorized correctly (platforms/ vs patterns/ vs anti-patterns/)
- [ ] Platform-specific BOK entries are in `bok/platforms/{vendor}/`
- [ ] General patterns are in `bok/patterns/{category}/`
- [ ] DEIA product docs are in `docs/`
- [ ] Dave's local files are in `.deia/` and gitignored
- [ ] Root README.md explains DEIA product
- [ ] Each BOK category has a README.md
- [ ] CLI tool (`src/deia/bok.py`) searches correct BOK path
- [ ] Resume instructions updated with new paths
- [ ] No broken internal links
- [ ] Git history preserved (use `git mv` not `mv`)

---

## Benefits After Reorganization

### For DEIA Product
- ✅ Clear what's public vs private
- ✅ BOK organized by category (platforms, patterns, anti-patterns)
- ✅ Easy to find Railway vs Vercel vs general patterns
- ✅ Scalable structure for future domains
- ✅ Professional open-source layout

### For Dave's Usage
- ✅ All local files in `.deia/` (gitignored)
- ✅ Can work freely without exposing private info
- ✅ Clear separation of concerns
- ✅ Project-specific instructions organized

### For Contributors
- ✅ Clear contribution guidelines
- ✅ Know where to put new BOK entries
- ✅ Platform-specific vs general patterns obvious
- ✅ No confusion about what's example vs product

---

## Open Questions for Dave

1. **Name of .deia/ directory:** Should it be `.deia/` or `my-deia/` or something else?
2. **Public vs Private:** Should `.deia/` be gitignored, or should parts be public?
3. **Session logs:** Should reviewed sessions eventually become BOK entries, or stay private?
4. **Website directory:** What's in `website/`? Does it need reorganization too?
5. **Timing:** Do this now, or after constitutional questions answered?
6. **Git history:** Use `git mv` to preserve history, or fresh copy?

---

## Execution Plan (When Approved)

**Claude will:**
1. Create all new directories
2. Use `git mv` to move files (preserves history)
3. Create README.md files for each category
4. Update internal references
5. Update .gitignore
6. Clean up empty directories
7. Create new RESUME_INSTRUCTIONS.md in `.deia/working/`
8. Verify all links work
9. Run git status to show changes
10. Ask Dave to review before committing

**Estimated time:** 30-45 minutes of systematic work

**Risk:** Low (using git mv, can revert if needed)

---

## Next Steps

**Dave: Please review and answer:**
1. Approve this structure? (y/n)
2. Name for local directory? (`.deia/` or other?)
3. Execute now, or after constitutional questions? (now/later)

Once approved, Claude will execute the reorganization systematically.

---

*This is a working document. Update as needed before execution.*
