# CORS and TrustedHost Configuration (Proposed)

This document proposes safe defaults for CORS and TrustedHost for staging and production.

## CORS — `ALLOWED_ORIGINS`

Set `ALLOWED_ORIGINS` (comma-separated) to include only known frontends:

- Local dev: `http://localhost:3000`
- Production: `https://app.familybondbot.com,https://familybondbot.com,https://www.familybondbot.com`
- Vercel previews (if used): Prefer explicit per-project preview URLs, or a strict regex in code.

Example `.env` value:

```
ALLOWED_ORIGINS=http://localhost:3000,https://app.familybondbot.com,https://familybondbot.com,https://www.familybondbot.com
```

Note: The code also sets `allow_origin_regex` for Vercel. If we keep regex support, constrain it to the project scope (e.g., `^https://.*\.familybondbot-.*\.vercel\.app$`).

## TrustedHost (FastAPI)

TrustedHost restricts the Host header in production (debug=False). Proposed list:

- `api.familybondbot.com`
- Railway production host (exact), e.g., `familybondbot-production.up.railway.app`
- Staging host (exact), e.g., `familybondbot-staging.up.railway.app`
- Local dev: `localhost`, `127.0.0.1`

Do not use wide wildcards (e.g., `*.railway.app`) in production.

## Actions

- Confirm actual Railway hostnames for prod/staging and add them to TrustedHost list in code if missing.
- Set `ALLOWED_ORIGINS` accordingly in the environment for each deployment.

