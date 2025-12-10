# Session Shutdown Protocol

**Category:** Collaboration Patterns
**Tags:** `session-management`, `claude-code`, `cli`, `logging`, `best-practices`
**Difficulty:** Beginner
**Platforms:** Claude Code, CLI-based AI tools
**Version:** 1.0
**Author:** Dave Eccles (DEIA Solutions)
**Date:** 2025-10-10
**Status:** Validated

---

## Problem

When wrapping up a coding session with an AI assistant:
- You want to capture decisions and progress made
- You need a record for future sessions
- There's too much context to review immediately
- You want to defer detailed review until later

Without a shutdown protocol, you either:
- Lose context when the session ends
- Spend time manually creating notes
- Miss important decisions or action items

---

## Solution

Use a standardized shutdown prompt that triggers the AI to:
1. Record all decisions and context
2. Create structured documentation for later review
3. Log the session for continuity
4. Ask what's next (acknowledge you're still in control)

---

## The Prompt

```
do this for me, record the question and the prompts you would give for each answer,
so we can come back to it. record the progress of where we are and next steps
according to our coding practices, which if they aren't now will soon be codified.
but i see there is a lot of text for me to review in the last couple responses,
and i will want you to spoon feed me that info later.

After you do that, do a final log update, and ask me what's next
```

---

## What This Does

**Immediate actions:**
1. **Records decisions** - Captures all open questions and decision points
2. **Creates review structure** - Formats complex information for easy consumption later
3. **Documents prompts** - Writes the exact questions you'll be asked when you return
4. **Logs session** - Creates permanent record in your logging system
5. **Asks what's next** - Doesn't assume session is over, hands control back

**Deferred review:**
- You don't need to process everything right now
- Information is structured for "spoon-feeding" later
- Decisions can be made one at a time when you're ready

---

## Example Output

When you use this prompt, the AI should:

```markdown
# [Topic] - Decision Points

**Date:** 2025-10-10
**Context:** [Brief summary]

## Decision 1: [Topic]

**Question:** [Clear question]

**Options:**
A) [Option with explanation]
B) [Option with explanation]
C) [Option with explanation]

**Prompt to use later:**
> "[Simple question format]
> A) [Short option]
> B) [Short option]
> C) [Short option]
>
> Just give me A, B, or C."

## Next Steps (In Order)
1. [First step]
2. [Second step]
...

**Status:** Awaiting your input on decisions above
**Next:** [What happens when you return]
```

Plus a session log update with full transcript.

---

## Why This Works

**Cognitive load management:**
- Acknowledges you're overwhelmed with information
- Provides structure for later processing
- No pressure to decide everything now

**Continuity:**
- Future sessions can pick up exactly where you left off
- Decisions are captured as simple A/B/C choices
- Context isn't lost

**Control:**
- AI asks "what's next" - doesn't assume session is ending
- You can continue or close the session
- Respects your workflow

---

## Usage Tips

### When to use this:
- End of a planning discussion with many options
- After complex technical analysis
- When you need to review detailed proposals
- Before context switching to another task

### When NOT to use this:
- Simple, already-completed tasks
- When you've already decided everything
- Quick questions with immediate answers

### Adapt the language:
The exact wording isn't sacred. The pattern is:
1. "Record decisions and questions"
2. "Structure for later review"
3. "Spoon-feed format"
4. "Log the session"
5. "Ask what's next"

---

## Integration with DEIA

If using DEIA auto-logging:
- This triggers the session-end logging breakpoint
- Session gets saved to `.deia/sessions/`
- Decision documents go in `.deia/private/notes/`
- `project_resume.md` gets updated automatically

If not using DEIA:
- Adapt to your note-taking system
- Store decision documents where you track project decisions
- Use your existing logging approach

---

## Platform Compatibility

**Works with:**
- Claude Code (tested and validated)
- Any CLI-based AI assistant
- Browser-based tools (Claude.ai, ChatGPT) with manual saving
- IDEs with AI chat (adapt the logging portion)

**Key requirement:**
- AI must have access to file system or you manually save its output
- Some persistence mechanism for session logs

---

## Real Example

**Context:** Discussion about documenting Claude Code startup protocol for BOK

**User prompt:** *(the shutdown protocol above)*

**AI response:**
1. Created `.deia/private/notes/20251010-bok-documentation-decisions.md`
2. Recorded 6 decision points with A/B/C/D options
3. Wrote exact prompts to use later
4. Logged session to `.deia/sessions/20251010-154813-conversation.md`
5. Asked: "What's next?"

**User can now:**
- Review decisions at their own pace
- Answer with simple "A", "B", "C" responses
- Pick up exactly where they left off
- Not lose any context

---

## Variations

### Minimal version (no decision recording):
```
Log this session and ask me what's next
```

### Extended version (with specific focus):
```
record the decisions about [TOPIC], structure them for spoon-feeding later,
log the session, and ask me what's next
```

### Emergency version (context window filling):
```
context window is getting full - log everything we discussed about [TOPIC]
before it gets truncated, and ask me what's next
```

---

## Benefits

1. **No context loss** - Everything is captured before session ends
2. **Reduced cognitive load** - Complex decisions structured for easy review
3. **Continuity** - Future sessions start with full context
4. **Control** - You decide when session actually ends
5. **Flexibility** - Can defer decisions without losing information

---

## Related Patterns

- **Session Resume Protocol** - How to start sessions (see `project_resume.md` pattern)
- **Spoon-Feed Decision Making** - Breaking complex choices into simple A/B/C options
- **Session Logging** - Automated conversation capture (DEIA auto-logging)

---

## Contributing

If you adapt this pattern for your workflow, consider sharing:
- Variations that work for your use case
- Integration with other tools
- Improvements to the structure

Submit to DEIA BOK: https://github.com/deiasolutions/deia

---

## License

CC0 1.0 Universal - Public Domain
Use freely, no attribution required (but appreciated!)
