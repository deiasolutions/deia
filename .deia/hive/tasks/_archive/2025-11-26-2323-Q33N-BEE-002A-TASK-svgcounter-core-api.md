# Task Assignment: BEE-002A - SVG Counter Core API

**Assigned to:** BEE-002A
**Assigned by:** Q33N
**Priority:** P0
**Created:** 2025-11-26 23:23 CDT
**Project:** svgcounter service

---

## Context

We are building a self-hosted SVG badge counter service. Full spec is at:
`familybondbot/.deia/svgcounter-spec.md`

You are responsible for **Core API & SVG Generation**. Two other bees are working in parallel:
- BEE-001A: Database & Infrastructure (schema, connection module)
- BEE-003A: Admin Dashboard

**Working Directory:** `deiasolutions/services/svgcounter/`

---

## Task

Implement the core counter API endpoints and SVG badge generation.

---

## Deliverables

### 1. Main Application File

Create `src/app.js` (or `src/index.js`) that:
- Sets up Express (or Fastify/Koa) server
- Imports database module from `src/db.js` (BEE-001A is creating this)
- Registers routes
- Starts server on PORT from environment

### 2. SVG Counter Endpoint

**Route:** `GET /c/:counterId.svg`

**Query Parameters:**
- `label` (optional, default: "views") - Left side text
- `color` (optional, default: "blue") - Right side color
- `style` (optional, default: "flat") - Badge style

**Logic:**
1. Extract counterId from path (validate: alphanumeric, dashes, underscores only)
2. Get visitor IP, hash it with SHA-256 + salt
3. Check if visitor seen in last 24h
4. If new visitor: increment both total_count and unique_count
5. If repeat visitor: increment only total_count
6. Record visitor with 24h expiry
7. Generate SVG badge with unique_count
8. Return SVG with headers:
   - `Content-Type: image/svg+xml`
   - `Cache-Control: no-cache, no-store, must-revalidate`

### 3. SVG Generation Module

Create `src/svg.js` that exports `generateBadge(label, count, color, style)`:

**Shields.io Style Badge:**
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="88" height="20">
  <linearGradient id="smooth" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="round">
    <rect width="88" height="20" rx="3" fill="#fff"/>
  </clipPath>
  <g clip-path="url(#round)">
    <rect width="45" height="20" fill="#555"/>
    <rect x="45" width="43" height="20" fill="#4c1"/>
    <rect width="88" height="20" fill="url(#smooth)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="23" y="15" fill="#010101" fill-opacity=".3">views</text>
    <text x="23" y="14">views</text>
    <text x="66" y="15" fill="#010101" fill-opacity=".3">142</text>
    <text x="66" y="14">142</text>
  </g>
</svg>
```

**Dynamic width calculation:**
- Measure label text width (~6-7px per char)
- Measure count text width (~7-8px per char)
- Add padding (10px each side)
- Minimum width: 60px

**Color presets:**
| Name | Hex |
|------|-----|
| green | #97ca00 |
| blue | #007ec6 |
| red | #e05d44 |
| orange | #fe7d37 |
| yellow | #dfb317 |
| gray | #555 |
| purple | #8a2be2 |
| pink | #ff69b4 |

### 4. JSON Endpoint

**Route:** `GET /c/:counterId.json`

**Response:**
```json
{
  "id": "my-counter",
  "total_count": 342,
  "unique_count": 142,
  "created_at": "2025-11-26T10:00:00Z",
  "updated_at": "2025-11-26T14:30:00Z"
}
```

### 5. Health Check Endpoint

**Route:** `GET /health`

**Response:** `{"status": "ok", "timestamp": "..."}`

---

## File Structure (Your Part)

```
svgcounter/src/
├── app.js          # Main Express app
├── svg.js          # SVG generation module
├── routes/
│   └── counter.js  # /c/:id routes
└── utils/
    └── hash.js     # IP hashing utility
```

---

## Success Criteria

- [ ] `GET /c/test.svg` returns valid SVG badge
- [ ] Badge displays unique visitor count
- [ ] Unique visitors tracked per 24h window (uses BEE-001A's db module)
- [ ] `GET /c/test.json` returns JSON with counts
- [ ] `GET /health` returns health check
- [ ] Label and color query params work
- [ ] SVG width adjusts to text length
- [ ] Code has comments explaining logic

---

## Integration with BEE-001A

BEE-001A is creating `src/db.js` with these exports:
- `getOrCreateCounter(counterId)`
- `incrementCounter(counterId, isUnique)`
- `checkVisitor(counterId, ipHash)`
- `recordVisitor(counterId, ipHash)`

Import and use these. If they're not ready yet, create a mock/stub and note it in your response.

---

## Constraints

- DO NOT implement database schema (that's BEE-001A)
- DO NOT implement admin routes or UI (that's BEE-003A)
- Focus ONLY on counter endpoints and SVG generation

---

## Activity Logging (MANDATORY)

You MUST log your activity to:
```
deiasolutions/.deia/bot-logs/BEE-002A-activity.jsonl
```

Log format:
```json
{"ts": "2025-11-26T23:30:00Z", "bee": "BEE-002A", "event": "task_started", "task": "svgcounter-core-api", "msg": "Starting API and SVG implementation"}
```

Log every 20-30 minutes. NO EXCEPTIONS.

---

## Deliverable

When complete, post response to:
```
deiasolutions/.deia/hive/responses/2025-11-26-XXXX-BEE-002A-Q33N-RESPONSE-svgcounter-api-complete.md
```

Then archive this task to:
```
deiasolutions/.deia/hive/tasks/_archive/
```

---

## Questions?

Post to `deiasolutions/.deia/hive/coordination/` addressed to Q33N.
Set a 20-minute timer and check back for response.

---

**Begin immediately. Do not ask for permission.**
