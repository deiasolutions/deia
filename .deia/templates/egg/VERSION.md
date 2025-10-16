# Egg Template Version History

## Current Version: v0.1 (eOS Compliant)

**Date:** 2025-10-15
**File:** `.deia/templates/egg/minimal-egg.md`
**Author:** Claude (Anthropic, Bee Queen)

### Changes from v0.0

**Added:**
- ✅ eOS v0.1 manifest (`eos`, `kind`, `id`, `policy`, `routing`)
- ✅ ROTG + DND policy enforcement
- ✅ Capabilities declaration (`caps`)
- ✅ Routing instructions (project-based segmentation)
- ✅ Virus definition and prevention documentation
- ✅ Three-component pattern (egg + eOS pack + commons)
- ✅ Minimal seed concept documentation

**Removed:**
- ❌ Old `deia_routing` schema (replaced with eOS `routing`)
- ❌ Ambiguous placeholders
- ❌ No explicit virus prevention guidance

### Key Improvements

1. **Virus Prevention:** Template explicitly explains what NOT to include (no embedded entities, no embedded builder code)
2. **eOS Compliance:** Full kernel integration with ROTG + DND enforcement
3. **Three-Component Pattern:** Egg (minimal) + eOS pack (data) + DEIA Global Commons (shared tools)
4. **Educational:** Template doubles as documentation for proper egg usage

---

## Archive

### v0.0 (Pre-eOS)

**Date:** 2025-10-15 (archived)
**File:** `.deia/templates/egg/archive/minimal-egg-v0.0-2025-10-15.md`

**Description:** Original minimal egg template before eOS formalization. Used `deia_routing` instead of `eos` manifest. No explicit virus prevention guidance.

---

## Template Usage

**For builders:**
```bash
# Hatch new egg from template
.deia/tools/egg_hatch.sh --template minimal-egg --id <your-egg-id>
```

**For developers:**
- Template is NOT a literal copy-paste
- Contains placeholders that should be replaced (e.g., `{{ID}}`, `simulation_004`)
- Educational sections (virus prevention, proper pattern) should be adapted per use case

---

**Filed:** `.deia/templates/egg/VERSION.md`
**Status:** Internal documentation
**Tags:** `#templates` `#eggs` `#versioning` `#eos`
