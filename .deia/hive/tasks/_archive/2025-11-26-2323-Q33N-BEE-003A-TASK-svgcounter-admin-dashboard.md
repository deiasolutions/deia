# Task Assignment: BEE-003A - SVG Counter Admin Dashboard

**Assigned to:** BEE-003A
**Assigned by:** Q33N
**Priority:** P0
**Created:** 2025-11-26 23:23 CDT
**Project:** svgcounter service

---

## Context

We are building a self-hosted SVG badge counter service. Full spec is at:
`familybondbot/.deia/svgcounter-spec.md`

You are responsible for **Admin Dashboard**. Two other bees are working in parallel:
- BEE-001A: Database & Infrastructure (schema, connection module)
- BEE-002A: Core API (counter logic, SVG generation)

**Working Directory:** `deiasolutions/services/svgcounter/`

---

## Task

Implement the admin dashboard for viewing and managing counters.

---

## Deliverables

### 1. Admin API Endpoints

Create `src/routes/admin.js`:

**GET /admin/api/counters**
- Requires Bearer token auth: `Authorization: Bearer {ADMIN_TOKEN}`
- Returns all counters with stats

**Response:**
```json
{
  "counters": [
    {
      "id": "ra96it-readme",
      "total_count": 342,
      "unique_count": 142,
      "created_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T14:30:00Z"
    }
  ],
  "summary": {
    "total_counters": 5,
    "total_views": 1842,
    "total_unique": 567
  }
}
```

**Query params (optional):**
- `sort` - Sort by: count, name, updated (default: updated)
- `order` - asc or desc (default: desc)
- `search` - Filter by counter ID

### 2. Admin Dashboard UI

**Route:** `GET /admin`
- Requires Bearer token (via query param `?token=` or cookie)
- Returns server-rendered HTML page

**Features:**
- Table of all counters
- Columns: Name, Total Views, Unique Views, Created, Last Updated
- Sortable columns (client-side JS okay)
- Search/filter box
- Summary stats at top (total counters, total views, total unique)

**Styling:**
- Simple, clean design
- Can use Tailwind CDN or minimal inline CSS
- Mobile-friendly (responsive)
- Dark mode optional

### 3. Auth Middleware

Create `src/middleware/auth.js`:
- Validates Bearer token against ADMIN_TOKEN env var
- Returns 401 if invalid/missing
- Used by all /admin/* routes

### 4. Admin HTML Template

Create `src/views/admin.html` (or use template string):

```html
<!DOCTYPE html>
<html>
<head>
  <title>SVG Counter Admin</title>
  <style>/* inline CSS or Tailwind CDN */</style>
</head>
<body>
  <h1>SVG Counter Dashboard</h1>

  <!-- Summary stats -->
  <div class="stats">
    <div>Total Counters: {{totalCounters}}</div>
    <div>Total Views: {{totalViews}}</div>
    <div>Total Unique: {{totalUnique}}</div>
  </div>

  <!-- Search -->
  <input type="text" placeholder="Search counters..." id="search">

  <!-- Table -->
  <table>
    <thead>
      <tr>
        <th>Counter ID</th>
        <th>Total Views</th>
        <th>Unique Views</th>
        <th>Created</th>
        <th>Last Updated</th>
      </tr>
    </thead>
    <tbody>
      {{#counters}}
      <tr>
        <td>{{id}}</td>
        <td>{{total_count}}</td>
        <td>{{unique_count}}</td>
        <td>{{created_at}}</td>
        <td>{{updated_at}}</td>
      </tr>
      {{/counters}}
    </tbody>
  </table>

  <script>/* sorting and filtering JS */</script>
</body>
</html>
```

---

## File Structure (Your Part)

```
svgcounter/src/
├── routes/
│   └── admin.js        # Admin API routes
├── middleware/
│   └── auth.js         # Bearer token auth
└── views/
    └── admin.html      # Dashboard template
```

---

## Success Criteria

- [ ] `GET /admin` shows dashboard (requires token)
- [ ] `GET /admin/api/counters` returns JSON (requires token)
- [ ] Unauthorized requests get 401
- [ ] Dashboard shows all counters in table
- [ ] Summary stats display correctly
- [ ] Search/filter works
- [ ] Basic styling (not ugly)
- [ ] Code has comments

---

## Integration with Other Bees

- BEE-001A creates database module - you'll import for queries
- BEE-002A creates main app - you'll export routes to register

Export your routes so BEE-002A can register them:
```js
// In admin.js
module.exports = router;

// In app.js (BEE-002A will add)
const adminRoutes = require('./routes/admin');
app.use('/admin', authMiddleware, adminRoutes);
```

---

## Constraints

- DO NOT implement database schema (that's BEE-001A)
- DO NOT implement counter endpoints (that's BEE-002A)
- Focus ONLY on admin functionality

---

## Activity Logging (MANDATORY)

You MUST log your activity to:
```
deiasolutions/.deia/bot-logs/BEE-003A-activity.jsonl
```

Log format:
```json
{"ts": "2025-11-26T23:30:00Z", "bee": "BEE-003A", "event": "task_started", "task": "svgcounter-admin-dashboard", "msg": "Starting admin dashboard implementation"}
```

Log every 20-30 minutes. NO EXCEPTIONS.

---

## Deliverable

When complete, post response to:
```
deiasolutions/.deia/hive/responses/2025-11-26-XXXX-BEE-003A-Q33N-RESPONSE-svgcounter-admin-complete.md
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
