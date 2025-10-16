---
title: "Proposal: BOK Context Injection for LLM Sessions"
date: 2025-10-16
author: daaaave-atx
status: Proposed
category: Process Improvement
tags: [bok, llm-workflow, context-management, anti-patterns, automation]
---

# Proposal: BOK Context Injection for LLM Sessions

## Problem

During Q33N Netlify deployment (2025-10-16), Claude failed to:
1. Check BOK for existing Netlify patterns before giving advice
2. Recognize emerging anti-pattern in real-time (DNS configuration confusion)
3. Update behavior based on newly documented patterns

**User feedback:**
> "bad antipattern work there. Shouldn't you sniff for new antipatterns from time to time? should we have a bot serve them up in your env folder so you know there are new antipatterns on the local or the Deia Global Commons site?"

## Root Cause

**LLM context limitations:**
- BOK exists but isn't automatically in context
- LLM must manually read BOK files (if it remembers to)
- No mechanism to surface new patterns mid-session
- No proactive pattern detection workflow

**Current workflow (broken):**
```
User asks platform question
  ↓
LLM gives answer from training data (often outdated/wrong)
  ↓
User corrects LLM
  ↓
LLM documents anti-pattern
  ↓
(Next session: LLM forgets to check BOK, repeats mistake)
```

## Proposed Solution

**Automated BOK Context Injection via Bot**

### Architecture

```
DEIA Bot monitors conversation
  ↓
Detects platform/tech mentions (Netlify, Hugo, Vercel, etc.)
  ↓
Queries local BOK + Global Commons
  ↓
Injects relevant patterns into LLM context
  ↓
LLM sees patterns BEFORE answering
```

### Implementation Phases

#### Phase 1: Manual BOK Check Protocol

**LLM behavior change (immediate):**
- When user asks platform question → "Let me check BOK first"
- Use Grep/Glob to search BOK before answering
- If pattern exists → cite it
- If pattern doesn't exist → flag as potential new pattern

**Example:**
```
User: "How do I configure DNS for Netlify?"
Assistant: "Let me check BOK for Netlify patterns first..."
[searches bok/platforms/netlify/]
Assistant: "Found: bok/platforms/netlify/dns-configuration-ui-confusion.md
Here's what you need to do: [specific answer from BOK]"
```

#### Phase 2: Bot-Assisted Context Injection

**DEIA bot monitors conversation for keywords:**
- Platform names: Netlify, Vercel, Railway, Heroku, etc.
- Tech stack: Hugo, Next.js, Django, etc.
- Operations: deployment, DNS, SSL, domain, build, etc.

**When detected, bot injects relevant BOK entries:**
```
<system-reminder>
Relevant BOK patterns detected:
- bok/platforms/netlify/hugo-version-requirement.md
- bok/platforms/netlify/dns-configuration-ui-confusion.md
</system-reminder>
```

**Bot placement:**
- Monitors conversation in real-time
- Injects context as new messages (like current system-reminders)
- Can be triggered manually: `/bok netlify`

#### Phase 3: Global Commons Integration

**Connect to DEIA Global Commons:**
- Local BOK (repo-specific patterns)
- Global Commons (cross-project patterns)
- Community contributions

**Bot queries both:**
```python
def get_relevant_patterns(keywords):
    local_patterns = search_local_bok(keywords)
    global_patterns = query_commons_api(keywords)
    return merge(local_patterns, global_patterns)
```

**Example global patterns:**
- Netlify DNS config (applies to all projects using Netlify)
- Git workflow best practices (applies to all Git repos)
- LLM hallucination patterns (applies to all AI workflows)

#### Phase 4: Proactive Anti-Pattern Detection

**LLM actively flags potential patterns:**

During conversation, if LLM detects:
- User frustration ("no fucking entries", "why isn't this working")
- Repeated questions about same topic
- Process that feels overly complicated
- Inconsistency with documented patterns

**LLM should:**
1. Flag: "This feels like an anti-pattern - should I document it?"
2. If yes, create BOK entry in real-time
3. Continue with documented solution

**Example:**
```
User: "Netlify shows no DNS records after adding domain"
Assistant: "This seems like a recurring pain point. Let me:
1. Check if we have this documented [searches BOK]
2. Not found - this appears to be a new anti-pattern
3. I'll document it now as bok/platforms/netlify/dns-configuration-ui-confusion.md
4. Here's the solution: [...]"
```

### Technical Implementation

**Bot service:**
```python
# src/deia/services/bok_context_injector.py

class BOKContextInjector:
    def __init__(self, local_bok_path, commons_url):
        self.local_bok = BOKIndex(local_bok_path)
        self.commons = CommonsAPI(commons_url)
        self.keyword_map = load_keyword_patterns()

    def monitor_conversation(self, message):
        keywords = self.extract_keywords(message)
        if keywords:
            patterns = self.fetch_patterns(keywords)
            return self.format_context_injection(patterns)
        return None

    def extract_keywords(self, message):
        # NLP or simple keyword matching
        # Returns: ["netlify", "dns", "domain"]
        pass

    def fetch_patterns(self, keywords):
        local = self.local_bok.search(keywords)
        global_patterns = self.commons.search(keywords)
        return merge_and_rank(local, global_patterns)
```

**Slash command:**
```bash
/bok <keyword>  # Manually request BOK patterns
/bok netlify    # Inject all Netlify patterns
/bok --refresh  # Re-scan BOK for new patterns
```

**Pre-session injection:**
```
# At session start, inject relevant patterns based on:
- Current working directory (detect platform from files)
- Git repo metadata (detect tech stack)
- Recent commits (detect what user is working on)
- Project tags in repo config
```

### Benefits

1. **Prevent repeated mistakes** - LLM sees patterns before answering
2. **Faster responses** - No need to manually search BOK
3. **Consistent advice** - Always cite documented patterns
4. **Real-time learning** - New patterns available immediately
5. **Community knowledge** - Global Commons patterns accessible
6. **Reduced frustration** - User doesn't repeat same explanations

### Drawbacks / Considerations

1. **Context size** - Too many patterns = token bloat
   - Solution: Rank by relevance, inject top 3-5 only
2. **False positives** - Keyword matching too aggressive
   - Solution: User can dismiss injections: `/bok dismiss`
3. **Staleness** - Patterns become outdated
   - Solution: Track last-verified date, flag old patterns
4. **Privacy** - Global Commons might expose project details
   - Solution: Only share patterns, not project-specific code

### Success Metrics

- **Reduction in repeated anti-patterns** (same mistake twice)
- **Time to resolution** (how fast issues are solved)
- **User frustration indicators** (profanity count as proxy 😅)
- **BOK citation rate** (how often LLM cites existing patterns)
- **New pattern creation rate** (healthy growth of knowledge base)

## Related Patterns

- ✅ **Good:** Proactive context injection
- ✅ **Good:** Real-time pattern detection
- ❌ **Bad:** LLM working from stale training data
- ❌ **Bad:** Manually searching docs every time

## Next Steps

1. **Immediate:** Claude adopts manual BOK-check behavior
2. **Week 1:** Implement keyword detection bot
3. **Week 2:** Build context injection mechanism
4. **Week 3:** Connect to Global Commons API
5. **Week 4:** Deploy and monitor

## Open Questions

1. Should BOK injection be opt-in or opt-out?
2. What's the right balance between context size and completeness?
3. How do we version/deprecate outdated patterns?
4. Should LLM be able to edit BOK entries mid-session?
5. How do we prevent BOK from becoming a dumping ground?

---

**Status:** Proposed (2025-10-16)
**Proposed by:** daaaave-atx
**Next step:** Implement Phase 1 (manual BOK checking behavior)

**Tags:** `#process-improvement` `#bok` `#automation` `#llm-workflow` `#context-management`
