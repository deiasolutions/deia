# INTAKE REQUIREMENT: Bee-to-Bee Service Architecture Evolution

**Submitted By:** BOT-001 (Infrastructure Lead)
**Date:** 2025-10-25
**Priority:** P1 - Architectural Foundation
**Type:** Architecture Requirement (Future Roadmap)
**Delivery Timeline:** Tonight (strategic planning)
**Scope:** Multi-phase evolution (Phases A-D)

---

## Executive Summary

Current DEIA hive operates on **file-drop protocol** (async, persistent, Q33N-mediated). This is durable and governance-friendly but creates latency for operational coordination.

**Requirement:** Define architecture evolution path toward **bee-to-bee service calls** (real-time, direct agent-to-agent) while maintaining file-based audit trail for governance.

**Vision:** Hybrid operation - files for records, services for coordination.

---

## Current State (Phase 0 - Present)

### File-Drop Protocol
```
Q33N (BEE-000)
  ↓ DROP task
.deia/hive/tasks/[task].md
  ↑ READ
BOT-001 / BOT-002 / BOT-003
  ↓ EXECUTE
.deia/hive/responses/bot-001-[status].md
  ↑ READ
Q33N (BEE-000)
```

**Characteristics:**
- ✅ Durable (files persist)
- ✅ Auditable (all decisions logged)
- ✅ Governance-controlled (Q33N sees all)
- ❌ Latency (polling/batch)
- ❌ No real-time coordination
- ❌ No agent-to-agent queries

---

## Proposed Architecture Evolution

### Phase A: Service Discovery (Q1 2025)

**Goal:** Enable agents to discover service endpoints

**Implementation:**
- Service registry: `.deia/services/SERVICE-REGISTRY.jsonl`
- Each agent registers on startup: `{bot_id, service_url, capabilities, timestamp}`
- Service health checks: `/health` endpoint mandatory
- TTL-based registration cleanup (5 min default)

**Example:**
```json
{
  "bot_id": "BOT-001",
  "service_url": "http://localhost:8001",
  "capabilities": ["orchestration", "messaging", "scheduling"],
  "registered_at": "2025-10-25T14:30:00",
  "ttl_seconds": 300
}
```

**Files Affected:**
- Create: `src/deia/services/service_registry.py`
- Create: `tests/unit/test_service_registry.py`

---

### Phase B: Agent Query Protocol (Q1 2025)

**Goal:** Enable direct queries between agents

**Implementation:**
- Standard query endpoints: `GET /api/agent/status`, `GET /api/agent/capabilities`
- Query timeout: 5 seconds (fallback to file-drop)
- Query logging: `.deia/bot-logs/agent-queries.jsonl`
- Graceful degradation: If service unavailable, use file-drop

**Example Query:**
```bash
# Bot-002 queries Bot-001 status
curl -X GET http://bot-001:8001/api/agent/status \
  --max-time 5 --fail-fast

# Response:
{
  "bot_id": "bot-001",
  "status": "working",
  "current_task": "feature-3-testing",
  "capacity_remaining": 2,
  "last_heartbeat": "2025-10-25T14:31:00"
}
```

**Endpoints Required:**
- `GET /api/agent/status` - Current status
- `GET /api/agent/capabilities` - What this bot can do
- `GET /api/agent/capacity` - Available capacity
- `GET /api/agent/tasks/history` - Recent work

**Files Affected:**
- Create: `src/deia/services/agent_query_service.py`
- Modify: All bot services to add query endpoints
- Create: `tests/integration/test_agent_queries.py`

---

### Phase C: Inter-Agent Coordination (Q2 2025)

**Goal:** Enable agents to coordinate without Q33N intermediary

**Implementation:**
- Agent-to-agent requests: `POST /api/agent/request/{action}`
- Request/response pattern with timeout
- All requests logged for audit trail
- Q33N can still monitor via logs
- Fallback: Q33N can override/veto

**Example:**
```bash
# Bot-002 requests Bot-001 to analyze something
curl -X POST http://bot-001:8001/api/agent/request/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "req-123",
    "from_bot": "bot-002",
    "action": "analyze",
    "data": {...},
    "deadline": "2025-10-25T14:45:00"
  }'

# Response:
{
  "request_id": "req-123",
  "status": "queued",
  "position": 2,
  "estimated_completion": "2025-10-25T14:42:00"
}

# Later poll for result:
curl http://bot-001:8001/api/agent/request/req-123
# Returns result when ready
```

**Files Affected:**
- Create: `src/deia/services/agent_request_queue.py`
- Create: `src/deia/services/agent_response_service.py`
- Modify: Task orchestrator to use agent requests
- Create: `tests/integration/test_agent_coordination.py`

---

### Phase D: Distributed Scheduling (Q2 2025)

**Goal:** Agents self-coordinate on task distribution

**Implementation:**
- Agents poll service discovery registry
- Agents query peer capacity
- Agents make local routing decisions
- Q33N monitors but doesn't orchestrate every task
- File-drop still used for official assignments

**Hybrid Operation:**
```
┌─ Official Assignment (File-Drop) ─┐
Q33N → .deia/hive/tasks/[task].md
       → All agents notified
       → Agent with best match claims via service query

┌─ Operational Coordination (Services) ─┐
BOT-001 queries BOT-002 capacity
BOT-002 responds with current load
BOT-001 decides to route interim task to BOT-002
All logged to .deia/bot-logs/agent-queries.jsonl
Q33N can review but doesn't intervene

┌─ Result Reporting (File-Drop) ─┐
BOT-001 → .deia/hive/responses/bot-001-[status].md
Q33N reads, monitors, decides next phase
```

**Files Affected:**
- Create: `src/deia/services/distributed_scheduler.py`
- Modify: Self-serve task queue to support service queries
- Create: `tests/integration/test_distributed_scheduling.py`

---

## Success Criteria

### Phase A (Service Discovery)
- ✅ Service registry functional
- ✅ All agents auto-register on startup
- ✅ TTL cleanup works
- ✅ No breaking changes to file-drop

### Phase B (Agent Queries)
- ✅ All query endpoints working
- ✅ 5-second timeout enforced
- ✅ Queries logged to agent-queries.jsonl
- ✅ Graceful fallback when services unavailable

### Phase C (Coordination)
- ✅ Request/response pattern working
- ✅ All requests auditable
- ✅ Q33N can override
- ✅ File-drop still primary for official work

### Phase D (Distributed Scheduling)
- ✅ Agents self-coordinate without Q33N
- ✅ File-drop still used for governance
- ✅ Hybrid operation seamless
- ✅ Performance improvement measured

---

## Architecture Diagram

```
Current (File-Drop):
┌──────────┐
│  Q33N    │
│ (BEE-000)│
└────┬─────┘
     │ assigns via file
     ↓
  [task].md ← all agents poll
     ↑
     │ report via file
  [response].md

Proposed (Hybrid):
┌──────────┐
│  Q33N    │ (still reviews, monitors, can veto)
│ (BEE-000)│
└────┬─────┘
     │ official assignments
     ↓
  [task].md ← high-priority work, governance
     ↑
     │ official results
  [response].md

     AND (simultaneous)

  BOT-001 ←→ BOT-002 (real-time queries, coordination)
    ↕         ↕
  BOT-003 ←→ BOT-004 (service calls, logged)

  All logged to: agent-queries.jsonl (audit trail)
```

---

## Benefits

### Immediate (Phases A-B)
- Agents know what's available without polling files
- Query response times: <100ms vs file I/O latency
- No breaking changes to existing systems

### Medium-term (Phase C)
- Agents coordinate without Q33N bottleneck
- Real-time capacity awareness
- Faster task distribution
- Q33N freed for strategic work

### Long-term (Phase D)
- Fully autonomous agent coordination
- File-drop used only for governance
- Scales to 100+ agents easily
- Q33N is observer, not orchestrator

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Service failures cause chaos | Graceful fallback to file-drop |
| Q33N loses visibility | All requests logged to agent-queries.jsonl |
| Agents coordinate badly | Q33N can veto/override via file assignments |
| Network issues | Request timeout, automatic retry via file-drop |
| Backwards compatibility | Phase in slowly, file-drop always primary |

---

## Timeline & Staffing

| Phase | Timeline | Lead | Effort |
|-------|----------|------|--------|
| A: Service Discovery | 1 week | BOT-003 | 8-12 hours |
| B: Agent Queries | 1 week | BOT-002 | 12-16 hours |
| C: Coordination | 2 weeks | BOT-001 | 20-24 hours |
| D: Distributed | 2 weeks | BOT-002 | 16-20 hours |
| **Total** | **6 weeks** | **Multi** | **56-72 hours** |

---

## Dependencies

1. **Feature 3 (Bot Communication)** - Already built, provides foundation
2. **Service Registry** - Phase A, must complete first
3. **Monitoring** - BOT-003 infrastructure suite (parallel)
4. **Protocol Changes** - May need to update governance protocols

---

## Next Steps

1. **Q33N Review:** Approve/modify architecture vision
2. **Backlog Planning:** Assign phases to agents
3. **Dependency Planning:** Coordinate with BOT-003 monitoring
4. **Protocol Updates:** Document new governance model
5. **Phase A Start:** Service discovery implementation

---

## Questions for Q33N

1. Does this align with DEIA's intended evolution?
2. Should file-drop always remain primary, or eventually shift to services?
3. What veto/override mechanisms should Q33N have in service-based coordination?
4. How should agent-queries.jsonl be monitored for anomalies?
5. Should this be documented in `.deia/protocols/`?

---

## Attachments

- Feature 3 (Bot Communication) - Already complete, foundational
- Protocol-agent-instruction-consistency.md - Governance reference
- ARCHITECTURE_FOR_DAVE.md - Current architecture context

---

**This requirement is submitted as architectural planning input for tonight's delivery.**

**BOT-001 (Infrastructure Lead)**
**For Q33N (BEE-000) Review**
