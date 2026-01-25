
# Grove Foundation Loop — Sprint Methodology

## Overview

The Foundation Loop is Grove's structured approach to Terminal development that ensures:
- Clear requirements before coding
- Architectural decisions documented
- Migration paths planned
- Tests written for critical paths
- Human-readable health checks

## When to Use

Use the Foundation Loop for:
- Any refactoring work
- New feature development
- Infrastructure changes
- Bug fixes that touch multiple files
- Any work that would benefit from planning
**Skip** for trivial changes (typo fixes, config tweaks).

## The 8 Artifacts

Every sprint produces these artifacts in `docs/sprints/{sprint-name}/`:

<table header-row="true">
	<tr>
		<td>Artifact</td>
		<td>Purpose</td>
		<td>When Created</td>
	</tr>
	<tr>
		<td>`REPO_AUDIT.md`</td>
		<td>Current state analysis</td>
		<td>First</td>
	</tr>
	<tr>
		<td>`SPEC.md`</td>
		<td>Goals, non-goals, acceptance criteria</td>
		<td>After audit</td>
	</tr>
	<tr>
		<td>`ARCHITECTURE.md`</td>
		<td>Target state, data flows, schemas</td>
		<td>After architecture</td>
	</tr>
	<tr>
		<td>`MIGRATION_MAP.md`</td>
		<td>File-by-file change plan</td>
		<td>After architecture</td>
	</tr>
	<tr>
		<td>`DECISIONS.md`</td>
		<td>ADRs explaining "why"</td>
		<td>During planning</td>
	</tr>
	<tr>
		<td>`SPRINTS.md`</td>
		<td>Epic/story breakdown with commits</td>
		<td>After decisions</td>
	</tr>
	<tr>
		<td>`EXECUTION_PROMPT.md`</td>
		<td>Self-contained handoff for Claude Code</td>
		<td>Last planning artifact</td>
	</tr>
	<tr>
		<td>`DEVLOG.md`</td>
		<td>Execution tracking, issues encountered</td>
		<td>During execution</td>
	</tr>
</table>

## Sprint Phases

### Phase 0: Sprint Setup

```plain text
1. Create sprint folder: docs/sprints/{sprint-name}/
2. Name format: {feature}-v{version} (e.g., automated-testing-v1)
```

### Phase 1: Repository Audit

```plain text
Analyze current state:
- What files exist?
- What's the current architecture?
- What patterns are established?
- What technical debt exists?

Output: REPO_AUDIT.md
```

### Phase 2: Specification

```plain text
Define scope:
- Goals (what we're doing)
- Non-goals (what we're NOT doing)
- Acceptance criteria (how we know we're done)

Output: SPEC.md
```

### Phase 3: Architecture

```plain text
Design target state:
- Data structures
- File organization
- API contracts
- Component relationships

Output: ARCHITECTURE.md
```

### Phase 4: Migration Planning

```plain text
Plan the path:
- Files to create
- Files to modify (with line numbers)
- Files to delete
- Execution order
- Rollback plan

Output: MIGRATION_MAP.md
```

### Phase 5: Decisions

```plain text
Document choices:
- ADR format (Status, Context, Decision, Rationale, Consequences)
- One ADR per significant decision
- Include rejected alternatives

Output: DECISIONS.md
```

### Phase 6: Story Breakdown

```plain text
Create executable plan:
- Epics (major themes)
- Stories (individual tasks)
- Commit sequence
- Build gates (verify after each phase)

Output: SPRINTS.md
```

### Phase 7: Execution Prompt

```plain text
Create self-contained handoff:
- Context summary
- Repository intelligence (key file locations)
- Step-by-step execution order
- Code samples where helpful
- Build verification commands
- Forbidden actions

Output: EXECUTION_PROMPT.md
```

### Phase 8: Testing (REQUIRED)

```plain text
Every sprint MUST include:
- Tests for new/modified functionality
- Health check verification
- Update to test counts if applicable

Test requirements by change type:

| Change Type | Required Tests |
|-------------|----------------|
| Schema change | Schema validation tests |
| API change | API contract tests |
| UI change | E2E smoke test |
| Logic change | Unit tests |
| New feature | All applicable above |
Acceptance criteria MUST include:
- "Tests pass: npm test"
- "Health check passes: npm run health"
- Specific test assertions for the feature

Output: Test files in tests/, updated SPRINTS.md with test stories
```

### Phase 9: Execution

```plain text
Hand off EXECUTION_PROMPT.md to Claude Code
Track progress in DEVLOG.md
Run build gates after each phase
Verify smoke tests before marking complete
```

## Quick Commands

Jim may say:
- "Start a sprint for X" → Create sprint folder, begin REPO_AUDIT
- "Continue the sprint" → Resume from last DEVLOG entry
- "Sprint status" → Show current phase and blockers
- "Show execution prompt" → Present EXECUTION_PROMPT.md
- "Handoff to Claude Code" → Confirm EXECUTION_PROMPT is ready

## Sprint Naming Convention

```plain text
{domain}-{feature}-v{version}

Examples:
- knowledge-architecture-v1
- automated-testing-v1
- terminal-ux-v2
- rag-orchestration-v1
```

## Commit Message Format

```plain text
{type}: {description}

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code restructuring
- test: Adding tests
- docs: Documentation
- chore: Maintenance
- ci: CI/CD changes

Examples:
- feat: add health check CLI
- test: add schema validation tests
- refactor: extract hubs to knowledge/hubs.json
```

## Build Gates

After each epic, verify:

```bash
npm run build    # TypeScript compiles
npm test         # Unit tests pass
npm run health   # Health check passes
```

Before deploy:

```bash
npm run test:all  # All tests including E2E
npm run health    # Final health check
```

## Health Check Integration

The health check (`npm run health`) is a first-class tool that:
- Validates schema integrity
- Checks API contracts
- Verifies journey navigation
- Reports failures with IMPACT and INSPECT guidance
Every sprint's smoke test checklist MUST include:
- [ ] `npm run health` passes
- [ ] Health report shows no regressions

## Test Requirements

### Minimum Test Coverage by Sprint Type

<table header-row="true">
	<tr>
		<td>Sprint Type</td>
		<td>Required Tests</td>
	</tr>
	<tr>
		<td>Schema/Data changes</td>
		<td>Schema validation, cross-reference tests</td>
	</tr>
	<tr>
		<td>API changes</td>
		<td>Contract tests for affected endpoints</td>
	</tr>
	<tr>
		<td>Frontend changes</td>
		<td>E2E smoke tests</td>
	</tr>
	<tr>
		<td>Logic changes</td>
		<td>Unit tests for new/modified functions</td>
	</tr>
	<tr>
		<td>Refactoring</td>
		<td>Existing tests still pass, no regressions</td>
	</tr>
</table>

### Test File Locations

```plain text
tests/
├── unit/           # Pure logic, no I/O
├── integration/    # API calls, data flows
├── e2e/            # Browser tests
├── fixtures/       # Test data
└── utils/          # Test helpers
```

### Adding Tests Checklist

When adding tests to a sprint:
1. [ ] Identify what can break
1. [ ] Write test that would catch it
1. [ ] Include in SPRINTS.md as story
1. [ ] Include in EXECUTION_PROMPT.md
1. [ ] Verify test passes before marking epic complete

## Artifact Templates

### REPO_AUDIT.md Template

```markdown
# Repository Audit — {Sprint Name}

## Audit Date: {date}

## Current State Summary
{What exists today}

## File Structure Analysis
{Key files and their purposes}

## Technical Debt
{What needs fixing}

## Recommendations
{What to do about it}
```

### SPEC.md Template

```markdown
# Specification — {Sprint Name}

## Overview
{One paragraph summary}

## Goals
1. {Goal 1}
2. {Goal 2}

## Non-Goals
- {What we're NOT doing}

## Acceptance Criteria
- [ ] AC-1: {Specific, testable criterion}
- [ ] AC-2: {Include test requirements}
```

### DECISIONS.md Template (per ADR)

```markdown
## ADR-{N}: {Title}

### Status
{Proposed|Accepted|Deprecated}

### Context
{Why we need to make this decision}

### Decision
{What we decided}

### Rationale
{Why this option over alternatives}

### Consequences
{What follows from this decision}
```

## Example Sprint Structure
