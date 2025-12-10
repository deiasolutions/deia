# Observation: Manual Dependency Installation Required

**Date:** 2025-10-17
**Agent:** CLAUDE-CODE-002
**Context:** Phase 3 integration work

---

## Issue

User (Dave) had to manually install `rapidfuzz` after it was requested by the hive.

**Command required:**
```bash
pip install rapidfuzz
```

---

## Root Cause

**UPDATE:** After checking `pyproject.toml`, I found that `rapidfuzz>=3.0.0` and `scikit-learn>=1.3.0` ARE declared in the dependencies (lines 49-50).

**Actual issue:** The dependencies were declared in the manifest but the environment wasn't reinstalled after the manifest was updated.

**Gap:** Missing step between "update pyproject.toml" and "use the new dependencies"

---

## Impact

- **User friction:** Manual intervention required during integration
- **Deployment risk:** Missing dependencies won't be caught until runtime
- **Coordination overhead:** User has to track what's been requested vs. installed

---

## Affected Packages (Known)

1. `rapidfuzz` - For fuzzy string matching (likely in Enhanced BOK Search)
2. `scikit-learn` - Mentioned in Task 4 specs (for TF-IDF)

---

## Recommendations

### Immediate Actions

1. ✅ **Dependencies already in pyproject.toml** (lines 49-50)

2. **Missing step:** After updating pyproject.toml, reinstall the package:
   ```bash
   pip install -e .
   ```

3. **Document in README:** Note about reinstalling after dependency updates

4. **Create dependency audit:** Review all Phase 1-3 deliverables for additional undeclared dependencies

### Process Improvements

1. **Dependency checklist for deliverables:**
   - All imports must be declared
   - Include in companion files: "Dependencies: package>=version"
   - Test in clean virtual environment before delivery

2. **Automated dependency detection:**
   - Scan .py files for imports
   - Cross-reference with pyproject.toml
   - Flag missing dependencies

3. **Integration protocol update:**
   - Integration Specialist (me) checks dependencies before deployment
   - Add missing packages to pyproject.toml as part of integration
   - Document in integration observations

---

## Action Items

**For CLAUDE-CODE-002 (me):**
- [ ] Audit Phase 3 deliverables for import statements
- [ ] Create list of all required dependencies
- [ ] Update pyproject.toml with missing packages
- [ ] Test installation in clean environment

**For Agent BC:**
- Include "Dependencies:" section in future deliverables
- List all non-stdlib imports with version requirements

**For Left Brain:**
- Add dependency management to integration checklist
- Consider automation for dependency scanning

---

## Related Patterns

This connects to:
- **Build system management** (pyproject.toml as source of truth)
- **Integration testing** (dependency resolution before deployment)
- **Documentation completeness** (companion files should list deps)

---

## Lessons Learned

**What worked:**
- User identified and resolved the issue quickly
- Manual install was straightforward

**What could improve:**
- Proactive dependency declaration in deliverables
- Automated dependency checking during integration
- Better coordination between code delivery and dep management

---

**Status:** Documented, awaiting dependency audit and pyproject.toml updates

**Next:** Add rapidfuzz and scikit-learn to pyproject.toml, audit all Phase 1-3 code for additional undeclared dependencies
