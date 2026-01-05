# RAQCOON KB Model

## Entity Types
- RULE: dos/don'ts and non-negotiable guardrails.
- PLAYBOOK: step-by-step procedures (deploys, rollbacks, ops).
- PATTERN: repeatable design or architecture patterns.
- SNIPPET: configs or code fragments (vercel.json, railway.toml).
- CHECKLIST: release and QA gates.
- REFERENCE: docs, links, and context notes.

## Required Fields
- id
- title
- summary
- tags
- delivery_mode: cache_prompt | task_file | both
- load_mode: always | situation | on_demand

## Optional Fields
- attachments (inline snippets or file references)
- examples
- related_entities
