# PROCESS-0003 — Process Discovery & Contribution Workflow

**Status:** OFFICIAL
**Version:** 1.0
**Date:** 2025-11-14
**Owner:** Q33N Authority

---

## Rule

Processes are discovered hierarchically (local → global), created locally when missing, tested, and contributed back to the global DEIA repository for collective knowledge.

**Hierarchy:**
1. Check local project `.deia/processes/`
2. Check global DEIA (deiasolutions) `.deia/processes/`
3. If not found anywhere: create locally, follow it, test it, submit it

---

## When to Apply

- Before attempting any workflow, tool usage, one-off task, or workaround
- When implementing a new task type not covered by existing processes
- When discovering a better way to do something already done
- When coordinating between agents (human/bot/bot)

---

## Steps

### 1. Discover (Check for Existing Process)

**Search locations in order:**

1. **Local project processes**
   ```
   .deia/processes/PROCESS-XXXX-*.md
   ```
   Check your current project's `.deia/processes/` directory first.

2. **Global DEIA processes (mother ship)**
   ```
   C:\Users\davee\onedrive\documents\github\deiasolutions\.deia\processes\
   ```
   If not found locally, check the deiasolutions repository.

3. **Related documentation**
   - `.deia/hive-coordination-rules.md` - coordination procedures
   - `.deia/instructions/README.md` - communication system
   - `bok/` (Body of Knowledge) - patterns and anti-patterns
   - `docs/` - project-specific guides

**If found:**
- Follow the process exactly as written
- If gaps exist, propose a patch (non-invasive, local first)

### 2. Create (If Process Missing Everywhere)

**Location:** `.deia/processes/PROCESS-XXXX-process-name.md` (local project)

**Standard format (required):**
```markdown
# PROCESS-XXXX — [Human-readable title]

**Status:** DRAFT / OFFICIAL
**Version:** 1.0
**Date:** YYYY-MM-DD
**Owner:** [Q33N / BOT-ID / Human name]

---

## Rule
[Core principle in 1-2 sentences]

---

## When to Apply
[Scenarios where this process is used]

---

## Steps
1. [First step]
2. [Second step]
...

---

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## Rollback
[How to undo/recover if something goes wrong]

---

## Telemetry Plan
[What to log, where, and why]

---

## Integration with Other Processes
[What other processes this relates to]

---

## Change Log
- **YYYY-MM-DD:** Initial creation

---

## Authority
[Who approved this: Q33N / Author]
```

**Minimum required sections:**
- Title & scope
- Rule (why does this process exist?)
- When to apply
- Steps (numbered, LLM-agnostic)
- Timebox (how long should it take?)
- Success criteria (measurable)
- Rollback (how to recover)
- Telemetry plan
- Worker usage (if any non-LLM workers involved)

### 3. Execute & Test

**Procedure:**
1. Follow the draft process end-to-end
2. Validate with a small example or test case
3. Ensure reversibility (can you undo it?)
4. Document any gaps or improvements discovered
5. Fix gaps, re-test, iterate until satisfied

### 4. Telemetry & Evidence (Local-first)

**Log your work:**
```bash
# Create a session log for this process work
.deia/bot-logs/[BOT-ID or YOUR-NAME]-[DATE]-process-work.jsonl
```

**Log entries should include:**
- `event_type`: "process_created", "process_tested", "process_submitted"
- `lane`: "Processes"
- `actor`: Your bot ID or name
- `data`:
  - `process_id`: "PROCESS-XXXX"
  - `process_name`: [title]
  - `tokens`: [tokens used, if applicable]
  - `duration_ms`: [time spent]
  - `status`: "draft", "tested", "ready_for_submission"
- `message`: Short description

### 5. Submit to Collective Knowledge

**Location:** `.deia/submissions/processes/PROCESS-XXXX-submission-note.md`

**Submission note format:**

```markdown
# Process Submission: PROCESS-XXXX

**Process Name:** [Human-readable title]
**Author:** [Your name / BOT-ID]
**Date:** YYYY-MM-DD
**Status:** Ready for review / Ready for global inclusion

## What We Tried to Do
[Brief description of the problem or workflow this solves]

## Solution
Link to process file:
`PROCESS-XXXX-process-name.md`

## Evidence of Testing
- [ ] Tested locally with [example/scenario]
- [ ] Process executed end-to-end without errors
- [ ] Reversibility verified
- [ ] No blockers encountered
- [ ] [Any other testing done]

## Metrics
- **Tokens used:** [If applicable]
- **Time required:** X hours Y minutes
- **People/bots involved:** [List]
- **Value:** [How much time/effort does this save? How many times will this be used?]

## Integration Notes
- Relates to: [Other PROCESS-XXXX files]
- Conflicts with: [If any]
- Blocks/unblocks: [What this enables]

## Feedback Requested
[Any areas where you want input before global submission]

## Log Files
- Location: `.deia/bot-logs/[name]-[date]-*.jsonl`
- Shows: [Brief description of what's logged]
```

### 6. Global Inclusion (PR to deiasolutions)

**When ready for global:**

1. **Copy to deiasolutions:**
   ```bash
   cp .deia/processes/PROCESS-XXXX-name.md \
      /path/to/deiasolutions/.deia/processes/PROCESS-XXXX-name.md
   ```

2. **Create PR to deiasolutions:**
   - Title: "feat: add PROCESS-XXXX - [Human-readable name]"
   - Description: Copy from submission note
   - Include evidence (test results, metrics, feedback)

3. **After merge:**
   - Update local processes to reference global version (if preferred)
   - OR keep local variant if it's project-specific
   - Document the relationship in both files

---

## Process Numbering Scheme

**Local projects:** Use any numbering
- `PROCESS-0001`, `PROCESS-0002` (local variants)
- `CUSTOM-PROCESS-xyz` (project-specific)

**Global DEIA (deiasolutions):** Maintained sequentially
- `PROCESS-0001`, `PROCESS-0002`, `PROCESS-0003` (official)
- Next available: Check `.deia/processes/` for highest number

---

## LLM-Agnostic Requirement

All processes MUST be:
- **Language-neutral:** No Claude-specific, Codex-specific, or vendor-specific instructions
- **Tool-agnostic:** Describe what needs to happen, not tool-specific CLI commands
- **Executable by any LLM:** A process should work equally for Claude, Codex, or a human

**Example (GOOD):**
```
1. Read the configuration file
2. Validate all required fields exist
3. Report any errors found
```

**Example (BAD - vendor-specific):**
```
1. Use Claude's file_operations tool to read config
2. Parse JSON using Python's json module
3. Print errors to stdout
```

---

## Success Criteria

After completing PROCESS-0003:

- [x] Existing process found or new process created
- [x] Process tested locally with at least one example
- [x] Process is LLM-agnostic (no vendor-specific instructions)
- [x] Submission note filed in `.deia/submissions/processes/`
- [x] Telemetry logged to `.deia/bot-logs/`
- [x] Ready to submit to global DEIA or file exists in `.deia/processes/`

---

## Rollback

If a process needs to be reverted:

1. **Local variant:** Delete from `.deia/processes/` or move to `_deprecated/`
2. **Global variant:** PR to deiasolutions moving file to `archive/` or deprecating it
3. **History preserved:** Old versions remain in git history

---

## Telemetry Plan

**Track process-related work:**
- Event: `process_discovery` - When searching for a process
- Event: `process_created` - When creating a new process
- Event: `process_tested` - When testing locally
- Event: `process_submitted` - When submitted for global inclusion

**Location:** `.deia/bot-logs/[actor]-activity.jsonl`

---

## Integration with Other Processes

**Related:**
- **PROCESS-0001:** Always Check (or Create) the Process, Then Submit
- **PROCESS-0002:** Task Completion & Archival
- **hive-coordination-rules.md:** How agents coordinate (uses processes)

---

## Change Log

- **2025-11-14:** Initial capture of process discovery and contribution workflow

---

## Authority

This is a Q33N-issued official process documenting how the DEIA system itself evolves.

**Q33N DIRECTIVE:** All bots and workers discovering new processes MUST follow PROCESS-0003 for contribution to collective knowledge.
