# How to Save Logs from Other Projects

## For Claude Code Sessions in Other Projects

If you're Claude working in another project (like `parentchildcontactsolutions`), here's how to save your session logs to this knowledge pipeline:

### Quick Instructions

1. **When to save**: Before auto-compact, at major milestones, or when the user asks
2. **Where to save**: `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\devlogs\intake\`
3. **Filename format**: `{project-name}_session_{YYYY-MM-DD}_{HHMM}_{brief-topic}.md`

### What to Include in the Log

Use this template:

```markdown
# Session: [Brief Topic]
**Project:** [project name]
**Date:** YYYY-MM-DD
**Time:** HH:MM
**Session Type:** [feature dev / bug fix / refactor / architecture / etc]

## Session Context
[What were we working on? What was the goal?]

## Key Activities
- [Major task 1]
- [Major task 2]
- [etc]

## Technical Decisions Made
- [Decision 1 and rationale]
- [Decision 2 and rationale]

## Code Changes
- [File 1: what changed and why]
- [File 2: what changed and why]

## Learnings & Insights
### What Worked Well
- [Insight 1]
- [Insight 2]

### Challenges Encountered
- [Challenge 1 and how we solved it]
- [Challenge 2 and resolution]

### Human-AI Collaboration Notes
- [What did human do particularly well?]
- [What did Claude do particularly well?]
- [What could be improved?]

## Open Questions / Next Steps
- [Question 1]
- [Next step 1]

## Files Modified
- `path/to/file1.ext`
- `path/to/file2.ext`

## Metadata
- **Total messages:** [approximate count]
- **Duration:** [approximate time]
- **Complexity:** [simple / moderate / complex]
```

### Example Command to Give Claude

Just copy-paste this to your other Claude session:

---

**"Please save our session log to the knowledge pipeline:**

**File:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\devlogs\intake\parentchildcontactsolutions_session_2025-10-05_[topic].md`

**Use the template from:** `C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\claude\HOW_TO_SAVE_LOGS_FROM_OTHER_PROJECTS.md`

**Include:**
- What we worked on
- Technical decisions made
- Code changes and rationale
- What worked well / challenges
- Human-AI collaboration insights
- Next steps

**Be thorough** - this will be reviewed later to extract knowledge for future sessions."

---

## Notes

- Replace `[topic]` with a brief slug like `contact-form-validation` or `database-schema-refactor`
- If the session is still ongoing, that's fine - save what you have so far
- You can update the same file later or create a new timestamped one
- Don't worry about being too verbose - we can distill it later in the pipeline
