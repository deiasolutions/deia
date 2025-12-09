# IMMEDIATE ASSIGNMENT: BOT-003 - Feature 2: Conversation Analytics

**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-003 (Chat Controller)
**Date:** 2025-10-25 18:20 CDT
**Priority:** P0 - START NOW
**Status:** QUEUE READY

---

## You've Got Momentum

Feature 1 (Advanced Search) done. Now: Insights.

---

## Feature 2: Conversation Analytics (2 hours)

**What it is:**
Show insights about conversations. What works, what doesn't.

**What to build:**

### Analytics Engine
- Word frequency analysis (most used words, topics)
- Bot performance metrics (avg response time, success rate, user satisfaction)
- Conversation patterns (average length, most common flows)
- Time analytics (when users chat most, peak hours)
- Engagement metrics (sessions per user, repeat users)

### REST API Endpoints
- `POST /api/analytics/calculate` - Force analytics recalculation
- `GET /api/analytics/summary` - Overall system analytics
- `GET /api/analytics/bot/{bot_id}` - Analytics for specific bot
- `GET /api/analytics/export` - Export analytics as CSV/JSON

### Dashboard
- Visual charts (word clouds, bar charts, line graphs)
- Key metrics displayed prominently
- Trends over time
- Filters by date range, bot type, session

**Implementation:**
- `src/deia/services/analytics_engine.py` (NEW) - ConversationAnalytics class
- Pre-computed stats stored in `.deia/hive/logs/analytics.jsonl` (updated hourly)
- Efficient calculations using Python collections (Counter for word frequency)
- Caching to avoid recalculating on every request

**Success criteria:**
- [ ] Word frequency accurate
- [ ] Pattern detection working
- [ ] Charts render correctly
- [ ] Export works (CSV + JSON)
- [ ] Performance < 2s to load
- [ ] 70%+ test coverage

**Time estimate:** 2 hours

---

## Key Metrics to Calculate

**Word Frequency:**
- Top 50 words (exclude common words: "the", "a", "to", etc.)
- Frequency count for each
- Generate from all messages in history

**Bot Performance:**
- Messages per bot (count)
- Average response time per bot
- Task completion rate per bot
- User satisfaction (if available)

**Patterns:**
- Average session length (messages)
- Average user messages per session
- Most common task types
- Busiest time of day

**Engagement:**
- Users per day
- Return user percentage
- Session frequency per user
- Average daily active users

---

## Integration with Previous Features

- Search results can be analyzed for trends
- Analytics shown in dashboard (Feature 6)
- Custom commands can trigger analytics reports
- Templates track analytics (which flows are popular)
- Collaboration features visible in engagement metrics

---

## Queue Status

**Completed:** Feature 1 (Search)
**Next in queue:** Feature 3 (Custom Commands) - ready when done
**After that:** Features 4-6 queued and ready

Smooth pipeline. No idle time.

---

## GO

Analytics transforms raw data into insights.

Build it.

**003: Start Feature 2 immediately.**

---

**Q33N out. Insights matter.**
