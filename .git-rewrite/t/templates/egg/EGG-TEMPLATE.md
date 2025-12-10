---
kind: egg
id: {{ID}}
title: {{TITLE}}
date: {{DATE}}
version: 0.1.0
deia_routing:
  project: governance
  destination: docs/eggs/
  filename: {{FILENAME}}
  action: create
eos: 0.1
bundle:
  profile: generic
  variables:
    project: default
  steps:
    - name: expand_egg
      note: Always work on a copy of the egg (Rule 3)
      ps: .deia\tools\egg_expand.ps1 -Path <this-file>
      sh: .deia/tools/egg_expand.sh <this-file>
    - name: next_steps
      note: Append profile-specific steps (LLH hatches, validation) below in a profile-specific egg
---

Explain the Egg’s purpose and how it routes artifacts.
