# Task Assignment: BEE-001A - SVG Counter Database & Infrastructure

**Assigned to:** BEE-001A
**Assigned by:** Q33N
**Priority:** P0
**Created:** 2025-11-26 23:23 CDT
**Project:** svgcounter service

---

## Context

We are building a self-hosted SVG badge counter service. Full spec is at:
`familybondbot/.deia/svgcounter-spec.md`

You are responsible for **Database & Infrastructure**. Two other bees are working in parallel:
- BEE-002A: Core API (counter logic, SVG generation)
- BEE-003A: Admin Dashboard

**Working Directory:** `deiasolutions/services/svgcounter/`

---

## Task

Set up the PostgreSQL database schema and project infrastructure for the SVG Counter service.

---

## Deliverables

### 1. Project Structure

Create the following structure in `deiasolutions/services/svgcounter/`:

```
svgcounter/
├── README.md              # Brief project overview
├── package.json           # Node.js project (or equivalent if you choose Python/Go)
├── .env.example           # Environment variable template
├── db/
│   ├── schema.sql         # PostgreSQL schema
│   └── seed.sql           # Optional seed data for testing
└── src/
    └── db.js              # Database connection module (or db.py/db.go)
```

### 2. Database Schema (db/schema.sql)

Implement the schema from the spec:

```sql
-- Counters table
CREATE TABLE counters (
  id VARCHAR(100) PRIMARY KEY,
  total_count BIGINT NOT NULL DEFAULT 0,
  unique_count BIGINT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Visitors table (for unique tracking)
CREATE TABLE visitors (
  id SERIAL PRIMARY KEY,
  counter_id VARCHAR(100) NOT NULL REFERENCES counters(id) ON DELETE CASCADE,
  ip_hash VARCHAR(64) NOT NULL,
  first_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  expires_at TIMESTAMPTZ NOT NULL,
  UNIQUE(counter_id, ip_hash)
);

-- Daily stats (optional but recommended)
CREATE TABLE daily_stats (
  id SERIAL PRIMARY KEY,
  counter_id VARCHAR(100) NOT NULL REFERENCES counters(id) ON DELETE CASCADE,
  date DATE NOT NULL,
  total_views INT NOT NULL DEFAULT 0,
  unique_views INT NOT NULL DEFAULT 0,
  UNIQUE(counter_id, date)
);

-- Indexes
CREATE INDEX idx_counters_updated ON counters(updated_at DESC);
CREATE INDEX idx_counters_unique ON counters(unique_count DESC);
CREATE INDEX idx_visitors_lookup ON visitors(counter_id, ip_hash);
CREATE INDEX idx_visitors_expires ON visitors(expires_at);
CREATE INDEX idx_daily_stats_lookup ON daily_stats(counter_id, date DESC);
```

### 3. Database Connection Module

Create `src/db.js` (or equivalent) that:
- Reads DATABASE_URL from environment
- Exports a connection pool
- Exports helper functions for common queries:
  - `getOrCreateCounter(counterId)` - Get counter, create if doesn't exist
  - `incrementCounter(counterId, isUnique)` - Increment counts
  - `checkVisitor(counterId, ipHash)` - Check if visitor seen in 24h
  - `recordVisitor(counterId, ipHash)` - Record new visitor
  - `cleanupExpiredVisitors()` - Delete expired visitor records

### 4. Environment Template (.env.example)

```
DATABASE_URL=postgres://user:pass@localhost:5432/svgcounter
ADMIN_TOKEN=your-secret-admin-token
IP_HASH_SALT=random-string-for-hashing
PORT=3000
```

---

## Success Criteria

- [ ] Project structure created in `deiasolutions/services/svgcounter/`
- [ ] `db/schema.sql` contains all tables and indexes from spec
- [ ] `src/db.js` exports working database connection and helper functions
- [ ] `.env.example` documents required environment variables
- [ ] `README.md` has brief setup instructions
- [ ] Code has comments/docstrings explaining each function

---

## Tech Stack Decision

**Recommendation:** Node.js with `pg` package (PostgreSQL client)

But you may choose Python (psycopg2/asyncpg) or Go (pgx) if you have strong preference. Just ensure the interface is clean for BEE-002A to consume.

---

## Constraints

- DO NOT implement API routes (that's BEE-002A)
- DO NOT implement admin UI (that's BEE-003A)
- Focus ONLY on database layer
- Export clean interfaces for other bees to use

---

## Activity Logging (MANDATORY)

You MUST log your activity to:
```
deiasolutions/.deia/bot-logs/BEE-001A-activity.jsonl
```

Log format:
```json
{"ts": "2025-11-26T23:30:00Z", "bee": "BEE-001A", "event": "task_started", "task": "svgcounter-database-infrastructure", "msg": "Starting database schema implementation"}
```

Log every 20-30 minutes. NO EXCEPTIONS.

---

## Deliverable

When complete, post response to:
```
deiasolutions/.deia/hive/responses/2025-11-26-XXXX-BEE-001A-Q33N-RESPONSE-svgcounter-db-complete.md
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
