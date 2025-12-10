---
title: "Case Study: LLM Name Hallucination and Privacy Violation Risk"
date: 2025-10-16
severity: Critical
category: AI Safety / Privacy
contributed_by: DEIA Project
llm: Claude Sonnet 4.5
tags: [hallucination, privacy, doxxing-risk, ai-safety, case-study]
license: CC BY 4.0
---

# Case Study: LLM Name Hallucination and Privacy Violation Risk

## Summary

During documentation work, an LLM hallucinated a complete real-world name for a user who consistently operated under a pseudonym, creating a potential privacy violation (doxxing risk). The incident was caught before publication through review processes.

## What Happened

While creating documentation for a deployment, the LLM (Claude) attributed work to a hallucinated full real-world name despite:
- User consistently identifying with a GitHub handle/pseudonym
- No prior mention of any real-world name in conversation history
- User explicitly operating under pseudonym for privacy reasons

**Files affected:** Technical documentation files with `discovered_by:` metadata fields

**Example hallucination:**
```markdown
discovered_by: [Real Name] (self-identified)
```

**Reality:** User never provided this name; it was completely fabricated.

## Timeline

1. LLM created documentation with attribution
2. User reviewed and immediately caught the error: "Who is [Name]? I'm [github-handle]"
3. LLM corrected files to use pseudonym
4. User requested formal incident logging
5. Incident documented with prevention measures

## Root Cause

**Primary:** LLM hallucination with unknown source
- Possible training data associations (some GitHub profiles show real names)
- Pattern matching on username/folder paths
- No actual source for the fabricated name

**Contributing factor:** No validation or confirmation before attributing identity

## Why This Is Critical

1. **Privacy violation** - Exposed potential real-world identity without consent
2. **Doxxing risk** - Could have been published to public repo
3. **Complete fabrication** - Name had zero basis in conversation
4. **Professional harm** - User uses pseudonym professionally
5. **Trust violation** - User expects pseudonymity to be respected

## Impact Assessment

**Actual:** Low (caught before publication, corrected immediately)

**Potential:** High (if published and propagated)

**If published:**
- Privacy violation documented in Git history
- Difficult to fully retract (Git is permanent)
- Reputational damage to project
- Loss of user trust
- Potential legal/ethical issues

## Prevention Measures Implemented

### Immediate
1. **Default to pseudonyms** - Always use GitHub handles or "User" unless explicit consent
2. **Never assume identity** - Don't infer real names from usernames
3. **Explicit consent required** - Ask before using any real-world identifiers

### Process Changes
1. **Attribution validation in doc templates**
   - Use `contributor: [github-handle]` format
   - No real names without explicit consent

2. **Pre-commit hook (proposed)**
   - Detect potential PII in documentation
   - Flag for review before commit

3. **Review process**
   - All AI-generated content reviewed for hallucinated personal info
   - Special attention to attribution fields

### LLM Instructions (Added)
```markdown
## Identity Attribution Rules

NEVER use real-world names unless:
1. User explicitly provided it in current session
2. User gave explicit permission to use it
3. It appears in committed code with user's approval

ALWAYS use:
- GitHub handles (e.g., daaaave-atx)
- Generic terms (e.g., "User", "Contributor")
- Project roles (e.g., "Project Lead")

IF unsure about name/identity:
- Ask: "How should I attribute this work?"
- Don't fabricate or infer
```

## Lessons Learned

1. **Pseudonymity is a boundary** - Must be respected absolutely
2. **Hallucinations can be dangerous** - Not just technical errors
3. **Attribution needs verification** - Can't trust LLM to "know" identity
4. **Privacy by default** - Use handles unless told otherwise
5. **Git is permanent** - Privacy violations in commits are hard to undo

## Applicable Contexts

This pattern applies to any project where:
- Contributors use pseudonyms/handles
- LLMs generate documentation with attribution
- Privacy is a concern
- Multiple contributors with varying identity preferences

## Related Patterns

- ✅ **Good:** Always use GitHub handles for attribution
- ✅ **Good:** Explicit consent before using real-world identifiers
- ❌ **Bad:** Assuming real names from usernames
- ❌ **Bad:** LLM hallucinating personal details

## Recommended Safeguards

1. **For LLM Operators:**
   - Include identity/privacy guidelines in system prompts
   - Review all attribution before publication
   - Default to most conservative option (pseudonym)

2. **For Projects:**
   - Document contributor identity preferences
   - Use CONTRIBUTORS.md with preferred attribution
   - Implement pre-commit hooks for PII detection

3. **For AI Systems:**
   - Flag when generating personal information
   - Require confirmation for identity attribution
   - Log all identity-related decisions for audit

## Discussion Questions

1. How can LLMs be trained to better respect pseudonymity?
2. Should identity attribution always require human confirmation?
3. What's the right balance between attribution and privacy?
4. How do we handle cases where training data contains privacy violations?

---

**Contributed to DEIA Global Commons:** 2025-10-16
**Original Incident:** Internal project deployment
**Sanitized for public sharing:** Specific project details removed

**License:** CC BY 4.0 International
**Status:** Published Case Study

**Tags:** `#case-study` `#ai-safety` `#privacy` `#hallucination` `#llm-incident`
