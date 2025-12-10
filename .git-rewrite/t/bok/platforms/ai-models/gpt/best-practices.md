# GPT Best Practices

**What makes GPT shine**

## 1. Function Calling & Tool Integration

GPT excels at structured function calling and API integration.

**Pattern:**
- Define functions with JSON schemas
- GPT determines which functions to call
- Returns structured JSON responses
- Excellent for building agents and workflows

**Why it works:**
- Trained specifically for function calling
- Reliable JSON structure output
- Strong at parsing requirements into API calls

**Example:**
```json
// Define function schema
{
  "name": "search_products",
  "parameters": {
    "query": "string",
    "price_range": {"min": "number", "max": "number"}
  }
}

// GPT usage
User: "Find laptops under $1000"
GPT: Calls search_products(query="laptops", price_range={min:0, max:1000})
```

**Contributed by:** Community (2025-10-06)

---

## 2. Speed & Responsiveness (GPT-3.5/4-Turbo)

GPT-3.5 and GPT-4-Turbo optimize for speed over context.

**Pattern:**
- Quick iterations during development
- Simple code generation tasks
- Rapid prototyping

**When to choose GPT-3.5:**
- Cost-sensitive applications
- Simple, well-defined tasks
- Speed more important than nuance

**Benchmark:**
- GPT-3.5: ~1-2 seconds for typical responses
- GPT-4: ~3-5 seconds
- Claude: ~4-6 seconds
- Gemini: ~2-4 seconds

**Contributed by:** Community (2025-10-06)

---

## 3. Code Generation (GPT-4)

GPT-4 strong at generating working code from specifications.

**Pattern:**
- Provide clear spec with examples
- Request specific language/framework
- GPT generates syntactically correct code
- Good for greenfield development

**When to choose GPT-4 over Claude:**
- Need code fast with minimal iteration
- Spec is clear and unambiguous
- Less concerned with architectural reasoning

**Example:**
```
Prompt: "Write a Python function that validates email addresses
         using regex. Include tests."

GPT-4: [Generates complete function + pytest tests in one shot]
```

**Contributed by:** Community (2025-10-06)

---

## 4. Broad Knowledge Base

GPT-4 trained on massive, diverse dataset.

**Pattern:**
- Cross-domain questions
- Obscure libraries or frameworks
- Historical or cultural context needed

**Why it works:**
- Trained on wider range of sources
- Good at connecting disparate concepts
- Strong general knowledge

**Contributed by:** Community (2025-10-06)

---

## 5. o1 Series: Advanced Reasoning

GPT-o1 models excel at complex reasoning tasks.

**Pattern:**
- Mathematical proofs
- Complex algorithmic problems
- Multi-step logical reasoning
- Scientific analysis

**When to choose o1:**
- Problem requires deep reasoning
- Willing to wait longer for response
- Need step-by-step mathematical work

**Example:**
```
Prompt: "Prove that the sum of two even numbers is always even"
o1: [Provides formal mathematical proof with clear steps]
```

**Caveat:** o1 models slower and more expensive than GPT-4.

**Contributed by:** Community (2025-10-06)

---

## When NOT to Use GPT

**Choose other models when:**

1. **Need ethical guardrails** - Claude more reliable at refusing harmful requests
2. **Iterative refinement** - Claude better at maintaining context over long conversations
3. **Massive context** - Gemini 1.5 Pro (1M tokens) > GPT-4 (128K tokens)
4. **Code execution** - Gemini can run Python internally

---

## GPT Model Selection

| Model | Best For |
|-------|----------|
| GPT-4 | Complex tasks, code generation, broad knowledge |
| GPT-4-Turbo | Balance of speed and capability |
| GPT-3.5 | Cost-sensitive, simple tasks, speed critical |
| o1-preview | Advanced reasoning, math, science |
| o1-mini | Faster reasoning tasks, lower cost than o1-preview |

---

## Common Pitfalls

### 1. Hallucination
GPT more likely to confidently state incorrect information than Claude.

**Mitigation:**
- Always verify critical facts
- Ask for sources/citations
- Cross-check with documentation

### 2. Over-Confident Responses
GPT rarely says "I don't know."

**Mitigation:**
- Question responses that seem too perfect
- Test generated code thoroughly
- Use Claude for uncertain domains

### 3. Function Calling Limitations
GPT may call functions incorrectly with complex schemas.

**Mitigation:**
- Keep function schemas simple
- Provide clear parameter descriptions
- Validate all function call arguments

---

## Contributing

Found a GPT best practice? Submit a PR with:
- Clear description of the pattern
- Example use case
- When it works (and when it doesn't)
- Your attribution (username + date)

---

**Last updated:** 2025-10-06
**Contributors:** Community
