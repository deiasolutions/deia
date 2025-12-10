# DEIA Global Submission Sanitization Requirements

**CRITICAL: All submissions to DEIA Global MUST be sanitized.**

## What Must Be Removed

### 1. Personal Identifiable Information (PII)
- Full names (keep only first name or pseudonym)
- Email addresses (replace with examples: user@example.com)
- Phone numbers
- Physical addresses
- Social media handles (except approved public handles)
- URLs to personal websites/profiles
- Company/employer names
- Location information (city, state, country)

### 2. Secrets & Credentials
- API keys, tokens, passwords
- SSH keys, certificates
- Database connection strings
- OAuth credentials
- Any authentication data

### 3. Proprietary Information
- Company-specific code/logic
- Customer data
- Business metrics/KPIs
- Internal tool names
- Proprietary algorithms
- Trade secrets

### 4. System Information
- Internal server names/IPs
- Network topology details
- File system paths (replace with generic paths)
- Database schemas with sensitive fields
- Infrastructure details

## Sanitization Workflow

### For Conversation Logs

**NEVER share raw logs to DEIA Global.**

1. Draft in `.deia/private/logs/`
2. Extract pattern/insight from log
3. Sanitize extracted content
4. Save to `.deia/submissions/`

### For Bug Reports

1. Draft in `.deia/private/drafts/bug-report.md`
2. Replace real error messages with sanitized versions
3. Replace file paths: `/Users/dave/company/project/` → `/path/to/project/`
4. Remove stack traces with company code
5. Review in `.deia/submissions/`

### For Patterns

1. Draft in `.deia/private/drafts/pattern.md`
2. Replace company-specific examples with generic ones
3. Remove proprietary context
4. Generalize to be useful for anyone
5. Review in `.deia/submissions/`

## Using DEIA Sanitize Tool

```bash
# Sanitize a draft submission
deia sanitize --input .deia/private/drafts/my-pattern.md --output .deia/submissions/my-pattern.md

# Review changes
deia sanitize --diff .deia/private/drafts/my-pattern.md .deia/submissions/my-pattern.md

# Sanitize for AI review (less aggressive)
deia sanitize --for-ai --input .deia/private/drafts/my-pattern.md --output .deia/submissions/my-pattern.md
```

## Approved Public Information

### What CAN be included:
- ✅ First names or pseudonyms (e.g., "Dave", "dave-atx")
- ✅ Generic technology names (Python, VS Code, Claude)
- ✅ Open source project names
- ✅ Public documentation references
- ✅ Generic examples (user@example.com, /path/to/project)
- ✅ Common error patterns (without sensitive context)
- ✅ General architectural patterns

## Privacy Levels

### Level 1: Private (`.deia/private/`)
- Unsanitized content
- Real data, real paths, real errors
- Company-specific context
- **NEVER shared**

### Level 2: Sanitized (`.deia/submissions/`)
- PII removed
- Secrets removed
- Proprietary info removed
- Generic examples used
- **Ready for DEIA Global**

### Level 3: Public (DEIA Global BOK)
- Fully sanitized
- Reviewed by admin
- Useful for community
- **Publicly accessible**

## Dave's Approved Public Identity

**Allowed:**
- "Dave" (first name)
- "@dave-atx" (GitHub handle)
- "DEIA project maintainer"

**NOT allowed:**
- Last name
- Other GitHub handles
- Email addresses
- Company affiliation
- Location

## Checklist Before Submission

- [ ] No full names (only first names/pseudonyms)
- [ ] No email addresses (use examples)
- [ ] No phone numbers or addresses
- [ ] No company/employer names
- [ ] No secrets, API keys, tokens, passwords
- [ ] No proprietary code or algorithms
- [ ] No real file paths (use generic paths)
- [ ] No customer data or business metrics
- [ ] No internal tool/server names
- [ ] Examples are generic and reusable
- [ ] Content is useful for community
- [ ] Reviewed in `.deia/submissions/` before submitting

## Automated Checks

DEIA sanitization tools check for:
- Common PII patterns (email regex, phone formats)
- Secret patterns (API key formats, tokens)
- File path patterns
- Company name lists
- Flagged terms

**But automation isn't perfect - always manual review!**

## When in Doubt

**ASK: "Would I be comfortable with this on a billboard?"**

If not, sanitize more. Privacy and security are non-negotiable.

## Recovery from Mistakes

If you accidentally submit unsanitized content:

1. Immediately contact admin: (see CONTRIBUTING.md)
2. Request removal/redaction
3. Submit sanitized version
4. Update sanitization workflow to prevent recurrence

## References

- See `docs/sanitization-guide.md` for detailed examples
- See `docs/sanitization-workflow.md` for process details
- See `.private/README.md` for private workspace usage
- See `.deia/private/README.md` for project-level privacy
