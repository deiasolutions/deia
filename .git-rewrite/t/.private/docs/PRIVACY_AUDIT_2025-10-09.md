# Privacy Audit & Remediation - 2025-10-09

## Summary

Completed comprehensive PII scan and privacy infrastructure setup for DEIA repository.

## Actions Taken

### 1. PII Scan Results ✅

**Found and fixed:**
- 6 instances of "Dave Eichler" → Changed to "Dave (@dave-atx)"
- Files updated:
  - `README.md` (line 284)
  - `docs/decisions/0001-extension-python-installation-strategy.md` (line 5)
  - `docs/postmortems/logger-claims-vs-reality-rca.md` (line 320)
  - `docs/claude-code/project-resume-pattern.md` (line 406)
  - `docs/claude-code/clarifying-questions-policy.md` (line 186)
  - CLAUDE-PROJECT-BRIEFING.md (moved to private)

**No other PII found:**
- ✅ No phone numbers
- ✅ No physical addresses
- ✅ No additional email addresses (project emails are intentional)
- ✅ No social media handles beyond approved ones
- ✅ No employer information
- ✅ No location data

### 2. Private Directory Structure Created ✅

**Repo-level private space (`.private/`):**
```
.private/
├── README.md                    # Usage guide
├── docs/                        # Private documentation
│   ├── CLAUDE-PROJECT-BRIEFING.md  # Moved here (had PII + strategic info)
│   └── PRIVACY_AUDIT_2025-10-09.md # This file
├── logs/                        # Private conversation logs
├── notes/                       # Personal notes
└── experiments/                 # Experimental work
```

**Project-level private space (`.deia/private/`):**
```
.deia/private/
├── README.md                    # Usage guide
├── logs/                        # Unsanitized conversation logs
├── drafts/                      # Pre-sanitization submissions
├── notes/                       # Personal project notes
└── experiments/                 # Private experiments
```

### 3. .gitignore Updated ✅

Added:
```gitignore
# Private directories (never commit)
.private/
.deia/private/
```

Verified: Neither directory appears in `git status` ✅

### 4. Sanitization Documentation Created ✅

Created `.deia/SANITIZATION_REQUIREMENTS.md` with:
- What must be removed (PII, secrets, proprietary info)
- Sanitization workflow
- Privacy levels (Private → Sanitized → Public)
- Dave's approved public identity (only "Dave" and "@dave-atx")
- Checklist for submissions
- Recovery process for mistakes

## Directory Separation Rationale

### User Preferences (Public)
- `~/.deia/dave/preferences.md` - Coding practices, TDD rules, communication preferences
- **Public** - General dev practices for ANY AI tool to read
- NOT private - No PII, just workflow preferences

### Claude-Specific Instructions (Public)
- `.claude/INSTRUCTIONS.md` - Auto-logging instructions
- `.claude/commands/` - Slash commands
- **Public** - Tool-specific, no PII

### Repo-Level Private (`.private/`)
- Dave's private workspace for THIS repo
- Contains PII-bearing docs (CLAUDE-PROJECT-BRIEFING.md)
- Strategic notes not ready for public
- **Never committed to git**

### Project-Level Private (`.deia/private/`)
- Per-user, per-project private space
- Unsanitized conversation logs
- Draft submissions before sanitization
- **Every DEIA user gets this**

## Business Model Clarification ✅

Updated `docs/CLAUDE-PROJECT-BRIEFING.md` (now in `.private/docs/`) to clearly state:

**DEIA is free and always will be.** No paid tiers, no data selling, no ads.

**Funding model:**
- Community donations/sponsorships (GitHub Sponsors, Patreon, etc.)
- University partnerships (grant funding)
- Goal: Cover Dave's development costs + future infrastructure

**Why:** Dave has a full-time job but would rather work on DEIA. Supporters help sustain the project.

## Files Modified

**Git tracked changes:**
- `.gitignore` - Added private directories
- `README.md` - Fixed PII (Dave Eichler → Dave (@dave-atx))
- `docs/decisions/0001-extension-python-installation-strategy.md` - Fixed PII
- `docs/postmortems/logger-claims-vs-reality-rca.md` - Fixed PII
- `docs/claude-code/project-resume-pattern.md` - Fixed PII
- `docs/claude-code/clarifying-questions-policy.md` - Fixed PII

**New private files (not tracked):**
- `.private/README.md`
- `.private/docs/CLAUDE-PROJECT-BRIEFING.md` (moved)
- `.private/docs/PRIVACY_AUDIT_2025-10-09.md` (this file)
- `.deia/private/README.md`
- `.deia/SANITIZATION_REQUIREMENTS.md`

## Approved Public Identity

**What CAN be public:**
- ✅ "Dave" (first name)
- ✅ "@dave-atx" (GitHub handle)
- ✅ "DEIA project maintainer"

**What must NEVER be public:**
- ❌ Last name
- ❌ Other GitHub handles
- ❌ Email addresses (personal)
- ❌ Company/employer info
- ❌ Location data

## Verification

```bash
# Verify private dirs are ignored
git status | grep -E "\.private|\.deia/private"
# (Should return nothing)

# Verify PII removed from public docs
grep -r "Dave Eichler" --include="*.md" .
# (Should only find matches in .private/)

# Verify gitignore working
ls -la .private .deia/private
# (Directories exist but not in git)
```

## Next Steps

1. ✅ Commit PII fixes to public docs
2. ✅ Keep CLAUDE-PROJECT-BRIEFING.md private
3. ✅ Use `.deia/private/` for unsanitized work
4. ✅ Always sanitize before submitting to DEIA Global

## Lessons Learned

1. **Separate concerns properly:**
   - User preferences (coding practices) ≠ Private docs (PII)
   - Tool-specific configs ≠ Personal workspace
   - Per-repo privacy ≠ Per-user privacy

2. **Multiple privacy levels needed:**
   - Public (git tracked)
   - Private per-project (`.deia/private/`)
   - Private per-repo (`.private/`)
   - User-level (`~/.deia/dave/`)

3. **Privacy audit should be regular:**
   - PII can creep in through docs, examples, attribution
   - Automated scanning helps but manual review essential
   - Clear policies prevent future issues

## Status

✅ **All tasks completed**
✅ **No PII in public docs**
✅ **Private infrastructure in place**
✅ **Sanitization workflow documented**
✅ **Business model clarified**

---

*This file lives in `.private/docs/` and will never be committed to git.*
