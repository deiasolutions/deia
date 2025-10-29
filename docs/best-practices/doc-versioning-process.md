---
deia_routing:
  project: deia
  destination: docs/best-practices/
  filename: documentation-versioning.md
  action: move
replaces:
  - filename: documentation-versioning.md
    routing: project=deia-user-level
    reason: Corrected routing to main deia repository
    superseded_date: 2025-10-11
---

# DEIA Documentation Versioning & Change Tracking

**Version:** 1.0.1  
**Date:** 2025-10-11  
**Replaces:** Earlier version with incorrect routing (project: deia-user-level)  
**Purpose:** Establish standards for tracking document changes, versions, and sprint activities

---

## 1. Document Versioning Standards

### 1.1 Version Number Format

**Semantic versioning for documents:**
- **Major (X.0):** Complete restructure, new purpose, breaking changes
- **Minor (X.Y):** New sections, substantial additions, significant corrections
- **Patch (X.Y.Z):** Typo fixes, clarifications, formatting only

**Examples:**
- 1.0 → 1.1: Added new section on hallucination checks
- 1.1 → 2.0: Completely rewrote for different audience
- 1.1.0 → 1.1.1: Fixed typos in section 3

### 1.2 Version Metadata Location

**In document header (YAML frontmatter if applicable, or top of doc):**
```yaml
---
version: 1.1
last_updated: 2025-10-11
change_summary: Added hallucination check to quality checklist
sprint: 2025-Q4-Sprint-02
modified_by: claude-sonnet-4.5 (claude.ai)
change_log: see docs/sprints/2025-Q4-Sprint-02-changes.md
---
```

### 1.3 In-Document Change History

**At bottom of every document:**
```markdown
---

## Document History

### Version 1.1 (2025-10-11)
**Sprint:** 2025-Q4-Sprint-02  
**Modified by:** claude-sonnet-4.5 (claude.ai)  
**Changes:** Added hallucination check to Section 2.3 quality checklist  
**Details:** See docs/sprints/2025-Q4-Sprint-02-changes.md

### Version 1.0 (2025-10-11)
**Sprint:** 2025-Q4-Sprint-02  
**Created by:** claude-sonnet-4.5 (claude.ai)  
**Purpose:** Initial submission workflow guide  
**Details:** See docs/sprints/2025-Q4-Sprint-02-changes.md
```

---

## 2. Sprint Activity Tracking

### 2.1 Sprint Naming Convention

**Format:** `YYYY-QQ-Sprint-NN`

**Examples:**
- 2025-Q4-Sprint-01
- 2025-Q4-Sprint-02
- 2026-Q1-Sprint-01

**Sprint duration:** Typically 1-2 weeks, flexible based on work cadence

### 2.2 Sprint Activity Log Location

**Path:** `docs/sprints/YYYY-QQ-Sprint-NN-changes.md`

**Example:** `docs/sprints/2025-Q4-Sprint-02-changes.md`

### 2.3 Sprint Activity Log Format

```markdown
# Sprint Activity Log: 2025-Q4-Sprint-02

**Dates:** 2025-10-09 to 2025-10-11  
**Focus:** Initial DEIA documentation series  
**Agents:** claude-sonnet-4.5 (claude.ai), claude-sonnet-4.5 (claude-code as Bot 1)

---

## Documents Created

### Doc 1: DEIA Integration Map
- **Version:** 1.0
- **Status:** Complete
- **Agent:** claude-sonnet-4.5 (claude.ai)
- **Purpose:** Connect DEIA ecosystem with philosophical manifestos
- **File:** docs/DEIA-Integration-Map.md
- **Notes:** Single-pass creation, no issues

### Doc 2: DEIA Developer Onboarding Guide
- **Version:** 1.0
- **Status:** Complete
- **Agent:** claude-sonnet-4.5 (claude.ai)
- **Purpose:** Get developers from install to first contribution
- **File:** docs/DEIA-Developer-Onboarding.md
- **Notes:** Initial creation had update loop issues; resolved with rewrite

---

## Documents Modified

### Doc 4: DEIA Submission Workflow (v1.0 → v1.1)
- **Date:** 2025-10-11
- **Agent:** claude-sonnet-4.5 (claude.ai)
- **Changes:**
  - Added hallucination check to Section 2.3 quality checklist
  - Updated version metadata
  - Added document history section
- **Reason:** User identified missing critical quality check
- **Previous version:** Archived to docs/archive/DEIA-Submission-Workflow-v1.0.md

---

## Code/Tools Created

### downloads-monitor.py
- **Version:** 1.0 prototype
- **Agent:** claude-sonnet-4.5 (claude-code, Bot 1)
- **Purpose:** Monitor Downloads folder, route .md files via DEIA headers
- **Status:** Prototype testing
- **Location:** [TBD - Bot 1's project]

---

## Processes Created

### Documentation Versioning Process
- **Version:** 1.0
- **Agent:** claude-sonnet-4.5 (claude.ai)
- **Purpose:** Establish standards for doc versioning and change tracking
- **File:** best-practices/documentation-versioning.md
- **Trigger:** Need identified during Doc 4 revision

---

## Backlog Items Created

### DEIA-2025-042-PROCESS: Formalize Sprint Documentation Workflow
- **Priority:** P2
- **Description:** Create templates and automation for sprint activity tracking
- **Agent:** claude-sonnet-4.5 (claude.ai)
- **Sprint:** 2025-Q4-Sprint-02
- **Status:** Backlog

---

## Lessons Learned

1. Update loops in artifacts: Use rewrite instead of multiple updates
2. Hallucination checks needed: Add to all quality checklists
3. Document versioning needed: Created process this sprint
4. Sprint tracking needed: Created basic format, needs formalization

---

## Next Sprint Focus

- Continue documentation series (Docs 5-10)
- Test downloads-monitor.py with real files
- Implement sprint tracking automation
- Apply versioning process to all existing docs
```

---

## 3. Agent Attribution System

### 3.1 Agent Identification Format

**Format:** `[model-name] ([platform/tool])`

**Examples:**
- `claude-sonnet-4.5 (claude.ai)` - Strategic/doc work in Claude Projects
- `claude-sonnet-4.5 (claude-code)` - Implementation work via Claude Code
- `claude-opus-4 (claude.ai)` - If using different model
- `github-copilot (vscode)` - If assisted by Copilot
- `human-dave` - When Dave makes direct changes

### 3.2 Multi-Agent Collaboration

**When multiple agents contributed:**
```markdown
**Modified by:** 
- claude-sonnet-4.5 (claude.ai) - Sections 1-3
- claude-sonnet-4.5 (claude-code) - Code examples in Section 4
- human-dave - Final review and edits
```

### 3.3 Agent Role Clarity

**claude.ai (this bot):** Strategy, documentation, planning, manifestos  
**claude-code (Bot 1):** Implementation, code, technical execution  
**human-dave:** Vision, decisions, review, approval

---

## 4. Archive Process

### 4.1 When to Archive

**Archive previous version when:**
- Document moves to new minor or major version
- Significant changes made (not just typo fixes)
- Historical reference may be needed

**Don't archive for:**
- Patch versions (X.Y.Z typo fixes)
- In-progress drafts
- Documents marked as "living" (e.g., backlog)

### 4.2 Archive Location

**Path:** `docs/archive/[filename]-vX.Y.md`

**Example:** `docs/archive/DEIA-Submission-Workflow-v1.0.md`

### 4.3 Archive Metadata

**Add to top of archived file:**
```markdown
# [ARCHIVED VERSION 1.0]

**Superseded by:** docs/DEIA-Submission-Workflow.md (v1.1)
**Archived date:** 2025-10-11
**Reason:** Added missing hallucination check to quality checklist
**Archived by:** claude-sonnet-4.5 (claude.ai)

---

[Original content follows...]
```

### 4.4 Why We Archive (Don't Delete)

The principle of **"we don't delete stuff"** is fundamental to our documentation practice. All artifacts, even mistakes, should be archived and marked as deprecated rather than deleted.

**Rationale:**

- **Preserves Institutional Memory:** Archiving mistakes and outdated information provides a complete historical record of the hive's evolution. This is essential for understanding why things are the way they are.

- **Creates Learning Opportunities:** Mistakes are valuable learning opportunities. By preserving them, we can analyze them, learn from them, and create patterns to prevent them from happening again.

- **Encourages Psychological Safety:** A culture that does not punish mistakes, but instead learns from them, encourages psychological safety. This makes team members more likely to take risks, innovate, and self-report their own errors.

- **Provides a Revert Path:** In the event that a new process or document is found to be flawed, the archived version provides an easy way to revert to the previous state.

---

## 5. Routing Header Updates

### 5.1 Version in Filename

**For updated docs, routing header should specify version:**
```yaml
---
deia_routing:
  project: quantum
  destination: docs/
  filename: DEIA-Submission-Workflow-v1.1.md
  action: move
---
```

**Downloads monitor handles:**
- Detects version number in filename
- Archives old version if exists
- Replaces with new version
- Logs change in sprint activity file

### 5.2 Archive Routing

**For archived versions:**
```yaml
---
deia_routing:
  project: quantum
  destination: docs/archive/
  filename: DEIA-Submission-Workflow-v1.0.md
  action: move
---
```

---

## 6. Implementation Checklist

### 6.1 When Creating New Document

- [ ] Set version to 1.0
- [ ] Include version metadata in header
- [ ] Create initial Document History section
- [ ] Log creation in current sprint activity file
- [ ] Attribute creating agent

### 6.2 When Updating Existing Document

- [ ] Increment version number appropriately
- [ ] Update version metadata (date, sprint, agent)
- [ ] Add entry to Document History section
- [ ] Create archive of previous version (if minor/major change)
- [ ] Update sprint activity log with changes
- [ ] Route updated file with new version number
- [ ] Route archived file to archive folder

### 6.3 Sprint Activity Tracking

- [ ] Create sprint activity file at sprint start
- [ ] Log all doc creations
- [ ] Log all doc modifications
- [ ] Log all code/tool development
- [ ] Log all processes created
- [ ] Log lessons learned
- [ ] Plan next sprint focus

---

## 7. Backlog Integration

### 7.1 Backlog Item Format for Process Improvements

**Item ID:** `DEIA-YYYY-NNN-TYPE`

**Example:**
```markdown
## DEIA-2025-042-PROCESS: Formalize Sprint Documentation Workflow

**Priority:** P2  
**Type:** Process Improvement  
**Created:** 2025-10-11  
**Sprint:** 2025-Q4-Sprint-02  
**Created by:** claude-sonnet-4.5 (claude.ai)

**Problem:** 
Sprint activity tracking currently manual. Need templates and possibly automation.

**Proposed Solution:**
1. Create sprint activity log template
2. Script to initialize new sprint files
3. Script to update sprint logs from document changes
4. Integration with downloads-monitor.py

**Acceptance Criteria:**
- [ ] Template exists in docs/templates/sprint-activity-template.md
- [ ] Script can create new sprint file from template
- [ ] Script can parse doc changes and update sprint log
- [ ] Documentation updated with automation usage

**Dependencies:** None

**Effort:** 2-3 hours

**Notes:** Identified during Doc 4 revision when realizing we lack formal process.
```

### 7.2 Backlog Location

**Path:** `docs/backlog/YYYY-QQ-backlog.md`

**Example:** `docs/backlog/2025-Q4-backlog.md`

---

## 8. Tool Integration

### 8.1 Downloads Monitor Enhancement

**downloads-monitor.py should:**
- Detect version numbers in filenames
- Check if older version exists in destination
- Archive old version automatically
- Log changes to sprint activity file
- Update document's Document History section

**Future enhancement backlog item created.**

### 8.2 Sprint Activity Automation

**Potential script: `deia-sprint-tracker.py`**
- Initialize new sprint activity file
- Parse document changes (via git diff or file comparison)
- Auto-update sprint log
- Generate sprint summary report

**Backlog item created for future development.**

---

## 9. Examples

### 9.1 Complete Example: Doc Update Flow

**Step 1: User requests change**
```
User: "Doc 4 needs hallucination check in quality checklist"
```

**Step 2: Agent updates document**
- Increments version 1.0 → 1.1
- Updates metadata (date, sprint, agent)
- Adds change to Document History section
- Creates updated artifact with v1.1 in routing header

**Step 3: Agent archives old version**
- Creates archive artifact with v1.0
- Adds archive metadata header
- Routes to docs/archive/

**Step 4: Agent updates sprint log**
- Opens docs/sprints/2025-Q4-Sprint-02-changes.md
- Adds entry under "Documents Modified"
- Logs what changed and why

**Step 5: User downloads both files**
- downloads-monitor.py detects versions
- Archives old version
- Replaces with new version
- Logs activity

### 9.2 Complete Example: New Process Creation

**Step 1: Need identified**
```
User: "We need a doc versioning process"
```

**Step 2: Agent creates process document**
- Creates documentation-versioning.md
- Sets version 1.0
- Includes Document History section
- Routes to best-practices/

**Step 3: Agent logs in sprint activity**
- Adds to "Processes Created" section
- Explains trigger (Doc 4 revision)

**Step 4: Agent creates backlog item**
- DEIA-2025-042-PROCESS for automation
- Adds to docs/backlog/2025-Q4-backlog.md

**Step 5: Agent updates DEIA practices**
- References new versioning process
- Adds to best-practices index

---

## 10. Compliance

### 10.1 All Documentation Must

- Include version metadata
- Include Document History section
- Be logged in sprint activity
- Attribute agent/author
- Follow semantic versioning
- Archive previous versions (if substantial change)

### 10.2 Exceptions

**Living documents (don't archive):**
- Backlogs
- Sprint activity logs
- Meeting notes
- Brainstorming docs

**Patch versions (don't archive):**
- Typo fixes
- Formatting corrections
- Link updates
- Minor clarifications

---

## Document History

### Version 1.0 (2025-10-11)
**Sprint:** 2025-Q4-Sprint-02  
**Created by:** claude-sonnet-4.5 (claude.ai)  
**Purpose:** Establish documentation versioning and change tracking standards  
**Trigger:** Need identified during Doc 4 revision  
**Details:** See docs/sprints/2025-Q4-Sprint-02-changes.md

---

**Acknowledgments:**
Created in response to systematic documentation needs during DEIA doc series development. Claude (Anthropic) with Dave Eichler.

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
**Purpose:** Establish documentation versioning and change tracking standards  
**Trigger:** Need identified during Doc 4 revision  
**Details:** See docs/sprints/2025-Q4-Sprint-02-changes.md