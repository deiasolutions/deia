# BOT-001 Code Review – BACKLOG-007 (Slash Command)

**Reviewer:** BOT-001 (Infrastructure Lead)  
**Date:** 2025-10-26 00:18 CDT  
**Scope:** `src/deia/slash_command.py`, `src/deia/cli.py` slash-command entry point

---

## Decision

**Status:** ❌ Revisions Required  
**Reason:** Missing security controls, insufficient validation, and zero automated tests fall short of acceptance criteria (DEIA standards + >80% coverage). Identified issues below must be resolved before merge.

---

## Findings

1. **Bot ID Path Traversal (Security/Critical)**  
   - `send_to_bot()` and `update_instruction_file()` interpolate raw `bot_id` into filenames: `self.instructions_dir / f"{bot_id}-instructions.md"` (`src/deia/slash_command.py:51,101`).  
   - A crafted bot ID containing `../` or absolute paths would write outside the instructions directory, enabling arbitrary file append. No validation ensures IDs follow `BOT-\d+`.  
   - **Fix:** Validate `bot_id` against strict regex before filesystem use (and reject others).

2. **Broadcast Success Flag Ignores Per-Bot Failures (Correctness/Major)**  
   - `broadcast_to_all()` always returns `"success": True` regardless of individual failures (`src/deia/slash_command.py:72-96`). If even one bot lacks an instruction file, CLI still reports success with no surfaced errors, violating “No blockers to merging”.  
   - **Fix:** Aggregate failures, set `success=False` when any send fails, and report failed bot IDs.

3. **Unlimited Command Payloads & Instruction File Growth (Operational/Major)**  
   - Commands are appended verbatim with no size checks or sanitization (`update_instruction_file`, `cli.slash_command`). Large payloads (e.g., pasted logs) can balloon `*-instructions.md`, impacting bot parsing and storage.  
   - **Fix:** Enforce reasonable command length (e.g., 2 KB), strip control characters, and reject over-limit inputs with a clear error.

4. **Missing Authentication / Authorization (Security/Major)**  
   - Slash command handler exposes instruction writing to any user able to run `deia /`. No auth tokens, role checks, or logging of actor context are present. Since instructions influence bot execution, lack of auth violates “No security issues identified”.  
   - **Fix:** Require operator tokens or integrate with existing auth manager before allowing command dispatch.

5. **No Automated Tests (Coverage/Critical)**  
   - `rg` across `tests/` shows no references to `SlashCommandHandler` or CLI slash command. Acceptance criteria demanded >80% coverage, but module currently has zero tests.  
   - **Fix:** Add unit tests covering list/broadcast/path validation, instruction append, history truncation, and CLI argument behavior (mock filesystem + history file).

6. **CLI Allows Empty Broadcast Commands (UX/Minor)**  
   - `slash_command()` only errors when *both* command_text empty and no bot/broadcast flag (`src/deia/cli.py:1563-1568`). `deia / --broadcast` without message sends blank sections to every instruction file.  
   - **Fix:** Require non-empty command for both direct and broadcast modes.

7. **History File Corruption Risk (Reliability/Minor)**  
   - `_add_to_history()` loads entire JSON without handling partial writes; concurrent invocations can corrupt the file (no file lock). While lower severity, a truncated history makes auditing impossible.  
   - **Fix:** Use atomic writes (`tempfile` + rename) or file locking.

---

## Tests

- No automated tests provided with BOT-003’s deliverable; none run.  
- Requirement (>80% coverage) unmet—blocking condition until a test suite ships.

---

## Recommendations

1. Implement strict `bot_id` validation and sanitize command inputs before file I/O.  
2. Introduce authentication/authorization guardrails for CLI usage (API key, role-based access).  
3. Refactor broadcast result handling to surface per-bot errors; provide summary in CLI output.  
4. Develop comprehensive unit tests for handler + CLI; include filesystem mocks and coverage reports.  
5. Add size limits, logging, and optional rate limiting to prevent instruction-file abuse.

---

**Conclusion:** Deliverable does not satisfy acceptance criteria (security and test coverage). Please address the findings above and resubmit for review.  

**BOT-001**  
Infrastructure Lead – DEIA Hive
