# Agent Coordination Infrastructure

**Repository:** claude-assist (testbed)
**Purpose:** Sandbox for testing and refining agent coordination system
**Production:** Deploy proven patterns to grove-foundation

---

## Directory Structure

```
.agent/
├── roles/           # Agent role definitions
├── config/          # Coordination configuration
└── status/
    ├── current/     # Active status entries (gitignored)
    ├── archive/     # Historical entries (tracked)
    └── ENTRY_TEMPLATE.md
```

---

## Sandbox Directories

```
sandbox/
├── test-sprints/    # Mock sprint artifacts for testing
├── work/            # Agent working directory (gitignored)
└── temp/            # Temporary files (gitignored)
```

---

## Status Entry Protocol

**Location:** `.agent/status/current/{NNN}-{timestamp}-{agent}.md`
**Template:** `ENTRY_TEMPLATE.md`

### Status Values
- `STARTED` - Agent begins work
- `IN_PROGRESS` - Active work with heartbeat updates
- `COMPLETE` - Work finished
- `BLOCKED` - Waiting on dependency

### Severity Levels
- `INFO` - Normal operations
- `WARN` - Potential issue
- `URGENT` - Needs attention
- `BLOCKER` - Critical failure

---

## Testing Workflow

1. Create test sprint in `sandbox/test-sprints/`
2. Launch test agent with activation prompt
3. Agent writes status entries to `.agent/status/current/`
4. Monitor coordination behavior
5. Archive successful patterns
6. Deploy to production (grove-foundation)

---

*This is a testing environment. Breaking changes are expected and welcome.*
