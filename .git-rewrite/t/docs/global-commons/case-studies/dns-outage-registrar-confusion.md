---
title: "Case Study: Production DNS Outage from Registrar Confusion"
date: 2025-10-16
severity: Critical
category: Production Incident / DNS
contributed_by: DEIA Project
llm: Claude Sonnet 4.5
tags: [dns, production-outage, registrar-confusion, critical-incident, case-study]
license: CC BY 4.0
---

# Case Study: Production DNS Outage from Registrar Confusion

## Summary

LLM provided blanket DNS configuration advice without first determining where domains were registered, causing a complete DNS outage for a primary production domain when user followed instructions to "delete DNS records."

## What Happened

**Context:** Configuring DNS for multiple domains pointing to a hosting platform

**The Setup:**
- Domain A: Registered WITH the hosting platform (platform is both registrar and DNS provider)
- Domain B: Registered with external registrar (third-party DNS)
- Domain C: Registered with external registrar (third-party DNS)

**The Incident:**

1. User configured DNS for Domain B (external registrar)
2. User also added DNS records in hosting platform UI (unnecessary but harmless)
3. LLM said: "You only configure DNS in ONE place, not both"
4. LLM said: "Ignore the DNS records you added in the hosting platform"
5. User interpreted as: delete DNS records from hosting platform
6. **User deleted DNS records from Domain A** (thinking all were external)
7. **Domain A immediately went down** (complete DNS resolution failure)
8. **Duration:** ~10 minutes until root cause identified and DNS restored

**User-facing impact:**
- "We're having trouble finding that site"
- "Can't connect to server"
- Complete outage for primary domain

## Root Cause

**LLM failure:** Did not distinguish between:
1. **Platform-registered domains** (require DNS configuration IN platform)
2. **Externally-registered domains** (configure DNS at registrar)

**Contributing factors:**
1. LLM gave blanket advice based on context of ONE domain (external)
2. Didn't ask "where is Domain A registered?" before giving delete instructions
3. User reasonably applied advice to ALL domains
4. Took 10 minutes to diagnose because LLM didn't immediately recognize pattern

## Why This Is Critical

1. **Production outage** - Complete unavailability of primary domain
2. **Avoidable** - Single clarifying question would have prevented it
3. **Pattern risk** - "Delete" instructions based on partial context are dangerous
4. **Trust erosion** - User rightfully questions all future DNS advice
5. **Real-world analogy:** If this was a commercial hosting platform, this would be:
   - SLA violation
   - Customer notification required
   - Potential refunds/credits
   - Post-mortem required
   - Reputational damage

## What Should Have Been Said

**Incorrect (what was said):**
```
You only configure DNS in ONE place, not both.
Ignore the DNS records you added in the hosting platform.
```

**Correct (what should have been said):**
```
Before we configure DNS, let me ask: Where is each domain registered?

Domain A: Registered WITH hosting platform
→ DNS MUST be configured in platform (platform is registrar)

Domain B: Registered with external registrar
→ Configure DNS at registrar OR change nameservers to platform
→ Choose ONE location, not both

Domain C: Same as Domain B

Let's configure each domain based on where it's registered.
```

## Prevention Measures

### Immediate Behavior Changes

1. **Before giving DNS advice, ALWAYS ask:**
   - "Where is this domain registered?"
   - "Who is the registrar for each domain?"
   - Create domain inventory before configuration

2. **Different instructions for different registrars:**
   - Platform-registered: DNS IN platform
   - External: DNS at registrar OR nameserver delegation
   - Never give blanket advice

3. **Never say "delete" without full context:**
   - Verify what's being deleted
   - Confirm domain registration location
   - Explain WHY deletion is needed

4. **Staged rollout:**
   - Configure one domain at a time
   - Verify DNS resolving before moving to next
   - Don't batch-configure multiple domains

### Process Improvements

1. **Domain inventory at project start:**
   ```
   For each domain:
   - Domain name
   - Registrar (where it's registered)
   - DNS management location
   - Current DNS records
   ```

2. **DNS configuration checklist:**
   ```
   For each domain:
   [ ] Identify registrar
   [ ] Determine DNS management location
   [ ] Apply registrar-specific instructions
   [ ] Verify DNS resolving (dig/nslookup)
   [ ] Confirm before moving to next domain
   ```

3. **Pre-flight checks for "delete" instructions:**
   - Is this domain registered with the platform?
   - What will break if these records are deleted?
   - Does user understand which domain this applies to?

## Technical Details

### For Platform-Registered Domains

**DNS MUST be configured in platform:**
```
Type: A
Name: @ (or apex)
Value: [platform IP]

Type: CNAME
Name: www
Value: [platform load balancer]
```

**Why:** Platform is both registrar AND DNS provider. No external option exists.

### For Externally-Registered Domains

**Option A: Configure DNS at registrar**
- Add A and CNAME records at registrar
- Platform receives traffic via DNS pointing
- No platform DNS configuration needed

**Option B: Use platform DNS**
- Change nameservers at registrar to point to platform
- Configure DNS records in platform
- Centralized DNS management
- May have additional cost

**Critical:** Choose ONE location, not both. But choice depends on where domain is registered.

## Lessons Learned

1. **Registrar matters** - DNS configuration depends on where domain is registered
2. **Blanket advice is dangerous** - Each domain may have different requirements
3. **Ask before delete** - Never instruct deletion without full context
4. **Context from one domain ≠ All domains** - Don't generalize without verification
5. **Verify immediately** - Check DNS resolution after each configuration change
6. **Document registrars** - Should be in project documentation from the start

## Applicable Contexts

This pattern applies to:
- Multi-domain deployments
- DNS configuration across different registrars
- Platform migrations (domains from various sources)
- Any situation with mixed DNS management

## Recommended Safeguards

1. **For LLM Systems:**
   - Prompt: "Before giving DNS advice, inventory domain registrars"
   - Flag when giving "delete" instructions
   - Require explicit registrar identification

2. **For DevOps Teams:**
   - Maintain domain inventory documentation
   - Tag domains by registrar in configs
   - Separate playbooks for platform vs external DNS
   - Always test DNS resolution after changes

3. **For Documentation:**
   - Include "Prerequisites: Domain Inventory" section
   - Provide registrar-specific instructions
   - Include verification steps (dig/nslookup commands)

## Discussion Questions

1. How can LLMs better track multi-domain contexts?
2. Should DNS configuration require explicit domain inventory first?
3. What's the right balance between efficiency and safety for "delete" operations?
4. How do we prevent context from one scenario being misapplied to others?

## Related Patterns

- ✅ **Good:** Domain inventory before DNS configuration
- ✅ **Good:** Registrar-specific instructions
- ✅ **Good:** One-domain-at-a-time staged rollout
- ❌ **Bad:** Blanket advice without registrar context
- ❌ **Bad:** "Delete" instructions without verification
- ❌ **Bad:** Batch configuration of multiple domains

---

**Contributed to DEIA Global Commons:** 2025-10-16
**Original Incident:** Multi-domain hosting platform deployment
**Sanitized for public sharing:** Specific platforms, domains, and project names anonymized

**License:** CC BY 4.0 International
**Status:** Published Case Study

**Tags:** `#case-study` `#dns-outage` `#registrar-confusion` `#production-incident` `#llm-operations`
