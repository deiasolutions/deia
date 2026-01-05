# Routing Policy

## Inputs
- Task intent (design, planning, code, ops)
- KB profile (domain tags, delivery modes)
- Execution constraints (local only, terminal only, etc.)

## Outputs
- Lane: LLM, terminal, local LLM, or task file
- Provider: specific adapter instance
- Delivery: cache + prompt, task file, or both

## Default Rules
1. **Design and planning**: LLM chat with KB cache + prompt.
2. **Code changes**: Terminal bee unless explicitly allowed for LLM-only.
3. **Local-only tasks**: Local LLM + task file.
4. **Governance**: Always include RULE entities in delivery.

## Overrides
User can force a lane or provider per task or per project.
