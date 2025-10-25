---
# Pattern Metadata (YAML frontmatter)
# Required: title, tags, date_added, contributors, status
# Recommended: urgency, platforms, audience, version
# Optional: last_updated, source_project, confidence

title: "Pattern: [Clear and Descriptive Name]"
tags:
  - tag1  # Primary topic (e.g., git, testing, deployment, coordination)
  - tag2  # Secondary topic (e.g., multi-agent, automation, security)
  - tag3  # Context (e.g., python, javascript, windows, cli, devops)
  # Add 3-10 relevant tags total

urgency: medium  # Options: low, medium, high, critical
platforms:
  - Platform-Agnostic  # Or specific: windows, linux, macos, netlify, aws, etc.
audience:
  - developers  # Who benefits? developers, designers, admins, devops, all, etc.

date_added: YYYY-MM-DD  # Date you created this pattern
last_updated: YYYY-MM-DD  # Optional: Date of last significant change
contributors:
  - Your Name or Handle  # Your name, GitHub username, or agent ID
status: active  # Options: active, deprecated, experimental
version: 1.0  # Start with 1.0, increment for major changes
confidence: Experimental  # Optional: Experimental, Validated, Proven
source_project: project-name  # Optional: Which project discovered this?
---

# Pattern: [Clear and Descriptive Name]

**One-sentence summary of what this pattern does and why it matters.**

---

## Context

When should you use this pattern?

**Use this pattern when:**
- Situation A (specific scenario)
- Situation B (another scenario)
- Problem C that this solves

**NOT for:**
- When this pattern doesn't apply
- Alternative approaches are better
- Specific constraints that make this inappropriate

---

## Problem

**What problem does this solve? Why is it important?**

Be specific about:
- What goes wrong without this pattern?
- What pain point does it address?
- Why existing solutions don't work?
- Who experiences this problem?
- How often does this problem occur?

**Example problem scenario:**
> [Describe a concrete situation where this problem manifests]

---

## Solution

**How to implement this pattern (step-by-step):**

### Step 1: Preparation

[Describe what needs to be set up first]

```bash
# Setup commands (if applicable)
command --option value
```

**What this does:** [Explain the command]

---

### Step 2: Implementation

[Describe the main implementation]

```python
# Code example (use appropriate language)
def example_function():
    """
    Clear docstring explaining what this does
    """
    # Implementation with comments
    result = do_something()
    return result
```

**Key points:**
- Explain important details
- Note any gotchas or traps
- Clarify non-obvious choices

---

### Step 3: Verification

[How to test that it works]

```bash
# Verification commands
test-command --verify
```

**Expected output:**
```
[Show what success looks like]
```

---

### Step 4: [Additional Steps as Needed]

[Continue with more steps if necessary]

---

## Examples

### Example 1: Common Use Case

**Scenario:** [Describe a typical situation where this pattern applies]

**Before (without pattern):**
```python
# Show the problem
old_approach()  # This has issues
```

**After (with pattern):**
```python
# Show the solution
new_approach()  # This fixes the problem
```

**Result:** [Explain what happens and why it's better]

---

### Example 2: Edge Case or Variation

**Scenario:** [Describe a less common but important case]

**Implementation:**
```python
# Variation of the pattern for this specific case
variant_approach()
```

**Result:** [Explain outcome]

---

### Example 3: Real-World Usage (Optional)

**Project:** [Project name or description]

**Challenge:** [What problem they faced]

**Solution:** [How they applied this pattern]

**Outcome:** [Results achieved]

---

## Testing

**How to verify the pattern works correctly:**

### Test 1: Basic Functionality
```bash
# Command to test basic case
test-basic-case
```
**Expected:** [What should happen]

### Test 2: Edge Cases
```bash
# Command to test edge cases
test-edge-case
```
**Expected:** [What should happen]

### Test 3: Failure Modes
```bash
# Test what happens when things go wrong
test-failure-handling
```
**Expected:** [How it should fail gracefully]

---

## Variations

**Alternative approaches or modifications:**

### Variation A: For Situation X

When you encounter [specific situation], modify the pattern:
- Change: [What to modify]
- Reason: [Why this variation is needed]

```python
# Modified implementation
variation_a()
```

---

### Variation B: Alternative Approach Using Z

Instead of [main approach], you can use [alternative]:
- Pros: [Benefits of this variation]
- Cons: [Drawbacks of this variation]

```python
# Alternative implementation
variation_b()
```

---

## Related Patterns

**Patterns that work well with this one:**
- [Pattern Name](../path/to/pattern.md) - [How it relates]
- [Pattern Name](../path/to/pattern.md) - [When to use together]

**Alternative patterns:**
- [Pattern Name](../path/to/pattern.md) - [When to use instead]

**Supersedes:**
- [Old Pattern Name](../path/to/old-pattern.md) - [Why this is better]

---

## References

**External documentation:**
- [Official Docs](https://example.com/docs) - Relevant official documentation
- [Tool Homepage](https://example.com/tool) - Related tools

**Further reading:**
- [Article Title](https://example.com/article) - Deeper dive into concepts
- [Research Paper](https://example.com/paper) - Academic background (if applicable)

**Tools and libraries:**
- [Tool Name](https://example.com/tool) - Installation and usage
- [Library Name](https://example.com/library) - Related libraries

---

## Evidence

**Projects using this pattern:**
- [Project Name] (Date - Status)
- [Project Name] (Date - Status)

**Metrics and validation:**
- [Metric 1]: Improved by [X%]
- [Metric 2]: Reduced from [A] to [B]
- [Metric 3]: Success rate of [Y%]

**Confidence level:**
- **Experimental:** Tried once, seems to work, needs more validation
- **Validated:** Used in 2-3 projects, proven effective
- **Proven:** Used across 5+ projects, well-established

---

## Notes

**Additional context, gotchas, or tips:**

### Gotcha 1: [Common Mistake]
**Problem:** [What goes wrong]
**Solution:** [How to avoid it]

### Gotcha 2: [Edge Case]
**Problem:** [What to watch out for]
**Solution:** [How to handle it]

### Performance Considerations
[Any performance implications or optimization tips]

### Security Considerations
[Any security concerns or best practices]

### Maintenance Notes
[How to maintain or update this pattern over time]

---

## Author Notes

**Origin story (optional):**
[How this pattern emerged, what problem led to discovering it, lessons learned while developing it]

**Acknowledgments (optional):**
[Credit to people, projects, or resources that inspired or contributed to this pattern]

**Changelog (optional):**
- **v1.0** (YYYY-MM-DD): Initial pattern
- **v1.1** (YYYY-MM-DD): Added variation B
- **v2.0** (YYYY-MM-DD): Major revision - [what changed]

---

**Author:** [Your Name or ID]
**Date:** YYYY-MM-DD
**License:** CC0-1.0 (Public Domain)

---

## Pattern Quality Checklist

**Before submitting, verify:**

### Required (All Must Pass)
- [ ] **Completeness** - All essential information included?
  - [ ] Clear title with pattern type prefix
  - [ ] 2-3 sentence summary
  - [ ] Problem statement
  - [ ] Step-by-step solution
  - [ ] At least one working example
  - [ ] All required YAML fields (title, tags, date_added, contributors, status)

- [ ] **Clarity** - Easy to understand and follow?
  - [ ] Written in clear, concise language
  - [ ] Proper grammar and formatting
  - [ ] Logical structure (problem → solution → example)
  - [ ] Technical terms defined
  - [ ] No ambiguous references

- [ ] **Accuracy** - Technically correct and tested?
  - [ ] Code examples compile/run (if code included)
  - [ ] No misleading statements
  - [ ] Proper attribution for external sources
  - [ ] Caveats and limitations documented

- [ ] **Reusability** - Applicable beyond single use case?
  - [ ] General approach, not project-specific implementation
  - [ ] Describes pattern, not one-off solution
  - [ ] Clear applicability scope
  - [ ] Works across similar situations

- [ ] **Unique Value** - Not duplicating existing patterns?
  - [ ] Searched BOK directory for similar patterns
  - [ ] Checked master-index.yaml for duplicates
  - [ ] Adds new knowledge or perspective
  - [ ] Fills a gap (not redundant)

- [ ] **Safety & Ethics** - No harmful or sensitive content?
  - [ ] NO PII (names, emails, addresses, phone numbers)
  - [ ] NO secrets (API keys, passwords, tokens)
  - [ ] NO malicious code or exploits
  - [ ] NO proprietary information (internal URLs, company names)
  - [ ] Appropriate disclaimers for risky patterns

### Recommended (Nice to Have)
- [ ] **Evidence** - Metrics or validation provided
- [ ] **Related Patterns** - Cross-references to similar patterns
- [ ] **Variations** - Alternative approaches documented
- [ ] **Testing** - Verification steps included
- [ ] **Images/Diagrams** - Visual aids for complex concepts
- [ ] **Real-world examples** - Concrete usage from projects

### Sanitization Check
- [ ] All real names replaced with `<YOUR_NAME>` or generic names
- [ ] All email addresses replaced with `user@example.com`
- [ ] All API keys replaced with `YOUR_API_KEY_HERE`
- [ ] All passwords replaced with `your-secure-password`
- [ ] All internal URLs replaced with `https://example.com`
- [ ] All company names replaced with `AcmeCorp` or `<YOUR_COMPANY>`
- [ ] All IP addresses replaced with `192.0.2.1` or `example.com`

---

## Submission Instructions

Once your pattern is complete:

### 1. Save This File
```bash
# Save with descriptive name
my-pattern-name.md
```

### 2. Create Intake Directory
```bash
# Create dated submission folder
mkdir -p .deia/intake/$(date +%Y-%m-%d)/my-pattern-name
mv my-pattern-name.md .deia/intake/$(date +%Y-%m-%d)/my-pattern-name/
```

### 3. Create MANIFEST.md
Create `.deia/intake/YYYY-MM-DD/my-pattern-name/MANIFEST.md`:

```markdown
# Submission Manifest

**Title:** [Your Pattern Title]
**Category:** [Pattern|Anti-Pattern|Process|Platform-Specific|Methodology]
**Tags:** tag1, tag2, tag3
**Author:** [Your Name or Agent ID]
**Date:** YYYY-MM-DD
**Confidence:** [Experimental|Validated|Proven]

---

## Summary

[2-3 sentences explaining your pattern]

---

## Why This is Valuable

[Explain what gap this fills, who benefits, why it should be in BOK]

---

**Ready for review:** Yes
```

### 4. Submit
```bash
# Commit and push (if you have access)
git add .deia/intake/
git commit -m "docs(bok): Submit pattern - [Pattern Title]"
git push

# OR create Pull Request
# OR create GitHub Issue with bok-submission tag
```

### 5. Wait for Review
- Master Librarian reviews within 24-48 hours
- You'll receive feedback or acceptance
- Pattern integrated to BOK and indexed

---

**Need help?** See [Pattern Submission Guide](../docs/guides/PATTERN-SUBMISSION-GUIDE.md)

**Questions?** Create GitHub Issue with tag: `bok-submission-question`

---

**Thank you for contributing to the DEIA Body of Knowledge!**

Your pattern will help developers save time, avoid mistakes, and build better AI-assisted systems.

---

*Template Version: 1.0*
*Last Updated: 2025-10-18*
*Maintained By: DEIA Documentation Team*
