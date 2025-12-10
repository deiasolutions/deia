---
title: Railway HTTPS Redirect Middleware Pattern
platform: Railway
category: Platform-Specific Pattern
tags: [railway, https, middleware, edge-proxy, fastapi]
confidence: Validated
date: 2025-10-05
source_project: parentchildcontactsolutions (Family Bond Bot)
---

# Railway HTTPS Redirect Middleware Pattern

## Problem

Railway's edge proxy rewrites HTTPS requests to HTTP when forwarding to backend services. This causes FastAPI redirect responses (301, 302, 307, 308) to return HTTP Location headers instead of HTTPS, breaking client redirects.

**Symptoms:**
- Client makes HTTPS request to API
- API returns redirect with `Location: http://...` header
- Browser follows HTTP redirect, breaking secure connection
- SSL warnings or connection failures

**Time cost:** ~10 hours debugging across 2 sessions

## Investigation Method

Using `curl -I` revealed the protocol-level issue:
```bash
curl -I https://api.familybondbot.com/auth/magic-link/verify?token=...
# Returns: Location: http://api.familybondbot.com/...
```

## Solution

Create middleware that intercepts redirect responses and rewrites HTTP → HTTPS in Location headers:

```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class ForceHTTPSRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Check if this is a redirect response
        if response.status_code in (301, 302, 307, 308):
            location = response.headers.get("location")
            if location and location.startswith("http://"):
                # Rewrite HTTP to HTTPS
                response.headers["location"] = location.replace("http://", "https://", 1)

        return response
```

**Integration (FastAPI):**
```python
from fastapi import FastAPI

app = FastAPI()
app.add_middleware(ForceHTTPSRedirectMiddleware)
```

## Why This Works

Railway edge proxy terminates SSL and forwards plain HTTP to backend. FastAPI constructs redirect URLs using the protocol from the incoming request (HTTP), not the original client protocol (HTTPS). The middleware fixes this at the response level.

## When to Use

- Deploying to Railway with redirect-based flows (OAuth, magic links, etc.)
- Using FastAPI, Django, or any framework that generates redirect responses
- Edge proxy terminates SSL before backend receives request

## Validation

Deployed to production (app.familybondbot.com), tested with:
- Magic link authentication flow
- OAuth redirects
- curl testing: `curl -I https://api.familybondbot.com/...`

Working in production as of 2025-10-05.

## Alternative Approaches Considered

1. **Railway configuration changes** - No Railway setting available to preserve protocol
2. **Nginx reverse proxy** - Adds complexity, middleware is simpler
3. **Per-route URL construction** - Fragile, must remember for every redirect

## Related Patterns

- See: Frontend Environment Auto-Detection (for client-side URL handling)
- See: Platform Friction Points (Railway edge proxy behavior)

## Contributing Developer

Original pattern discovered during 6-hour debugging session on Family Bond Bot project.

## License

CC0-1.0 (Public Domain) - freely usable by anyone
