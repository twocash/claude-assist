# Skills Master Plan

**Sprint:** skill-builder-and-suite-v1
**Purpose:** Build comprehensive skill suite for agent coordination testbed
**Approach:** Meta-first - build skill-builder, then use it to create all others

---

## Phase 0: Foundation (Meta-Tooling)

### Skill 0: skill-builder ⭐ BUILD FIRST
**Purpose:** Interactive wizard for creating new skills
**Features:**
- Interactive Q&A to gather skill details
- Auto-generate from template
- Validate skill format
- Save to appropriate category directory
- Generate test scenarios

**Why First:** Accelerates all subsequent skill creation

---

## Phase 1: Coordination Skills (Infrastructure)

### Skill 1: health-check
**Purpose:** Validate infrastructure and agent status
**Features:**
- Check directory structure exists
- Parse YAML frontmatter from status entries
- Detect stale agents (>30 min heartbeat)
- Count unsynced COMPLETE entries
- Generate health report

### Skill 2: agent-dispatch
**Purpose:** Launch test agents with activation prompts
**Features:**
- Select agent role from .agent/roles/
- Generate activation prompt
- Display launch instructions
- Track dispatched agents

### Skill 3: status-inspector
**Purpose:** Parse and analyze status log entries
**Features:**
- List all current status entries
- Parse YAML frontmatter
- Show timeline view
- Filter by agent/sprint/status
- Highlight anomalies

### Skill 4: heartbeat-monitor
**Purpose:** Track agent heartbeats in real-time
**Features:**
- Monitor heartbeat timestamps
- Alert on staleness (>30 min)
- Show last heartbeat time
- Auto-refresh view

---

## Phase 2: Testing Skills (Quality Assurance)

### Skill 5: mock-sprint
**Purpose:** Generate fake sprint artifacts for testing
**Features:**
- Create sprint directory in sandbox/test-sprints/
- Generate SPEC.md with mock ACs
- Generate USER_STORIES.md
- Generate EXECUTION_PROMPT.md
- Populate with realistic test data

### Skill 6: protocol-validator
**Purpose:** Verify status entries follow format correctly
**Features:**
- Parse YAML frontmatter
- Validate required fields
- Check timestamp format (ISO 8601)
- Verify status values (STARTED|IN_PROGRESS|COMPLETE|BLOCKED)
- Report violations

### Skill 7: workflow-simulator
**Purpose:** Simulate multi-agent workflows
**Features:**
- Define workflow scenarios (e.g., Developer→QA)
- Execute simulated agents
- Generate status entries
- Verify handoffs
- Report on workflow health

### Skill 8: log-analyzer
**Purpose:** Parse status logs and generate reports
**Features:**
- Aggregate statistics (avg completion time, etc.)
- Identify bottlenecks
- Graph timeline
- Export reports

---

## Phase 3: Utility Skills (General Tools)

### Skill 9: python-env
**Purpose:** Check Python environment health
**Features:**
- Show Python version
- List installed packages
- Check for missing dependencies
- Validate virtual environment
- Suggest package installations

### Skill 10: sandbox-clean
**Purpose:** Clean up test files and reset sandbox
**Features:**
- Clear sandbox/temp/*
- Clear sandbox/work/*
- Archive or delete status/current/*.md
- Reset to clean state
- Preserve important artifacts

### Skill 11: git-snapshot
**Purpose:** Show git context quickly
**Features:**
- Current branch
- Recent commits (last 5)
- Uncommitted changes
- Untracked files
- Quick status overview

### Skill 12: directory-map
**Purpose:** Show repo structure with explanations
**Features:**
- Display directory tree
- Annotate each directory with purpose
- Highlight key files
- Show gitignored areas
- Quick navigation guide

---

## Phase 4: Meta Skills (Skill Management)

### Skill 13: skill-builder (already built in Phase 0)
See Phase 0

### Skill 14: skill-test
**Purpose:** Test a skill against mock scenarios
**Features:**
- Load skill definition
- Define test scenarios
- Simulate skill execution
- Verify outputs
- Report test results

### Skill 15: skill-deploy
**Purpose:** Deploy proven skills to production
**Features:**
- Validate skill is ready
- Copy to ~/.claude/skills/
- Update skill registry
- Generate deployment notes
- Verify installation

---

## Implementation Strategy

### Sprint Plan

**Iteration 1:** Build skill-builder (Skill 0)
- Create interactive wizard
- Test with mock skill
- Validate output format

**Iteration 2:** Build coordination skills (Skills 1-4)
- Use skill-builder for each
- Test infrastructure validation
- Verify agent monitoring

**Iteration 3:** Build testing skills (Skills 5-8)
- Use skill-builder for each
- Create mock sprint artifacts
- Validate testing workflows

**Iteration 4:** Build utility skills (Skills 9-12)
- Use skill-builder for each
- Test environment checking
- Verify cleanup operations

**Iteration 5:** Build meta skills (Skills 14-15)
- Use skill-builder for each
- Test skill testing (!meta)
- Deploy to production

---

## Success Criteria

- [ ] All 15 skills created
- [ ] Each skill has test scenarios
- [ ] All skills documented
- [ ] skill-builder accelerates creation
- [ ] Skills are production-ready
- [ ] Deployment guide created

---

## Timeline Estimate

- **Phase 0 (Skill Builder):** 1 session
- **Phase 1 (Coordination):** 1-2 sessions
- **Phase 2 (Testing):** 1-2 sessions
- **Phase 3 (Utilities):** 1 session
- **Phase 4 (Meta):** 1 session

**Total:** ~5-7 sessions to complete full suite

---

*Skills Master Plan v1.0 - Let's build the builder!*
