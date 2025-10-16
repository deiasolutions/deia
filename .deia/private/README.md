# .deia/private/ - Project-Level Private Space

**This directory is gitignored and will never be committed.**

## Purpose

Per-user, per-project private workspace. Every DEIA user can use this for:

### 1. Draft Submissions (before sanitization)
- Bug reports with real error messages
- Patterns with company-specific examples
- Test cases with real data

**Flow:** Draft here → Sanitize → Move to `.deia/submissions/`

### 2. Personal Project Notes
- Architecture decisions with private context
- Technical debt notes with customer/company details
- Performance observations with real metrics
- Ideas/experiments not ready to share

### 3. Unsanitized Conversation Logs
- Full AI transcripts with real code
- Debugging sessions with real data
- Crash recovery logs
- **Never shared to DEIA Global - local insurance only**

### 4. Sensitive Pattern Variations
- Company-specific implementations
- Domain-specific solutions with proprietary context
- Team patterns that reveal too much to publish

### 5. Personal Learning Journal
- What you learned debugging
- Mistakes made (private reflection)
- AI interaction quality notes

## Structure

```
.deia/private/
├── logs/           # Unsanitized conversation logs
├── drafts/         # Pre-sanitization submissions
├── notes/          # Personal project notes
└── experiments/    # Private experiments/ideas
```

## Sanitization Workflow

1. **Draft** in `private/drafts/[item].md`
2. **Sanitize** with `deia sanitize --input private/drafts/[item].md --output submissions/[item].md`
3. **Review** sanitized version in `.deia/submissions/`
4. **Submit** to DEIA Global when ready

## Privacy Guarantee

- This directory is **always gitignored**
- Never synced to DEIA Global
- Local to your machine only
- Safe space for messy, unsanitized work

## Multi-User Note

Each user gets their own `private/` space in the project `.deia/` directory. This is YOUR private workspace for THIS project.
