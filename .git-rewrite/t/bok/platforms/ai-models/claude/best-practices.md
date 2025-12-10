# Claude Best Practices

**What makes Claude shine**

## 1. Iterative Refinement & Context Retention

Claude excels at back-and-forth refinement over long conversations.

**Pattern:**
- Start with rough architecture idea
- Let Claude propose detailed design
- Iterate with feedback and questions
- Claude maintains context, improves with each iteration

**Why it works:**
- Strong context window (200K tokens)
- Constitutional AI training optimizes for helpful iteration
- Remembers earlier decisions in conversation

**Example use case:**
```
Session 1: "Design a logging system"
Session 10: "Remember the logging system we designed? Add PII redaction"
Claude: References original design, maintains consistency
```

**Contributed by:** @deiasolutions (2025-10-06)

---

## 2. Constitutional AI for Security & Ethics

Claude refuses harmful requests more reliably and explains why.

**Pattern:**
- Security code reviews
- Ethical considerations in system design
- Compliance-sensitive applications

**When to choose Claude over GPT:**
- Need AI to flag potential security issues
- Building systems with ethical implications
- Want explanations of why something might be problematic

**Example:**
```
User: "Help me scrape competitor pricing"
Claude: Explains legal concerns (ToS violations, CFAA),
        suggests ethical alternatives (public APIs, partnerships)
GPT: Often provides scraping code without hesitation
```

**Contributed by:** @deiasolutions (2025-10-06)

---

## 3. Structured Thinking for Complex Problems

Claude shows reasoning process when solving complex problems.

**Pattern:**
- Ask Claude to "think step by step"
- Request explicit reasoning before solutions
- Use for architecture decisions, not just code generation

**Example:**
```
Prompt: "Think step by step: How should we design user authentication
        for a multi-tenant SaaS with SSO requirements?"

Claude response:
1. First, let's consider the tenant isolation requirements...
2. SSO implies we need SAML/OIDC support...
3. This suggests a federated identity architecture...
[Detailed reasoning follows]
```

**Why this works:**
- Claude trained to show reasoning
- Catches flaws in logic before implementation
- Helps human understand trade-offs

**Contributed by:** @deiasolutions (2025-10-06)

---

## 4. Nuanced Understanding of Requirements

Claude better interprets ambiguous or high-level requirements.

**Pattern:**
- Provide context-rich but loosely specified requirements
- Let Claude ask clarifying questions
- Iterate to precise specification

**When to choose Claude:**
- Early-stage architecture exploration
- Requirements are fuzzy or evolving
- Need AI to identify unstated assumptions

**Contributed by:** @deiasolutions (2025-10-06)

---

## 5. Refusal to Hallucinate (Usually)

When Claude doesn't know, it tends to say so rather than make things up.

**Pattern:**
- Ask about unfamiliar libraries or APIs
- Request information outside training data
- Claude more likely to say "I don't know" than hallucinate

**Example:**
```
User: "How do I use the FooBarBaz library for quantum computing?"
Claude: "I'm not familiar with a library called FooBarBaz.
         Could you provide more context or check if the name is correct?"
GPT: [May generate plausible-sounding but fictional API documentation]
```

**Caveat:** Claude still hallucinates sometimes, always verify critical information.

**Contributed by:** @deiasolutions (2025-10-06)

---

## When NOT to Use Claude

**Choose other models when:**

1. **Need massive context** - Gemini 1.5 Pro (1M tokens) > Claude (200K tokens)
2. **Code execution required** - Gemini can run Python internally
3. **Speed critical** - GPT-3.5 or Gemini Flash faster than Claude
4. **Integrated into IDE** - Copilot better for inline suggestions

---

## Model Comparison Quick Reference

| Use Case | Best Model |
|----------|-----------|
| Architecture design | Claude |
| Iterative refinement | Claude |
| Security review | Claude |
| Ethical considerations | Claude |
| Massive context (>200K tokens) | Gemini 1.5 Pro |
| Code execution validation | Gemini |
| Speed over quality | GPT-3.5, Gemini Flash |
| IDE inline completion | Copilot |

---

## Contributing

Found a Claude best practice? Submit a PR with:
- Clear description of the pattern
- Example use case
- When it works (and when it doesn't)
- Your attribution (username + date)

---

**Last updated:** 2025-10-06
**Contributors:** @deiasolutions
