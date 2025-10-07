---
title: Frontend Environment Auto-Detection
platform: Vercel
category: Pattern
tags: [vercel, preview-deployments, environment-detection, magic-links, frontend]
confidence: Validated
date: 2025-10-05
source_project: parentchildcontactsolutions (Family Bond Bot)
---

# Frontend Environment Auto-Detection

## Problem

Magic link emails (and other backend-generated URLs) were hardcoded to production domain, breaking testing on Vercel preview deployments.

**Symptoms:**
- Preview deployment at `project-abc123.vercel.app`
- Magic link email contains `https://app.familybondbot.com/auth/verify?token=...`
- Clicking link redirects to production, not preview environment
- Can't test auth flow on preview deployments

**Impact:**
- Preview deployments unusable for end-to-end testing
- Must test authentication in production (dangerous)
- Slows development velocity

## Solution

Use `window.location.origin` to dynamically detect the current environment, with production domain as fallback for known production hostnames.

### Frontend Implementation (TypeScript/React)

```typescript
const getFrontendUrl = () => {
  // Check if we're on production domain
  if (window.location.hostname === 'app.familybondbot.com' ||
      window.location.hostname === 'familybondbot.com') {
    return 'https://app.familybondbot.com';
  }

  // Otherwise, use current origin (covers preview deployments, localhost, etc.)
  return window.location.origin;
};

// Use in API calls
const requestMagicLink = async (email: string) => {
  const response = await fetch(`${API_URL}/auth/magic-link`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email,
      redirect_url: `${getFrontendUrl()}/auth/verify`
    })
  });
  return response.json();
};
```

### Backend Support (FastAPI example)

```python
from fastapi import FastAPI, Body
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class MagicLinkRequest(BaseModel):
    email: str
    redirect_url: HttpUrl  # Accept frontend URL

@app.post("/auth/magic-link")
async def create_magic_link(request: MagicLinkRequest):
    # Generate token...

    # Use provided redirect_url instead of hardcoded domain
    magic_link = f"{request.redirect_url}?token={token}"

    # Send email with magic_link...
    return {"success": True}
```

## When to Use

- ✅ Vercel preview deployments
- ✅ Netlify branch previews
- ✅ Any platform with dynamic preview URLs
- ✅ Magic link authentication
- ✅ OAuth callback URLs
- ✅ Password reset links
- ✅ Email verification links

## Why This Works

**Environment detection at runtime:**
- Production: Explicitly checks production domains, returns canonical URL
- Preview: Falls back to `window.location.origin` (e.g., `project-abc123.vercel.app`)
- Localhost: Falls back to `window.location.origin` (e.g., `http://localhost:3000`)

**Backend agnostic:**
- Backend receives `redirect_url` from frontend
- No backend environment detection needed
- Works with any backend (Python, Node, Go, etc.)

## Security Considerations

**Validate redirect URLs on backend:**

```python
from urllib.parse import urlparse

ALLOWED_DOMAINS = [
    'app.familybondbot.com',
    'familybondbot.com',
    'vercel.app',  # Allow Vercel preview domains
    'localhost',   # Allow local development
]

def validate_redirect_url(url: str) -> bool:
    parsed = urlparse(url)
    hostname = parsed.hostname

    # Check against allowed domains
    for allowed in ALLOWED_DOMAINS:
        if hostname == allowed or hostname.endswith(f'.{allowed}'):
            return True

    return False
```

**Prevent open redirects:**
- Always validate `redirect_url` parameter
- Use allowlist of domains, not blocklist
- Log suspicious redirect attempts

## Alternative Approaches

**Environment variables (not recommended for this use case):**
```typescript
// ❌ Breaks preview deployments
const FRONTEND_URL = process.env.NEXT_PUBLIC_FRONTEND_URL;
```

**Why environment variables don't work:**
- Vercel preview deployments have unique URLs
- Can't set env var for every preview deployment
- `window.location.origin` is simpler and more reliable

**Build-time detection (not recommended):**
```typescript
// ❌ Requires separate builds for each environment
const FRONTEND_URL = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : 'http://localhost:3000';
```

**Why build-time detection is inferior:**
- Must rebuild for each environment
- Doesn't work for unexpected preview URLs
- Runtime detection is more flexible

## Validation

Deployed to production (app.familybondbot.com), tested with:
- Production domain → Returns production URL
- Vercel preview deployment → Returns preview URL
- Localhost development → Returns localhost URL
- Magic link email flow works in all environments

Working in production as of 2025-10-05.

## Related Patterns

- See: Railway HTTPS Redirect Middleware (backend protocol handling)
- See: Platform Friction Points (Vercel preview deployments)

## Edge Cases

**Subdomain handling:**
```typescript
const getFrontendUrl = () => {
  const hostname = window.location.hostname;

  // Production domains (with or without subdomain)
  if (hostname === 'app.familybondbot.com' ||
      hostname === 'familybondbot.com' ||
      hostname === 'www.familybondbot.com') {
    return 'https://app.familybondbot.com';
  }

  // Everything else (preview, localhost, etc.)
  return window.location.origin;
};
```

**Multiple production environments:**
```typescript
const getFrontendUrl = () => {
  const hostname = window.location.hostname;

  // Production
  if (hostname === 'app.example.com') {
    return 'https://app.example.com';
  }

  // Staging
  if (hostname === 'staging.example.com') {
    return 'https://staging.example.com';
  }

  // Preview/localhost
  return window.location.origin;
};
```

## Contributing Developer

Original pattern developed during Family Bond Bot authentication implementation.

## License

CC0-1.0 (Public Domain) - freely usable by anyone
