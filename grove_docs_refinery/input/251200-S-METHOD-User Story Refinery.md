---
name: user-story-refinery
description: Extract user stories with acceptance criteria from requirements specifications. Transforms product specs into testable stories with INVEST assessment, Gherkin acceptance criteria, and critical flow analysis. Use when refining requirements, preparing for sprint planning, or generating test scaffolding. Triggers on phrases like "extract user stories", "refine requirements", "story extraction", "acceptance criteria", "prepare for testing", or when turning a specification into actionable development work.
version: 1.0
---

# User Story Refinery v1

A structured methodology for transforming requirements specifications into testable user stories with acceptance criteria. Produces review-ready story documents, flags clunky flows, proposes simplifications, and prepares for downstream test generation.

**Four-Phase Pipeline:**
1. **Story Extraction** — Parse spec into INVEST-assessed user stories
2. **Acceptance Criteria** — Gherkin scenarios for each story
3. **Test Case Generation** — Derive test cases from criteria (Phase 3)
4. **Playwright Scaffolding** — Generate test file structure (Phase 4)

This skill covers Phases 1-2. Phases 3-4 are downstream execution.

---

## When to Use This Skill

| Trigger | Description |
|---------|-------------|
| "Extract user stories from [spec]" | Primary trigger |
| "Refine requirements for [feature]" | Requirements → stories |
| "Prepare [sprint] for development" | Pre-sprint refinement |
| "Create acceptance criteria for [feature]" | Direct criteria generation |
| "Review the spec and flag issues" | Critical analysis mode |

---

## Input Requirements

### Required
- **Requirements Specification** — Markdown, Word doc, or Notion page containing:
  - Feature description
  - User flows (numbered steps)
  - Screen/component inventory
  - Dependencies
  - Out of scope items

### Optional
- **Parent Notion page** — For creating story review document
- **DEX alignment requirements** — For compliance verification
- **Existing user role definitions** — Explorer, Cultivator, Observer, etc.

---

## Output Deliverable

A **User Stories & Acceptance Criteria Review** document containing:

1. **Critical Observations** — Issues flagged before diving into stories
2. **Proposed Simplifications** — v1.0 scope recommendations
3. **User Stories by Epic** — Grouped, INVEST-assessed stories
4. **Gherkin Acceptance Criteria** — Testable scenarios per story
5. **Deferred Items** — Stories/features pushed to future versions
6. **Open Questions** — Decisions needed from stakeholders
7. **DEX Alignment Verification** — How stories support architecture principles

---

## Phase 1: Story Extraction

### Step 1.1: Read the Spec Critically

Before extracting stories, analyze the spec for:

| Check | Question | Action if Yes |
|-------|----------|---------------|
| **Over-engineering** | Does the spec add features beyond core need? | Flag for deferral |
| **Undefined concepts** | Are there references to undefined objects/states? | Flag as blocker |
| **Clunky flows** | Does any flow feel awkward or multi-step when simpler exists? | Propose simplification |
| **Premature optimization** | Stats, dashboards, analytics before core flow? | Defer to v1.1 |
| **Leaky abstractions** | Implementation details in UX? (e.g., "agent spawns") | Abstract for user |
| **Missing dependencies** | Does flow assume something that doesn't exist? | Document dependency |

### Step 1.2: Identify Epics

Group related functionality into epics. Typical patterns:

- **Foundation Epic** — Core UI components, navigation, layout
- **Data Display Epic** — Lists, cards, status indicators
- **Action Epic** — User-initiated operations (create, promote, archive)
- **Notification Epic** — Alerts, badges, toasts
- **Quick Actions Epic** — Shortcuts, keyboard nav, power user features

### Step 1.3: Extract Stories per Epic

For each user flow in the spec, create a story:

```markdown
### US-{Sprint}{Number}: {Title}

**As a** {role}
**I want to** {action}
**So that** {benefit}

**INVEST Assessment:**
- **I**ndependent: {Yes/No — can be developed standalone?}
- **N**egotiable: {Yes/No — implementation details flexible?}
- **V**aluable: {Yes/No — delivers user value?}
- **E**stimable: {Yes/No — can estimate effort?}
- **S**mall: {Yes/No — fits in sprint?}
- **T**estable: {Yes/No — has clear pass/fail criteria?}

**Traceability:** Spec section "{section name}"
```

### Step 1.4: Assign Story IDs

Convention: `US-{Sprint Letter}{Three-digit number}`

| Sprint | ID Range | Example |
|--------|----------|---------|
| Sprint A | US-A001 - US-A999 | US-A003 |
| Sprint B | US-B001 - US-B999 | US-B007 |
| Sprint C | US-C001 - US-C999 | US-C002 |

---

## Phase 2: Acceptance Criteria

### Step 2.1: Gherkin Format

Every story gets acceptance criteria in Gherkin format:

```gherkin
Scenario: {Descriptive name}
  Given {precondition}
  And {additional precondition if needed}
  When {action taken}
  Then {expected outcome}
  And {additional outcome if needed}
```

### Step 2.2: Scenario Coverage

Each story should have scenarios for:

| Scenario Type | Description | Example |
|---------------|-------------|---------|
| **Happy path** | Primary success flow | "User completes checkout" |
| **Edge cases** | Boundary conditions | "Cart with 100 items" |
| **Empty state** | No data present | "No orders to display" |
| **Error state** | Graceful failure | "Network timeout" |
| **Accessibility** | Screen reader, keyboard | "aria-label announced" |

### Step 2.3: Table-Driven Scenarios

For scenarios with multiple similar cases, use data tables:

```gherkin
Scenario: Status badge displays correct styling
  Given I have sprouts with various statuses
  When I view the sprout cards
  Then each card should display the correct badge:
    | Status | Badge Text | Color |
    | planted | Queued | gray |
    | germinating | In Progress | blue |
    | ready | Ready | green |
    | failed | Failed | red |
```

---

## Critical Analysis Framework

### Clunky Flow Indicators

Flag flows that exhibit:

| Indicator | Example | Question to Ask |
|-----------|---------|-----------------|
| **Multi-modal** | Dialog → drawer → dialog | Can this be one interaction? |
| **Confirmation cascades** | Confirm → re-confirm → triple confirm | Is this justified by risk? |
| **Hidden actions** | "Click gear, then advanced, then..." | Should this be surfaced? |
| **Undefined terms** | "Select the tier" (tiers not defined) | What are the actual options? |
| **Future dependencies** | "When USER objects exist..." | Should we defer this feature? |

### Simplification Proposal Format

```markdown
## Proposed v1.0 Simplifications

| Spec Feature | v1.0 Approach | Rationale |
|--------------|---------------|-----------|
| {Feature} | Defer | {Why not needed for v1.0} |
| {Feature} | Simplify to X | {What's the minimal viable version} |
| {Feature} | Keep as-is | {Why it's correctly scoped} |
```

---

## DEX Alignment Verification

Every story set should be checked against DEX pillars:

| Pillar | Verification Question | Pass/Fail |
|--------|----------------------|-----------|
| **Declarative Sovereignty** | Can behavior be changed via config, not code? | |
| **Capability Agnosticism** | Does it work regardless of which model/agent executes? | |
| **Provenance as Infrastructure** | Is origin/authorship tracked for all data? | |
| **Organic Scalability** | Does structure support growth without redesign? | |

### Alignment Summary Template

```markdown
## DEX Alignment Verification

| Pillar | How Stories Support |
|--------|---------------------|
| Declarative Sovereignty | {explanation} |
| Capability Agnosticism | {explanation} |
| Provenance as Infrastructure | {explanation} |
| Organic Scalability | {explanation} |
```

---

## Output Template

```markdown
# User Stories & Acceptance Criteria v1.0 Review

**Sprint:** {Letter} - {Name}
**Codename:** {codename}
**Phase:** Story Extraction + Acceptance Criteria
**Status:** Draft for Review

---

## Critical Observations

{List issues found during spec analysis}

### 1. {Issue Title}

{Description of the issue}

**Recommendation:** {What to do about it}

---

## Proposed v1.0 Simplifications

| Spec Feature | v1.0 Approach | Rationale |
|--------------|---------------|-----------|
| ... | ... | ... |

---

## Epic 1: {Name}

### US-{X}001: {Title}

**As a** {role}
**I want to** {action}
**So that** {benefit}

**INVEST Assessment:**
- **I**ndependent: Yes/No
- **N**egotiable: Yes/No
- **V**aluable: Yes/No
- **E**stimable: Yes/No
- **S**mall: Yes/No
- **T**estable: Yes/No

**Acceptance Criteria:**

\```gherkin
Scenario: {Name}
  Given {precondition}
  When {action}
  Then {outcome}
\```

**Traceability:** Spec section "{section}"

---

{Repeat for each story}

---

## Deferred to v1.1

### US-{X}0XX: {Title} (DEFERRED)

**Reason:** {Why deferred}

**Original Flow:** {What the spec described}

**v1.1 Prerequisite:** {What needs to exist first}

---

## Open Questions

1. **{Question}** — {Context}

---

## Summary

| Story ID | Title | Priority | Complexity |
|----------|-------|----------|------------|
| US-X001 | ... | P0/P1/P2 | S/M/L |

**Total v1.0 Stories:** {N}
**Deferred:** {N}

---

## DEX Alignment Verification

| Pillar | How Stories Support |
|--------|---------------------|
| Declarative Sovereignty | ... |
| Capability Agnosticism | ... |
| Provenance as Infrastructure | ... |
| Organic Scalability | ... |
```

---

## Integration with Notion

When outputting to Notion:

1. **Create child page** under the sprint's Feature Roadmap entry
2. **Use title:** "User Stories & Acceptance Criteria v1.0 Review"
3. **Include all sections** from the output template
4. **Link back** to the parent spec page

---

## Downstream: Phases 3-4 (Future Skill)

Once stories are approved, the pipeline continues:

### Phase 3: Test Case Generation
- Derive test cases from Gherkin scenarios
- Map scenarios to test file structure
- Identify shared fixtures and utilities

### Phase 4: Playwright Scaffolding
- Generate `.spec.ts` file skeletons
- Create page object models
- Establish baseline snapshot structure

These phases will be a separate `test-scaffolding` skill.

---

## Quick Reference

### Story ID Format
`US-{Sprint}{000}` — e.g., US-A001, US-B007, US-C003

### Priority Levels
- **P0:** Must have for MVP
- **P1:** Important, not blocking
- **P2:** Nice to have

### Complexity
- **S:** < 1 day
- **M:** 1-3 days
- **L:** > 3 days (consider splitting)

### Gherkin Keywords
- `Given` — Precondition
- `When` — Action
- `Then` — Outcome
- `And` — Additional (any of above)
- `But` — Negative condition

---

## Principles

1. **Question upstream work** — Specs aren't sacred; flag clunky flows
2. **Keep v1.0 minimal** — Defer aggressively, ship faster
3. **Test everything** — If it can't be tested, rewrite the criteria
4. **Trace everything** — Every story links back to spec section
5. **INVEST always** — Stories that fail INVEST need rework
6. **DEX compliance** — Stories must support architecture principles
