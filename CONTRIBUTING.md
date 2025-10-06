# Contributing to DEIA

**Thank you for helping build collective intelligence for AI collaboration.**

---

## Quick Start

**Three ways to contribute:**

1. **Share Patterns** - Submit useful patterns from your work
2. **Improve Code** - Enhance the DEIA toolkit
3. **Write Docs** - Help others understand and use DEIA

---

## How to Contribute Patterns (BOK)

### Step 1: Log Your Work

Use DEIA conversation logging:

```bash
deia log conversation
```

Or manually create logs in `.deia/sessions/`

### Step 2: Identify Shareable Patterns

**What makes a good pattern:**
- ✅ Universally useful (not project-specific)
- ✅ Actionable (others can apply it)
- ✅ Validated (you've proven it works)
- ✅ Clear (easy to understand)

**Examples:**
- "Test AI changes before asking human to test"
- "Railway HTTPS redirect middleware pattern"
- "How to structure AI decision-making"

**Not patterns:**
- ❌ Project-specific code
- ❌ "It depends" without guidance
- ❌ Theoretical ideas (not tested)

### Step 3: Extract Pattern

Create a markdown file following the BOK template:

```markdown
---
id: unique-slug
date: 2025-10-06
platform: claude-code
category: pattern
confidence: validated
sources: 1
---

# Pattern: [Descriptive Name]

## Problem
What problem does this solve?

## Solution
How to solve it (step-by-step if complex)

## Context
When to use this pattern (and when NOT to)

## Example
Code, conversation, or concrete example

## Validation
How you know it works

## Related
Links to related patterns or anti-patterns
```

### Step 4: Sanitize

**CRITICAL: Remove sensitive information**

**Must remove:**
- Names, emails, usernames → `[Name]`, `User`, `Developer`
- Company names → `Company X`, `Organization`
- Internal URLs → `example.com`, `internal.com`
- API keys → `[REDACTED]` or `YOUR_API_KEY`
- Passwords, tokens → `[REDACTED]`
- Proprietary code → Generic examples only
- Client information → `Client`, `Customer`

**Use sanitization tool:**
```bash
deia sanitize pattern.md
```

**Then manually review** - automation can't catch everything.

### Step 5: Submit

**Option A: Pull Request** (preferred when public repo exists)

```bash
# Fork the repo
git clone https://github.com/YOUR_USERNAME/deia.git
cd deia

# Create branch
git checkout -b pattern/your-pattern-name

# Add your pattern to appropriate category
# bok/patterns/[category]/your-pattern.md
# bok/platforms/[platform]/your-pattern.md
# bok/anti-patterns/your-antipattern.md

# Commit
git add bok/
git commit -m "Add pattern: Your Pattern Name"

# Push and create PR
git push origin pattern/your-pattern-name
# Then create PR on GitHub
```

**Option B: Issue submission** (if unsure about PR)

1. Go to [Issues](https://github.com/deiasolutions/deia/issues)
2. Create new issue: "Pattern Submission: [Name]"
3. Paste sanitized pattern in issue body
4. Maintainers will review and add to BOK

**Option C: Email** (for sensitive discussions)

Send to: contact@deiasolutions.org (coming soon)

### Step 6: Review Process

**What happens:**
1. Maintainer reviews submission
2. Checks sanitization (no PII, secrets, IP)
3. Verifies pattern is universal
4. Tests if applicable
5. Accepts → merges to BOK
6. Rejects → explains why with suggestions

**Timeline:** 1-7 days typically

---

## How to Contribute Code

### Areas Needing Help

**High priority:**
- Improved sanitization detection
- Automated pattern extraction from logs
- Web dashboard for BOK search
- Integration tests
- Platform integrations (Cursor, Copilot)

**Medium priority:**
- CLI improvements
- Documentation enhancements
- Example projects
- MCP server integration

### Development Setup

```bash
# Clone repo
git clone https://github.com/deiasolutions/deia.git
cd deia

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check src/
```

### Code Standards

**Style:**
- Follow PEP 8
- Use type hints
- Write docstrings (Google style)
- Keep functions small and focused

**Testing:**
- Write tests for new features
- Maintain 80%+ coverage
- Test edge cases

**Documentation:**
- Update docs for user-facing changes
- Add inline comments for complex logic
- Update CHANGELOG.md

### Submitting Code

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes, commit
git add .
git commit -m "Add feature: Description"

# Push and create PR
git push origin feature/your-feature-name
```

**PR checklist:**
- [ ] Tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Code follows style guide
- [ ] No secrets or PII in code

---

## How to Contribute Documentation

### Documentation Needs

**Always needed:**
- Clearer explanations
- More examples
- Troubleshooting guides
- Video tutorials (link to external)

**Process:**

1. Find docs to improve (in `docs/`)
2. Make changes
3. Submit PR with `docs:` prefix
4. Example: `docs: Improve sanitization guide with examples`

---

## BOK Categories

### Where to Submit

**General patterns:** `bok/patterns/[subcategory]/`
- `collaboration/` - Human-AI collaboration patterns
- `governance/` - Project governance patterns
- `security/` - Security patterns
- `performance/` - Performance patterns

**Platform-specific:** `bok/platforms/[platform]/`
- `railway/` - Railway-specific patterns
- `vercel/` - Vercel-specific patterns
- `aws/`, `azure/`, `gcp/` - Cloud platforms

**Anti-patterns:** `bok/anti-patterns/`
- What NOT to do and why

### Naming Convention

**Files:** `descriptive-name.md` (lowercase, hyphens)

**Examples:**
- `test-before-asking-human.md`
- `https-redirect-middleware.md`
- `autonomous-production-deployment.md`

---

## Review Criteria

### For Patterns

**Accepted if:**
- ✅ Universally useful
- ✅ Properly sanitized
- ✅ Well-explained
- ✅ Validated (proven to work)
- ✅ Follows template

**Rejected if:**
- ❌ Contains PII, secrets, or proprietary info
- ❌ Too project-specific
- ❌ Unclear or incomplete
- ❌ Duplicate of existing pattern
- ❌ Not actionable

**Improvements requested if:**
- 🔧 Needs better sanitization
- 🔧 Needs more context or examples
- 🔧 Could be split into multiple patterns
- 🔧 Needs clearer explanation

### For Code

**Accepted if:**
- ✅ Tests pass
- ✅ Follows style guide
- ✅ Documented
- ✅ Addresses real need
- ✅ Doesn't break existing functionality

**Rejected if:**
- ❌ No tests
- ❌ Breaks existing features
- ❌ Doesn't follow standards
- ❌ Out of scope for DEIA

---

## Community Standards

### Code of Conduct

**Expected behavior:**
- Be respectful and inclusive
- Assume good intent
- Give constructive feedback
- Focus on ideas, not people
- Help newcomers

**Unacceptable:**
- Harassment, discrimination, or personal attacks
- Trolling or inflammatory comments
- Sharing others' private information
- Spam or self-promotion

**Enforcement:**
- First violation: Warning
- Second violation: Temporary ban
- Third violation: Permanent ban

**Report violations:** contact@deiasolutions.org

### Recognition

**Contributors get:**
- Name in CONTRIBUTORS.md
- Credit in pattern frontmatter (`sources: [your-name]`)
- Voting rights in governance (after 3+ contributions)
- Profile badges (planned)

---

## License

**By contributing, you agree:**

- Code contributions: MIT License
- BOK contributions: CC BY-SA 4.0
- Documentation: CC BY-SA 4.0

You retain copyright but grant DEIA irrevocable license to use your contribution.

---

## Questions?

**Before submitting:**
- Read [Documentation](docs/)
- Check [existing patterns](bok/)
- Search [Issues](https://github.com/deiasolutions/deia/issues)

**Still stuck?**
- Ask in [Discussions](https://github.com/deiasolutions/deia/discussions)
- Create an [Issue](https://github.com/deiasolutions/deia/issues)
- Email: contact@deiasolutions.org (coming soon)

---

## Thank You

Every contribution helps build collective intelligence for AI collaboration.

**Your patterns help others avoid mistakes and learn faster.**

**Your code improves the tools we all use.**

**Your docs make DEIA accessible to more people.**

**Thank you for contributing to the commons.**
