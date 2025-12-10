# Documentation Patterns

Patterns for maintaining high-quality, accurate documentation in software projects.

---

## Available Patterns

### [Documentation Audit](documentation-audit.md)

**What:** Systematic verification and rationalization of project documentation

**When to use:**
- Quarterly maintenance
- Before major releases
- After significant refactoring
- Multiple doc-related bug reports

**How to run:**
- **AI-assisted (recommended):** `/doc-audit` in Claude Code
- **Automated checks:** `deia doctor docs`
- **Manual:** Follow pattern guide step-by-step

**Outputs:**
- Accuracy verification report
- Redundancy analysis
- Actionable remediation plan
- Execution-ready bash commands

**Time required:** 1-3 hours depending on project size

---

## Quick Reference

```bash
# Run automated documentation audit
deia doctor docs

# Apply recommended fixes
deia doctor docs --fix

# AI-assisted audit (in Claude Code)
/doc-audit
```

---

## Pattern Metadata

- **Category:** Project Maintenance
- **Created:** 2025-10-07
- **Tested on:** DEIA project
- **License:** CC BY-SA 4.0
