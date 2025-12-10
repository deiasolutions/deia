---
title: "Process: Netlify Nuclear Option - Complete Recovery Checklist"
category: Deployment Process
platform: Netlify
date: 2025-10-16
created_by: daaaave-atx
tags: [netlify, nuclear-option, deployment, recovery, checklist]
---

# Process: Netlify Nuclear Option - Complete Recovery Checklist

## When to Use This

When you choose to **delete and recreate** a Netlify project (the "nuclear option") due to:
- Unrecoverable configuration errors
- Build system completely broken
- Faster to start fresh than debug

## ⚠️ WARNING

**Deleting a Netlify project erases ALL configuration:**
- Build settings
- Environment variables
- Domain configuration
- Deploy settings
- SSL certificates (will regenerate)
- Deploy history

**You must manually reconfigure EVERYTHING.**

## Complete Recovery Checklist

### Phase 1: Delete Old Project

- [ ] **Backup critical info BEFORE deleting:**
  - [ ] Screenshot build settings
  - [ ] Copy environment variables
  - [ ] List all custom domains
  - [ ] Note any custom headers/redirects
- [ ] Delete project in Netlify
- [ ] Confirm deletion

### Phase 2: Create New Project

- [ ] Create new project from GitHub repo
- [ ] Select correct repository
- [ ] Select correct branch (usually `master` or `main`)
- [ ] **DO NOT** click "Deploy" yet - settings are blank

### Phase 3: Configure Build Settings (CRITICAL)

**In Project settings → Build & deploy → Build settings:**

- [ ] **Build command:** `cd website && hugo` (adjust for your structure)
- [ ] **Publish directory:** `website/public` (adjust for your structure)
- [ ] **Base directory:** (leave blank unless needed)
- [ ] Click **Save**

**Verification (MANDATORY):**
- [ ] Refresh page and verify fields still show correct values
- [ ] Take screenshot of filled settings
- [ ] Double-check publish directory path matches repo structure

### Phase 4: Configure Environment Variables

**In Project settings → Environment variables:**

For Hugo sites:
- [ ] Add `HUGO_VERSION` = `0.134.3` (or latest)
- [ ] Scopes: All scopes (Production, Deploy Previews, Branch Deploys)
- [ ] Click **Save**

For other frameworks:
- [ ] Add any required variables (NODE_VERSION, etc.)
- [ ] Copy from backup/screenshot taken earlier

**Verification:**
- [ ] Refresh and verify variables still listed
- [ ] Check variable names match exactly (case-sensitive)

### Phase 5: Test Deploy (BEFORE Adding Domains)

**Trigger deploy:**
- [ ] Go to Deploys tab
- [ ] Click "Trigger deploy" → "Deploy site"
- [ ] Wait for build to complete (~1-2 minutes)

**Check deploy log (CRITICAL):**
- [ ] Open latest deploy → "Deploy log"
- [ ] Verify: "Building sites ..." appears (Hugo ran)
- [ ] Verify: Shows page count (e.g., "built 15 pages")
- [ ] Verify: NO "No build steps found" message
- [ ] Verify: Deploy status = "Published" ✅

**Check published site:**
- [ ] Click "Open production deploy" button
- [ ] Verify site loads at `[project-name].netlify.app` URL
- [ ] Check homepage loads
- [ ] Check key pages load
- [ ] Verify no 404 errors

**If ANY of the above fail, STOP and fix before continuing.**

### Phase 6: Configure Domains

**For each custom domain:**

#### Netlify-Registered Domains (e.g., q33n.com)

- [ ] Go to Domain management → Add custom domain
- [ ] Enter domain name
- [ ] Verify ownership
- [ ] Go to DNS settings IN NETLIFY
- [ ] Add A record: `@` → `75.2.60.5`
- [ ] Add CNAME: `www` → `apex-loadbalancer.netlify.com`
- [ ] Save DNS records

#### Externally-Registered Domains (e.g., Squarespace, Wix)

- [ ] Go to Domain management → Add custom domain
- [ ] Enter domain name
- [ ] Netlify will show "Awaiting external DNS"
- [ ] Go to registrar (Squarespace/Wix/etc.)
- [ ] Delete existing A and CNAME records for `@` and `www`
- [ ] Add A record: `@` → `75.2.60.5`
- [ ] Add CNAME: `www` → `apex-loadbalancer.netlify.com`
- [ ] Save at registrar

**After each domain:**
- [ ] Wait 2-5 minutes for DNS propagation
- [ ] Test domain in browser
- [ ] Verify site loads (not 404)
- [ ] Check SSL certificate provisioned (https works)

**Do ONE domain at a time. Verify each before adding next.**

### Phase 7: Final Verification

**For each domain:**
- [ ] Visit `https://[domain]` in browser
- [ ] Verify homepage loads
- [ ] Check navigation/links work
- [ ] Verify SSL certificate valid (no warnings)
- [ ] Test from multiple browsers/devices
- [ ] Check mobile view

**Check Netlify dashboard:**
- [ ] All domains show "Netlify DNS configured" or equivalent
- [ ] Latest deploy shows "Published"
- [ ] No error messages in domain management

### Phase 8: Optional Configuration

**If needed, reconfigure:**
- [ ] Deploy notifications (Slack, email)
- [ ] Deploy hooks
- [ ] Form handling
- [ ] Function settings
- [ ] Custom headers/redirects
- [ ] Branch deploy settings
- [ ] Deploy preview settings

## Verification Commands

**To verify Hugo built correctly:**
```bash
# In deploy log, look for:
Building sites …
... built in XXX ms
```

**To test DNS from command line:**
```bash
# Check A record
nslookup q33n.com

# Check CNAME
nslookup www.q33n.com
```

**Expected output:**
```
Server: ...
Address: ...

Non-authoritative answer:
Name: q33n.com
Address: 75.2.60.5
```

## Common Mistakes

❌ **Marking "Configure build settings" complete without verification**
✅ Check deploy log shows build actually ran

❌ **Adding all domains at once**
✅ Add one domain, verify, then add next

❌ **Assuming settings saved**
✅ Refresh page and verify fields still populated

❌ **Configuring DNS before site works**
✅ Test at netlify.app URL first

❌ **Forgetting environment variables**
✅ Screenshot before nuclear option

## When to Abort Nuclear Option

**Don't use nuclear option if:**
- Original problem is simple (typo in config)
- You can fix with targeted change
- You don't have backup of all settings
- Domains are actively receiving traffic

**Nuclear option is last resort, not first option.**

## Time Estimate

**Minimum time for complete recovery:**
- Phase 1-2: 5 minutes
- Phase 3-5: 10 minutes (build + verification)
- Phase 6: 10 minutes PER DOMAIN
- Phase 7: 15 minutes

**For 3 domains: ~60 minutes minimum**

**DO NOT RUSH THIS PROCESS.**

## Related Documents

- Anti-pattern: Direct-to-production deployment (bok/anti-patterns/direct-to-production-deployment.md)
- Incident: Nuclear option incomplete recovery (docs/observability/incidents/2025-10-16-nuclear-option-incomplete-recovery.md)
- Platform: Netlify DNS configuration (bok/platforms/netlify/dns-configuration-ui-confusion.md)

---

**Created:** 2025-10-16 after production incident
**Lesson learned:** Nuclear option without complete checklist = extended outage

**Tags:** `#netlify` `#nuclear-option` `#deployment` `#recovery` `#checklist` `#process`
