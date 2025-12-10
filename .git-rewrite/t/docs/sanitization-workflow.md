# DEIA Sanitization Workflow

**Purpose:** Ensure no IP, PII, or proprietary information is committed to public GitHub repo

---

## Two-Repository Strategy

### Local Repository (This One)
**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\`

**Purpose:**
- Work freely without worrying about IP leakage
- Contains unsanitized session logs
- Personal notes and drafts
- Client-specific information

**Safety:**
- Never push to public GitHub
- .gitignore blocks IP-related files
- Local commits only

### Public Repository (To Be Created)
**Location:** `github.com/deiasolutions/deia` (or similar)

**Purpose:**
- Share sanitized knowledge with community
- Templates and documentation
- BOK entries (after sanitization)
- Open-source methodology

**Safety:**
- Only manually reviewed and sanitized content
- No automatic sync from local
- Human approval required for every push

---

## Workflow

### Step 1: Work Locally (Unrestricted)

```bash
# In local repo - work freely
cd C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude

# Create session logs with any content
# Add personal notes
# Include client information
# Don't worry about IP protection yet

# Commit locally
git add .
git commit -m "Local work - not sanitized"
```

**This stays local. Never push.**

---

### Step 2: Prepare for Public Sharing

When you have content ready to share publicly:

**Create sanitization workspace:**
```bash
mkdir sanitization-workspace
```

**Copy file to sanitize:**
```bash
cp devlogs/intake/session.md sanitization-workspace/
```

**Run sanitization:**
```bash
# Use sanitization script (to be built)
python scripts/sanitize.py sanitization-workspace/session.md

# Or manual sanitization following SANITIZATION_GUIDE.md
```

**Review sanitized output:**
- No IP references
- No PII/PHI
- No client names
- No proprietary information
- No file paths with personal info

---

### Step 3: Copy to Public Repo

**In separate public repo directory:**
```bash
cd /path/to/public/deia/repo

# Copy sanitized file
cp ~/local/sanitization-workspace/session_SANITIZED.md pipeline/intake/

# Review one more time
git diff

# Commit with clear message
git commit -m "Add: Sanitized session log on [topic]"

# Push to public GitHub
git push origin main
```

---

## Safety Checks

### Before Any Public Commit

**Checklist:**
- [ ] Ran through sanitization script
- [ ] Manually reviewed for IP references
- [ ] No personal names remain
- [ ] No client/company names
- [ ] No file paths with personal info
- [ ] No API keys or credentials
- [ ] No proprietary code or logic
- [ ] Reviewed SANITIZATION_GUIDE.md

### .gitignore Protection

**.gitignore blocks:**
- `*[Ii][Pp]*` - Any file/folder with "ip" in name
- `*davee*` - Personal name patterns
- `.env*` - Environment files
- `secrets/`, `credentials/` - Obvious sensitive folders
- `personal/`, `private/`, `proprietary/` - Explicit markers

**If you accidentally try to commit something that should be private, git will block it.**

---

## File Naming Convention

### Local Files (Can Contain IP)
```
session_2025-10-05_client-acme-ip-discussion.md  ← .gitignore blocks this
personal-notes-ip-strategy.md                     ← .gitignore blocks this
davee-thoughts.md                                  ← .gitignore blocks this
```

### Public Files (Sanitized)
```
session_2025-10-05_governance-patterns.md         ← Safe to commit
bok_entry_001_biometric-auth.md                   ← Safe to commit
```

**Strategy:** If a file contains IP, put "ip" in the filename. It won't be committable.

---

## Directory Structure

```
claude/ (local repo)
├── .gitignore (strict IP protection)
├── personal/ (never committed - in .gitignore)
│   ├── client-notes/
│   └── ip-discussions/
├── sanitization-workspace/ (never committed - in .gitignore)
│   ├── original.md
│   └── sanitized.md
├── devlogs/
│   └── intake/
│       ├── session_raw.md (may contain IP)
│       └── session_sanitized.md (ready for public)
└── scripts/
    └── sanitize.py (sanitization automation)

deia/ (public repo - separate directory)
├── .gitignore (standard open source)
├── README.md
├── pipeline/
│   ├── intake/
│   ├── bok/
│   └── wisdom/
└── templates/
```

---

## Scripts to Build

### 1. `scripts/sanitize.py`

**Purpose:** Automate common sanitization tasks

**What it does:**
- Removes email addresses
- Removes URLs (except public docs)
- Removes file paths with personal info
- Replaces high-entropy strings
- Flags potential PII for manual review

**Usage:**
```bash
python scripts/sanitize.py input.md --output sanitized.md --review
```

### 2. `scripts/check_before_commit.sh`

**Purpose:** Pre-commit safety check

**What it does:**
- Scans staged files for IP references
- Checks for PII patterns
- Flags files that might need sanitization
- Blocks commit if issues found

**Usage:**
```bash
# Install as pre-commit hook
cp scripts/check_before_commit.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### 3. `scripts/prepare_for_public.sh`

**Purpose:** One-command sanitization workflow

**What it does:**
- Creates sanitization workspace
- Copies file to sanitize
- Runs sanitization script
- Opens for manual review
- Prompts for approval before copying to public repo

**Usage:**
```bash
./scripts/prepare_for_public.sh devlogs/intake/session.md
```

---

## Public Repository Setup

### When Creating Public Repo

**Don't fork or sync from local repo.**

**Instead:**
1. Create fresh repo on GitHub: `github.com/deiasolutions/deia`
2. Clone locally to separate directory: `git clone ...`
3. Manually copy sanitized files from local repo
4. Never set local repo as remote

**This prevents accidental pushes of unsanitized content.**

---

## Emergency: If IP Gets Committed

### If Committed Locally Only

```bash
# Remove from history
git reset --soft HEAD~1
# or
git rebase -i HEAD~5  # interactive rebase to remove commit
```

### If Pushed to Public GitHub

**This is serious.**

1. **Immediately delete the commit:**
   ```bash
   git reset --hard HEAD~1
   git push --force origin main
   ```

2. **Assume the IP is compromised**
   - GitHub caches all commits
   - Anyone watching the repo may have seen it
   - Change any credentials exposed
   - Document incident in `incidents/`

3. **Contact GitHub support**
   - Request cache purge
   - Provide commit SHA

4. **Update .gitignore**
   - Add patterns that would have blocked it
   - Update sanitization scripts

---

## Best Practices

### DO:
✅ Work freely in local repo
✅ Use descriptive filenames (including "ip" if it contains IP)
✅ Commit often locally
✅ Sanitize carefully before public sharing
✅ Review sanitized content twice
✅ Use automation scripts for common patterns
✅ Keep local and public repos completely separate

### DON'T:
❌ Never push local repo to public GitHub
❌ Never add public repo as remote in local
❌ Never automate local → public sync
❌ Never skip manual review of sanitized content
❌ Never rush the sanitization process
❌ Never assume the script caught everything

---

## Questions to Ask Before Public Commit

1. **Would I show this to a stranger?** If no, don't commit.
2. **Does this reveal client information?** If yes, sanitize more.
3. **Could someone identify me or my work from this?** If yes, anonymize.
4. **Does this contain any code I don't own?** If yes, remove or get permission.
5. **Have I reviewed it twice?** If no, review again.

---

## Summary

**Local Repo:** Work freely, .gitignore protects against accidental IP commits
**Public Repo:** Separate directory, only sanitized content, manual review required
**Workflow:** Local work → Sanitize → Manual review → Copy to public → Push

**Remember:** It's easier to add information later than to remove it after it's public.

---

**Next Steps:**
1. ✅ .gitignore created with IP protection
2. ⏳ Build `scripts/sanitize.py`
3. ⏳ Build `scripts/check_before_commit.sh`
4. ⏳ Create public GitHub repo (when ready)
5. ⏳ Test workflow with first sanitized file
