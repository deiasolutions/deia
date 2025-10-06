# DEIA Sanitization Guide

**Your privacy is your responsibility. This guide helps you contribute safely.**

---

## Why Sanitization Matters

When you share session logs and insights, you're making them **publicly visible on GitHub**. Once published, it's extremely difficult to fully retract information. This guide helps you remove sensitive data before contributing.

---

## Quick Reference: What to Remove

| Category | Examples | Replace With |
|----------|----------|--------------|
| **Names** | "Dave worked on this", "Sarah's code" | "The developer", "A team member" |
| **Companies** | "Acme Corp", "client XYZ" | "The client", "The organization" |
| **Emails** | dave@company.com | [email] or [developer-email] |
| **URLs** | https://internal.company.com | [internal-url] or example.com |
| **Paths** | C:\Users\dave\project\ | /path/to/project/ |
| **IPs** | 192.168.1.100 | [internal-ip] or 0.0.0.0 |
| **API Keys** | sk_live_abc123xyz | [api-key] |
| **Databases** | mongodb://user:pass@host | [database-connection] |
| **Specific IDs** | user_12345, order_ABC-789 | user_XXXXX, order_XXXXX |

---

## Step-by-Step Sanitization Process

### Step 1: Run the Auto-Sanitizer

```bash
cd /path/to/deia
python scripts/sanitize_session.py devlogs/intake/your_session.md
```

This catches most common issues. **But it's not perfect** - you must still review manually.

### Step 2: Manual Review

Open your session log and search for these patterns:

#### 🔍 Search for: Real Names

**Find:**
- Common first names (John, Sarah, etc.)
- Your name or teammates' names
- Usernames (especially in file paths or git commits)

**Replace:**
- "John" → "The developer" or "Developer A"
- "Sarah reviewed" → "A team member reviewed"
- "@dave" → "@developer"

**Example:**
```markdown
❌ Before: "Dave implemented the authentication module while Sarah worked on the UI"
✅ After: "One developer implemented the authentication module while another worked on the UI"
```

#### 🔍 Search for: Company/Client Names

**Find:**
- Your company name
- Client names
- Product codenames
- Internal project names

**Replace:**
- "Acme Corp" → "The organization"
- "Project Phoenix" → "The project"
- "ClientCo" → "The client"

**Example:**
```markdown
❌ Before: "We're building this for MegaBank's mobile app"
✅ After: "We're building this for a financial institution's mobile app"
```

#### 🔍 Search for: URLs and Domains

**Find:**
- Internal URLs (*.internal, *.local, *.corp)
- Company domains
- API endpoints with real hosts

**Replace:**
- https://api.company.com → https://api.example.com
- company.slack.com → [internal-chat]
- jira.company.com/PROJECT-123 → [ticket-system]/TICKET-123

**Example:**
```markdown
❌ Before: "API documentation at https://docs.acmecorp.com/api"
✅ After: "API documentation at [internal-docs-url]"
```

#### 🔍 Search for: File Paths

**Find:**
- Paths with usernames: `C:\Users\dave\`
- Paths with company names: `/opt/acmecorp/`
- Paths revealing internal structure

**Replace:**
- `C:\Users\dave\projects\client-app\` → `/path/to/project/`
- `/var/www/acmecorp/` → `/var/www/app/`
- `~/acme/secret-project/` → `~/project/`

**Example:**
```markdown
❌ Before: Modified file: C:\Users\dave\Documents\AcmeCorp\secret-api\auth.py
✅ After: Modified file: /path/to/project/auth.py
```

#### 🔍 Search for: Credentials

**Find:**
- API keys (starts with sk_, pk_, live_, prod_)
- Access tokens (long alphanumeric strings)
- Passwords (even in examples!)
- Database connection strings

**Replace:**
- `sk_live_abc123xyz` → `[api-key]`
- `password='MyP@ssw0rd'` → `password='[redacted]'`
- `mongodb://user:pass@host:port/db` → `[database-url]`

**Example:**
```markdown
❌ Before: OPENAI_API_KEY=sk_live_abc123xyz789
✅ After: OPENAI_API_KEY=[api-key]
```

#### 🔍 Search for: IP Addresses

**Find:**
- Internal IPs (192.168.x.x, 10.x.x.x, 172.16-31.x.x)
- Server IPs
- Database hosts

**Replace:**
- 192.168.1.100 → [internal-ip]
- 10.0.5.42 → [server-ip]

**Exception:** Public IPs in documentation are usually fine (like 8.8.8.8 for Google DNS)

#### 🔍 Search for: Email Addresses

**Find:**
- Regex: `\S+@\S+\.\S+`
- Personal emails
- Work emails

**Replace:**
- dave@company.com → [email]
- support@acme.com → [support-email]

#### 🔍 Search for: Unique Identifiers

**Find:**
- User IDs
- Order IDs
- Transaction IDs
- Session tokens

**Replace:**
- user_12345 → user_XXXXX
- order_ABC-789 → order_XXXXX
- session_xyz123 → [session-id]

**Example:**
```markdown
❌ Before: "Found bug when processing order_DB-12345 for user_98765"
✅ After: "Found bug when processing order_XXXXX for user_XXXXX"
```

### Step 3: Check Code Snippets

If you include code examples:

#### Safe to Include:
- Generic algorithms
- Common design patterns
- Framework/library usage examples
- Stack Overflow-style solutions

#### Must Remove:
- Proprietary business logic
- Unique algorithms (if patent-pending)
- Database schemas with sensitive fields
- Complete files (only share relevant snippets)

**Example:**
```python
❌ Before:
def calculate_proprietary_score(user):
    # Our secret sauce algorithm
    secret_multiplier = 42.7  # calibrated from years of data
    return user.engagement * secret_multiplier * user.acme_premium_factor

✅ After:
def calculate_score(user):
    # Generic scoring algorithm
    multiplier = get_multiplier()  # implementation varies
    return user.engagement * multiplier
```

### Step 4: Use the Checklist

Before submitting, complete this checklist in your session log:

```markdown
## Pre-Submission Sanitization Checklist

I confirm that I have:
- [ ] Replaced all real names with roles
- [ ] Removed all company/client names
- [ ] Removed all internal URLs and domains
- [ ] Sanitized file paths (no usernames/org names)
- [ ] Removed or genericized proprietary code
- [ ] Checked for API keys, tokens, credentials
- [ ] Removed email addresses
- [ ] Removed IP addresses
- [ ] Removed unique identifiers (user IDs, order IDs, etc.)
- [ ] Ensured no PII/PHI remains
- [ ] Verified I have rights to share this knowledge
- [ ] Run automated sanitizer: `python scripts/sanitize_session.py [file]`

**Date:** [YYYY-MM-DD]
**Sanitized by:** [your GitHub username or "anonymous"]
```

---

## Special Cases

### Medical/Healthcare Projects

**Extra sensitive - remove:**
- Patient names, even in examples
- Medical record numbers
- Diagnosis codes
- Any clinical data
- Provider names
- Healthcare facility names

**If in doubt, don't contribute medical project logs.** The privacy risks are too high.

### Financial Projects

**Remove:**
- Account numbers
- Transaction details
- Credit card info (even test cards)
- SSN/EIN
- Bank names (unless public)

### Government/Defense Projects

**Consider not contributing at all** if:
- You work on classified systems
- Contract prohibits disclosure
- Could reveal security vulnerabilities

**Ask your security officer first.**

---

## What's Safe to Share

You might wonder: "If I remove all this, what's left?"

**These are valuable AND safe:**
- **Patterns:** "We found that using X pattern solved Y problem"
- **Lessons:** "Claude struggled with Z, so we adapted our approach"
- **Techniques:** "Using this prompting strategy improved results"
- **Challenges:** "We hit a wall when trying to refactor legacy code"
- **Workflows:** "Our session flow: plan → implement → test → iterate"
- **Tool insights:** "Feature X in Claude Code saved us time on task Y"
- **Anti-patterns:** "Don't do X because it causes Y issue"

**Focus on the HOW and WHY, not the WHAT.**

---

## Examples: Before & After

### Example 1: Bug Fix Session

❌ **Before:**
```markdown
# Session: Authentication Bug Fix
**Project:** AcmeCorp Mobile Banking App
**Date:** 2025-10-05

Dave and Sarah debugged the login issue affecting user_12345. The problem
was in C:\Users\dave\acmecorp\mobile-app\auth\jwt_handler.py where we were
using the wrong secret key from PROD_JWT_SECRET=abc123xyz789.

Fixed by updating the config at https://config.acmecorp.com/prod/secrets.
```

✅ **After:**
```markdown
# Session: Authentication Bug Fix
**Project:** Mobile Banking Application
**Date:** 2025-10-05

Two developers debugged a login issue affecting a specific user. The problem
was in the JWT handler module where the application was using an incorrect
secret key from the production configuration.

Fixed by updating the secret management configuration.
```

### Example 2: Feature Development

❌ **Before:**
```markdown
# Session: Payment Processing Feature

Built a new payment processor for ClientCo that integrates with Stripe.
API key: sk_live_abcdefg123456.

Code at: /Users/sarah/Documents/ClientCo/payment-service/

def process_payment(amount, user_email):
    stripe.api_key = "sk_live_abcdefg123456"
    charge = stripe.Charge.create(
        amount=amount,
        currency="usd",
        customer=user_email,
        description="Payment for order"
    )
```

✅ **After:**
```markdown
# Session: Payment Processing Feature

Built a payment processing integration with a third-party payment provider.

Implementation approach:
```python
def process_payment(amount, user_identifier):
    payment_provider.api_key = get_api_key()  # from secure config
    charge = payment_provider.create_charge(
        amount=amount,
        currency="usd",
        customer=user_identifier,
        description="Payment description"
    )
```

**Insights:**
- Using environment variables for API keys worked well
- Error handling for failed charges required careful consideration
- Rate limiting was an important edge case
```

---

## Tools to Help

### 1. Regex Patterns (for find/replace)

**Email addresses:**
```regex
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

**API keys (common formats):**
```regex
(sk|pk)_(live|test)_[a-zA-Z0-9]{24,}
```

**IPv4 addresses:**
```regex
\b(?:\d{1,3}\.){3}\d{1,3}\b
```

**File paths (Windows):**
```regex
C:\\Users\\[^\\]+\\
```

**File paths (Unix):**
```regex
/home/[^/]+/
```

### 2. Automated Sanitizer

The DEIA sanitizer script (when complete) will:
- Detect and replace common patterns
- Flag potential issues for manual review
- Generate a sanitization report

**Usage:**
```bash
python scripts/sanitize_session.py input.md --output sanitized.md --report
```

### 3. VSCode Extension (Future)

We're planning a VSCode extension to:
- Highlight sensitive data as you type
- Suggest replacements
- Pre-validate before submission

---

## FAQ

**Q: Can I use fake names instead of roles?**
A: Yes! "Alice" and "Bob" are fine for examples. Just don't use real people's names.

**Q: What about open-source project names?**
A: Open-source projects are fine to name (React, Django, etc.). It's proprietary/internal project names you should avoid.

**Q: I accidentally pushed unsanitized content. What do I do?**
A: Immediately notify a maintainer via GitHub issue. We'll help you delete/redact it. Don't panic - mistakes happen.

**Q: Can I mention the programming language?**
A: Absolutely! Language, framework, and technology stack are all safe to share.

**Q: What if I'm not sure if something is sensitive?**
A: When in doubt, remove it. Better safe than sorry. Ask in Discussions if you need guidance.

**Q: Do I need to sanitize even for private repos?**
A: DEIA is public, so yes. Even if you're testing in a fork, assume it will eventually be public.

---

## When NOT to Contribute

**Don't contribute if:**
- Your employment contract prohibits sharing work-related information
- The project involves classified/confidential information
- You're working with sensitive PII/PHI that's hard to sanitize
- You're under NDA
- You have any doubts about legal/ethical implications

**It's okay to keep some sessions private.** Only contribute what's safe and appropriate.

---

## Getting Help

**If you need sanitization help:**
1. Open a GitHub Discussion (don't paste sensitive data there!)
2. Ask general questions: "How do I sanitize database schema discussions?"
3. Maintainers can review your draft privately if needed (via email, then deleted)

**Remember:** Maintainers will review your contribution, but YOU are responsible for the initial sanitization.

---

*When in doubt, redact. We can always clarify later, but we can't un-leak private information.*
