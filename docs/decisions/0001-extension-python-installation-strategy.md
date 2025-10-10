# ADR 0001: Extension and Python Installation Strategy

**Date:** 2025-10-09
**Status:** ACCEPTED
**Deciders:** Dave (@dave-atx)

---

## Context

DEIA consists of:
1. **Python package** (core functionality)
2. **VS Code extension** (optional UI layer)
3. **Other integrations** (Claude Code, Cursor, etc.)

The VS Code extension calls the Python CLI commands. This creates a dependency:
- Extension requires Python package to function
- Need to keep versions in sync
- Need clear installation process

**Question:** How do users install DEIA, and how do we manage the Python package + extension dependency?

---

## Decision

### Phase 1: Separate Installs (CURRENT - Implement Now)

**Option C from architecture discussion**

Users install in two steps:

1. **Python package first:**
   ```bash
   pip install deia
   ```

2. **VS Code extension (optional):**
   - Install from VS Code Marketplace
   - Extension detects and uses installed Python package

**Why this approach:**
- ✅ Simple architecture (no bundling complexity)
- ✅ Works immediately (no new code needed)
- ✅ Python package works standalone (for non-VS Code users)
- ✅ Extension is truly optional
- ✅ Follows common pattern (ESLint, Prettier, Black, etc.)

**Trade-offs:**
- ❌ Two manual installation steps
- ❌ Users might install extension first and get confused
- ❌ Requires clear documentation

### Phase 2: Auto-Install (FUTURE - When Mature)

**Option B from architecture discussion**

Extension auto-installs Python package:

1. User installs extension from Marketplace
2. Extension detects: "deia Python package not found"
3. Extension prompts: "Install DEIA Python package? (requires pip)"
4. User approves → Extension runs `pip install deia`
5. Extension checks version compatibility on startup
6. Extension offers to upgrade if version mismatch

**Why wait:**
- Need to handle edge cases (permissions, Python not installed, pip missing)
- Need good error messages
- Need to test across Windows/Mac/Linux
- Want to validate approach with Phase 1 first

**"When Mature" means:**
- ✅ Python package has been published to PyPI
- ✅ At least 50 users successfully installed manually (Phase 1)
- ✅ Extension has basic features working reliably
- ✅ We've collected feedback on installation pain points
- ✅ Version 0.2.0 or later (not during 0.1.x)
- ✅ We have bandwidth to handle installation support issues
- ✅ Automated tests for installation process exist

**Estimated timeline:** 2-3 months after initial release

---

## Implementation Plan

### Phase 1 (Implement Now)

**Documentation:**
- [ ] Update README.md with installation steps
- [ ] Create INSTALLATION.md guide
- [ ] Add "Prerequisites" section (Python 3.8+, pip)
- [ ] Document VS Code extension as optional
- [ ] Add troubleshooting section

**Extension Changes:**
- [ ] Add startup check: is `deia` CLI available?
- [ ] Show helpful error if Python package not found
- [ ] Link to installation docs in error message
- [ ] Add version compatibility check (warn if mismatch)

**Python Package:**
- [ ] Ensure `deia --version` command exists
- [ ] Add machine-readable version output (for extension)
- [ ] No changes needed (already works standalone)

**Example Error Message:**
```
❌ DEIA Python package not found

The DEIA VS Code extension requires the Python package.

Install it with:
  pip install deia

Then reload VS Code.

[Installation Guide] [Dismiss]
```

**Example Version Mismatch Warning:**
```
⚠️ DEIA version mismatch

VS Code Extension: v0.1.0
Python Package:    v0.0.9

Please update:
  pip install --upgrade deia

[Update Now] [Dismiss]
```

### Phase 2 (Future - When Mature)

**New Extension Features:**
- [ ] Detect Python + pip availability
- [ ] Auto-install prompt on first activation
- [ ] Progress indicator during installation
- [ ] Handle installation errors gracefully
- [ ] Auto-upgrade capability
- [ ] Settings: "Auto-update DEIA" (yes/no)

**Testing Required:**
- [ ] Windows (various Python installations)
- [ ] macOS (system Python, Homebrew, pyenv)
- [ ] Linux (apt, snap, various distros)
- [ ] Virtual environments (venv, conda)
- [ ] Permissions issues (user vs. system install)

**Documentation:**
- [ ] Update to reflect auto-install
- [ ] Keep manual install as fallback
- [ ] Document troubleshooting for auto-install failures

---

## Version Sync Strategy

**All Phases:**

1. **Shared versioning:**
   - Python package version: `0.1.0`
   - VS Code extension version: `0.1.0`
   - Always match

2. **Extension checks on startup:**
   ```typescript
   const pythonVersion = getPythonPackageVersion(); // Calls 'deia --version'
   const extensionVersion = getExtensionVersion();

   if (pythonVersion !== extensionVersion) {
     showVersionMismatchWarning();
   }
   ```

3. **Release process:**
   - Release Python package to PyPI first
   - Test manually
   - Release VS Code extension with matching version
   - Update documentation

4. **Breaking changes:**
   - Increment major version (1.0.0 → 2.0.0)
   - Extension shows error if Python package too old
   - Refuse to activate until updated

---

## Alternatives Considered

### Option A: Bundle Python Package in Extension

**Rejected because:**
- Complex build process (bundle for Windows/Mac/Linux)
- Large download size
- Harder to update Python package independently
- Overkill for initial release

**Might reconsider if:**
- Auto-install (Phase 2) proves too problematic
- Users consistently struggle with pip install
- We want "one-click" installation experience
- Later stage (v1.0+), not now

### Monorepo with Shared Versioning

**Not decided yet, but considering:**

```
deia/
  ├── packages/
  │   ├── python/          # Python package (PyPI)
  │   ├── vscode/          # VS Code extension (Marketplace)
  │   └── shared/          # version.json, schemas
  ├── lerna.json           # Or similar monorepo tool
  └── version.json         # Single source of truth
```

**Benefits:**
- Single version number
- Release both together
- Easier to keep in sync

**Drawbacks:**
- More complex repo structure
- Need monorepo tooling
- Might be overkill for 2 packages

**Decision:** Defer until we have 3+ packages (e.g., Cursor extension, web dashboard)

---

## Success Criteria

### Phase 1 Success:
- ✅ Users can install Python package via pip
- ✅ Users can install VS Code extension separately
- ✅ Extension detects and uses Python package
- ✅ Clear error if Python package missing
- ✅ Warning if version mismatch
- ✅ Documentation is clear
- ✅ <5% of users report installation confusion

### Phase 2 Success (Future):
- ✅ Users can install just the extension
- ✅ Auto-install works on Windows/Mac/Linux
- ✅ <10% installation failure rate
- ✅ Good error messages for failures
- ✅ Auto-upgrade works reliably

---

## References

- Installation patterns from ESLint, Prettier, Black (all use separate installs)
- Jupyter extension (uses auto-install)
- Pylance (bundles language server)

---

## Next Actions

**Immediate (this session):**
1. Add to redesign plan: "Phase 1 installation strategy"
2. Document version checking in Python package
3. Update extension to show helpful errors

**Before 0.1.0 release:**
1. Write INSTALLATION.md
2. Update README.md
3. Test installation process end-to-end
4. Create installation troubleshooting guide

**After 0.1.0 stable (2-3 months):**
1. Evaluate Phase 1 feedback
2. Decide if Phase 2 is needed
3. Prototype auto-install
4. Test extensively before release

---

**Status:** Phase 1 is active development
**Phase 2 Timeline:** 2-3 months (when mature criteria met)
