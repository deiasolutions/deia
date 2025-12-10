---
title: "Production Outage: DNS Configuration Confusion Causes 3-Domain Outage"
date: 2025-10-16
severity: Critical
category: Production Incident / DNS
reported_by: daaaave-atx
llm: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
duration: ~10 minutes
impact: 3 production domains completely unreachable
tags: [production-outage, dns, netlify, critical-incident, customer-impact]
---

# Production Outage: DNS Configuration Confusion Causes 3-Domain Outage

## Impact

**Complete DNS resolution failure for all three configured domains:**
- q33n.com - DOWN (primary domain)
- deiasolutions.org - DOWN
- efemera.live - DOWN

**Duration:** ~10 minutes
**User-facing error:** "We're having trouble finding that site" / "Can't connect to server"
**Root cause:** DNS records deleted from Netlify-registered domain

## Timeline

**1:56 PM** - Deploy with _redirects file succeeds
**~2:00 PM** - User reports "three dead sites"
**2:05 PM** - Diagnosed as DNS resolution failure (not routing)
**2:08 PM** - Discovered root cause: DNS records deleted from q33n.com (Netlify-registered domain)
**2:10 PM** - Added A and CNAME records back to Netlify DNS
**2:15 PM** - Sites recovering (DNS propagation in progress)

## What Happened

### The Setup

- q33n.com registered WITH Netlify (Netlify is the registrar)
- deiasolutions.org registered with Squarespace
- efemera.live registered with Squarespace

### The Mistake

**Claude's incorrect instructions:**
1. User added DNS records for efemera.live in Netlify UI
2. Claude said "you only configure DNS in ONE place, not both"
3. Claude said "ignore the DNS records you added in Netlify"
4. User interpreted this as: delete DNS records from Netlify
5. **User deleted DNS records from q33n.com in Netlify**
6. But q33n.com is REGISTERED with Netlify, so those records were required
7. DNS resolution immediately failed for q33n.com

### The Confusion

**External DNS vs Netlify DNS:**
- **External DNS:** Domain registered elsewhere (Squarespace), DNS configured at registrar, Netlify just receives traffic
- **Netlify DNS:** Domain registered WITH Netlify OR using Netlify nameservers, DNS configured IN Netlify

**What should have been configured:**
- q33n.com: DNS IN Netlify (because Netlify is registrar)
- deiasolutions.org: DNS at Squarespace (external)
- efemera.live: DNS at Squarespace (external)

**What Claude said:**
- "Don't configure DNS in both places"
- "Ignore Netlify DNS"
- (Correct for Squarespace domains, WRONG for q33n.com)

## Root Cause Analysis

**Primary cause:** Claude failed to distinguish between:
1. Domains registered WITH Netlify (require DNS in Netlify)
2. Domains registered externally (configure DNS at registrar)

**Contributing factors:**
1. User added DNS in Netlify for efemera.live (not needed, but harmless)
2. Claude gave blanket advice "don't use Netlify DNS" without checking WHERE domains were registered
3. User reasonably applied that advice to ALL domains
4. q33n.com DNS got deleted, causing outage
5. Took 10 minutes to diagnose because Claude didn't immediately recognize the pattern

**Why Claude missed it:**
- Didn't track which domains were registered where
- Gave advice based on efemera.live context (Squarespace-registered)
- Failed to consider q33n.com might be Netlify-registered
- Didn't ask "where is q33n.com registered?" before giving blanket DNS advice

## Correct Configuration

### For Netlify-Registered Domains (q33n.com)

**DNS MUST be configured in Netlify:**
```
Type: A
Name: @
Value: 75.2.60.5

Type: CNAME
Name: www
Value: apex-loadbalancer.netlify.com
```

**Why:** Netlify is the registrar AND DNS provider, no external option.

### For Externally-Registered Domains (deiasolutions.org, efemera.live)

**Option A: Configure DNS at registrar (Squarespace)**
- Add A and CNAME records at Squarespace
- Netlify receives traffic via DNS pointing
- Free, simple

**Option B: Use Netlify DNS**
- Change nameservers at Squarespace to point to Netlify
- Configure DNS records in Netlify
- Cost: $0.50/month per domain
- Benefit: Centralized DNS management

**We chose Option A for these domains.**

## Impact Assessment

**If this was a real hosting platform:**
- Customer outage: 100% of sites down
- SLA violation: Critical
- Customer notifications required
- Post-mortem required
- Potential refunds/credits
- Reputational damage

**Actual impact:**
- Pre-launch testing/setup
- No actual customers affected
- But demonstrated critical process failure

## Prevention Measures

**Immediate:**
1. **Before giving DNS advice, ask:** "Where is this domain registered?"
2. **Document domain registrar for each domain**
3. **Different instructions for Netlify-registered vs external**
4. **Never say "delete DNS entries" without context**

**Process improvements:**
1. **Inventory domains at project start:**
   - List all domains
   - Note registrar for each
   - Note DNS management location
   - Document in README or config

2. **DNS configuration checklist:**
   ```
   For each domain:
   [ ] Identify registrar
   [ ] Determine DNS management location
   [ ] Apply registrar-specific instructions
   [ ] Verify DNS resolving before moving to next domain
   ```

3. **Staged rollout:**
   - Add one domain at a time
   - Verify working before adding next
   - Don't batch-configure multiple domains

4. **Pre-flight checks:**
   - Before giving "delete" instructions, confirm what's being deleted
   - Ask "is this domain registered with Netlify or externally?"

## Related Incidents

- 2025-10-16: Direct-to-production deployment (bok/anti-patterns/direct-to-production-deployment.md)
- 2025-10-16: Incomplete instructions (docs/observability/incidents/2025-10-16-incomplete-instructions.md)
- 2025-10-16: DNS UI confusion (bok/platforms/netlify/dns-configuration-ui-confusion.md)

**Meta-pattern:** Multiple critical failures in same deployment session, all related to insufficient process rigor

## Lessons Learned

1. **Registrar matters** - DNS config depends on where domain is registered
2. **Blanket advice is dangerous** - Each domain has different requirements
3. **Ask before delete** - Never instruct deletion without full context
4. **One-at-a-time** - Don't configure multiple domains in parallel
5. **Verify immediately** - Check each domain works before moving on
6. **Document registrars** - Should be in repo README from the start

## Status

- **Incident:** Resolved (DNS records restored)
- **Sites:** Recovering (DNS propagation in progress)
- **Documentation:** Updated with registrar-specific guidance
- **Prevention:** Process improvements documented

---

**Severity:** Critical (production outage)
**Customer impact:** None (pre-launch)
**If this was production:** Severity 1, all-hands incident

**Tags:** `#production-outage` `#dns` `#netlify` `#critical-incident` `#process-failure`
