
# Bedrock Sprint Contract

**Version:** 1.1  
**Status:** BINDING FOR ALL BEDROCK DEVELOPMENT  
**Amended:** January 4, 2026 (Added core infrastructure provisions)  
**Effective:** December 30, 2025  
**Branch:** `bedrock`

---

## Preamble

This contract governs all development work on Grove's `bedrock` branch—the reference implementation of Trellis Architecture. It operates as a **binding overlay** to the Foundation Loop methodology. Every Bedrock sprint satisfies both:

1. The Foundation Loop requirements (Phases 0-8)
2. This Bedrock Sprint Contract (additional constraints)

**Violation blocks merge to `bedrock` branch.**

---

## Article I: Constitutional Compliance

### Section 1.1: Document Hierarchy

Every Bedrock sprint acknowledges this document hierarchy:

<table header-row="true">
	<tr>
		<td>Document</td>
		<td>Authority</td>
		<td>Must Reference</td>
	</tr>
	<tr>
		<td>`The_Trellis_Architecture__First_Order_Directives.md`</td>
		<td>Constitutional</td>
		<td>Yes, in every SPEC.md</td>
	</tr>
	<tr>
		<td>`Bedrock_Architecture_Specification.md`</td>
		<td>Architectural</td>
		<td>Yes, for pattern decisions</td>
	</tr>
	<tr>
		<td>`Trellis_Architecture_Bedrock_Addendum.md`</td>
		<td>Implementation</td>
		<td>Yes, for compliance tests</td>
	</tr>
	<tr>
		<td>`copilot-configurator-vision.md`</td>
		<td>Feature spec</td>
		<td>When implementing Copilot</td>
	</tr>
	<tr>
		<td>`grove-object.ts`</td>
		<td>Data model</td>
		<td>When creating/modifying objects</td>
	</tr>
</table>

### Section 1.2: DEX Compliance Tests

Every feature in a Bedrock sprint passes all four DEX tests. Document results in SPEC.md:

```markdown
## DEX Compliance Matrix

### Feature: [Feature Name]

| Test | Pass/Fail | Evidence |
|------|-----------|----------|
| Declarative Sovereignty | [ ] | Can non-technical Observer modify via config? How? |
| Capability Agnosticism | [ ] | What happens if model hallucinates? |
| Provenance as Infrastructure | [ ] | Can every fact trace to source? |
| Organic Scalability | [ ] | Can new types use this without code changes? |

**Blocking issues:** [List any failures that require resolution]
```

**Features failing any DEX test cannot ship.**

---

## Article II: The Canonical Console Pattern

### Section 2.1: Structure Mandate

Every Bedrock console implements this exact structure:

```
┌──────────────────────────────────────────────────────────────┐
│ Console Header (title, description, actions)                 │
├──────────────────────────────────────────────────────────────┤
│ Metrics Row (4-6 key stats, always visible)                 │
├────────────┬─────────────────────────┬──────────────────────┤
│ Navigation │ Content Area            │ Inspector + Copilot  │
│ (240px)    │ (flex)                  │ (360px)              │
└────────────┴─────────────────────────┴──────────────────────┘
```

**No exceptions.** Consoles that cannot fit this pattern escalate to architectural review before proceeding.

### Section 2.2: Required Components

Every console uses these shared components:

<table header-row="true">
	<tr>
		<td>Component</td>
		<td>Location</td>
		<td>Required For</td>
	</tr>
	<tr>
		<td>`BedrockLayout`</td>
		<td>`src/bedrock/primitives/`</td>
		<td>Console shell</td>
	</tr>
	<tr>
		<td>`BedrockNav`</td>
		<td>`src/bedrock/primitives/`</td>
		<td>Navigation column</td>
	</tr>
	<tr>
		<td>`BedrockInspector`</td>
		<td>`src/bedrock/primitives/`</td>
		<td>Inspector column</td>
	</tr>
	<tr>
		<td>`BedrockCopilot`</td>
		<td>`src/bedrock/primitives/`</td>
		<td>Copilot panel</td>
	</tr>
	<tr>
		<td>`StatCard`</td>
		<td>`src/bedrock/components/`</td>
		<td>Metrics display</td>
	</tr>
	<tr>
		<td>`ObjectList`</td>
		<td>`src/bedrock/components/`</td>
		<td>Collection navigation</td>
	</tr>
	<tr>
		<td>`ObjectGrid`</td>
		<td>`src/bedrock/components/`</td>
		<td>Content display</td>
	</tr>
</table>

**Creating new structural components requires architectural review.**

### Section 2.3: Console Checklist

Every console implementation completes this checklist in SPEC.md:

```markdown
## Console Implementation Checklist

- [ ] Uses `BedrockLayout` as shell
- [ ] Header displays: title, description, primary action
- [ ] Metrics row shows 4-6 relevant stats
- [ ] Navigation column uses `ObjectList` or equivalent
- [ ] Content area uses `ObjectGrid` or appropriate view
- [ ] Inspector uses `BedrockInspector` shell
- [ ] Copilot panel integrated with console context
- [ ] Navigation declaratively configured in `navigation.ts`
- [ ] All object types use `GroveObject` schema
```

---

## Article III: Copilot Integration

### Section 3.1: Copilot Mandate

Every Bedrock console includes a Copilot. No console ships without AI assistance—this enables Grove's exploration architecture vision.

### Section 3.2: Context Protocol

Every Copilot implementation provides context following this interface:

```typescript
interface BedrockCopilotContext {
  // Identity
  consoleId: string;
  
  // Current selection
  selectedObject?: GroveObject;
  selectedObjectType?: GroveObjectType;
  
  // View state
  filters: FilterState;
  sortOrder: SortState;
  
  // Schema for validation
  schema?: ObjectSchema;
  
  // Related objects for reference resolution
  relatedObjects: Record<GroveObjectType, GroveObject[]>;
}
```

### Section 3.3: Required Copilot Capabilities

Every console Copilot supports these baseline capabilities:

<table header-row="true">
	<tr>
		<td>Capability</td>
		<td>Description</td>
		<td>Implementation</td>
	</tr>
	<tr>
		<td>Schema awareness</td>
		<td>Knows valid fields for current object</td>
		<td>Load schema on selection</td>
	</tr>
	<tr>
		<td>Patch generation</td>
		<td>Produces JSON patches from natural language</td>
		<td>Structured output prompt</td>
	</tr>
	<tr>
		<td>Validation</td>
		<td>Rejects invalid patches before display</td>
		<td>Schema validation layer</td>
	</tr>
	<tr>
		<td>Diff preview</td>
		<td>Shows changes before applying</td>
		<td>Standard diff component</td>
	</tr>
	<tr>
		<td>Model indicator</td>
		<td>Shows which model is active</td>
		<td>UI indicator</td>
	</tr>
</table>

### Section 3.4: Console-Specific Actions

Each console defines its specific Copilot actions in SPEC.md:

```markdown
## Copilot Actions

| Action | Trigger | Output | Model Preference |
|--------|---------|--------|------------------|
| [Action name] | [Observer intent] | [What Copilot produces] | [local/hybrid/cloud] |
```

---

## Article IV: Object Model Compliance

### Section 4.1: GroveObject Mandate

Every entity in Bedrock uses the `GroveObject` schema:

```typescript
interface GroveObject<T = unknown> {
  meta: GroveObjectMeta;  // id, type, title, timestamps, provenance
  payload: T;             // Type-specific data
}
```

**No raw objects.** Data that doesn't fit GroveObject escalates to architectural review.

### Section 4.2: Object Model Boundary

Respect the object model boundary:

<table header-row="true">
	<tr>
		<td>Category</td>
		<td>Object Types</td>
		<td>Console Group</td>
	</tr>
	<tr>
		<td>Sprouts (Write Path)</td>
		<td>Sprout, SproutClaim, SproutProposal</td>
		<td>Knowledge Garden</td>
	</tr>
	<tr>
		<td>DEX Objects (Read Path)</td>
		<td>Hub, Journey, Node, Lens, Moment, Persona</td>
		<td>Experience Design</td>
	</tr>
	<tr>
		<td>System Objects</td>
		<td>FeatureFlag, SystemVoice, AudioTrack, HealthCheck</td>
		<td>System Configuration</td>
	</tr>
</table>

**Sprouts are the atomic unit of knowledge change.** DEX objects organize how Sprouts surface. Do not conflate.

### Section 4.3: Type Registration

Every new object type:

1. Adds to `GroveObjectType` union in `grove-object.ts`
2. Documents in `BEDROCK_OBJECT_CATALOG.md`
3. Receives a schema definition
4. Receives default Copilot actions

### Section 4.4: Events vs. Objects

**Events (`GroveEvent`) are NOT GroveObjects.** This intentional architectural distinction:

<table header-row="true">
	<tr>
		<td>Concept</td>
		<td>Base Type</td>
		<td>Purpose</td>
		<td>Lifecycle</td>
	</tr>
	<tr>
		<td>**GroveObject**</td>
		<td>`GroveObjectMeta`</td>
		<td>Persistent entities</td>
		<td>Long-lived, mutable</td>
	</tr>
	<tr>
		<td>**GroveEvent**</td>
		<td>`MetricAttribution`</td>
		<td>Temporal occurrences</td>
		<td>Immutable, append-only</td>
	</tr>
</table>

Events record **what happened**; Objects represent **what exists**. Events use `MetricAttribution` as their base type (fieldId + timestamp) to ensure provenance. GroveObjects derive from events via projections, but events themselves don't follow Section 4.1 requirements.

**Event infrastructure** resides in `src/core/events/` and follows the event sourcing pattern established in `src/core/schema/telemetry.ts`.

---

## Article V: Strangler Fig Awareness

### Section 5.1: No Legacy Coupling

Bedrock code does NOT:

- Import from `src/foundation/` (legacy Foundation console)
- Share state with legacy components
- Assume legacy behavior or data structures
- Use legacy component patterns

**Exception:** Core infrastructure in `src/core/` is **shared by design**. Both Bedrock and legacy routes import from:
- `src/core/events/` — Event sourcing infrastructure
- `src/core/schema/` — Shared type definitions (telemetry, etc.)
- `src/core/types/` — Common TypeScript interfaces

This enables strangler fig migration where new infrastructure is built once and consumed by both systems until legacy is deprecated.

**Bedrock is a clean-room implementation** that builds on shared core infrastructure.

### Section 5.2: Feature Parity Tracking

Every sprint updates the feature parity checklist:

```markdown
## Feature Parity Status

| Feature | Legacy Location | Bedrock Status | Parity? |
|---------|-----------------|----------------|---------|
| Sprout moderation | SproutQueue.tsx | [status] | [ ] |
| Journey editing | NarrativeArchitect.tsx | [status] | [ ] |
| ... | ... | ... | ... |
```

### Section 5.3: Migration Path

When implementing a feature that exists in legacy:

1. **Audit legacy** — Document what exists, what works, what's broken
2. **Design fresh** — Apply Bedrock patterns, ignore legacy implementation
3. **Verify parity** — Ensure all legacy capabilities are covered
4. **Document differences** — Note intentional deviations from legacy

---

## Article VI: Sprint Artifacts

### Section 6.1: Required Sections

Every Bedrock sprint SPEC.md includes:

```markdown
# Sprint: [name]

## Constitutional Reference
- [ ] Read: The_Trellis_Architecture__First_Order_Directives.md
- [ ] Read: Bedrock_Architecture_Specification.md
- [ ] Read: Relevant object schemas

## DEX Compliance Matrix
[Per Section 1.2]

## Console Implementation Checklist
[Per Section 2.3]

## Copilot Actions
[Per Section 3.4]

## Object Types Used
[List all GroveObject types touched]

## Feature Parity Status
[Per Section 5.2]

## Patterns Extended
[Standard Foundation Loop requirement]
```

### Section 6.2: EXECUTION_PROMPT Additions

Every Bedrock EXECUTION_PROMPT.md includes:

```markdown
## Bedrock Verification

Before starting:
- [ ] On `bedrock` branch
- [ ] No imports from `src/foundation/`
- [ ] BedrockLayout available

After each epic:
- [ ] Console pattern checklist passes
- [ ] Copilot receives correct context
- [ ] GroveObject schema used for all entities
- [ ] DEX compliance tests documented

Final verification:
- [ ] Feature parity checklist updated
- [ ] No legacy coupling introduced
- [ ] All DEX tests pass
```

### Section 6.3: Core Infrastructure Sprints

Sprints creating **shared infrastructure** in `src/core/` have modified requirements:

**Required sections:**
- Constitutional Reference (Article I)
- DEX Compliance Matrix (Article I Section 1.2)
- Pattern Check (Foundation Loop Phase 0)
- No Legacy Coupling verification (Article V Section 5.1)
- Standard Foundation Loop artifacts

**Omitted sections** (console-specific):
- Console Implementation Checklist (Section 2.3)
- Copilot Actions table (Section 3.4)
- Feature Parity Status (Section 5.2) — unless replacing legacy infrastructure

**Object Model clarification:**
- Core infrastructure creates **event types** (`GroveEvent`) which are NOT GroveObjects (per Section 4.4)
- Event types use `MetricAttribution` as base, not `GroveObjectMeta`
- Projection functions derive GroveObject-compatible state from events

**File locations for core infrastructure:**
```
src/core/
├── events/       # Event sourcing (GroveEvent, projections)
├── schema/       # Type definitions (telemetry, validation)
├── types/        # Shared TypeScript interfaces
└── utils/        # Shared utilities
```

---

## Article VII: Enforcement

### Section 7.1: Pre-Merge Checklist

Before any PR merges to `bedrock`:

```markdown
## Bedrock Merge Checklist

- [ ] SPEC.md includes all required sections (Article VI)
- [ ] DEX compliance matrix shows all passes (Article I)
- [ ] Console pattern checklist complete (Article II)
- [ ] Copilot integrated with context (Article III)
- [ ] All objects use GroveObject schema (Article IV)
- [ ] No imports from src/foundation/ (Article V)
- [ ] Feature parity status updated (Article V)
- [ ] Tests pass (Foundation Loop requirement)
- [ ] Visual baselines updated if applicable
```

### Section 7.2: Architectural Review Triggers

These situations require architectural review before proceeding:

1. Console doesn't fit canonical pattern
2. New structural component needed
3. Object doesn't fit GroveObject schema
4. DEX test fails and workaround proposed
5. Legacy coupling seems necessary
6. New object type proposed

### Section 7.3: Contract Amendments

This contract amends via:

1. Proposal documented in sprint SPEC.md
2. Architectural review approval
3. Contract version increment
4. All team members notified

---

## Article VIII: Quick Reference

### The Bedrock Mantra

> Features are proven. Patterns are established. Now we produce them correctly.

### The Four Questions

Before shipping any Bedrock feature:

1. **Does it use BedrockLayout?** (Console pattern — N/A for core infrastructure)
2. **Does it have a Copilot?** (AI assistance — N/A for core infrastructure)  
3. **Does it use GroveObject?** (Data model — events use MetricAttribution instead)
4. **Does it pass DEX tests?** (Constitutional compliance — **always required**)

### The Build Sequence

```
Sprint 0: Infrastructure (BedrockLayout, Nav, Inspector, Copilot)
Sprint 1: Sprout Queue (first complete console, proves pattern)
Sprint 2+: Feature conveyor (one console per sprint)
```

### File Locations

```
src/bedrock/                    # Bedrock consoles and components
├── primitives/                 # BedrockLayout, Nav, Inspector, Copilot
├── components/                 # Shared components (StatCard, ObjectList, etc.)
├── consoles/                   # Individual console implementations
├── config/                     # Declarative configuration (navigation.ts, etc.)
├── copilot/                    # Copilot context and actions
└── types/                      # TypeScript interfaces

src/core/                       # Shared infrastructure (both bedrock + legacy)
├── events/                     # Event sourcing (GroveEvent, projections)
│   ├── types.ts                # Event type definitions
│   ├── schema.ts               # Zod validation
│   ├── projections/            # State derivation from events
│   └── store.ts                # Event log management
├── schema/                     # Type definitions (telemetry.ts, etc.)
└── types/                      # Shared TypeScript interfaces
```

---

## Signatures

By commencing work on the `bedrock` branch, contributors agree to this contract.

**Effective Date:** December 30, 2025  
**Version:** 1.1

---

## Changelog

### v1.1 (January 4, 2026)

**Amendments for Core Infrastructure:**

1. **Section 4.4 (NEW):** Events vs. Objects
   - Clarifies that `GroveEvent` types are NOT `GroveObjects`
   - Events use `MetricAttribution` as base type (provenance-first)
   - Objects derive from events via projections

2. **Section 5.1 (AMENDED):** No Legacy Coupling
   - Added exception for shared `src/core/` infrastructure
   - Clarifies strangler fig migration pattern

3. **Section 6.3 (NEW):** Core Infrastructure Sprints
   - Modified requirements for `src/core/` sprints
   - Specifies which sections are required vs. omitted
   - Documents valid file locations for shared infrastructure

4. **Article VIII (AMENDED):** Quick Reference
   - Updated "Four Questions" to note console-specific vs. universal requirements
   - Expanded file locations to include `src/core/`

**Rationale:** The `bedrock-event-architecture-v1` sprint exposed a gap: the contract was written for console development but core infrastructure sprints have different requirements. These amendments maintain contract rigor while acknowledging legitimate architectural distinctions between consoles, objects, and events.

---

*This contract ensures Bedrock delivers on Grove's architectural vision. Deviations fragment the reference implementation. When in doubt, escalate to architectural review.*