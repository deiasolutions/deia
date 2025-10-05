# DEIA Session Resume Instructions

**Created:** 2025-10-05 (Updated after MUDA/meta-ROTG discussion)
**Status:** VS Code glitching, safe restart point

---

## Critical Documents Created This Session

**Read these in order:**

### 1. START_HERE.md
**Full path:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\START_HERE.md`

Your foundation - what DEIA is and how it works.

---

### 2. META_ROTG.md ⭐ NEW & IMPORTANT
**Full path:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\META_ROTG.md`

**Why this matters:**
This changes how you make decisions. Read this BEFORE asking Dave questions.

**Key concepts:**
- MUDA framework (minimize waste)
- When to ask vs decide
- Question taxonomy
- Agent communication protocols

**Apply this to every decision.**

---

### 3. IDEAS_CAPTURE.md ⭐ NEW
**Full path:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\IDEAS_CAPTURE.md`

**All ideas from this session:**
- Multi-domain DEIA expansion (not just coding!)
- Non-profit foundation structure
- Platform vendor collaboration
- 16 major concepts captured
- Priority order based on MUDA

**This is your context dump. Everything we discussed is here.**

---

### 4. WORKING_DECISIONS.md (Updated)
**Full path:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\WORKING_DECISIONS.md`

**What's new:**
- Section 10: Long-term governance & foundation
- Section 11: Multi-domain expansion vision
- All open questions tracked

---

## What We Built This Session

### Documents (25+ files created):
- Constitution (DEIA_CONSTITUTION.md)
- Security Architecture (SECURITY_ARCHITECTURE.md)
- Sanitization Guide (SANITIZATION_GUIDE.md)
- Sanitization Workflow (SANITIZATION_WORKFLOW.md)
- Python CLI tool (complete, in src/deia/)
- Package config (pyproject.toml)
- README.md for package
- META_ROTG.md (decision framework)
- IDEAS_CAPTURE.md (all session ideas)
- Multiple session logs and reviews

### Python CLI Tool:
```
src/deia/
├── __init__.py
├── cli.py          (Click interface)
├── core.py         (init, create, sanitize)
├── sanitizer.py    (automated PII/secret detection)
├── validator.py    (pre-submission checks)
├── bok.py          (search and sync)
├── config.py       (configuration)
└── templates.py    (template generation)
```

**Status:** Functional, ready for testing

### Git Repository:
- Initialized with IP protection (.gitignore)
- All work committed
- Safe to restart VS Code

---

## Where We Are

### Completed:
✅ DEIA Constitution with biometric auth
✅ Security architecture
✅ Sanitization guide and workflow
✅ Python CLI tool (v0.1.0)
✅ Cross-project pipeline validated (FamilyBondBot session reviewed)
✅ 8 BOK entries identified
✅ Foundation governance structure designed
✅ Multi-domain expansion vision captured
✅ MUDA decision framework established
✅ meta-ROTG created

### Next Priorities (MUDA-Optimized):

**Priority 1: Answer Constitutional Questions**
- From: `devlogs/intake/parentchildcontactsolutions_questions-from-the-field_2025-10-05.md`
- Why first: Defines what DEIA is, prevents rework
- Questions:
  1. What are "production" equivalents for DEIA Solutions?
  2. What needs biometric protection beyond constitution?
  3. DEIA-specific rules (inclusive language, cultural sensitivity)?
  4. Human-AI collaboration patterns in DEIA work?
  5. Error handling for sensitive topics?

**Priority 2: Extract 8 BOK Entries**
- From FamilyBondBot session review
- Validates BOK format
- Creates examples for community

**Priority 3: Build Public GitHub Repo**
- After constitutional answers (prevents restructure)
- After BOK format validated (prevents rework)

---

## Context: The Big Realization

**From Dave (this session):**

> "What if we had AI helping a researcher, and his AI could upload a best practice, like a lab technique that someone found that worked. Shit ANY domain where people are using AI to do things, there is the opportunity to learn from the work."

**DEIA isn't just for coding.**

It's foundational infrastructure for how humanity learns to collaborate with AI across:
- Coding
- Research
- Writing
- Design
- Healthcare
- Legal
- Education
- Business
- ... ANY domain

**Gap identified:**
- MIT/Microsoft have top-down research
- DEIA provides bottom-up practitioner knowledge
- Cross-domain learning
- Privacy-preserving sharing

**Nobody else is doing this.**

---

## Applying META_ROTG

**Before asking Dave anything:**

1. **MUDA check:**
   - Will this question create waste?
   - Can I find answer in documents?
   - Can I decide with current info?

2. **Question taxonomy:**
   - Is this scope/choice/information/validation/permission/preference?
   - Is it valid for this type?

3. **Think 6 moves ahead:**
   - What downstream impacts?
   - What rework does this prevent?

4. **If must ask:**
   - State recommendation
   - Show reasoning
   - Make response easy (y/n)

**Example:**
- ❌ "What should we work on next?"
- ✅ "Based on MUDA analysis, I recommend answering constitutional questions first (prevents rework on templates). Approve? (y/n)"

---

## When You Resume

**Step 1:** Read META_ROTG.md (decision framework)

**Step 2:** Read IDEAS_CAPTURE.md (all context)

**Step 3:** Read constitutional questions file:
`C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\devlogs\intake\parentchildcontactsolutions_questions-from-the-field_2025-10-05.md`

**Step 4:** Apply MUDA framework:
- Recommend starting with Question 1 (production equivalents)
- Explain why (foundation for security architecture)
- Make it easy for Dave to approve

**Don't ask "what next?" - use MUDA to decide, then get approval.**

---

## Files in This Directory

**Core documents:**
- START_HERE.md
- DEIA_CONSTITUTION.md
- SECURITY_ARCHITECTURE.md
- SANITIZATION_GUIDE.md
- SANITIZATION_WORKFLOW.md
- META_ROTG.md ⭐
- IDEAS_CAPTURE.md ⭐
- WORKING_DECISIONS.md
- RESUME_INSTRUCTIONS.md (this file)

**Code:**
- pyproject.toml
- src/deia/ (Python package)
- README.md

**Session logs:**
- devlogs/intake/ (multiple files)
- devlogs/raw/ (reviews)

**Git:**
- .gitignore (IP protection)
- .git/ (initialized, work committed)

---

## Important Pattern Learned

**Single-document resume instructions:**

Don't give multi-step instructions to human.
Create ONE document with ALL steps.
Give ONE file path.

**You're following this pattern right now.**

---

**Everything is saved. Safe to restart VS Code.**

**Next session starts with:**
1. Read this file (RESUME_INSTRUCTIONS.md) - you're reading it now
2. Apply MUDA framework
3. Present recommendation for what Claude can do autonomously
4. Identify what requires Dave's decision

---

## What CLAUDE Can Do Autonomously (No Dave Decision Needed)

Based on MUDA framework and meta-ROTG:

✅ **Extract 8 BOK Entries**
- From FamilyBondBot session review (already analyzed)
- Create files in `devlogs/bok/`
- Follow BOK template format
- Claude knows what to extract, just needs to do it

✅ **Create BOK Entry Template**
- Define standard format for BOK entries
- Based on examples we discussed
- YAML frontmatter + markdown content

✅ **Write Documentation**
- CONTRIBUTING.md (how to submit)
- CODE_OF_CONDUCT.md (community standards)
- Technical docs for CLI tool

✅ **Code Improvements**
- Bug fixes in Python CLI
- Additional sanitization patterns
- Validator improvements

---

## What Requires DAVE'S Decision

Based on constitutional questions and strategic direction:

🔴 **Constitutional Questions (MUST ask Dave)**
From: `devlogs/intake/parentchildcontactsolutions_questions-from-the-field_2025-10-05.md`

1. **What are "production" equivalents for DEIA Solutions?**
   - What operations require explicit approval?
   - Publishing? BOK updates? Documentation?

2. **What needs biometric protection beyond constitution?**
   - Client data? BOK structure? Brand identity?

3. **DEIA-specific rules needed?**
   - Inclusive language requirements?
   - Cultural sensitivity guidelines?
   - Representation standards?

4. **Human-AI collaboration patterns in DEIA work?**
   - Where should AI decide autonomously?
   - Where should AI ask for guidance?

5. **Error handling for sensitive topics?**
   - How to correct mistakes in DEIA work?

🔴 **Strategic Direction (MUST ask Dave)**
- Which domain to add after coding? (research vs writing vs other)
- When to form non-profit foundation?
- When to approach vendors (Vercel, Railway)?
- Licensing decisions for sensitive domains

🔴 **Git Workflow (NEW - MUST ask Dave)**
- Push/pull request process
- Public repo vs local repo relationship
- How updates propagate
- Review and merge process

---

## Recommended Session Flow (When You Resume)

### Claude's Opening Move:

**Don't ask:** "What should we work on?"

**Do say:**
> "I've read RESUME_INSTRUCTIONS.md, META_ROTG.md, and IDEAS_CAPTURE.md.
>
> **My recommendation based on MUDA analysis:**
> I can autonomously extract the 8 BOK entries from the FamilyBondBot session while you're thinking about the constitutional questions. This prevents blocking and maximizes parallel work.
>
> Then we tackle constitutional questions together (requires your domain expertise).
>
> Approve? (y/n)"

### If Dave approves:
1. Claude extracts BOK entries (autonomous work)
2. Claude presents BOK entries for review
3. Move to constitutional questions (Dave's decisions)

### If Dave has other priorities:
1. Listen to Dave's direction
2. Apply MUDA to proposed approach
3. Recommend optimization if applicable
4. Execute

---

## Critical Files for Next Session

**This file (RESUME_INSTRUCTIONS.md) has everything you need.**

But if you want supporting context:
- META_ROTG.md - Decision framework
- IDEAS_CAPTURE.md - All session ideas
- WORKING_DECISIONS.md - Open questions (including new Git workflow question)

---

*Local git repo committed. Safe to restart VS Code.*

**When Dave says "Read RESUME_INSTRUCTIONS.md" - that's THIS file. You'll know what to do.**
