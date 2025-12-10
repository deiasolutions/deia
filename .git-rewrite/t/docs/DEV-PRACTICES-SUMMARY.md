# DEIA Development Practices - Quick Reference

**Last Updated:** 2025-10-09

---

## Core Practices

### 1. **TDD Always** 🧪
- Write tests FIRST, implementation second
- No code without tests
- No exceptions, no excuses
- Run tests before committing

### 2. **Platform-Agnostic Design** 🌐
- Python does the work
- AI/editors are just interfaces
- Works with Claude Code, Cursor, GitHub Copilot, or manually
- Thin wrappers for each platform

### 3. **Automation-First** 🤖
- Minimize manual steps
- User runs one command, Python does the rest
- AI assists but doesn't replace automation

### 4. **Privacy & Security First** 🔒
- Sanitize before sharing (PII, secrets, API keys)
- User controls their data
- Two-tier sanitization: `--for-ai` vs `--for-public`
- Opt-in telemetry only

### 5. **Question Complexity** 🤔
- If it feels overengineered, it probably is
- Start simple, add complexity only when needed
- Challenge assumptions

---

## Communication Standards

### With Dave

**"Yes, but..." Pattern:**
- If Dave says "Yes. And..." or "Yes, but..."
- STOP immediately
- Answer the question FIRST
- Don't proceed until question is answered
- Then ask: "Ready to proceed now?"

**No Multiple Yes/No Questions:**
- Don't ask: "Should I do X? And do you want Y?"
- Instead: "What would you like? A) X, B) Y, C) Something else"
- If you mess up: Recognize ambiguity, ask for clarification

**Ask Clarifying Questions:**
- Never assume
- If unclear, ask BEFORE proceeding
- It's better to ask than to build the wrong thing

---

## Development Workflow

### 1. **Bug Reports & Feature Requests**
- All submissions (even from Dave) go through official process
- Create submission in `.deia/submissions/pending/`
- Assign ID: `DEIA-YYYY-NNN-TYPE`
- Review → Prioritize → Implement

### 2. **Prioritization**
- Flexible: Can do feature before bug if strategic
- Priority levels: P0 (critical) → P3 (low)
- Some bugs are fixed by upcoming features (skip them)
- Some features need bugs fixed first

### 3. **Git Workflow**
- Commit messages: Clear, concise, explain WHY
- Reference issues: "Fixes DEIA-2025-001-BUG"
- Small, focused commits
- Tests pass before commit

### 4. **Code Review**
- Self-review before asking Dave
- Check TDD compliance
- Verify tests cover edge cases
- Confirm follows standards

---

## Code Standards

### Testing
```python
# 1. Write failing test FIRST
def test_safe_print_handles_unicode():
    result = safe_print(console, "✓ Success")
    assert result is True

# 2. Write minimal implementation
def safe_print(console, message):
    console.print(message)
    return True

# 3. Run test (should pass)
# 4. Refactor
# 5. Repeat
```

### Python
- Python 3.8+ compatibility
- Type hints where helpful
- Docstrings for public functions
- Click for CLI
- pytest for tests

### TypeScript (VS Code Extension)
- Calls Python CLI (subprocess)
- Thin wrapper, no business logic
- VS Code API best practices

---

## Documentation

### What to Document
- ✅ Why (context, decisions)
- ✅ How to use (examples)
- ✅ Architecture decisions (ADRs)
- ❌ What (code documents itself)

### Where
- `README.md` - Quick start, overview
- `CONTRIBUTING.md` - How to contribute
- `docs/` - Detailed guides, ADRs
- `bok/patterns/` - Community patterns
- Code comments - Why, not what

---

## Tools & Stack

### Current
- **Python 3.13** (but support 3.8+)
- **Click** - CLI framework
- **Rich** - Terminal UI
- **pytest** - Testing
- **TypeScript** - VS Code extension
- **Git + GitHub** - Version control

### Future
- FastAPI (web dashboard)
- PostgreSQL (global BOK)
- React (dashboard UI)

---

## Anti-Patterns (Don't Do This)

❌ Code without tests
❌ Assume what Dave wants
❌ Overengineer solutions
❌ Ask multiple yes/no questions
❌ Proceed before answering follow-up questions
❌ Manual steps when automation is possible
❌ Lock into one AI platform
❌ Share data without sanitization
❌ Commit without running tests

---

## Quality Standards

### Before Merge
- [ ] Tests written FIRST
- [ ] All tests pass
- [ ] Code follows standards
- [ ] Documentation updated
- [ ] No security issues
- [ ] Sanitization works
- [ ] Platform-agnostic (if applicable)

### Metrics
- Test coverage: Aim for >80%
- No failing tests in main
- All submissions reviewed
- No secrets in commits

---

## Issue Tracking

### Format
`DEIA-YYYY-NNN-TYPE`

Examples:
- `DEIA-2025-001-BUG` - Unicode crash
- `DEIA-2025-002-FEAT` - AI review feature
- `DEIA-2025-003-PAT` - Pattern submission

### Priority
- **P0** - Critical (security, data loss)
- **P1** - High (blocks users, major bugs)
- **P2** - Medium (important features, minor bugs)
- **P3** - Low (nice-to-have, polish)

### Status
`Pending → Triaged → In Progress → Review → Done → Closed`

---

## Version Control

### Branching (Future)
- `main` - Stable, production
- `develop` - Integration branch
- `feature/xyz` - Feature branches
- `fix/bug-123` - Bug fix branches

### Currently
- Working directly on `main` (early stage)
- Will adopt branching when team grows

---

## Release Process (Future)

1. Update version in `pyproject.toml` and `package.json`
2. Run full test suite
3. Build Python package
4. Publish to PyPI
5. Build VS Code extension
6. Publish to Marketplace
7. Tag release in Git
8. Update changelog

---

## Learning & Improvement

### Track Hallucinations
- Report AI mistakes
- Build dataset
- Share with AI vendors
- Improve over time

### Track Token Usage
- Measure efficiency
- Show cost to users
- Optimize prompts
- Share metrics (opt-in)

### Community Feedback
- Submissions teach us patterns
- Users find bugs we missed
- Build BOK together

---

**Remember:** Simple, tested, automated, private, platform-agnostic.
