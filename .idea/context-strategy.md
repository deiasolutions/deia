# Context-Window Management Strategy

## The Challenge

Bots have limited context windows (e.g., Claude: 200K tokens, ~150K words).

For complex tasks spanning multiple files and long conversations, context can be exhausted.

## Strategy: Role Assignment Based on Context Needs

### High Context Continuity Roles (assign to single bot)
- **Backend Coder**: Keep all backend code in one bot's context
- **Frontend Coder**: Keep all frontend code in one bot's context
- **Architect**: Maintain system-wide view in single context
- **Test Runner**: Maintain test suite awareness

**Why:** These roles benefit from accumulated context. A bot that's been coding the backend for 50 messages understands the codebase deeply. Don't split this.

### Low Context Dependency Roles (can distribute)
- **Researcher**: Each research task is independent
- **Documenter**: Can synthesize from files, doesn't need conversation history
- **Reviewer**: Reviews specific artifacts, doesn't need full history
- **Validator**: Checks specific criteria

**Why:** These roles work from files/artifacts, not accumulated conversational context.

### Parallel vs Sequential

**Parallel (different bots simultaneously):**
- Frontend coder + Backend coder (independent domains)
- Researcher A (domain 1) + Researcher B (domain 2)
- Tester + Documenter (different activities)

**Sequential (same bot, preserve context):**
- Backend coder → Backend coder → Backend coder (accumulate context)
- Architect → Architect (maintain system view)

## Implementation

When creating handoffs, consider:
1. Does this task benefit from prior context?
2. Is this a continuation of previous work?
3. Should this be assigned to same bot that did related work?

Tag handoffs with:
```json
{
  "context_continuity": "required" | "preferred" | "not_needed",
  "preferred_bot_id": "bot-2-researcher" | null,
  "reasoning": "This continues backend coding from h-005"
}
```
