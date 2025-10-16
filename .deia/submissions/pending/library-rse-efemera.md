---
type: improvement
project: deiasolutions
created: 2025-10-15
status: pending
sanitized: true
category: documentation
---

# Library: Add src/efemera/rse.py to REPO_INDEX

## Summary
New Python library for RSE (Runtime System Events) logging created for the Efemera project should be documented in the REPO_INDEX so other bots/agents can discover and use it.

## Details

**Library Location:** `src/efemera/rse.py`

**Purpose:** Append-only event logging to `.deia/telemetry/rse.jsonl` for observability and telemetry.

**Event Shape:**
```python
{
  "ts": "2025-10-15T12:34:56Z",  # ISO timestamp
  "type": "event_type",           # Event type (e.g., "identity_bind", "activity_post")
  "lane": "Code",                 # Lane (e.g., "Code", "Edge", "Node")
  "actor": "role",                # Actor role (e.g., "Edge", "Node", "Queen")
  "data": {}                      # Additional event data
}
```

**API:**
```python
from src.efemera.rse import log_rse

log_rse(
    event_type="identity_bind",
    lane="Code",
    actor="Edge",
    data={"actorId": "edge-001", "keyId": "abc123"}
)
```

**Features:**
- Automatic timestamp generation (UTC ISO format)
- Automatic directory creation (`.deia/telemetry/`)
- Append-only JSONL format
- Optional root path override for testing

**Current Usage:**
- `services/identity_dev/main.py` - Identity service telemetry
- Planned for all Efemera subsystems per RSE-0.1 spec

## Category
`.claude/REPO_INDEX.md` → "Code" section (after DEIA core libraries)

## Proposed REPO_INDEX Addition

Add this section after the existing "Code:" block:

```markdown
**Efemera Libraries:**
- `src/efemera/rse.py` - RSE (Runtime System Events) logging helper for telemetry
```

## Validation

**Library tested with:**
- `services/identity_dev/main.py` successfully uses `log_rse()` function
- Creates `.deia/telemetry/rse.jsonl` correctly
- Events written in proper JSONL format
- No errors during imports or execution

**Follows standards:**
- ✅ Python type hints used
- ✅ Docstring present
- ✅ No external dependencies (uses stdlib only)
- ✅ Simple, focused API
- ✅ Aligns with RSE-0.1 specification (`docs/observability/RSE-0.1.md`)

## Related Documentation

**Efemera Architecture:**
- `docs/efemera/EFEMERA-SYSTEM-ARCHITECTURE-v0.1.md` - References RSE as core observability
- `docs/observability/RSE-0.1.md` - RSE standard specification
- `docs/specs/Efemera-Build-Spec-v2.0.md` - Technical roadmap
- `docs/comms/BL-2025-10-14-efemera-kickstart.md` - Usage examples

## Why This Matters

**Discoverability:** Other bots working in the repo need to know this library exists to:
1. Use it for their own telemetry needs
2. Understand where telemetry events are being written
3. Build compatible tooling (viewers, analyzers, etc.)

**Governance:** Following proper submission process instead of directly editing REPO_INDEX (avoiding "jailbreaker" behavior)

**Commons Value:** This library could be useful for any DEIA-integrated project needing lightweight event logging

## Tags
library, telemetry, observability, rse, efemera, logging, jsonl
