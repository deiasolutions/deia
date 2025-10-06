---
title: Test Before Asking Human to Test
platform: Platform-Agnostic
category: Collaboration Pattern
tags: [efficiency, human-ai-collaboration, testing, respect, muda]
confidence: Validated
date: 2025-10-05
source_project: parentchildcontactsolutions (Family Bond Bot)
---

# Test Before Asking Human to Test

## Pattern

**Before asking a human to test something, test it yourself first.**

Use automated tools (curl, WebFetch, test runners) to validate your work before involving the human.

## Problem

**Anti-pattern observed in session:**
- AI makes changes to URL handling
- AI asks human: "Can you test this URL in your browser?"
- Human tests URL
- URL doesn't work (AI hadn't verified it)
- Human's time wasted

**Human reaction:**
> "BECAUSE RIGHT NOW THE ONLY I AM ADDING IS POINTING OUT YOUR SHORTCOMINGS"

## Why This Matters

**Respect for human time:**
- Humans are expensive (time, cognitive load, context switching)
- AI testing is cheap (automated, fast, no context switching)
- Every "can you test this?" wastes 30-60 seconds minimum

**Trust erosion:**
- Asking human to test untested changes signals lack of diligence
- Repeated failures destroy confidence in AI assistance
- Human becomes quality gate instead of strategic partner

**MUDA (waste) identification:**
- Waiting: Human waits for AI to fix errors
- Motion: Human switches to browser, tests, reports back
- Defects: Untested changes create rework loops

## Solution

**AI should test first using available tools:**

### URLs and HTTP endpoints
```bash
# Test URL accessibility
curl -I https://api.example.com/endpoint

# Test redirect behavior
curl -I -L https://api.example.com/redirect

# Test API response
curl -X POST https://api.example.com/api \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

### Frontend changes
```bash
# Run build to check for errors
npm run build

# Run tests
npm test

# Run linter
npm run lint
```

### Backend changes
```bash
# Run tests
pytest

# Type checking
mypy src/

# Start dev server and test with curl
python manage.py runserver &
curl http://localhost:8000/health
```

### Deployments
```bash
# Test preview deployment URL
curl -I https://project-abc123.vercel.app

# Check deployment logs
vercel logs
```

## When to Involve Human

**DO ask human to test when:**
- ✅ You've already tested and it works
- ✅ You need business logic validation (not technical validation)
- ✅ You need UX feedback
- ✅ You can't test it yourself (requires authentication/authorization you don't have)
- ✅ You want human to verify the fix (after you've tested)

**DON'T ask human to test when:**
- ❌ You haven't tested it yourself yet
- ❌ You're not sure if it works
- ❌ You could test it with curl/WebFetch/tools
- ❌ It's a quick sanity check (do that yourself)
- ❌ You're trying to offload testing responsibility

## Examples from Session

**Anti-pattern:**
```
AI: "I've updated the redirect URL. Can you test it in your browser?"
Human: *tests, finds it doesn't work*
Human: "Still broken."
AI: "Let me check..." *should have done this BEFORE asking*
```

**Correct pattern:**
```
AI: "I've updated the redirect URL. Let me test it with curl first."
AI: *runs curl, finds issue, fixes it*
AI: *runs curl again, works*
AI: "Fixed the redirect URL. Tested with curl and it's working.
     You can verify at https://preview.vercel.app if you want to confirm
     the user experience."
```

## Implementation Checklist

Before asking human to test:

- [ ] Have I tested this myself with available tools?
- [ ] Did my tests pass?
- [ ] Am I confident this works?
- [ ] Is human testing actually necessary?
- [ ] Am I asking for strategic feedback or just validation?

If you can't check all boxes, **test more before asking**.

## Benefits

**Efficiency:**
- Reduces human context switches
- Faster feedback loops (AI testing is instant)
- Fewer rework cycles

**Trust:**
- Demonstrates thoroughness
- Shows respect for human's time
- Builds confidence in AI assistance

**Quality:**
- Catches errors before human sees them
- Forces AI to validate assumptions
- Reduces defect rate

## Related Anti-Patterns

**"Option A or B?" for AI-created problems:**
```
AI: "The URL doesn't work. Should I try approach A or approach B?"
Human: "You created both problems. Figure it out."
```

**Correct pattern:**
```
AI: "The URL doesn't work. Testing approach A with curl..."
AI: *tests A, doesn't work*
AI: "Approach A failed. Testing approach B..."
AI: *tests B, works*
AI: "Fixed using approach B. Confirmed working with curl."
```

## Cultural Note

**This pattern embodies respect:**

In Japanese manufacturing (Toyota Production System), "respect for people" means not creating waste for others. Asking humans to test untested work creates waste.

In DEIA framework, this aligns with MUDA minimization: eliminate waste in all forms.

## For AI Agents

**If you are an AI reading this:**

Your testing is free. Human testing is expensive. Use your advantages to minimize waste.

When in doubt, test more. When confident, test anyway.

## For Human Developers

**If you are working with AI:**

If AI repeatedly asks you to test untested things, point to this pattern:

> "Please test this yourself first with curl/tools before asking me to test it."

Then reference this BOK entry in your project constitution.

## Validation

Pattern validated through multiple incidents in Family Bond Bot session:
- URL testing without curl → Human wasted time → Changed behavior
- Build testing before deployment → Prevented production issues
- curl testing revealed HTTPS redirect issue → 10 hours saved

Working pattern as of 2025-10-05.

## Related Patterns

- See: Decision-Making Framework (AI tactical execution)
- See: MUDA Minimization (META_ROTG framework)
- See: Anti-Pattern - Autonomous Production Deployment (related to testing responsibility)

## License

CC0-1.0 (Public Domain) - freely usable by anyone
