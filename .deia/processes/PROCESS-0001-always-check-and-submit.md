## PROCESS-0001 — Always Check (or Create) the Process, Then Submit

Rule
- There is always a process. Check the process before you try to do something.
- If you don't find a process, use your best judgement to create one, follow it, test it, then submit it to the collective.

When to apply
- Any new workflow, tool usage, one-off task, workaround, or decision point.

Steps
1) Discover
   - Search for an existing process: `.deia/`, `docs/`, `bok/`, and team playbooks.
   - If found, follow it; if gaps exist, propose a patch (non-invasive first).
2) Create (if missing)
   - Draft a minimal, LLM‑agnostic process (who/what/where/when) as a Markdown file under `.deia/processes/`.
   - Define inputs, steps, timebox, expected outputs, and guardrails.
3) Execute & Test
   - Follow the draft end-to-end. Validate with a small example. Ensure reversibility.
4) Telemetry & Evidence (local‑first)
   - Log session telemetry to `.deia/bot-logs/<BOT>-activity.jsonl` using `.deia/tools/telemetry.ps1|.sh`:
     - `tokens` (prompt/completion if available), `duration_ms`, key `event`s (start/end), and a short `message`.
   - If using non‑LLM workers, log runs via `.deia/tools/worker-log.ps1|.sh` to count invocations.
5) Submit to collective knowledge
   - Create a submission note under `.deia/submissions/processes/` containing:
     - What you tried to do
     - Your solution/process (final Markdown or link)
     - Tokens/compute/time required
     - Evidence links (reports, logs)
   - Optionally open a PR to move a polished process into `bok/`.

Minimum contents for a new process doc
- Title, Scope, Preconditions, Steps, Timebox, Success Criteria, Rollback, Telemetry plan, Worker usage (if any), and Submission instructions.

Acceptance
- Process executes as written on a fresh checkout using only documented steps.
- No edits to core code unless explicitly scoped; `.deia/` changes preferred.

Versioning & Ownership
- Use `PROCESS-000X` numbering and update a change log in the file.
- Ownership = the Queen at time of submission, then community‑owned after review.

Change Log
- 2025‑10‑13: Initial capture of the rule and submission pattern.

