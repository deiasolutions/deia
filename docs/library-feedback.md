# Library Feedback - Giving Back to Open Source

**Problem:** We use open source libraries every day. We find bugs, create workarounds, discover novel use cases. But we rarely report back to the maintainers.

**Solution:** DEIA automatically detects library usage and prompts you to share feedback - bugs, workarounds, novel patterns - directly to library maintainers.

**We owe it to them.** They open-sourced their work. The least we can do is build an open-source feedback mechanism for them.

---

## How It Works

### Automatic Detection

When Claude Code logs a conversation, DEIA detects:
- **Imports used:** `import pandas as pd`
- **Problems encountered:** "DataFrame.merge() raising KeyError"
- **Workarounds created:** "Used concat() instead"
- **Novel patterns:** "Combined groupby() + apply() for streaming aggregation"

### Feedback Categories

1. **Bug Report** - Library behaving incorrectly
2. **Workaround** - You found a way around a bug/limitation
3. **Novel Use Case** - You used the library in an unexpected way
4. **Feature Request** - Library could do something it doesn't
5. **Performance Issue** - Library is slow in specific scenario
6. **Documentation Gap** - Docs missing critical info

### User Prompt

```
[DEIA] Detected library usage: pandas 2.1.0
  - Issue: DataFrame.merge() KeyError on duplicate columns
  - Your workaround: Used concat() with join parameter

Share with pandas maintainers? [Y/n]
  [1] Bug report (create GitHub issue)
  [2] Workaround only (add to community patterns)
  [3] Not now
```

### Where It Goes

**Option 1: Direct to Library**
- Creates GitHub issue on library's repo
- Auto-populated with:
  - Bug description
  - Code snippet
  - Workaround (if found)
  - Environment info (Python version, OS, etc.)
  - Your contact info (optional)

**Option 2: DEIA Community BOK**
- Adds to `bok/libraries/pandas/patterns/`
- Other DEIA users benefit
- Library maintainers can discover it via DEIA search
- Aggregated patterns can be submitted as batch PR to library docs

**Option 3: Both**
- Submit to library immediately
- Also save to DEIA BOK for community

---

## Privacy & Control

### What Gets Shared

**By default (with your permission):**
- Library name and version
- Description of issue/pattern
- Code snippet (sanitized)
- Your workaround/solution
- Environment info (OS, Python version, etc.)

**Never shared without asking:**
- Your name/email (unless you opt in)
- Project-specific code
- Proprietary logic
- Sensitive data

### Opt-Out

```bash
# Disable library feedback globally
deia config set library_feedback false

# Disable for specific library
deia library ignore pandas

# Re-enable
deia library track pandas
```

---

## Example Workflow

### Scenario: Bug in Requests Library

```python
# Your code
import requests

response = requests.get("https://api.example.com", timeout=5)
# Raises ConnectionError after 5 seconds, but should retry
```

**Claude helps you:**
```python
# Workaround
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

response = session.get("https://api.example.com", timeout=5)
```

**DEIA detects:**
- Library: `requests 2.31.0`
- Issue: No automatic retry on timeout
- Workaround: Session + HTTPAdapter + Retry
- Pattern: Retry configuration for API calls

**DEIA prompts:**
```
[DEIA] Library feedback opportunity

Library: requests 2.31.0
Issue: No automatic retry on connection timeout
Workaround: Session-based retry adapter

This is a common pattern that could help others.

Share with:
  [1] requests maintainers (GitHub issue)
  [2] DEIA community (BOK entry)
  [3] Both
  [4] Not now

Your choice: _
```

**You choose [2] - DEIA community**

DEIA creates:
- `bok/libraries/requests/patterns/automatic-retry-on-timeout.md`
- Includes your workaround
- Other DEIA users discover it when they hit same issue
- Prevents duplicate bug reports to requests repo

---

## Library Maintainer Benefits

### For Popular Libraries (pandas, requests, numpy)

**Problem:** They get hundreds of duplicate bug reports

**DEIA Solution:**
- DEIA tracks occurrence count
- If 50 users hit same bug, DEIA submits ONE report with:
  - "Confirmed by 50 DEIA users"
  - Most common workaround
  - Link to DEIA BOK entry with all variations

**Benefit:** Signal vs noise. High-impact issues float to top.

### For Small Libraries (your friend's side project)

**Problem:** No one reports bugs because it's "just a small library"

**DEIA Solution:**
- Every bug gets reported (if user approves)
- Workarounds are shared
- Novel use cases inspire maintainer

**Benefit:** Small projects get the feedback they deserve.

---

## Configuration

### Per-Project Settings

`.deia/config.json`:
```json
{
  "library_feedback": {
    "enabled": true,
    "auto_submit": false,
    "tracked_libraries": ["pandas", "requests", "flask"],
    "ignored_libraries": ["private-company-lib"],
    "default_action": "prompt"
  }
}
```

### Global Settings

`~/.deia-global/config.json`:
```json
{
  "library_feedback": {
    "default_enabled": true,
    "auto_submit_threshold": 10,
    "include_email": false,
    "preferred_contact": "github_username"
  }
}
```

---

## Auto-Submit Threshold

**Concept:** If DEIA detects the SAME bug 10 times across different users, auto-submit to library.

**How it works:**
1. User 1 hits bug, saves to DEIA BOK
2. User 2 hits bug, DEIA detects ditto
3. ...
4. User 10 hits bug, DEIA reaches threshold
5. DEIA auto-creates GitHub issue:

```markdown
## Issue: DataFrame.merge() KeyError on duplicate columns

**Confirmed by 10 DEIA users**

### Description
When merging DataFrames with duplicate column names...

### Most common workaround
Reset index before merge, or use concat()

### Environment
- pandas 2.1.0
- Python 3.11
- Windows 10 (6 users), Linux (4 users)

### References
See DEIA BOK for full pattern library:
https://github.com/deiasolutions/deia/bok/libraries/pandas/issues/merge-keyerror.md

---

*This issue was automatically reported by DEIA after reaching the community threshold.*
*10 users encountered this issue independently. No duplicates were filed.*
```

**Benefit:** Maintainers get ONE high-quality report instead of 10 low-quality ones.

---

## Novel Use Cases

### Example: Streaming Aggregation with Pandas

You discover:
```python
# Novel pattern: Streaming aggregation without loading full DataFrame
import pandas as pd

def stream_aggregate(file_path, chunk_size=10000):
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    return pd.concat([
        chunk.groupby('category').agg({'amount': 'sum'})
        for chunk in chunks
    ]).groupby(level=0).sum()

result = stream_aggregate('huge_file.csv')
```

**DEIA detects:**
- Novel use of `read_csv(chunksize=...)`
- Combined with `groupby().agg()`
- Solves memory issue for large files

**DEIA prompts:**
```
[DEIA] Novel pattern detected

You're using pandas.read_csv() with chunking + groupby aggregation.
This pattern isn't in pandas docs or common tutorials.

Share as:
  [1] Example for pandas docs (PR to pandas-dev/pandas)
  [2] Blog post idea
  [3] DEIA community pattern
  [4] All of the above

Your choice: _
```

**Result:** Pandas docs get better. Community learns. You get credit.

---

## Integration with Ditto Tracking

**Synergy:** Library feedback + Ditto tracking work together

When User 2 hits the same pandas bug as User 1:
1. DEIA detects duplicate
2. Shows User 1's workaround immediately
3. Asks: "Did this workaround work for you?"
4. If yes: +1 to workaround effectiveness
5. If no: "What did you do instead?"
6. Aggregate data improves for everyone

---

## Slash Command: `/library-feedback`

Manual trigger for when you want to report something:

```
You: /library-feedback

Claude: Which library?
You: flask

Claude: What type of feedback?
  [1] Bug report
  [2] Workaround
  [3] Novel use case
  [4] Feature request
  [5] Performance issue

You: 2

Claude: Describe the issue and your workaround...
```

---

## Why This Matters

### For Users
- **Get help faster** - Someone else already found the workaround
- **Learn patterns** - See how others use libraries
- **Build reputation** - Your contributions are tracked

### For Maintainers
- **Better signal** - High-impact issues clearly marked
- **Fewer duplicates** - DEIA deduplicates automatically
- **Community patterns** - See how people actually use your library
- **Novel use cases** - Discover unexpected applications

### For Humanity
- **Commons grows** - Every bug found benefits everyone
- **Knowledge persists** - Workarounds don't die with StackOverflow threads
- **Balance** - Open source deserves open feedback

---

## Implementation Priority

**Phase 1 (MVP):**
- Detect library imports in conversations
- Prompt user to save workarounds to DEIA BOK
- Manual `/library-feedback` command

**Phase 2:**
- Auto-detect bugs vs workarounds vs novel patterns
- GitHub issue creation
- Ditto tracking for library issues

**Phase 3:**
- Auto-submit at threshold
- Integration with library maintainer dashboards
- Aggregate reporting to maintainers

---

**We use their code. The least we can do is give back.**

This is the DEIA way.
