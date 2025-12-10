# DEIA Security Architecture

## Overview

This document defines the technical implementation of DEIA's security model, ensuring contributions are safe while enabling open collaboration.

---

## 1. Threat Model

### 1.1 Threats We Protect Against

**High Severity:**
- Malicious code injection in templates/scripts
- Credential harvesting via contributed logs
- Privacy violation through PII/PHI exposure
- Supply chain attacks via dependencies
- Trojan horse knowledge entries (misleading advice)

**Medium Severity:**
- Accidental secret leakage
- Unintentional IP disclosure
- Prompt injection in BOK entries
- Social engineering via contribution comments

**Low Severity:**
- Spam contributions
- Low-quality submissions
- Template format violations

### 1.2 Trust Boundaries

```
┌─────────────────────────────────────────┐
│  Contributor's Local Machine (UNTRUSTED)│
│  - Session logs generated                │
│  - Local sanitization                    │
└──────────────┬──────────────────────────┘
               │
               │ Manual submission (git push)
               ↓
┌─────────────────────────────────────────┐
│  GitHub PR (QUARANTINE ZONE)            │
│  - Automated scanning                    │
│  - Human review required                 │
│  - 48hr community review                 │
└──────────────┬──────────────────────────┘
               │
               │ After approval only
               ↓
┌─────────────────────────────────────────┐
│  Main Branch (TRUSTED)                   │
│  - Signed commits only                   │
│  - Immutable history                     │
│  - Public consumption                    │
└─────────────────────────────────────────┘
```

---

## 2. Automated Security Scanning

### 2.1 GitHub Actions Workflow

**File:** `.github/workflows/security-scan.yml`

Triggers on every PR to:
- `pipeline/intake/**`
- `pipeline/reviewed/**`
- `pipeline/bok/**`
- `pipeline/wisdom/**`
- `templates/**`
- `scripts/**`

**Scans performed:**

#### Secret Detection
```yaml
- name: Detect Secrets
  uses: gitleaks/gitleaks-action@v2
  with:
    config: .gitleaks.toml
```

**Detects:**
- API keys (AWS, OpenAI, Anthropic, Google, etc.)
- OAuth tokens
- Private keys (SSH, PGP, SSL)
- Database credentials
- JWT tokens
- Generic high-entropy strings

#### PII/PHI Detection
```yaml
- name: Scan for PII/PHI
  run: python scripts/detect_pii.py ${{ github.event.pull_request.changed_files }}
```

**Detects:**
- Email addresses (regex)
- Phone numbers (international formats)
- Social Security Numbers
- Credit card numbers
- IP addresses (private ranges)
- Medical record numbers
- Common name patterns in code

#### Code Safety Analysis
```yaml
- name: Static Analysis
  uses: github/super-linter@v5
  with:
    VALIDATE_PYTHON: true
    VALIDATE_JAVASCRIPT: true
    VALIDATE_BASH: true
```

**Checks:**
- No `eval()` or `exec()` in Python scripts
- No `curl | sh` patterns in bash
- No SQL injection patterns
- No command injection patterns
- No file system manipulation outside safe zones

#### Dependency Scanning
```yaml
- name: Dependency Review
  uses: actions/dependency-review-action@v3
```

**Flags:**
- Known CVEs in dependencies
- Unmaintained packages
- License incompatibilities

### 2.2 Pre-commit Hooks (Local)

**File:** `.pre-commit-config.yaml`

Contributors can install locally:
```bash
pip install pre-commit
pre-commit install
```

**Hooks:**
1. **Gitleaks** - Prevent secret commits
2. **Sanitization checklist** - Ensure template compliance
3. **File size limits** - Max 1MB per session log
4. **Filename validation** - Enforce naming conventions

---

## 3. Human Review Process

### 3.1 Maintainer Review Checklist

Every contribution requires a maintainer to verify:

**Privacy Review:**
- [ ] No real names, usernames, or identifying info
- [ ] No company/client names
- [ ] No internal URLs, domains, or IPs
- [ ] No file paths revealing org structure
- [ ] Code snippets are generic/sanitized

**Security Review:**
- [ ] No executable code in session logs
- [ ] Scripts (if any) reviewed line-by-line
- [ ] No external resource fetching
- [ ] No suspicious patterns or obfuscation

**Quality Review:**
- [ ] Follows template format
- [ ] Provides genuine value
- [ ] Well-written and clear
- [ ] Appropriate category/tags

**Metadata Review:**
- [ ] Platform correctly identified
- [ ] Date/timestamp valid
- [ ] Sanitization checklist completed

### 3.2 Multi-Maintainer Approval

**For high-risk contributions:**
- New scripts or automation
- Changes to templates
- Updates to documentation
- BOK entries with novel claims

**Require 2 maintainer approvals** before merge.

### 3.3 Community Review Period

After maintainer approval:
1. Label PR as "Ready for Community Review"
2. Wait 48 hours minimum
3. Community can flag concerns via comments
4. Maintainers address all flags before merge
5. Unanimous maintainer consensus required if flagged

---

## 4. Sanitization Tools

### 4.1 Auto-Sanitizer Script

**File:** `scripts/sanitize_session.py`

```python
# Pseudocode - actual implementation needed
def sanitize_session_log(file_path):
    content = read_file(file_path)

    # Replace patterns
    content = replace_emails(content, "[email]")
    content = replace_urls(content, "[url]")
    content = replace_file_paths(content, "[path]")
    content = replace_names(content)  # ML-based or manual
    content = replace_high_entropy_strings(content, "[redacted]")

    # Validate
    if contains_pii(content):
        raise Exception("PII detected after sanitization")

    return content
```

**Usage:**
```bash
python scripts/sanitize_session.py devlogs/intake/my_session.md
```

### 4.2 Sanitization Checklist (Manual)

**Included in every template:**

```markdown
## Pre-Submission Sanitization Checklist

I confirm that I have:
- [ ] Replaced all real names with roles (e.g., "the developer", "the user")
- [ ] Removed all company/client names
- [ ] Removed all internal URLs, domains, and IP addresses
- [ ] Sanitized file paths (no usernames, org names)
- [ ] Removed or genericized all code that reveals proprietary logic
- [ ] Checked for API keys, tokens, and credentials
- [ ] Ensured no PII/PHI remains
- [ ] Verified I have rights to share this knowledge
- [ ] Run automated sanitizer: `python scripts/sanitize_session.py [file]`

**I understand:**
- This will be publicly visible on GitHub
- I am responsible for ensuring privacy compliance
- Violating this checklist may result in contribution rejection
```

---

## 5. MCP Integration Security

### 5.1 Isolated MCP Server

When DEIA integrates MCP for agent coordination:

**Architecture:**
```
┌─────────────────────┐
│   AI Agent          │
│   (Claude/GPT/etc)  │
└──────────┬──────────┘
           │
           │ MCP Protocol
           ↓
┌─────────────────────┐
│   DEIA MCP Server   │
│   (Sandboxed)       │
│   - Read-only BOK   │
│   - No file write   │
│   - No network      │
└─────────────────────┘
```

**Security controls:**
- Server runs in Docker container
- Read-only filesystem access to `pipeline/bok/`
- No network access (airgapped)
- Resource limits (CPU, memory, time)
- All queries logged for audit

### 5.2 Tool Verification

**Prevent lookalike tools:**
```json
{
  "tool_registry": {
    "deia_query_bok": {
      "hash": "sha256:abc123...",
      "signature": "signed by DEIA maintainers",
      "verified": true
    }
  }
}
```

Agents verify tool authenticity before use.

### 5.3 Prompt Injection Defense

**Input validation:**
- Limit query length (max 500 chars)
- Sanitize special characters
- No system commands in queries
- Rate limiting per agent

**Output filtering:**
- Never return raw file paths
- Redact any leaked metadata
- Log suspicious query patterns

---

## 6. Incident Response

### 6.1 Security Incident Classification

**Critical (P0):**
- Credentials leaked to public repo
- Malicious code merged to main
- PII/PHI exposed

**High (P1):**
- Vulnerability in automation scripts
- Bypass of security controls
- Unauthorized access attempts

**Medium (P2):**
- Accidental PII in PR (caught before merge)
- Dependency CVE (no exploit path)

**Low (P3):**
- False positive from scanners
- Process improvement needed

### 6.2 Response Protocol

**For P0/P1 incidents:**
1. **Immediate action (within 1 hour):**
   - Revert/delete compromised content
   - Rotate any exposed credentials
   - Lock repository if necessary

2. **Investigation (within 24 hours):**
   - Determine root cause
   - Assess blast radius
   - Identify affected parties

3. **Notification (within 24 hours):**
   - Public incident report on GitHub
   - Direct notification to affected contributors
   - Update security documentation

4. **Remediation (within 1 week):**
   - Implement preventive controls
   - Update scanning rules
   - Conduct post-mortem

5. **Transparency:**
   - Publish incident report in `security/incidents/`
   - Update this document with lessons learned

---

## 7. Secure Development Practices

### 7.1 Repository Settings

**GitHub repository must have:**
- Branch protection on `main`:
  - Require PR reviews (minimum 1)
  - Require status checks to pass
  - Require signed commits
  - No force pushes
  - No deletions
- Private vulnerability reporting enabled
- Dependabot alerts enabled
- Code scanning (CodeQL) enabled
- Secret scanning enabled

### 7.2 Access Control

**Roles:**
- **Maintainers** (write access):
  - Require 2FA
  - PGP-signed commits
  - Background in security/privacy

- **Contributors** (fork/PR only):
  - No direct write access
  - All changes via PR

- **Bots** (automated processes):
  - Minimal permissions
  - Token rotation every 90 days
  - Audit logs monitored

### 7.3 Audit Logging

**Log all:**
- PR submissions and approvals
- Merge events
- Security scan failures
- Failed sanitization checks
- MCP queries (when implemented)

**Retention:** 2 years minimum

---

## 8. Compliance

### 8.1 GDPR Considerations

**For EU contributors:**
- Right to erasure (delete contributions)
- Right to data portability (export format available)
- Consent clearly obtained via checklist
- Data minimization enforced

### 8.2 CCPA Considerations

**For California contributors:**
- Disclosure of data use (in README)
- Opt-out mechanism (don't contribute)
- No sale of personal information (prohibited)

### 8.3 HIPAA Awareness

**Not a HIPAA-compliant system:**
- Explicitly prohibit PHI in contributions
- Scanner flags medical terminology
- Reject any healthcare-specific implementations

---

## 9. Continuous Improvement

### 9.1 Security Review Cadence

**Monthly:**
- Review security scan logs
- Update detection rules
- Check for new CVEs

**Quarterly:**
- Penetration testing (community volunteers)
- Review and update threat model
- Audit access controls

**Annually:**
- Full security architecture review
- Third-party audit (if funded)
- Update this document

### 9.2 Community Bug Bounty

**Rewards for finding:**
- Security vulnerabilities
- Privacy leaks
- Bypass techniques

**Recognition:**
- Hall of fame in README
- GitHub sponsor acknowledgment
- Co-authorship on security whitepapers

---

## 10. Implementation Checklist

**Phase 1 (MVP):**
- [ ] GitHub Actions workflows
- [ ] Gitleaks integration
- [ ] Basic PII detection script
- [ ] Contribution templates with checklists
- [ ] Branch protection rules

**Phase 2 (Enhanced):**
- [ ] Advanced PII/PHI ML detection
- [ ] Pre-commit hooks package
- [ ] Auto-sanitizer script
- [ ] Multi-maintainer approval workflow
- [ ] Incident response playbooks

**Phase 3 (MCP Integration):**
- [ ] MCP server implementation
- [ ] Tool verification system
- [ ] Prompt injection defenses
- [ ] Sandboxed execution environment

---

*Security is not a feature, it's a foundation.*
