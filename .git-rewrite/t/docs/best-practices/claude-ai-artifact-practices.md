---
deia_routing:
  project: deia
  destination: docs/best-practices/
  filename: claude-ai-artifacts.md
  action: move
replaces:
  - filename: claude-ai-artifacts.md
    routing: project=deia-user-level
    reason: Corrected routing to main deia repository
    superseded_date: 2025-10-11
---

# Best Practices: Working with Claude.ai Artifacts

**Version:** 1.0.1  
**Date:** 2025-10-11  
**Replaces:** Earlier version with incorrect routing (project: deia-user-level)  
**Context:** Strategic planning and documentation work  
**Tool:** Claude.ai (Sonnet 4.5) with Projects

---

## 1. Artifact Creation Strategy

### 1.1 Pre-Creation Planning

**Before creating any artifact, complete these steps:**

1. **Define the document purpose** - One clear sentence
2. **Identify target audience** - Who reads this and why
3. **Outline complete structure** - All sections with numbering
4. **Set length target** - Approximate word count
5. **Gather key points** - What must be included
6. **Choose format** - Markdown, React, HTML, etc.

**Why this matters:**
Planning prevents mid-creation restructuring that leads to multiple update cycles and potential loops.

### 1.2 Single-Pass Creation (Preferred)

**Approach:**
Write complete document content in a single `create` call.

**Advantages:**
- No update loops
- Faster completion
- Cleaner artifact history
- Less token usage
- Better final quality

**When to use:**
- Documents under 3,000 words
- Clear structure from planning phase
- Content ready to write straight through

**Example workflow:**
```
User: "Create onboarding doc"
Claude: [Plans structure first]
Claude: [Creates complete artifact in one call]
User: [Reviews and requests specific changes if needed]
```

### 1.3 Incremental Creation (Use Sparingly)

**When acceptable:**
- Very long documents (5,000+ words)
- Iterative design where user provides feedback per section
- Complex code where testing between additions is valuable

**Rules for incremental approach:**
- Complete each section fully before moving to next
- Use `update` to ADD new sections at end
- Never use multiple `update` calls on same text
- If restructuring needed, switch to `rewrite`

### 1.4 Rewrite vs. Update Decision Tree

**Use `rewrite` when:**
- Document needs structural changes
- Multiple sections require modification
- Simpler to provide full new content than surgical edits
- Previous attempts at `update` aren't working

**Use `update` when:**
- Single function/paragraph needs changing
- Exact text match is easy to identify
- Change is truly localized (not affecting structure)
- Only 1-2 update calls needed total

**NEVER:**
- Use 3+ `update` calls on same artifact
- Try to update text that's ambiguous or repeated
- Update when you're not certain of exact match

---

## 2. Common Pitfalls

### 2.1 The Update Loop

**Symptom:**
Multiple update calls trying to modify the same section, each failing or partially succeeding.

**Root cause:**
- Text match is ambiguous
- Trying to restructure via updates
- Not realizing `rewrite` is better option

**Solution:**
Stop after 2 failed updates. Use `rewrite` instead.

### 2.2 Incomplete Planning

**Symptom:**
Starting artifact creation, then realizing structure needs to change mid-way.

**Root cause:**
Skipped planning phase, jumped straight to creation.

**Solution:**
Always plan structure BEFORE creating artifact. Show outline to user if uncertain.

### 2.3 Update Text Mismatch

**Symptom:**
`old_str` doesn't match exactly, update fails or hits wrong location.

**Root cause:**
Whitespace differences, typos, or text appears multiple times.

**Solution:**
- Copy exact text including whitespace
- Make old_str unique enough to match once
- Test mentally: "Does this appear exactly once?"

---

## 3. Documentation-Specific Practices

### 3.1 DEIA Routing Headers

**Always include at document start:**
```yaml
---
deia_routing:
  project: quantum  # or deia-user-level for ~/.deia/
  destination: docs/
  filename: optional-specific-name.md
  action: move  # or copy
---
```

**Routing targets:**
- `project: quantum` → User's Quantum project
- `project: deia-user-level` → `~/.deia/` directory
- `project: deia` → deiasolutions repository

### 3.2 Document Structure Standards

**Use numbered outline format:**
- 1.1, 1.2, 1.3 (user preference)
- Not bullets unless specifically requested
- Hierarchical and scannable

**Include version metadata:**
- Version number (1.0, 1.1, etc.)
- Date created/updated
- Author attribution
- Change log for updates

**Length guidelines:**
- Onboarding/tactical: 1,500-2,000 words
- Strategic/vision: 2,000-3,000 words
- Reference/comprehensive: 3,000-5,000 words

### 3.3 Content Quality

**Brief and focused:**
User prefers concise over verbose. Cut unnecessary words.

**Scannable:**
Headers, numbering, short paragraphs. Easy to skim.

**Actionable:**
Practical next steps, not just philosophy. "Here's what to do."

**Honest:**
Acknowledge limitations, unknowns, work-in-progress status.

---

## 4. Working with Multiple Documents

### 4.1 Document Series Workflow

**When creating 10-20 related docs:**

1. **Plan full series first** - List all doc topics
2. **Create one doc at a time** - Complete, save, move to next
3. **Learn and improve** - Apply lessons from each doc to next
4. **Consistent formatting** - Same structure, same routing approach
5. **Cross-references** - Link docs together as series builds

**Example (current session):**
- Doc 1: Integration Map (complete)
- Doc 2: Developer Onboarding (complete, learned from issues)
- Doc 3: Constitutional Principles (planned with lessons applied)
- Docs 4-20: TBD, will follow same improved process

### 4.2 Version Control Considerations

**User has automated routing:**
- Downloads folder monitored by Python script
- DEIA headers route files automatically
- Claude shouldn't worry about file system
- Focus on content quality and routing header accuracy

**Filename conventions:**
- Use descriptive names in routing header
- Match repository conventions
- Include version number if needed

---

## 5. Interaction Patterns

### 5.1 Plan-First Approach

**Effective pattern:**
```
User: "Create doc about X"
Claude: "Here's my plan: [structure, audience, approach]"
User: "Looks good" or "Change Y"
Claude: [Creates complete artifact]
```

**Why this works:**
- User confirms direction before work
- Avoids creating wrong thing
- Claude has full context for creation
- Reduces need for revisions

### 5.2 Iterative Refinement

**When user requests changes:**
- Small changes (1-2 sections): Use `update`
- Large changes or restructure: Use `rewrite`
- Ask clarifying questions before modifying
- Confirm understanding of requested change

### 5.3 Multi-Bot Coordination

**Current session has multiple Claude instances:**
- **Bot 1 (Claude Code):** Implementation, code, technical
- **This Bot (Claude.ai):** Strategy, docs, planning

**Coordination practices:**
- Clear handoffs between bots
- This bot provides specs, Bot 1 executes
- Don't duplicate work across bots
- User orchestrates, bots respect their lanes

---

## 6. Quality Assurance

### 6.1 Pre-Creation Checklist

Before creating artifact, verify:
- [ ] DEIA routing header prepared
- [ ] Full document structure outlined
- [ ] Key points and examples ready
- [ ] Length target defined
- [ ] User preferences understood (brief, numbered, actionable)
- [ ] Audience clearly identified

### 6.2 Post-Creation Review

After artifact created, check:
- [ ] Routing header present and correct
- [ ] All planned sections included
- [ ] Numbering consistent (1.1, 1.2, not bullets)
- [ ] Length appropriate (not too verbose)
- [ ] Actionable next steps included
- [ ] Version metadata present

### 6.3 User Satisfaction Signals

**Good signs:**
- User says "Let's go" or "Next doc"
- Saves immediately to downloads
- Requests next in series
- Provides positive feedback

**Warning signs:**
- Multiple revision requests
- Asks to start over
- Suggests different approach
- Silence (may indicate dissatisfaction)

---

## 7. Tool-Specific Notes

### 7.1 Claude.ai Projects

**Advantages for documentation work:**
- Long context window (200K tokens)
- Attached documents for reference
- Persistent memory across sessions
- Good for strategic/planning work

**Best practices:**
- Upload key reference docs to project
- Use for vision, architecture, planning
- Keep implementation in Claude Code
- Leverage long context for complex integrations

### 7.2 Artifact Limits

**Be aware:**
- One artifact per response (STRICT)
- Max ~4 update calls before switching to rewrite
- Large artifacts (5K+ words) may need chunking
- Code artifacts have different rules than docs

---

## 8. Lessons Learned (Session 2025-10-11)

### 8.1 Doc 2 Issue: Update Loop

**What happened:**
Tried to modify same section multiple times with `update` calls, got stuck in loop.

**Why it happened:**
After initial `create`, realized content needed restructuring but used small updates instead of `rewrite`.

**Solution:**
For substantial documents, complete in single `create` call OR use `rewrite` immediately when restructuring needed.

**Applied to Doc 3:**
Pre-plan complete structure, create entire document in one call, no incremental updates unless user requests changes.

### 8.2 Success Pattern: Doc 1

**What worked:**
- Thorough planning first
- Complete document structure outlined
- Single creation call with full content
- User saved immediately, moved to next doc

**Replicate this:**
Plan → Create → Review → Next. No loops.

---

## 9. Future Improvements

### 9.1 Potential Enhancements

**Document templates:**
Create reusable templates for common doc types (onboarding, technical spec, vision doc).

**Automated quality checks:**
Script to verify DEIA headers, numbering consistency, length targets.

**Cross-document validation:**
Ensure series maintains consistent voice, structure, references.

### 9.2 Feedback Loop

**After each document:**
- What worked well?
- What caused friction?
- How to improve next time?
- Update this best practices doc

**Meta-learning:**
This document should evolve as we create more docs and discover better practices.

---

## 10. Quick Reference

### Artifact Creation Decision Tree

```
Need to create artifact?
  ↓
Plan structure first
  ↓
Can I write complete content in one pass?
  ↓                              ↓
YES                            NO
  ↓                              ↓
Single `create` call         Ask user if incremental okay
(PREFERRED)                      ↓
  ↓                         If yes: Create + Update at section boundaries
Done                        If no: Plan more, then single create
                                ↓
                            If updates get messy: Switch to `rewrite`
```

### When to Use Each Command

**`create`:** New artifact, complete content ready
**`update`:** 1-2 surgical changes to existing artifact
**`rewrite`:** Restructuring, multiple changes, or after 2+ failed updates

### Document Quality Checklist

- [ ] DEIA routing header present
- [ ] Numbered outline format (1.1, 1.2)
- [ ] Brief and scannable
- [ ] Actionable next steps
- [ ] Version metadata
- [ ] Length appropriate for purpose

---

## Appendix: User Preferences (Dave)

**Communication style:**
- Brief, focused responses
- Numbered outlines, not bullets
- Actionable over philosophical
- Honest about limitations

**Documentation standards:**
- TDD for code (tests first, always)
- Automation over manual steps
- Platform-agnostic design
- Privacy and security first

**Workflow:**
- Question complexity before acting
- "Yes, but..." handling: Stop, answer question, then proceed
- No multiple yes/no questions
- Use A/B/C alternatives

**Projects:**
- DEIA: Knowledge commons for AI coding
- Library Burning: Preserve institutional knowledge
- Boomerang: Intelligent resource circulation
- Quantum: Integration of above projects

---

**Version History:**
- 1.0 (2025-10-11): Initial best practices from Doc 1-2 creation experience

**Next Review:** After Doc 5 (to incorporate more lessons learned)

**Acknowledgments:**
Practices developed during DEIA documentation series, Claude.ai Sonnet 4.5, in collaboration with Dave Eichler.

---

## Document History

### Version 1.0.1 (2025-10-11)
**Sprint:** 2025-Q4-Sprint-02  
**Modified by:** claude-sonnet-4.5 (claude.ai)  
**Changes:** Corrected routing header from `project: deia-user-level` to `project: deia`  
**Reason:** Bot 1 identified incorrect project name; routed to main deia repository instead  
**Details:** Content unchanged, routing metadata only

### Version 1.0 (2025-10-11)
**Sprint:** 2025-Q4-Sprint-02  
**Created by:** claude-sonnet-4.5 (claude.ai)  
**Purpose:** Document best practices for artifact creation based on lessons learned  
**Details:** See docs/sprints/2025-Q4-Sprint-02-changes.md