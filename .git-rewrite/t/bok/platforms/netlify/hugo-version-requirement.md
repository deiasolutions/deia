---
title: "Hugo Version Must Be Specified in Netlify"
platform: Netlify
category: Build Configuration
date: 2025-10-16
discovered_by: daaaave-atx
severity: Critical
tags: [netlify, hugo, build-failure, environment-variables]
---

# Hugo Version Must Be Specified in Netlify

## Issue

When deploying a Hugo static site to Netlify, the build will fail if the Hugo version is not explicitly specified via environment variable.

## Symptom

Build fails with generic error:
```
Failed to parse configuration
```

Even with a valid or absent `netlify.toml` file.

## Root Cause

Netlify does not automatically detect or install Hugo. You must explicitly tell Netlify which version to use.

## Solution

**Add environment variable in Netlify:**

1. Site configuration → Build & deploy → Environment variables
2. Add variable:
   - **Key:** `HUGO_VERSION`
   - **Value:** `0.134.3` (or your desired version)
3. Save and redeploy

## Alternative (netlify.toml)

```toml
[build.environment]
HUGO_VERSION = "0.134.3"
```

**Note:** In our case, `netlify.toml` had parsing issues, so UI configuration was more reliable.

## Recommended Hugo Version

As of 2025-10-16: **`0.134.3`** (latest stable)

Check current version: https://github.com/gohugoio/hugo/releases

## Why This Matters

- Without version specified, Netlify won't install Hugo
- Build fails silently with unhelpful error
- Easy to miss if you're used to other platforms (Vercel auto-detects Hugo)

## Related

- Platform: Netlify
- Static site generator: Hugo
- Build system: Netlify Build

---

**Contributed to DEIA Commons:** 2025-10-16
**Project:** Q33N Platform deployment
