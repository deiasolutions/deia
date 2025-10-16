---
type: process_improvement
title: '[PROCESS] Add BOK documentation to Communications Director role in iDea Method'
labels: process, enhancement, documentation
submitted_by: BOT-00003 (Drone-Integration)
submitted_date: 2025-10-11
---

## Current Process Gap

**What process is missing or insufficient:**

The iDea Method documentation mentions "documentation" as a core responsibility for the Communications Director AI role, but doesn't explicitly distinguish between:
1. **Project documentation** (ADRs, insights logs, changelog)
2. **BOK documentation** (platform-specific patterns, gotchas, best practices)

This gap means AI assistants might not realize that documenting platform quirks in the Book of Knowledge is part of their responsibility.

## Problem / Impact

**What goes wrong because of this gap:**

- AI assistants discover platform-specific issues (like Windows/Git Bash path conversion) but don't document them in BOK
- Institutional knowledge gets lost instead of captured for future reference
- Future developers hit the same issues repeatedly
- The BOK doesn't grow organically during development work
- Pattern documentation feels like "extra work" rather than part of normal workflow

**Who is affected:**
- [x] DEIA developers
- [x] DEIA users
- [x] AI assistants (Claude, etc.)
- [x] Contributors
- [ ] Other:

## Proposed Improvement

**What should be added or changed:**

Add explicit mention in the iDea Method that the **Communications Director** AI role includes BOK documentation responsibilities alongside project documentation.

**How it would work:**

1. **Update iDea Method documentation** (`bok/methodologies/idea-method.md`)
   - Section: "AI Team Member (Developer)" lines 31-37
   - Add to Communications Director role: "Documents decisions AND platform patterns in BOK"

2. **Expand "Documentation-Driven Development" section** (lines 165-193)
   - Add subsection: "BOK Documentation"
   - When: During implementation when discovering platform quirks
   - What: Platform-specific patterns, workarounds, gotchas
   - Where: `bok/platforms/[platform]/` or `bok/patterns/[category]/`

3. **Update Implementation Phase checklist** (line 103)
   - Change: `[Implement] → [Test] → [Document] → [Cleanup] → [Commit]`
   - To: `[Implement] → [Test] → [Document (Project + BOK)] → [Cleanup] → [Commit]`

4. **Add to "Effort Factors" in prioritization** (already exists at line 339, but clarify)
   - Documentation needs include both project docs AND BOK when discovering new patterns

## Examples

**Where this gap caused issues (if applicable):**

- **Actual example from today (2025-10-11):**
  - BOT-00003 implemented `deia /` command
  - Discovered Windows/Git Bash MSYS path conversion issue
  - User asked: "Do we have a .deia practice written so we know if the windows git bash path issues and dont run into it again?"
  - Answer was NO - because BOK documentation wasn't explicitly called out as part of the implementation workflow
  - I then created `bok/platforms/shells/windows-git-bash-path-conversion.md` retroactively
  - This should have been done as part of Step 6 (File completion report), not as a separate follow-up

**How similar projects handle this:**

- **Stripe Engineering:** Documentation is part of "Definition of Done" for any feature
- **GitLab:** "Document everything" principle includes both user-facing docs and internal patterns
- **Thoughtbot Playbook:** "Document as you go" includes both project decisions and reusable patterns

## Implementation Checklist

- [ ] Document the new process (update `bok/methodologies/idea-method.md`)
- [ ] Create templates/tools to support it (BOK pattern template already exists in CONTRIBUTING.md)
- [ ] Update CONTRIBUTING.md (add section on "When to Document in BOK vs Project Docs")
- [ ] Add to CI/CD if applicable (N/A - this is process guidance)
- [ ] Announce to contributors (via CHANGELOG or docs update note)

## Success Criteria

**How we'll know this improvement is working:**

- BOK grows organically during normal development work
- Platform-specific patterns are documented when discovered, not retroactively
- AI assistants proactively document patterns without being asked
- Completion reports reference BOK documentation created during implementation
- Fewer duplicate platform issues encountered by different developers

---

**For DEIA Maintainers:**
- [ ] Process improvement approved
- [ ] Documentation created
- [ ] Tools/templates created (already exist, may need clarification)
- [ ] CONTRIBUTING.md updated
- [ ] Team notified

---

**Related Work:**
- Completion report: `.deia/reports/BOT-00003-slash-command-complete.md`
- BOK documentation created: `bok/platforms/shells/windows-git-bash-path-conversion.md`
- BOK documentation report: `.deia/reports/BOT-00003-documentation-windows-git-bash.md`
