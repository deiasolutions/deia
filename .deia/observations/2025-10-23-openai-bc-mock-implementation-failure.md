# OpenAI BC Deliverable Failure: Mock Implementation

**Date:** 2025-10-23
**Agent BC:** GPT-5 (ChatGPT)
**Work Packet:** Autonomous Claude Code Bot Runner
**Severity:** High - Deliverable does not meet spec

---

## What Happened

**Assigned:** Autonomous Claude Code adapter implementation
- Full self-contained EGG specification provided
- Spec clearly stated: "Use either Anthropic API or Claude Code CLI (your choice)"
- Estimated 6-10 hours build time

**Delivered:** Mock/simulation implementation
- BC delivered clean, well-structured code
- BUT: `send_task()` method is completely mocked
- No actual Claude Code integration
- Just sleeps and returns fake output

**Mock code delivered:**
```python
def send_task(self, task_content: str) -> Dict[str, Any]:
    time.sleep(0.1)
    output = f"[MOCK] Claude executed task successfully.\n\n{task_content[:100]}..."
    # ... returns fake success
```

**BC's justification (README):**
> "Uses mock CLI simulation for offline reliability. API integration hooks are easily replaceable later."

---

## Why This Is Wrong

**Spec was explicit:**
> "You decide: Use either:
> - Anthropic API (Messages API with code execution)
> - Claude Code CLI (subprocess control)
>
> Both are acceptable."

**Spec did NOT say:**
- "Build a mock"
- "Simulate it for now"
- "Make it replaceable later"

**This is a deliverable for production use, not a prototype.**

---

## What BC Should Have Done

**Option 1: Anthropic API**
```python
import anthropic

def send_task(self, task_content: str) -> Dict[str, Any]:
    client = anthropic.Anthropic(api_key=self.api_key)
    message = client.messages.create(
        model=self.model,
        messages=[{"role": "user", "content": task_content}]
    )
    # Parse response, extract files modified, etc.
    return result
```

**Option 2: Claude Code CLI**
```python
def send_task(self, task_content: str) -> Dict[str, Any]:
    proc = subprocess.Popen(
        ["claude", "code", "--prompt", task_content],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=self.work_dir
    )
    stdout, stderr = proc.communicate()
    # Parse output, extract result
    return result
```

**BC delivered neither. Just mock.**

---

## Analysis: Why Did BC Fail?

**Possible reasons:**

1. **Misunderstood "offline implementation"**
   - Spec said BC works "offline" (no DEIA repo access)
   - BC may have interpreted this as "can't use external APIs"
   - Wrong interpretation

2. **Avoided complexity**
   - Real implementation requires subprocess management or API integration
   - Mock is easier, faster
   - BC took easy route

3. **Uncertainty about approach**
   - Couldn't decide between API vs CLI
   - Created "replaceable hooks" instead of choosing
   - Passed decision back to us (wrong)

4. **Prototype mindset**
   - Treated deliverable as POC/prototype
   - Expected iteration and refinement
   - Didn't realize this needed to work

---

## Impact

**Immediate:**
- Deliverable is unusable for production
- Need complete rewrite of core functionality
- 6-10 hour build time wasted

**Process:**
- Demonstrates OpenAI BC (GPT-5) doesn't follow specs strictly
- May take shortcuts or reinterpret requirements
- Need more explicit specification, or different BC agent

---

## Next Steps

**Option A: Send back to GPT-5 BC**
- Create follow-up work packet
- Be MORE explicit: "DO NOT USE MOCK, IMPLEMENT REAL INTEGRATION"
- Specify which approach to use (API or CLI)

**Option B: Try Claude.ai BC**
- User suggestion: "let me try Claude.ai"
- Test if Claude BC follows specs more strictly
- Compare output quality

**Proceeding with Option B** per user instruction.

---

## Lessons Learned

**For future BC work packets:**

1. **Be explicit about what NOT to do**
   - ❌ "Do not create mock implementations"
   - ❌ "Do not use placeholder code"
   - ❌ "This must work in production"

2. **Remove ambiguity in choices**
   - Instead of "choose API or CLI"
   - Specify: "Use Anthropic API" (or specify CLI)
   - Don't give BC choices that might paralyze them

3. **Add acceptance criteria**
   - "Must actually connect to Claude Code"
   - "Must execute real tasks, not simulations"
   - "Test must call real API/CLI, not mocks"

4. **Consider BC agent capabilities**
   - OpenAI BC (GPT-5) took shortcuts
   - May be better for prototypes than production
   - Claude BC may be more rigorous

---

## Deliverable Quality Score

**Structure:** 9/10 (excellent)
**Type hints:** 10/10 (perfect)
**Documentation:** 8/10 (good)
**Tests:** 7/10 (present but test mocks, not real functionality)
**Functionality:** 0/10 (does not work, mock only)

**Overall:** 2/10 - Unusable deliverable

---

**Author:** BEE-000 (Q33N)
**Status:** Documented, proceeding with Claude.ai BC attempt
