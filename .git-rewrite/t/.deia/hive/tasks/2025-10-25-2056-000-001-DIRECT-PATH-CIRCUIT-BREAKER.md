# DIRECT PATH: BOT-001 - Circuit Breaker Implementation

**From:** Q33N (BEE-000 Meta-Governance)
**To:** BOT-001 (Bot Infrastructure)
**Date:** 2025-10-25 20:56 CDT
**Priority:** P0 - IMMEDIATE IMPLEMENTATION
**Task:** Hardening Task 1 - Circuit Breaker Pattern

---

## Your Code Locations (Absolute Paths)

### Primary Files to Modify/Create

**1. Circuit Breaker Service (NEW FILE)**
```
C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\src\deia\services\circuit_breaker.py
```

Create this file with:
- `CircuitBreaker` class
- States: Closed, Open, Half-Open
- Methods: `can_execute()`, `record_success()`, `record_failure()`, `state_transition()`
- Configuration: failure_threshold, recovery_timeout, success_threshold

**2. Bot Launcher Integration (MODIFY)**
```
C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\run_single_bot.py
```

Integrate circuit breaker into bot process lifecycle:
- Import: `from src.deia.services.circuit_breaker import CircuitBreaker`
- Create instance in bot launcher
- Check `circuit_breaker.can_execute()` before allowing tasks
- Call `record_success()` / `record_failure()` based on task outcome
- Log state transitions

**3. Bot Service (MODIFY)**
```
C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\src\deia\services\bot_service.py
```

Add circuit breaker health status to bot service:
- `GET /api/bot/{bot_id}/circuit-status` endpoint (returns: state, failure_count, last_transition)
- Include circuit state in existing `/api/bot/{bot_id}/status` response

**4. Logging (NEW FILE or APPEND)**
```
C:\Users\davee\OneDrive\Documents\GitHub\deiasolutions\.deia\bot-logs\circuit-breaker.jsonl
```

Log format (append mode):
```json
{"timestamp": "2025-10-25T20:56:00Z", "bot_id": "BOT-001", "event": "state_transition", "from": "Closed", "to": "Open", "reason": "failure_threshold_exceeded"}
{"timestamp": "2025-10-25T21:00:00Z", "bot_id": "BOT-001", "event": "task_blocked", "state": "Open", "message": "Circuit breaker open, rejecting request"}
```

---

## Implementation Checklist

- [ ] Create `src/deia/services/circuit_breaker.py` with full state machine
- [ ] Add circuit breaker to `run_single_bot.py` initialization
- [ ] Integrate into bot subprocess launch/execution flow
- [ ] Add endpoint to `bot_service.py` for circuit status
- [ ] Create logging to `.deia/bot-logs/circuit-breaker.jsonl`
- [ ] Write unit tests (70%+ coverage)
- [ ] Test with actual bot (launch, send tasks, trigger failure, verify circuit opens)
- [ ] Verify logging working
- [ ] No mock functions (real implementation only)

---

## Code Example Structure

**circuit_breaker.py should have:**

```python
from enum import Enum
from datetime import datetime, timedelta
import json

class CircuitState(Enum):
    CLOSED = "Closed"
    OPEN = "Open"
    HALF_OPEN = "Half-Open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30, success_threshold=2):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout  # seconds
        self.success_threshold = success_threshold
        self.last_failure_time = None
        self.last_state_change = datetime.now()

    def can_execute(self):
        """Check if request can proceed through circuit"""
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if datetime.now() - self.last_state_change > timedelta(seconds=self.recovery_timeout):
                self.transition_to(CircuitState.HALF_OPEN)
                return True
            return False
        elif self.state == CircuitState.HALF_OPEN:
            return True
        return False

    def record_success(self):
        """Call after successful task execution"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.transition_to(CircuitState.CLOSED)
        self.failure_count = 0

    def record_failure(self):
        """Call after failed task execution"""
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.transition_to(CircuitState.OPEN)

    def transition_to(self, new_state):
        """Transition state and log event"""
        old_state = self.state
        self.state = new_state
        self.last_state_change = datetime.now()
        self.log_transition(old_state, new_state)

    def log_transition(self, from_state, to_state):
        """Log state change to JSONL"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event": "state_transition",
            "from": from_state.value,
            "to": to_state.value
        }
        # Append to .deia/bot-logs/circuit-breaker.jsonl
```

---

## Success Criteria

✅ **Implementation:**
- Circuit breaker prevents cascading failures
- State transitions logged properly
- Failure/success rates tracked
- 70%+ test coverage
- Production code (no mocks)

✅ **Testing:**
- Launch 2 bots
- Send 10 successful tasks → Circuit stays CLOSED
- Send 5 failing tasks → Circuit transitions to OPEN
- New tasks rejected → Circuit blocks
- Wait 30s → Circuit transitions to HALF-OPEN
- Send 2 successful tasks → Circuit closes

✅ **Deliverable:**
- Update `bot-001-hardening-status.md` when complete
- Show test evidence (logs, metrics, state transitions)
- Confirm no blockers, 100% ready for Task 2

---

## Time Estimate

- Implementation: 45 min
- Testing: 30 min
- Debugging: 15 min
- **Total: 1.5 hours**

---

## Your Deadline

**Start:** 20:56 CDT
**Due:** ~22:26 CDT (1.5 hours + buffer)

When done, Task 2 (Metrics Collection) is queued and ready to start immediately.

---

**Q33N out. Direct path provided. Code locations marked. Go build.**

**The circuit breaker is foundational - everything after depends on this working.**
