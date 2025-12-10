---
title: DEIA Working Rules (v0.1)
date: 2025-10-15
---

# Core Rules
- Rule 1 — DND (Do Not Destroy): All operations are additive; no deletions without explicit archive approval.
- Rule 2 — ROTG‑2: Respect do‑not‑erase and do‑not‑read locks; use override protocol for sensitive actions.
- Rule 3 — Always Work on a Copy of the Egg: Never mutate the original egg in place. Expand or copy into a working folder first.
- Rule 4 — Segment Large Projects: Use `.projects/<project>/<kind>/` to avoid huge directories.
- Rule 5 — Human Validation for Eggs: Require explicit confirmation before routing/creating egg‑driven content.

# Tools
- Egg expand: `.deia/tools/egg_expand.ps1|sh` — copies egg to a working folder (auto‑increments if taken) and logs RSE.
- LLH hatch: `.deia/tools/llh_hatch.ps1|sh` — safe hatcher with segmentation, large‑dir guard, and egg confirm.

