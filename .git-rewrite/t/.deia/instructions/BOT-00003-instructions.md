# Instructions for BOT-00003 (Drone-Testing)
**Created:** 2025-10-13 10:56:29
**Status:** UNCLAIMED

---

## CLAIMED BY
**Instance ID:** 73d3348e
**Claimed at:** 2025-10-25 20:00:00
**Last check-in:** 2025-10-25 20:00:00
**Status:** ACTIVE

---

## Your Identity

You are **BOT-00003**, a Drone-Testing in the hive.

**Responsibilities:**
- Write tests
- Measure coverage
- Fix regressions

---

## Getting Started

1. Claim this identity:
   ```bash
   python ~/.deia/bot_coordinator.py claim BOT-00003 --instance <your-instance-id>
   ```

2. Update this file with your instance ID

3. Check the hive coordination rules:
   `.deia/hive-coordination-rules.md`

4. Check the backlog for tasks:
   `.deia/backlog.json`

5. Wait for Queen to assign you a task

---

## Current Task

**Status:** ACTION REQUIRED
**Task:** telemetry-audit-v1
**Expectation:** Audit telemetry fields & write report + checklist; signature required

---

## Notices
- Use the process submission template after completing any process: `.deia/submissions/processes/TEMPLATE.md`
- Include: what you tried, your solution/process, tokens/time, worker usage, and evidence.

## Boot Load Check (Keep it Light)
- Load only what you need now (Current Task + acceptance criteria + immediate next step).
- For background, follow links to `.deia/hive/ORDERS-PROTOCOL.md`, `.deia/DRONE-START.md`, processes, or BOK.
- If this file becomes too long, prefer links over inlining content.


## Proceed Now

- Start heartbeat: ./.deia/tools/heartbeat.ps1 -BotId BOT-00003 -Message "Working repo-health-actions"
- Run audit (one): deia doctor docs (fallback: python -m deia.cli doctor docs)
- Save stdout to: .deia/reports/doctor-docs-<YYYYMMDD-HHMM>.txt
- Create Top-5 actions (≤120 chars each incl. path): .deia/reports/repo-health-actions.md
- Finish heartbeat: ./.deia/tools/heartbeat.ps1 -BotId BOT-00003 -Message "Actions written: .deia/reports/repo-health-actions.md"
**End of Instructions**
- 2025-10-13T10:58:41 [BOT-00003] Ready

- 2025-10-13T11:10:01 [BOT-00003] Standing by
- 2025-10-13T11:13:01 [BOT-00003] Standing by

- 2025-10-13T11:16:01 [BOT-00003] Standing by
- 2025-10-13T11:17:01 [BOT-00003] 5m remaining
- 2025-10-13T11:19:01 [BOT-00003] Standing by
- 2025-10-13T11:22:01 [BOT-00003] Standby; awaiting assignment
- 2025-10-13T11:43:06 [BOT-00003] Doc audit started
- 2025-10-13T11:44:07 [BOT-00003] Report written: .\\.deia\\reports\\repo-health.md
- 2025-10-13T11:47:14 [BOT-00003] Reports archived: .\\.deia\\reports\\20251013
- 2025-10-13T11:49:28 [BOT-00003] Standing by
- 2025-10-13T11:52:28 [BOT-00003] Standing by
- 2025-10-13T11:55:28 [BOT-00003] Standing by
- 2025-10-13T11:58:28 [BOT-00003] Standing by
- 2025-10-13T11:59:28 [BOT-00003] 5m remaining
- 2025-10-13T12:01:28 [BOT-00003] Standing by
- 2025-10-13T12:04:29 [BOT-00003] Standby; awaiting assignment
- 2025-10-13T12:07:03 [BOT-00003] Doc audit started
- 2025-10-13T12:07:29 [BOT-00003] Report written: .\\.deia\\reports\\repo-health.md
- 2025-10-13T12:07:58 [BOT-00003] Reports archived: .\\.deia\\reports\\20251013

- 2025-10-13T12:10:27 [BOT-00003] Test run started
- 2025-10-13T12:12:09 [BOT-00003] Test fix applied; rerunning tests
- 2025-10-13T12:14:32 [BOT-00003] Tests: 69/69 passed; report archived: .\\.deia\\reports\\20251013
- 2025-10-13T12:19:24 [BOT-00003] Orders applied (repo-health-actions-v1)
- 2025-10-13T12:19:40 [BOT-00003] Report written: .\.deia\reports\repo-health-actions.md
- 2025-10-13T13:05:51 [BOT-00003] Ready
- 2025-10-13T13:11:51 [BOT-00003] Working repo-health-actions
- 2025-10-13T13:11:52 [BOT-00003] Doc audit saved: .\.deia\reports\doctor-docs-20251013-1311.txt
- 2025-10-13T13:14:02 [BOT-00003] Working repo-health-actions
- 2025-10-13T13:14:26 [BOT-00003] Doc audit saved: .\.deia\reports\doctor-docs-20251013-1314.txt
- 2025-10-13T13:35:56 [BOT-00003] Working repo-health-actions
- 2025-10-13T13:36:30 [BOT-00003] Working repo-health-actions
- 2025-10-13T13:36:33 [BOT-00003] Doc audit saved: .\\.deia\\reports\\doctor-docs-20251013-1336.txt

- 2025-10-13T13:57:04 [BOT-00003] No update; still on repo-health-actions-v1
- 2025-10-13T13:58:00 [BOT-00003] Working repo-health-actions
- 2025-10-13T13:58:05 [BOT-00003] Doc audit saved: .\\.deia\\reports\\doctor-docs-20251013-1358.txt
- 2025-10-13T17:25:37 [BOT-00003] Checking in: working repo-health-actions-v1
- 2025-10-13T17:28:53 [BOT-00003] Working repo-health-actions
- 2025-10-13T17:28:59 [BOT-00003] Actions written: .\\.deia\\reports\\repo-health-actions.md
- 2025-10-13T18:11:40 [BOT-00003] No update; still on repo-health-actions-v1


- 2025-10-13T18:13:51 [BOT-00003] Orders applied (repo-health-action-1-v1)
- 2025-10-13T18:28:38 [BOT-00003] repo-health-action-1-v1: fixing admin.py regex escapes
- 2025-10-13T18:28:59 [BOT-00003] repo-health-action-1-v1: running pytest -q
- 2025-10-13T18:34:46 [BOT-00003] Checking in: working repo-health-action-1-v1

- 2025-10-13T18:39:30 [BOT-00003] Checking in: working repo-health-action-1-v1

## Output Signature (Required)
- Append final line: Generated by BOT-00003 to each output file you produce.
- Include your BOT ID in completion heartbeats.

- 2025-10-13T18:43:07 [BOT-00003] Checking in: working repo-health-action-1-v1
- 2025-10-13T18:45:29 [BOT-00003] Checking in: working repo-health-action-1-v1
- 2025-10-13T18:46:24 [BOT-00003] Checking in: working repo-health-action-1-v1
- 2025-10-13T18:46:40 [BOT-00003] Checking in: working repo-health-action-1-v1
- 2025-10-13T18:47:56 [BOT-00003] Checking in: working repo-health-action-1-v1

- 2025-10-13T18:53:04 [BOT-00003] Checking in: scanning for new drone instructions

- 2025-10-13T18:54:22 [BOT-00003] Orders applied (repo-health-action-1-apply-plan-v1)
- 2025-10-13T18:55:47 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1
- 2025-10-13T18:59:24 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1
- 2025-10-13T19:00:33 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1
- 2025-10-13T19:01:05 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1
- 2025-10-13T19:02:30 [BOT-00003] No update; still on repo-health-action-1-apply-plan-v1
- 2025-10-13T19:02:30 [BOT-00003] Working repo-health-action-1-apply-plan-v1
- 2025-10-13T19:02:30 [BOT-00003] Report written: .\\.\.deia\reports\repo-health-apply-plan-20251013-1902.md
- 2025-10-13T19:03:12 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1
- 2025-10-13T19:03:26 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1
- 2025-10-13T19:05:56 [BOT-00003] Working repo-health-action-1-apply-plan-v1
- 2025-10-13T19:05:56 [BOT-00003] Report written: .\.deia\reports\repo-health-action-1-20251013-1905.md
- 2025-10-13T19:07:56 [BOT-00003] BOT-00003: Signatures added: .\.deia\reports\repo-health-actions.md; .\.deia\reports\20251013\repo-health-apply-plan-20251013-1902.md
- 2025-10-13T19:12:21 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1
- 2025-10-13T19:14:07 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:18:19 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:20:28 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:21:56 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:23:26 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)

- 2025-10-13T19:24:05 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:25:01 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:26:23 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:34:59 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:36:13 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:38:50 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)
- 2025-10-13T19:39:45 [BOT-00003] Checking in: working repo-health-action-1-apply-plan-v1 — BOT-00003 (db143728)

- 2025-10-13T19:41:01 [BOT-00003] Orders applied (telemetry-audit-v1) — BOT-00003 (db143728)
- 2025-10-13T19:41:20 [BOT-00003] Working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T19:41:25 [BOT-00003] Report written: .\\.\.deia\reports\telemetry-audit-20251013-1941.md — BOT-00003 (db143728)
- 2025-10-13T19:45:13 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T19:47:20 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T19:49:12 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T19:51:28 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T19:52:30 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T19:54:03 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:00:38 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:01:04 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:03:06 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:05:45 [BOT-00003] Checking in: working telemetry-audit-v1 - signature compliance updated — BOT-00003 (db143728)
- 2025-10-13T20:08:16 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:12:38 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:15:08 [BOT-00003] Working telemetry-audit-v1: writing checklist — BOT-00003 (db143728)
- 2025-10-13T20:15:09 [BOT-00003] Report written: .\\.\.deia\reports\telemetry-checklist-20251013-2015.md — BOT-00003 (db143728)
- 2025-10-13T20:17:59 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:18:50 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:22:14 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:24:31 [BOT-00003] Checking in: working telemetry-audit-v1 — BOT-00003 (db143728)
- 2025-10-13T20:28:36 [BOT-00003] Reboot checklist written: .\\.\.deia\reports\reboot-checklist-20251013-2028357569.md — BOT-00003 (db143728)
