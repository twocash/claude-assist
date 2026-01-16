# Test Agent

**Identity:** Simulated agent for testing coordination protocols
**Mode:** Execute
**Trigger:** Manual invocation for testing

---

## Responsibilities

- Write status entries following ENTRY_TEMPLATE.md
- Update heartbeat every 5 minutes
- Transition through status states properly
- Test coordination protocols

---

## Status Transitions

```
STARTED → IN_PROGRESS → COMPLETE
            ↓
         BLOCKED → IN_PROGRESS → COMPLETE
```

---

## Testing Scenarios

1. **Happy Path**
   - STARTED → IN_PROGRESS (with heartbeats) → COMPLETE

2. **Blocked Path**
   - STARTED → IN_PROGRESS → BLOCKED → IN_PROGRESS → COMPLETE

3. **Stale Agent**
   - STARTED → IN_PROGRESS (no heartbeat updates for >30 min)

4. **Crash Simulation**
   - STARTED → IN_PROGRESS → (exit without COMPLETE)

---

## Status Entry Format

Follow `.agent/status/ENTRY_TEMPLATE.md` exactly.

Key fields:
- `timestamp`: ISO 8601 format
- `heartbeat`: Updated in-place every 5 min
- `status`: One of STARTED | IN_PROGRESS | COMPLETE | BLOCKED
- `severity`: INFO | WARN | URGENT | BLOCKER

---

*Test Agent v1.0*
