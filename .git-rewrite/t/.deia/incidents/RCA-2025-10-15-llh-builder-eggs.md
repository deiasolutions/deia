---
title: RCA — LLH Builder Egg Launch Path Confusion
date: 2025-10-15
authors: [Whisperwing (OpenAI HMQ-01)]
status: Draft
---

# Summary
Hatching proceeded directly (house-llh, senate-llh, appropriations-2025-tag) without first expanding a simulation egg, contrary to Rule 3 (work on a copy of the egg). No destructive changes occurred; artifacts were later removed or will be archived on approval.

# Impact
- Minor: Entities created in non-segmented paths caused confusion about project boundaries.
- No data loss; DND honored.

# Timeline (UTC)
- 20:30–20:33: LLH Builder updated; Claude hatched LLHs/TAG.
- 20:3x: Realization that egg expansion step wasn’t executed.

# Contributing Factors
- Ambiguous instruction: kickoff mixed egg expansion guidance with direct hatch commands; execution chose the latter.
- Tool drift: We introduced an `egg_expand.py` tool but did not wire it into a single “feature-select” flow that enforces egg-first workflows.
- Precondition not enforced: Hatchers allowed direct creation without checking for an expanded egg workspace.
- Segmentation default changed mid-stream: PowerShell defaults initially targeted `.deia/llhs`, then we unified to `.projects/<project>`, creating split behavior.

# Corrective Actions (CA)
- CA-1: Add precondition check in hatchers — if `--project/-Project` is set and no `egg.md` exists under `.projects/<project>/`, prompt/warn and require explicit `--force`.
- CA-2: Update docs (DEIA-RULES) to make egg-first workflows explicit and primary.
- CA-3: Add a `builder_launch.ps1|sh` that runs: egg_expand → hatch → validate in one guided flow.

# Preventive Actions (PA)
- PA-1: “Feature select” switch in builder (egg-first vs direct) with default = egg-first.
- PA-2: Corpus playbook snippet for LLH sim kickoff with copy-paste commands (platform-specific).
- PA-3: 20-minute checkpoints to catch scope drift early.

# Status
- CA-2 delivered (DEIA-RULES); egg expand tool delivered; hatchers now include human validation + segmentation; CA-1/CA-3 pending.

