---
title: "Egg Offline Launch Capability Specification"
version: 0.1.0
date: 2025-10-16
author: daaaave-atx
status: Specification / Partially Implemented
category: Resilience / Architecture
tags: [egg, offline-mode, resilience, launch-protocol, telemetry]
---

# Egg Offline Launch Capability Specification

## Purpose

When a Factory Egg attempts to hatch but cannot access all required resources (eOS pack missing, DEIA Global Commons unreachable), it should gracefully degrade and operate in **offline mode** rather than failing completely.

This ensures:
1. Work can continue in disconnected environments
2. Launch events are logged for later sync
3. System demonstrates resilience and adaptability
4. Human/AI operators have visibility into what worked and what didn't

## Design Philosophy

> "An Egg should adapt to its environment, not the other way around."

This capability embodies the principle that DEIA systems should be:
- **Resilient:** Work offline when necessary
- **Observable:** Always log what happened
- **Syncable:** Reconcile with Commons when connection restored
- **Honest:** Report failures transparently

### What "Offline" Means

**"Offline launch" assumes these resources ARE available locally:**
- ✅ AI/LLM to read Egg instructions (Claude, GPT, local model, or API that still works)
- ✅ Python runtime environment
- ✅ Builder tools (`.deia/tools/llh_factory_build.py`, etc.)
- ✅ Cached templates (`.deia/templates/`)
- ✅ Local compute and storage

**"Offline" means these resources are NOT available:**
- ❌ Network access to DEIA Global Commons (GitHub repo)
- ❌ Remote eOS packs (not cached locally)
- ❌ Latest Commons tools/templates (working from cache)
- ❌ Validation against latest schema (deferred)
- ❌ Real-time sync with other hives

**Key insight:** The system works in **air-gapped or disconnected environments** (classified networks, offline field operations, restricted environments) as long as there is local compute and cached DEIA resources. This enables organizations to bootstrap using DEIA patterns even when isolated, then sync when they reconnect.

This is not "AI-less operation" - it's "Commons-disconnected operation with local AI."

## Offline Launch Scenarios

### Scenario 1: Missing eOS Pack

**Condition:** Egg launched but cannot find designated eOS pack file

**Behavior:**
1. Check if eOS pack exists at specified path
2. If NOT found:
   - Log: "eOS pack not found at {path}"
   - Offer: "Deploy with defaults? (y/n)"
   - If YES: Use minimal template/defaults
   - If NO: Abort with helpful error message
3. Create launch log with missing dependency noted

### Scenario 2: Global Commons Unreachable

**Condition:** Egg needs Commons tools but cannot reach network/repo

**Behavior:**
1. Check for Commons tools at expected paths (`.deia/tools/`, `.deia/templates/`)
2. If local copies exist: Use cached version
3. If NOT found locally:
   - Log: "Global Commons unreachable, required tools: {list}"
   - Check if minimal operation possible without them
   - If YES: Proceed with degraded capability
   - If NO: Enter offline queue mode (deferred launch)
4. Create launch log noting which tools were/weren't available

### Scenario 3: Partial Resources

**Condition:** Some resources available, others missing

**Behavior:**
1. Inventory available resources:
   - ✅ eOS pack: found
   - ❌ Builder tool: missing
   - ✅ Templates: found (local cache)
2. Determine minimal viable operation
3. Proceed with available resources
4. Log all missing dependencies for later resolution

## Launch Log Format

Every offline launch creates a structured log:

```yaml
---
type: offline_launch
timestamp: 2025-10-16T14:30:00Z
egg_id: llh-factory
launch_attempt: 1
environment:
  network_available: false
  eos_pack_found: false
  commons_tools_available: partial

resources_checked:
  - resource: eos-pack
    path: .deia/eos-packs/my-org.yaml
    status: not_found
    action_taken: offered_defaults

  - resource: builder_tool
    path: .deia/tools/llh_factory_build.py
    status: found_cached
    version: 0.1.0
    action_taken: used_local_copy

  - resource: global_commons
    url: https://github.com/deiasolutions/deia.git
    status: unreachable
    action_taken: skipped_sync

launch_outcome: partial_success
entities_created: 2
entities_failed: 1
degraded_capabilities:
  - validation_skipped
  - commons_sync_deferred

message_for_commons: |
  Offline launch completed with degraded capability.
  Missing: eOS pack, Commons network connection.
  Used: Cached builder v0.1.0, default templates.
  Created: 2 LLHs (basic structure only).

  Action needed on next sync:
  - Validate created entities against latest schema
  - Apply any eOS pack updates
  - Re-sync with Commons for latest templates

next_sync_actions:
  - validate_entities
  - fetch_eos_pack
  - sync_with_commons
  - report_launch_status
---
```

## Implementation Components

### 1. Resource Checker

**Function:** `check_resources(egg_manifest)`

```python
def check_resources(egg_manifest):
    """Check availability of required resources.

    Returns:
        dict: {
            'eos_pack': {'available': bool, 'path': str},
            'builder': {'available': bool, 'version': str},
            'templates': {'available': bool, 'cached': bool},
            'commons': {'reachable': bool, 'url': str}
        }
    """
    resources = {}

    # Check eOS pack
    eos_pack_path = egg_manifest.get('eos_pack_path')
    resources['eos_pack'] = {
        'available': Path(eos_pack_path).exists() if eos_pack_path else False,
        'path': eos_pack_path
    }

    # Check builder tool
    builder_path = '.deia/tools/llh_factory_build.py'
    resources['builder'] = {
        'available': Path(builder_path).exists(),
        'path': builder_path,
        'version': get_tool_version(builder_path) if Path(builder_path).exists() else None
    }

    # Check Commons connectivity
    try:
        # Simple check - can we reach the repo?
        import urllib.request
        commons_url = egg_manifest.get('commons_url', 'https://github.com/deiasolutions/deia.git')
        urllib.request.urlopen(commons_url, timeout=3)
        resources['commons'] = {'reachable': True, 'url': commons_url}
    except:
        resources['commons'] = {'reachable': False, 'url': commons_url}

    return resources
```

### 2. Offline Launch Coordinator

**Function:** `launch_offline(egg, resources_status)`

```python
def launch_offline(egg, resources_status):
    """Coordinate offline launch with degraded capabilities.

    Args:
        egg: Egg manifest
        resources_status: Output from check_resources()

    Returns:
        dict: Launch outcome and log
    """
    launch_log = {
        'type': 'offline_launch',
        'timestamp': iso_now(),
        'egg_id': egg['id'],
        'resources_checked': [],
        'degraded_capabilities': []
    }

    # Determine what we can do
    can_build = resources_status['builder']['available']
    can_validate = resources_status['commons']['reachable']
    has_pack = resources_status['eos_pack']['available']

    if not has_pack:
        # Offer defaults or abort
        response = input("eOS pack not found. Use default minimal structure? (y/n): ")
        if response.lower() == 'y':
            # Use minimal defaults
            launch_log['action_taken'] = 'used_defaults'
        else:
            launch_log['outcome'] = 'aborted'
            return launch_log

    if can_build:
        # Proceed with available resources
        if not can_validate:
            launch_log['degraded_capabilities'].append('validation_skipped')
        if not resources_status['commons']['reachable']:
            launch_log['degraded_capabilities'].append('commons_sync_deferred')

        # Execute build (simplified)
        outcome = execute_build(egg, has_pack)
        launch_log.update(outcome)
    else:
        # Can't build - queue for later
        launch_log['outcome'] = 'deferred'
        launch_log['action_taken'] = 'queued_for_sync'

    # Write launch log
    write_launch_log(launch_log)

    return launch_log
```

### 3. Launch Log Writer

**Function:** `write_launch_log(log)`

```python
def write_launch_log(log):
    """Write offline launch log for later sync.

    Log location: .deia/telemetry/offline-launches.jsonl
    """
    log_path = Path('.deia/telemetry/offline-launches.jsonl')
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open('a', encoding='utf-8') as f:
        f.write(json.dumps(log, ensure_ascii=False) + '\n')

    # Also create human-readable summary
    summary_path = Path('.deia/telemetry/offline-launch-summary.txt')
    with summary_path.open('a', encoding='utf-8') as f:
        f.write(f"\n=== Offline Launch: {log['timestamp']} ===\n")
        f.write(f"Egg: {log['egg_id']}\n")
        f.write(f"Outcome: {log.get('outcome', 'unknown')}\n")
        if log.get('degraded_capabilities'):
            f.write(f"Degraded: {', '.join(log['degraded_capabilities'])}\n")
        if log.get('message_for_commons'):
            f.write(f"\nMessage for Commons:\n{log['message_for_commons']}\n")
```

### 4. Sync Reconciliation (Future)

**Function:** `sync_offline_launches()`

When connection to Commons is restored:

```python
def sync_offline_launches():
    """Send offline launch logs to Commons and reconcile."""
    log_path = Path('.deia/telemetry/offline-launches.jsonl')
    if not log_path.exists():
        return

    # Read all offline launch logs
    logs = []
    with log_path.open('r') as f:
        for line in f:
            logs.append(json.loads(line))

    # For each log:
    for log in logs:
        # 1. Validate created entities against latest schema
        if 'entities_created' in log:
            validate_entities(log['entities_created'])

        # 2. Report to Commons
        report_to_commons(log)

        # 3. Apply any updates needed
        if 'next_sync_actions' in log:
            execute_sync_actions(log['next_sync_actions'])

    # Archive processed logs
    archive_path = log_path.with_suffix('.processed.jsonl')
    log_path.rename(archive_path)
```

## User Experience

### Command Line

```bash
$ python .deia/tools/llh_factory_build.py --eos-pack my-org.yaml

Checking resources...
✓ Builder tool found (v0.1.0)
✓ Templates available (local cache)
✗ eOS pack not found: my-org.yaml
⚠ Global Commons unreachable

Offline launch mode activated.

eOS pack not found. Options:
  1. Use default minimal structure
  2. Specify different pack path
  3. Abort and retry later

Choice (1/2/3): 1

Proceeding with defaults...
✓ Created 2 LLHs (basic structure)
⚠ Validation skipped (Commons unreachable)

Launch log saved to: .deia/telemetry/offline-launches.jsonl

Next steps:
  - Review created entities
  - When online, run: deia sync --offline-launches
  - This will validate and report to Commons
```

### Launch Log Example (Human-Readable)

```
=== Offline Launch: 2025-10-16T14:30:00Z ===
Egg: llh-factory
Outcome: partial_success
Degraded: validation_skipped, commons_sync_deferred

Message for Commons:
Offline launch completed with degraded capability.
Missing: eOS pack, Commons network connection.
Used: Cached builder v0.1.0, default templates.
Created: 2 LLHs (basic structure only).

Action needed on next sync:
- Validate created entities against latest schema
- Apply any eOS pack updates
- Re-sync with Commons for latest templates
```

## Implementation Status

### ✅ Currently Implemented (v0.1)
- Resource checking (eOS pack exists)
- Builder tool execution
- Basic error messages
- RSE logging

### ⏳ Partially Implemented
- Offline mode detection
- Launch log creation
- Human-readable summaries

### 🔮 Planned (Future)
- Automatic Commons sync on reconnect
- Validation reconciliation
- Queued launch execution
- Delta updates from Commons

## Testing Scenarios

### Test 1: No eOS Pack
```bash
# Remove pack
rm .deia/eos-packs/test.yaml

# Launch should offer defaults
python .deia/tools/llh_factory_build.py --eos-pack test.yaml
```

**Expected:** Prompt for default structure, create launch log

### Test 2: No Network
```bash
# Disable network
# (or set Commons URL to unreachable)

# Launch should use cached resources
python .deia/tools/llh_factory_build.py --eos-pack test.yaml
```

**Expected:** Build succeeds, validation skipped, sync deferred

### Test 3: Sync After Offline
```bash
# Re-enable network

# Sync offline launches
python .deia/tools/sync.py --offline-launches
```

**Expected:** Logs sent to Commons, entities validated, summary report

## Related Documents

- Factory Egg Specification: `.deia/docs/EGG-SPECIFICATION.md`
- Offline Sync Protocol: `docs/coordination/offline-sync-protocol.md` (TBD)
- RSE Telemetry: `docs/observability/RSE-0.1.md`

---

**Status:** Specification with partial implementation
**Next steps:** Implement launch log writer, sync reconciliation
**Owner:** DEIA Core Team

**Tags:** `#egg` `#offline-mode` `#resilience` `#specification` `#launch-protocol`
