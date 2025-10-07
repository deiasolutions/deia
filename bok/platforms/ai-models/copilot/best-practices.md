# GitHub Copilot Best Practices

**What makes Copilot shine**

## 1. Inline Code Completion (IDE Integration)

Copilot excels at real-time, context-aware code suggestions in your IDE.

**Pattern:**
- Write function signature, Copilot completes body
- Start typing pattern, Copilot suggests continuation
- Write comment describing logic, Copilot generates code
- Tab-complete through suggestions

**Why it works:**
- Trained on billions of lines of public code
- Understands language-specific patterns
- Fast inference for inline suggestions
- Integrated into natural coding flow

**Example:**
```python
# Write comment
def validate_email(email: str) -> bool:
    """Check if email is valid using regex"""
    # Copilot suggests complete implementation
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

**Better than Claude/GPT/Gemini for:**
- Flow state coding (no context switching)
- Boilerplate generation
- Learning new codebases (suggests based on repo patterns)

**Contributed by:** Community (2025-10-06)

---

## 2. Learning from Repository Context

Copilot analyzes your open files and repo patterns.

**Pattern:**
- Copilot suggests code matching your project's style
- Learns naming conventions
- Follows established patterns
- Adapts to your frameworks

**Why it works:**
- Indexes open editor tabs
- Analyzes repo structure
- Learns from your edits

**Example:**
```javascript
// Your repo uses camelCase for functions
// You start typing: function getUser
// Copilot suggests: function getUserById(userId) { ... }
// Matches your repo's naming style automatically
```

**Contributed by:** Community (2025-10-06)

---

## 3. Test Generation (Copilot Labs)

Copilot can generate test cases from existing functions.

**Pattern:**
- Select function
- Use Copilot Labs "Generate Tests"
- Review and refine generated tests
- Covers edge cases you might miss

**Why it works:**
- Trained on millions of test files
- Understands common testing patterns
- Suggests test frameworks matching your project

**Example:**
```python
# Original function
def divide(a, b):
    return a / b

# Copilot generates
def test_divide():
    assert divide(10, 2) == 5
    assert divide(0, 5) == 0
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
```

**Contributed by:** Community (2025-10-06)

---

## 4. Multi-File Awareness (Copilot X)

Copilot X can reference multiple files in suggestions.

**Pattern:**
- Import from other files
- Copilot suggests based on imported types
- Maintains consistency across files
- Understands module relationships

**Example:**
```typescript
// In models/User.ts
export interface User {
  id: string;
  email: string;
}

// In services/userService.ts
import { User } from '../models/User';

function createUser(email: string): User {
  // Copilot suggests implementation using User interface
  return {
    id: generateId(),
    email: email
  };
}
```

**Contributed by:** Community (2025-10-06)

---

## 5. Documentation Generation

Copilot generates docstrings and comments from code.

**Pattern:**
- Write function
- Type `"""` or `/**`
- Copilot suggests complete documentation
- Includes parameters, return values, examples

**Example:**
```python
def calculate_fibonacci(n: int) -> list[int]:
    # Type """ and Copilot suggests:
    """
    Calculate Fibonacci sequence up to n terms.

    Args:
        n: Number of terms to generate

    Returns:
        List of Fibonacci numbers

    Example:
        >>> calculate_fibonacci(5)
        [0, 1, 1, 2, 3]
    """
```

**Contributed by:** Community (2025-10-06)

---

## When NOT to Use Copilot

**Choose other models when:**

1. **Complex architecture** - Claude better at design discussions
2. **Explanation needed** - GPT/Claude better at explaining concepts
3. **Large context** - Gemini handles bigger codebases
4. **Novel algorithms** - Copilot suggests common patterns, not novel solutions

---

## Copilot Feature Comparison

| Feature | Availability |
|---------|--------------|
| Inline completion | All plans |
| Multi-line suggestions | All plans |
| Test generation | Copilot Labs |
| Chat interface | Copilot X |
| PR summaries | Copilot X |
| Command palette | Copilot X |

---

## Common Pitfalls

### 1. License Concerns
Copilot trained on public code, may suggest copyrighted snippets.

**Mitigation:**
- Enable "public code filter" in settings
- Review suggestions for familiar patterns
- Check licenses if code seems copied
- Use GitHub's code reference tool

### 2. Security Vulnerabilities
May suggest insecure patterns from training data.

**Mitigation:**
- Always review security-critical code
- Use linters and security scanners
- Don't blindly accept authentication/crypto suggestions
- Test thoroughly

### 3. Outdated Patterns
Training data has cutoff, may suggest deprecated APIs.

**Mitigation:**
- Verify against current documentation
- Check for deprecation warnings
- Update Copilot regularly
- Cross-reference with official docs

### 4. Over-Reliance
Can become crutch, reduces learning.

**Mitigation:**
- Understand what Copilot suggests
- Disable occasionally to practice
- Use as learning tool, not replacement
- Review and modify suggestions

---

## Pro Tips

### Maximize Suggestion Quality
```
1. Write clear function names
   - Good: getUserByEmail
   - Bad: get

2. Add type hints
   - Copilot uses types for better suggestions

3. Write descriptive comments
   - Comment explains intent → better code

4. Open related files
   - More context = better suggestions
```

### IDE-Specific Features

**VS Code:**
- `Ctrl+Enter`: Show all suggestions
- `Alt+]`: Next suggestion
- `Alt+[`: Previous suggestion

**JetBrains:**
- Similar shortcuts in IntelliJ/PyCharm
- Copilot panel for chat

**Vim/Neovim:**
- Plugin available
- Custom keybindings

---

## Copilot vs Chat Models

| Task | Best Tool |
|------|-----------|
| Inline completion | Copilot |
| Boilerplate generation | Copilot |
| Architecture design | Claude |
| Explaining code | GPT/Claude |
| Large refactors | Gemini (1M context) |
| Learning concepts | GPT/Claude |

**Use together:**
- Copilot for coding flow
- Claude for architecture discussion
- Switch contexts for different tasks

---

## Contributing

Found a Copilot best practice? Submit a PR with:
- Clear description of the pattern
- Example use case
- When it works (and when it doesn't)
- Your attribution (username + date)

---

**Last updated:** 2025-10-06
**Contributors:** Community
