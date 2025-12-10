---
kind: egg
id: llh-local-llm-egg
title: LLH Local LLM (LLaMA-compatible) Bootstrap
date: {{DATE}}
version: 0.1.0
deia_routing:
  project: llh-local-llm
  destination: .deia/.projects/llh_local_llm/
  filename: llh-local-llm-egg.md
  action: create
eos: 0.1
bundle:
  profile: llh-local-llm
  variables:
    project: llh-local-llm
    endpoint: http://localhost:11434  # default for ollama
  steps:
    - name: expand_egg
      note: Always work on a copy of the egg (Rule 3)
      ps: .deia\tools\egg_expand.ps1 -Path <this-file>
      sh: .deia/tools/egg_expand.sh <this-file>
    - name: configure_endpoint
      note: Write local LLM endpoint config (edit if different)
      ps: |
        @{
          provider = 'ollama'
          endpoint_url = '{{endpoint}}'
        } | ConvertTo-Json -Compress | Out-File -FilePath .deia\tools\local_llm\config.json -Encoding UTF8
      sh: |
        printf '{"provider":"ollama","endpoint_url":"{{endpoint}}"}' > .deia/tools/local_llm/config.json
    - name: instructions_install
      note: Install either Ollama or llama.cpp (manual; network required; see README)
      ps: Write-Host 'See .deia\tools\local_llm\README.md for install steps (Ollama or llama.cpp)'
      sh: echo 'See .deia/tools/local_llm/README.md for install steps (Ollama or llama.cpp)'
    - name: health_check
      note: Verify local LLM is reachable; logs RSE llm_local_check
      ps: python .deia\tools\local_llm\health_check.py
      sh: python .deia/tools/local_llm/health_check.py
    - name: ready_for_coding
      note: Point tools/agents at the local endpoint to avoid token spend
---

# LLH Local LLM (LLaMA-compatible) Bootstrap Egg

Purpose: Launch a minimal, instruction-ready LLH and attach a local LLaMA-compatible endpoint (e.g., Ollama or llama.cpp) so coding can run without external tokens.

