"""
Template management for DEIA
"""

from pathlib import Path


def get_start_here_template(platform: str) -> str:
    """Get START_HERE.md template"""

    return f"""# DEIA Knowledge Pipeline - Start Here

## Project Overview

This is a **DEIA (Development Evidence & Insights Automation)** pipeline for capturing and sharing learnings from AI-assisted development sessions.

**Your platform:** {platform}

## Quick Start

### 1. Create a session log
```bash
deia log create --topic "your-topic"
```

### 2. Sanitize before sharing
```bash
deia sanitize devlogs/intake/your-session.md
```

### 3. Validate
```bash
deia validate devlogs/intake/your-session_SANITIZED.md
```

### 4. Submit to community
```bash
deia submit devlogs/intake/your-session_SANITIZED.md
```

## Directory Structure

- `devlogs/intake/` - New session logs (before sanitization)
- `devlogs/raw/` - Processed logs
- `devlogs/reviewed/` - Annotated logs with insights
- `devlogs/bok/` - Book of Knowledge entries
- `devlogs/wisdom/` - Meta-findings for publication
- `sanitization-workspace/` - Workspace for sanitizing files (never committed)

## Important Documents

- `SANITIZATION_GUIDE.md` - How to protect your privacy
- `DEIA_CONSTITUTION.md` - Project governance
- `.deia/config.json` - Your local configuration

## Learn More

- GitHub: https://github.com/deiasolutions/deia
- Documentation: [coming soon]
- Community: [coming soon]

---

*"Learn together. Protect each other. Build better."*
"""


def get_session_log_template(session_type: str) -> str:
    """Get session log template"""

    return """# Session: {{{{TOPIC}}}}

**Project:** [Your project name]
**Date:** {{{{DATE}}}}
**Time:** {{{{TIME}}}}
**Session Type:** {{{{TYPE}}}}
**Platform:** [claude-code / cursor / copilot / other]

---

## Session Context

[What were you working on? What was the goal?]

---

## Key Activities

- [Major task 1]
- [Major task 2]
- [Major task 3]

---

## Technical Decisions Made

### Decision 1: [Decision title]

**Rationale:**
[Why did you make this choice?]

**Implementation:**
```
[Code snippet or description]
```

---

## Code Changes

- **File 1:** [What changed and why]
- **File 2:** [What changed and why]

---

## Learnings & Insights

### What Worked Well
- [Insight 1]
- [Insight 2]

### Challenges Encountered
- [Challenge 1 and how you solved it]
- [Challenge 2 and resolution]

### Human-AI Collaboration Notes
- [What did you do particularly well?]
- [What did the AI do particularly well?]
- [What could be improved?]

---

## Open Questions / Next Steps

- [Question or next step 1]
- [Question or next step 2]

---

## Files Modified

- `path/to/file1.ext`
- `path/to/file2.ext`

---

## Pre-Submission Sanitization Checklist

Before sharing this session log publicly, I confirm that I have:

- [ ] Replaced all real names with roles
- [ ] Removed all company/client names
- [ ] Removed all internal URLs and domains
- [ ] Sanitized file paths (no usernames/org names)
- [ ] Removed or genericized proprietary code
- [ ] Checked for API keys, tokens, credentials
- [ ] Removed email addresses
- [ ] Removed IP addresses
- [ ] Ensured no PII/PHI remains
- [ ] Verified I have rights to share this knowledge
- [ ] Run automated sanitizer: `deia sanitize [file]`

**Date sanitized:** [YYYY-MM-DD]

---

## Metadata

- **Total messages:** [approximate count]
- **Duration:** [approximate time]
- **Complexity:** [simple / moderate / complex]
"""


def copy_templates(target_path: Path):
    """Copy template files to target directory"""

    # For now, templates are generated dynamically
    # In production, could copy from package data
    pass
