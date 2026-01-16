# Test: agent-dispatch

## Scenario 1: Dispatching Developer for Sprint

**Input:**
```
User: dispatch agent
[Selects: developer]
[Sprint: skill-builder-v1]
[Branch: main]
```

**Expected Behavior:**
- Lists all available roles from .agent/roles/
- Asks for sprint name
- Asks for branch (with default)
- Reads developer role definition
- Generates complete activation prompt
- Displays launch instructions
- Offers dispatch tracking

**Verification:**
- [ ] All roles from .agent/roles/ are listed
- [ ] Generated prompt includes sprint name
- [ ] Generated prompt includes branch
- [ ] Activation prompt is complete and copy-paste ready
- [ ] Launch instructions are clear
- [ ] Reference paths are correct
- [ ] Dispatch tracking creates status entry (if accepted)

---

## Scenario 2: Dispatching Test Agent

**Input:**
```
User: launch agent
[Selects: test-agent]
[Test scenario: protocol-validation]
```

**Expected Behavior:**
- Lists available roles
- Asks for test scenario
- Generates test-agent specific prompt
- Displays launch instructions

**Verification:**
- [ ] Test scenario included in activation prompt
- [ ] Prompt references test-agent.md
- [ ] Status template path provided
- [ ] Launch instructions shown

---

## Scenario 3: Quick Dispatch (No Tracking)

**Input:**
```
User: spawn agent
[Selects: chief-of-staff]
[Tracking: no]
```

**Expected Behavior:**
- Generates activation prompt
- Shows launch instructions
- Does NOT create dispatch log entry

**Verification:**
- [ ] Activation prompt generated correctly
- [ ] No status entry created in .agent/status/current/

---

## Scenario 4: Multiple Dispatch Tracking

**Input:**
```
User: dispatch agent
[First: developer, Sprint: A, Track: yes]
[Second: qa-reviewer, Sprint: A, Track: yes]
```

**Expected Behavior:**
- Both dispatches logged separately
- Status entries have sequential numbers
- Both tracked in .agent/status/current/

**Verification:**
- [ ] Two separate activation prompts generated
- [ ] Two status entries created
- [ ] Entry numbers are sequential
- [ ] Both entries have status=DISPATCHED

---

*Test template for agent-dispatch v1.0*
