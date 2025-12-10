# Ditto Tracking - Duplicate Issue Detection

**Problem:** Users keep hitting the same bugs. Submitting duplicate reports wastes time.

**Solution:** Detect duplicates, record "ditto" (+1), point to existing workaround.

---

## How It Works

### User Hits Known Issue

```
User works with Claude on Railway deployment
Claude: "HTTPS redirects aren't working"
DEIA: Checking for similar issues...
      ✓ Found match: Railway HTTPS redirect (92% similarity)

Compare:
  Your issue: "HTTPS redirects failing on Railway"
  BOK entry:  "Railway requires custom middleware for HTTPS redirects"

Is this the same issue? [Y/n]: y

✓ Recorded as occurrence #47
  Workaround: bok/platforms/deployment/railway/https-redirect-middleware.md
```

### What Gets Saved

**NOT saved:**
- Full conversation log (already in BOK)
- Detailed context (redundant)
- Duplicate BOK entry

**SAVED:**
```json
{
  "issue_id": "railway-https-redirect",
  "occurrences": [
    {
      "user": "dave",
      "date": "2025-10-06T19:30:00Z",
      "project": "familybondbot",
      "resolved_by": "existing_workaround"
    }
  ],
  "total_count": 47
}
```

---

## Benefits

### For Users
- **Fast resolution:** Immediately pointed to workaround
- **No duplicate work:** Don't re-solve solved problems
- **Learn from community:** See how many others hit this

### For DEIA
- **Occurrence metrics:** Which issues are most painful?
- **Priority ranking:** 100 occurrences > 2 occurrences
- **Partner notifications:** Auto-alert vendors at thresholds

### For Partners (Railway, Vercel, etc.)
- **Impact data:** See how many users affected
- **Fix prioritization:** Focus on high-occurrence issues
- **Community feedback:** Real-world pain points

---

## Notification Thresholds

DEIA automatically notifies when thresholds reached:

| Threshold | Action |
|-----------|--------|
| 10 occurrences | Announce in Discord/Discussions |
| 50 occurrences | Email partner (Railway, Vercel, etc.) |
| 100 occurrences | Critical priority, public issue filed |

**Example notification to Railway:**
```
Subject: DEIA Community Report - HTTPS Redirect Issue (47 occurrences)

The DEIA community has reported 47 occurrences of HTTPS redirect
issues on Railway deployments since Sept 15, 2025.

Issue: Railway requires custom middleware for HTTPS redirects
Workaround: https://github.com/deiasolutions/deia/bok/platforms/deployment/railway/

Recommendation: Make HTTPS redirects default behavior to reduce
friction for developers.

View detailed data: [link to DEIA dashboard]
```

---

## Duplicate Detection Algorithm

### Similarity Matching

**Step 1: Extract issue description**
```
From conversation:
"HTTPS redirects aren't working on Railway. Getting ERR_TOO_MANY_REDIRECTS."
```

**Step 2: Search BOK for platform**
```
Search: platform="railway"
Results:
  - Railway HTTPS redirect issue
  - Railway environment variables
  - Railway build failures
```

**Step 3: Semantic similarity**
```
Calculate similarity:
  User description vs BOK entry description

Similarity scores:
  Railway HTTPS redirect: 92% match ✓
  Railway env vars: 15% match
  Railway build: 8% match
```

**Step 4: Present to user**
```
High confidence match (>85%): Auto-suggest ditto
Medium confidence (70-85%): Ask user to confirm
Low confidence (<70%): Offer as "similar issue"
```

---

## When to Submit vs Ditto

### Submit New Entry

**When:**
- No similar BOK entry found (similarity < 70%)
- User confirms "this is different"
- New platform or new bug category
- Existing workaround doesn't solve user's problem

**Result:**
- Full submission to DEIA intake
- New BOK entry created
- Becomes searchable for future dittos

### Record Ditto

**When:**
- High similarity match (>85%)
- User confirms "same issue"
- Existing workaround solves problem

**Result:**
- Increment occurrence counter
- No new BOK entry
- User gets immediate solution

### Ask User

**When:**
- Medium similarity (70-85%)
- Uncertain if variant or duplicate
- Multiple potential matches

**Result:**
- User decides: submit new or record ditto
- DEIA learns from user choice (improves matching)

---

## Status Lifecycle

Issues tracked through lifecycle:

```
workaround_exists → Partner notified → Fix pending → Resolved
```

### Status: Workaround Exists
- Community found solution
- Not yet fixed by partner
- Occurrences being tracked

### Status: Partner Notified
- Threshold reached (50+ occurrences)
- Partner has been informed
- Awaiting response

### Status: Fix Pending
- Partner acknowledged issue
- Fix in development
- ETA provided

### Status: Resolved
- Partner deployed fix
- Users can remove workaround
- Archived for historical data

**Partner can update status:**
```bash
# Railway fixes HTTPS redirect in v2024.10.1
curl -X POST https://deia.community/api/ditto/update \
  -H "Authorization: Bearer railway_api_key" \
  -d '{
    "issue_id": "railway-https-redirect",
    "status": "resolved",
    "note": "Fixed in Railway v2024.10.1. HTTPS redirects now default behavior.",
    "fix_version": "2024.10.1"
  }'
```

**DEIA notifies users:**
```
✓ Railway fixed: HTTPS redirect issue (resolved in v2024.10.1)

You have workaround code in: familybondbot/middleware/https-redirect.js

Options:
[1] Remove workaround (Railway handles it now)
[2] Keep workaround (for backward compatibility)
[3] Test first, decide later

> Your choice: _
```

---

## Storage Location

```
~/.deia-global/ditto-tracker/
├── railway-https-redirect.json
├── claude-hallucination-api.json
├── vercel-env-detection.json
└── gemini-context-limit.json
```

Each file contains:
- Issue metadata
- Full occurrence history
- Notification status
- Current status
- BOK entry reference

---

## Privacy

**Ditto tracking respects privacy:**

- Only saves: user, date, project name, resolution method
- No conversation logs stored (just +1 counter)
- User can opt out: `deia config set ditto_tracking false`
- Occurrence data can be anonymized for partner reports

---

## Command Line Usage

```bash
# Record a ditto
deia ditto record railway-https-redirect

# Check occurrence count
deia ditto count railway-https-redirect
# Output: 47 occurrences

# List high-impact issues
deia ditto list --min-occurrences 10

# Update issue status (partners only)
deia ditto update railway-https-redirect --status resolved

# View issue stats
deia ditto stats railway-https-redirect
```

---

## Integration with Logging

**Automatic detection during logging:**

```python
# In conversation logger
def detect_duplicate_issues(conversation):
    """Check if conversation contains known issues"""

    # Extract issue descriptions
    issues = extract_issues_from_conversation(conversation)

    for issue in issues:
        # Check for duplicates
        match = ditto_tracker.find_similar_issue(issue)

        if match and match.similarity > 0.85:
            # Prompt user to record ditto
            user_choice = prompt_ditto_or_new(match)

            if user_choice == "ditto":
                ditto_tracker.record_occurrence(
                    issue_id=match.issue_id,
                    bok_entry=match.bok_entry,
                    user=current_user,
                    project=current_project
                )
                return match.bok_entry  # Point user to solution
```

---

**This system reduces noise while capturing valuable occurrence data for prioritization.**
