# Clarifying Questions Policy for AI Assistants

**Pattern Category:** Human-AI Collaboration Best Practice

---

## Problem

AI assistants sometimes ask multiple yes/no questions in a single message and receive a single yes/no answer. Without clarification, the assistant may:
- Guess which question was answered
- Assume user intent incorrectly
- Proceed with the wrong action
- Create cascading errors from initial misunderstanding

**Real example that triggered this pattern:**
```
Assistant: "Would you like me to check if there's a # memory set up for DEIA,
            or would you prefer to manually start logging for this session?"
User: "yes"
Assistant: [immediately starts logging without asking which]
```

User feedback: *"bad habit - you asked me two yes/no questions which I misread and saw as one questions, and you did not ask a clarifying question"*

---

## Solution

**CRITICAL SAFETY RULE:**

When you ask multiple yes/no questions and receive a single yes/no answer:
- **ALWAYS ask a clarifying question** before proceeding
- Do NOT assume which question was answered
- Do NOT guess user intent
- Ask: "Which one - [option A], [option B], or both?"

---

## Implementation

### For Claude Code Preferences

Add to `.claude/preferences/deia.md` or user-level memory:

```markdown
## Clarifying Questions Policy

When you ask multiple yes/no questions and receive a single yes/no answer:
- ALWAYS ask a clarifying question before proceeding
- Do NOT assume which question was answered
- Ask: "Which one - [option A], [option B], or both?"

Apply to all ambiguous responses:
- Multiple questions answered with single response
- Unclear pronouns ("do that", "the first one")
- Vague confirmations when multiple paths are possible
```

### Code Example (if implementing in logic)

```python
def handle_user_response(questions_asked: List[str], user_response: str) -> str:
    """
    Handle potentially ambiguous user responses

    Args:
        questions_asked: List of questions posed to user
        user_response: User's answer

    Returns:
        Clarifying question if ambiguous, or None if clear
    """
    # Check if multiple questions were asked
    if len(questions_asked) > 1:
        # Check if response is ambiguous (yes/no/ok when multiple options exist)
        if user_response.lower().strip() in ['yes', 'y', 'no', 'n', 'ok', 'sure']:
            # Generate clarifying question
            options = " or ".join([f"'{q}'" for q in questions_asked])
            return f"Which one - {options}?"

    return None  # Response is unambiguous
```

---

## Examples

### ❌ INCORRECT Behavior

```
Assistant: "Would you like me to:
            1. Check the memory setup, or
            2. Start logging?"
User: "yes"
Assistant: [starts logging]
```

**Problem:** Assumed which option user meant.

---

### ✅ CORRECT Behavior

```
Assistant: "Would you like me to:
            1. Check the memory setup, or
            2. Start logging?"
User: "yes"
Assistant: "Which one - check memory setup, start logging, or both?"
User: "both"
Assistant: [proceeds with both actions]
```

**Why it's correct:** Asked for clarification before proceeding.

---

## When to Apply

### Always Clarify When:
- Multiple yes/no questions asked, single yes/no answer received
- Multiple options presented, user says "do that" or "the first one"
- Vague confirmations ("sure", "ok", "sounds good") when multiple paths exist
- Unclear pronouns that could refer to multiple things

### No Clarification Needed When:
- User explicitly references specific option ("yes to #2", "start logging")
- Only one question was asked
- User's response is detailed and unambiguous
- Context makes intent obvious

---

## Why This Matters

**From the user who reported this:**
> "sometimes the safety of the entire universe is on the line and if you ask two y/n questions and get one y/n answer back, you shouldn't proceed."

**Real-world impacts:**
- Medical AI: "Should I prescribe medication A or B?" "Yes" → Wrong med prescribed
- Financial AI: "Should I sell stocks or buy more?" "Yes" → Wrong action taken
- Deployment AI: "Deploy to staging or production?" "Yes" → Deployed to wrong environment
- Code changes: "Refactor or delete this function?" "Yes" → Wrong action applied

**Better to over-clarify than to proceed incorrectly.**

---

## Related Patterns

- [Active Confirmation](../patterns/collaboration/active-confirmation.md) - Always confirm destructive actions
- [Explicit Intent](../patterns/collaboration/explicit-intent.md) - Require clear statement of intent
- [Human-in-the-Loop](../patterns/governance/human-in-the-loop.md) - Human approval for critical decisions

---

## Anti-Pattern

**"Helpful" Guessing:**

```
Assistant: "Would you like A or B?"
User: "yes"
Assistant: "I'll assume you meant A since it's more common..."
```

**Never assume.** Always clarify.

---

## Testing Your Implementation

**Test cases:**

1. Ask two questions, user answers "yes" → Should ask clarification
2. Ask two questions, user answers "option 1" → No clarification needed
3. Present options A/B/C, user says "do that" → Should ask which one
4. Ask one question, user answers "yes" → No clarification needed
5. Ask "deploy to staging?" user says "yes" → No clarification needed (only one option)

---

## Attribution

- **Pattern discovered:** 2025-10-07
- **Reported by:** Dave (@dave-atx) (DEIA project)
- **Context:** Claude Code conversation logging implementation
- **Quote:** "sometimes the safety of the entire universe is on the line"

---

## License

CC BY-SA 4.0 - Share, adapt, attribute
