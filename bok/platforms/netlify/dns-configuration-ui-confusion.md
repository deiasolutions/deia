---
title: "Anti-Pattern: Netlify DNS Configuration UI Confusion"
platform: Netlify
category: DNS Configuration
date: 2025-10-16
discovered_by: daaaave-atx
severity: Medium
tags: [netlify, dns, ui-confusion, documentation-gap, dx-issue]
---

# Anti-Pattern: Netlify DNS Configuration UI Confusion

## Issue

When adding a custom domain to Netlify, the UI does NOT show DNS records that need to be configured. Instead, it just adds the domain and expects you to configure DNS at your registrar.

This creates confusion because:
1. Users expect to see "DNS records" or "configuration instructions"
2. Netlify shows NOTHING after adding domain
3. Documentation gap - unclear what records to create

## What We Did Wrong

After adding `deiasolutions.org` to Netlify:
1. Expected Netlify to show "Host/Alias" pairs or DNS instructions
2. Got frustrated when "no fucking entries" appeared
3. Wasted 10+ minutes trying to figure out what to do
4. Assistant (Claude) gave wrong advice about checking Netlify UI for records

## Root Cause

**Netlify's domain management flow:**
- Add domain → Domain added (no further info shown)
- User must know standard DNS configuration for apex domains
- No in-app guidance for what records to create

**Expected behavior (from other platforms like Vercel, Railway):**
- Add domain → Shows exact DNS records needed
- Copy/paste values into registrar
- Clear instructions with record type, name, value

## The Actual Process

**After adding domain to Netlify, you configure DNS at your registrar (NOT in Netlify):**

### For Apex Domain (example.com):

```
Type: A
Name: @ (or blank)
Value: 75.2.60.5
```

### For WWW Subdomain:

```
Type: CNAME
Name: www
Value: apex-loadbalancer.netlify.com
```

### Standard Values (as of 2025-10-16):
- **Netlify load balancer IP:** `75.2.60.5`
- **Netlify apex CNAME:** `apex-loadbalancer.netlify.com`

## Why This Is An Anti-Pattern (On Netlify's Part)

1. **Poor DX** - Users shouldn't need to memorize DNS config
2. **No feedback** - After adding domain, UI shows nothing actionable
3. **Documentation buried** - Standard records not surfaced in-app
4. **Inconsistent** - Other hosting platforms show this clearly
5. **Causes support burden** - Common confusion point

## Correct Workflow

**When adding custom domain to Netlify:**

1. **Add domain in Netlify** (Domain management → Add custom domain)
2. **Go to your registrar/DNS provider** (not back to Netlify)
3. **Add DNS records:**
   - A record: @ → 75.2.60.5
   - CNAME: www → apex-loadbalancer.netlify.com
4. **Wait for DNS propagation** (2-5 minutes typically)
5. **Verify in Netlify** - Domain management will show "Netlify DNS configured" when working

## Alternative: Use Netlify DNS

If you want Netlify to manage DNS records directly:

1. In Netlify: Domain management → "Use Netlify DNS"
2. Netlify provides nameservers (e.g., `dns1.p01.nsone.net`)
3. At your registrar: Change nameservers to Netlify's
4. Cost: $0.50/month per domain
5. Benefit: Configure DNS records directly in Netlify UI

## Registrar-Specific Gotchas

### Squarespace:
- Default A and CNAME records conflict with Netlify
- **CRITICAL: Must DELETE existing @ and www records FIRST** before adding Netlify records
- Squarespace will give error "we were unable to save this record" if you try to add before deleting
- Squarespace form uses "HOST" and "DATA" fields (same as Name/Value)

**Squarespace Step-by-Step:**
1. Go to domain → DNS Settings → Custom Records
2. **DELETE existing records:**
   - Delete A record with HOST: @ (or blank)
   - Delete CNAME record with HOST: www
3. **ADD Netlify records:**
   - Type: A, HOST: @, DATA: 75.2.60.5
   - Type: CNAME, HOST: www, DATA: apex-loadbalancer.netlify.com
4. Save and wait for propagation

### Wix:
- (TBD - not documented yet)

### Others:
- Most registrars work with standard A/CNAME records
- Key is deleting conflicting defaults first

## What Claude Should Have Done

1. ✅ **Check BOK first** for existing Netlify patterns
2. ✅ **Recognize new anti-pattern** - document in real-time
3. ✅ **Provide definitive answer** - not "Netlify will show you..."
4. ✅ **Surface standard values** - don't make user hunt for IP/CNAME

## Process Improvement Ideas

**For DEIA/Claude Code workflow:**

1. **Bot serves BOK to LLM context** - Auto-inject relevant patterns at session start
2. **Proactive anti-pattern detection** - LLM should flag "this feels like an anti-pattern" in real-time
3. **BOK refresh mechanism** - Periodically check for new patterns during session
4. **Context prioritization** - Surface platform-specific patterns when platform mentioned

**Proposed implementation:**
- Bot monitors conversation for platform mentions (Netlify, Vercel, etc.)
- Auto-injects relevant BOK entries into context
- LLM checks BOK before giving advice
- Pattern: "Let me check BOK first..." before answering platform questions

## Related Patterns

- ✅ **Good:** Vercel shows exact DNS records after domain add
- ✅ **Good:** Railway provides copy/paste DNS values
- ❌ **Bad:** Netlify hides DNS requirements (this pattern)
- ❌ **Bad:** LLM giving advice without checking BOK first

## References

- Netlify DNS Documentation: https://docs.netlify.com/domains-https/custom-domains/
- Netlify DNS IP: 75.2.60.5 (as of 2025-10-16, verify at link above)
- Netlify Apex Load Balancer: apex-loadbalancer.netlify.com

---

**Process Deviation Acknowledged:** 2025-10-16
**Contributing Factors:** Netlify UI/UX gap, Claude failed to check BOK, documentation not surfaced
**Corrective Action:** Document pattern, implement BOK-checking behavior
**Status:** Documented, process improvement proposed

**Tags:** `#anti-pattern` `#netlify` `#dns` `#ui-confusion` `#documentation-gap` `#dx-issue` `#process-improvement`
