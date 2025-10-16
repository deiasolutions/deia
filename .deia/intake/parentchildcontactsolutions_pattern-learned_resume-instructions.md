# Pattern Learned: Resume Instructions Document

**Project:** Family Bond Bot (parentchildcontactsolutions)
**Date:** 2025-10-05
**Pattern:** How to give humans resume instructions for AI sessions

---

## The Mistake

**What Claude did wrong:**
Gave Dave multi-step instructions verbally:
1. "Read file A"
2. "Then read file B"
3. "Then ask this question"

**Why this was wrong:**
- Multi-step instructions to humans are dangerous
- Human has to remember/track multiple things
- Human has to copy long file paths multiple times
- Violates Rule 7: Think Ahead

**Dave's feedback:**
> "Multi-step instructions to a human are dangerous. Especially when you can give those instructions in a document you save for claude."

---

## The Correct Pattern

**Create a single resume instructions document** that contains:
1. ALL the steps Claude needs to follow
2. Full file paths for all documents
3. Short filenames (if applicable)
4. What to do based on different scenarios

**Then give human ONLY:**
- Full path to that ONE document
- Short filename for that document

---

## Implementation Example

**Wrong (what Claude did):**
```
Read:
1. C:\Users\...\final-update.md
2. C:\Users\...\CONSTITUTION.md
Then ask: "Did the test work?"
```

**Correct (what Claude should do):**

Create `RESUME_INSTRUCTIONS.md` containing all steps, then tell human:

**Full path:**
`C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\RESUME_INSTRUCTIONS.md`

**Short name (if in project directory):** `RESUME_INSTRUCTIONS.md`

**That's it.** One file path, one short name, done.

---

## Why This Matters

**Cognitive load:**
- Humans shouldn't have to hold multi-step instructions in memory
- Humans shouldn't have to copy multiple long paths
- Humans shouldn't have to track "what comes next"

**Error prevention:**
- If human forgets step 2, session starts wrong
- If human copies wrong path, session starts wrong
- If instructions are in a doc, Claude can't forget them

**Respect:**
- Don't make humans do work AI can do
- Put the complexity in the document, not in the human's head

---

## Application to DEIA Solutions

When you (DEIA Solutions Claude) finish a session and need to tell Dave how to resume:

1. **Create `RESUME_INSTRUCTIONS.md`** in your project
2. **Put ALL resume steps in that document**
3. **Give Dave ONE file path** (full + short)
4. **Done**

Don't give Dave a list of steps. Put the list IN a document and give him the document path.

---

## Constitutional Rule Candidate

This pattern should probably be added to both constitutions:

**Rule: Single-Document Resume Instructions**
- When ending a session, create a resume instructions document
- Give human only ONE file path to that document
- Never give multi-step verbal instructions for session resume
- Exception: If resume is trivial ("just read PROJECT_RESUME.md"), one step is fine

**Rationale:** Multi-step instructions waste human cognitive load and increase error risk.

---

## File Created

**Location:** `C:\Users\davee\OneDrive\Documents\GitHub\familybondbot\RESUME_INSTRUCTIONS.md`

**Contains:**
- Step 1: Read final-update.md (with full path)
- Step 2: Read CONSTITUTION.md (with full path + short name)
- Step 3: Ask one question about /folders test
- Additional context if needed

**Human now has ONE file to give Claude, not three steps to remember.**

---

**Pattern documented for BOK extraction.**
