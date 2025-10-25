---
kind: egg
id: llh-startup-egg
title: LLH Startup (Minimum Viable Hive)
date: {{DATE}}
version: 0.1.0
deia_routing:
  project: llh-startup
  destination: .deia/.projects/llh_startup/
  filename: llh-startup-egg.md
  action: create
eos: 0.1
bundle:
  profile: llh-startup
  variables:
    project: llh-mvh
  steps:
    - name: expand_egg
      note: Always work on a copy of the egg (Rule 3)
      ps: .deia\tools\egg_expand.ps1 -Path <this-file>
      sh: .deia/tools/egg_expand.sh <this-file>
    - name: hatch_core_llhs
      note: Hatch a slim, instruction-ready hive
      ps: |
        $env:LLH_PROJECT='{{project}}'
        .deia\tools\llh_hatch.ps1 -Type llh -Id hive-core -Title "Hive Core"
      sh: |
        LLH_PROJECT='{{project}}' .deia/tools/llh_hatch.sh -t llh -i hive-core -T "Hive Core"
    - name: hatch_ops_tag
      ps: |
        $env:LLH_PROJECT='{{project}}'
        .deia\tools\llh_hatch.ps1 -Type tag -Id ops-boot -Title "Ops Boot"
      sh: |
        LLH_PROJECT='{{project}}' .deia/tools/llh_hatch.sh -t tag -i ops-boot -T "Ops Boot"
    - name: validate
      ps: .deia\tools\validate_all.ps1
      sh: .deia/tools/validate_all.sh
    - name: ready_for_instructions
      note: LLH Startup ready; proceed with domain-specific instructions or attach specialization bundle
---

# LLH Startup Egg (Minimum Viable Hive)

Purpose: Launch a slim, instruction-ready hive (LLH + TAG) segmented under `.projects/{{project}}/` and ready for further specialization.

