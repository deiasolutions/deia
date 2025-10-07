# Scaling the Book of Knowledge

**How DEIA BOK will scale from 10s to 100,000s of patterns.**

---

## Current Architecture (Phase 1)

**Status:** Implemented ✓

```
Main Repo (deia)
  - CLI, extensions, docs

BOK Repo (deia-bok)
  - Community patterns
  - Platform solutions
  - Conversation logs
```

**Capacity:** ~10,000 patterns
**Cost:** Free (GitHub)
**Access:** Git clone, GitHub web

---

## Problem at Scale

### What Breaks
- **GitHub repo size:** 1GB+ with thousands of patterns
- **Clone time:** Minutes instead of seconds
- **Search:** Slow, requires cloning entire repo
- **Storage:** Git not optimized for many large files

### When It Breaks
- 10,000+ patterns
- Large conversation logs (50KB+ each)
- Images/screenshots in patterns
- Video tutorials

---

## Solution: Hybrid Storage (Phase 2)

**Status:** Planned (backlog)

### Architecture

```
┌─────────────┐
│   GitHub    │  ← Curated patterns, metadata, index
│  deia-bok   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  deia.dev   │  ← API, search, web UI
│     API     │
└──────┬──────┘
       │
       ├──────────┐
       ▼          ▼
┌──────────┐  ┌──────────┐
│PostgreSQL│  │    S3    │  ← Full logs, large files
│ Metadata │  │  Object  │
└──────────┘  └──────────┘
```

### Components

#### 1. GitHub (Curated Patterns)
**What stays in Git:**
- High-quality, reviewed patterns
- Index/metadata
- README, docs
- Templates

**Size limit:** ~1000 curated patterns

#### 2. Object Storage (S3/Backblaze B2)
**What moves to storage:**
- Full conversation logs
- Large code samples
- Screenshots, diagrams
- Video tutorials

**Linked from Git patterns**

#### 3. PostgreSQL (Metadata)
**What goes in database:**
- Pattern metadata (title, author, tags, date)
- Full-text search index
- User contributions tracking
- Statistics

#### 4. API (deia.dev)
**Endpoints:**
```
GET  /api/patterns/search?q=railway
GET  /api/patterns/{id}
POST /api/patterns (authenticated)
GET  /api/stats
```

### How Users Access

#### CLI (unchanged for users)
```bash
# Works exactly the same
deia bok search "railway deployment"

# Behind the scenes:
# - Hits API if available
# - Falls back to Git if offline
```

#### VSCode Extension
```
Command: DEIA: Search Book of Knowledge
→ Calls API
→ Results in editor
```

#### Web (new)
```
https://deia.dev/bok
→ Browse, search, filter
→ No git clone needed
```

---

## Migration Path

### Phase 1 → Phase 2

1. **Keep Git as source of truth**
   - GitHub repo continues to work
   - API syncs from Git

2. **Gradually move large files**
   - Conversation logs → S3
   - Git stores links
   - Transparent to users

3. **API becomes primary**
   - CLI uses API first
   - Falls back to Git if offline
   - Zero breaking changes

---

## Cost Estimates

### Phase 1 (Current)
- GitHub: Free
- **Total: $0/month**

### Phase 2 (Hybrid)

**10,000 patterns:**
- S3 storage (10GB): $0.23/month
- PostgreSQL (Supabase free tier): $0
- API hosting (Vercel/Railway): $0-5/month
- **Total: ~$5/month**

**100,000 patterns:**
- S3 storage (100GB): $2.30/month
- PostgreSQL (Supabase Pro): $25/month
- API hosting: $20/month
- CDN: $5/month
- **Total: ~$50/month**

**Funded by:**
- Community donations
- GitHub Sponsors
- Optional paid features (analytics, private patterns)

---

## Timeline

### Now (2025 Q4)
- ✓ Separate BOK repo created
- ✓ Git-based distribution

### 2026 Q1-Q2
- Build API layer
- Add PostgreSQL metadata
- Web UI for browsing

### 2026 Q3
- Migrate large files to S3
- CLI switches to API-first
- Maintain Git fallback

### 2027+
- Advanced features (ML-powered search, recommendations)
- Community voting, ratings
- Cross-platform analytics

---

## Alternatives Considered

### 1. Git LFS
**Pros:** Stays in Git, familiar workflow
**Cons:** Still requires cloning, $5/50GB storage
**Verdict:** Not enough scalability

### 2. Monorepo
**Pros:** Everything in one place
**Cons:** Bloats main repo, breaks at scale
**Verdict:** Already ruled out (separate repos)

### 3. Full Database from Start
**Pros:** Maximum scalability
**Cons:** Complex, costs money, requires hosting
**Verdict:** Premature - start simple, scale when needed

---

## Technical Details

### Metadata Schema (PostgreSQL)

```sql
CREATE TABLE patterns (
  id UUID PRIMARY KEY,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  category TEXT NOT NULL, -- pattern, platform, anti-pattern, session
  platform TEXT, -- railway, vercel, aws, general
  content_url TEXT NOT NULL, -- S3 or GitHub raw
  contributor TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP,
  tags TEXT[],
  keywords TSVECTOR, -- Full-text search
  votes_up INT DEFAULT 0,
  votes_down INT DEFAULT 0
);

CREATE INDEX idx_patterns_search ON patterns USING GIN(keywords);
CREATE INDEX idx_patterns_category ON patterns(category);
CREATE INDEX idx_patterns_platform ON patterns(platform);
```

### API Response Format

```json
{
  "patterns": [
    {
      "id": "uuid",
      "title": "Railway Postgres Connection Pooling",
      "slug": "railway-postgres-connection-pooling",
      "category": "platform",
      "platform": "railway",
      "excerpt": "How to configure connection pooling...",
      "url": "https://deia.dev/patterns/railway-postgres-connection-pooling",
      "content_url": "https://s3.../patterns/railway-postgres-connection-pooling.md",
      "contributor": "username",
      "created_at": "2025-10-07T12:00:00Z",
      "tags": ["postgres", "database", "railway"],
      "votes": 42
    }
  ],
  "total": 1247,
  "page": 1,
  "per_page": 20
}
```

---

## Success Metrics

### Phase 1 (Git-based)
- ✓ Patterns submitted
- ✓ Contributors active
- ✓ CLI search usage

### Phase 2 (Hybrid)
- API uptime > 99.9%
- Search response < 200ms
- Storage costs < $100/month
- Zero downtime migration

---

## Open Questions

1. **When to trigger migration?**
   - Specific pattern count threshold?
   - Repo size limit?
   - Community vote?

2. **How to fund infrastructure?**
   - GitHub Sponsors
   - Community donations
   - Optional paid features
   - Corporate sponsorship

3. **Who hosts/maintains?**
   - DEIA maintainers
   - Community infrastructure team
   - Managed service (Supabase, Vercel)

---

## Related Documents

- [ROADMAP.md](../../ROADMAP.md)
- [CONSTITUTION.md](../../CONSTITUTION.md)
- [BOK Architecture](./bok-architecture.md)

---

**TL;DR:**
- Start simple (Git)
- Scale when needed (Hybrid)
- Keep it cheap (< $100/month)
- Zero breaking changes
- Community-funded
