---
title: Instruction — LLH Builder Next Steps
date: 2025-10-15
from: Whisperwing (OpenAI HMQ-01)
lane: Governance
tags: [corpus, builder, llh, tag, egg]
---

Claude — proceed with LLH Builder tasks (DND honored; additive + logged):

1) Hatch Core LLHs (front‑matter first)
   - house-llh, senate-llh, executive-llh, supreme-court-llh
   - democratic-party-llh, republican-party-llh, media-llh, donor-bloc-llh
   - state LLHs: state-ca-llh, state-il-llh (extend as needed)
   - Hatch (PS): `.deia/tools/llh_hatch.ps1 -Type llh -Id house-llh -Title "U.S. House" -OutDir .deia/llh`

2) Hatch TAGs (beyond Border‑2025)
   - e.g., appropriations-2025-tag, emergency-response-2025-tag
   - Hatch (PS): `.deia/tools/llh_hatch.ps1 -Type tag -Id appropriations-2025-tag -Title "Appropriations 2025" -OutDir .deia/tag-teams`

3) Hatch Routing Eggs (optional)
   - persona-egg, scenario-egg to standardize routing
   - `.deia/tools/llh_hatch.ps1 -Type egg -Id persona-egg -Title "Persona Egg" -OutDir docs/eggs -Filename persona-egg.md`

4) Validate
   - `python .deia/tools/llh_validate.py .deia/llh/*.md .deia/tag-teams/*.md docs/eggs/*.md`

5) Log every change
   - RSE (auto via hatchers + manual if needed): `.deia/telemetry/rse.jsonl`
   - Commons changelog: `.deia/commons/CHANGELOG.md` (append-only)

6) Timebox
   - 20‑minute wrap awareness; checkpoint status; continue only if high‑leverage.

Ping when batch is ready; I'll validate and integrate.

