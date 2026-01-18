> [Original Source: Foundation Console Deep Dive Extraction vs Rewrite 2d3780a78eef811fafbed07902ebc680.md]

# Foundation Console Deep Dive: Extraction vs Rewrite Analysis

**Date:** December 24, 2024

**Purpose:** Inform Foundation Sprint Spec for Kinetic Architecture migration

**Status:** Analysis Complete — Ready for Sprint Planning

---

## Executive Summary

The current Foundation console architecture is **80% feature-complete** but **architecturally inconsistent**. NarrativeArchitect demonstrates the target three-panel inspector pattern successfully, but other consoles (KnowledgeVault, HealthDashboard, EngagementBridge) use different layouts. The path to Kinetic Architecture requires:

1. **Extract** working patterns from NarrativeArchitect into reusable primitives
2. **Unify** schema types under DEXObject base interface
3. **Refactor** NarrativeArchitect to consume from DEXRegistry
4. **Migrate** other consoles to unified pattern

---

## Current Architecture Analysis

### Working Three-Panel Layout

```
FoundationWorkspace.tsx
├── FoundationHeader (48px fixed)
└── ThreeColumnLayout
    ├── FoundationNav (220px) — Sidebar navigation
    ├── <Outlet> → Console content (flex-1)
    └── FoundationInspector (340px, conditional)
```

**What's Working:**

- `ThreeColumnLayout` properly renders three columns
- `FoundationUIContext` manages inspector state globally
- `FoundationInspector` routes to correct inspector by mode type
- `JourneyInspector` and `NodeInspector` are fully implemented
- Click → openInspector() → Panel opens pattern works

---

## Component Inventory

### Shared Primitives (src/shared/)

| Component | Lines | Status | Reusable? |
| --- | --- | --- | --- |
| `ThreeColumnLayout` | 68 | ✅ Working | Yes — Core layout |
| `InspectorPanel` | 99 | ✅ Working | Yes — Inspector wrapper |
| `InspectorSection` | 15 | ✅ Working | Yes — Section primitive |
| `InspectorDivider` | 3 | ✅ Working | Yes — Divider |
| `CollectionHeader` | 106 | ✅ Working | Yes — Search/filter bar |
| `SearchInput` | ~40 | ✅ Working | Yes |
| `FilterButton` | ~60 | ✅ Working | Yes |
| `SortButton` | ~50 | ✅ Working | Yes |
| `EmptyState` | ~40 | ✅ Working | Yes |
| `LoadingSpinner` | ~30 | ✅ Working | Yes |
| `StatusBadge` | ~25 | ✅ Working | Yes |

### Foundation Components (src/foundation/components/)

| Component | Lines | Status | Action |
| --- | --- | --- | --- |
| `DataPanel` | 59 | ✅ Working | Keep — Generic panel wrapper |
| `MetricCard` | 76 | ✅ Working | Keep — Rename to StatCard |
| `GlowButton` | 114 | ✅ Working | Keep — Button primitive |

### Console-Specific Components (Inline in NarrativeArchitect)

| Component | Lines | Status | Action |
| --- | --- | --- | --- |
| `ViewToggle` | ~50 | Inline | **EXTRACT** → Generic toggle |
| `JourneyList` | ~45 | Inline | **EXTRACT** → ObjectList |
| `PersonaList` | ~35 | Inline | **EXTRACT** → ObjectList |
| `NodeGrid` | ~60 | Inline | **EXTRACT** → CollectionGrid |
| `CardGrid` | ~45 | Inline | **EXTRACT** → CollectionGrid |

### Inspectors (src/foundation/inspectors/)

| Inspector | Lines | Status | Action |
| --- | --- | --- | --- |
| `JourneyInspector` | 167 | ✅ Complete | Reference impl |
| `NodeInspector` | 192 | ✅ Complete | Reference impl |
| `SproutReviewInspector` | 215 | ✅ Complete | Reference impl |
| `PersonaInspector` | — | Placeholder | Implement |
| `CardInspector` | — | Placeholder | Implement |

---

## Data Layer Analysis

### Current Schema Types (narratives-schema.ts)

```tsx
// V2.1 Types (Journey-based)
interface Journey {
  id: string;
  title: string;
  description: string;
  status: 'draft' | 'active' | 'archived';
  version?: number;
  entryNodeId?: string;
  estimatedMinutes?: number;
  linkedHubId?: string;
  createdAt?: string;
  updatedAt?: string;
}

interface JourneyNode {
  id: string;
  label: string;
  query: string;
  journeyId: string;
  sequenceOrder?: number;
  primaryNext?: string;
  alternateNext?: string[];
  hubId?: string;
  sectionId?: string;
  contextSnippet?: string;
}

interface TopicHub {
  id: string;
  title: string;
  tags: string[];
  priority: number;
  enabled: boolean;
  primarySource: string;
  supportingSources: string[];
  expertFraming: string;
  keyPoints: string[];
  createdAt?: string;
  updatedAt?: string;
}

// V2.0 Types (Card-based)
interface Persona { ... }
interface Card { ... }
```

### Gap Analysis: Current Types vs DEXObject

**Missing from Current Types:**

- `proposedBy: 'human' | 'agent'` — Agent proposal tracking
- `approvedBy?: string` — Human approval tracking
- `telemetryScore?: number` — Usage/effectiveness metrics
- `evolutionHistory?: VersionEntry[]` — Change tracking

**Current Types That Map to DEX:**

| Current Type | DEX Type | Notes |
| --- | --- | --- |
| `Journey` | `DEXJourney` | Add kinetic fields |
| `JourneyNode` | `DEXNode` | Add kinetic fields |
| `TopicHub` | `DEXHub` | Add kinetic fields |
| `Persona` | `DEXLens` | Rename for clarity |
| `Card` | `DEXCard` | Legacy, keep for V2.0 |

---

## Hook Analysis

### useNarrativeSchema (337 lines)

**Current Responsibilities:**

1. Load schema from `/api/narrative`
2. Handle V1 → V2 migration
3. Provide derived data (allJourneys, allNodes, allCards)
4. Filter functions (getFilteredCards, getFilteredJourneys, getFilteredNodes)
5. Selectors (getJourney, getNode, getCard, getPersona)
6. Save to `/api/admin/narrative`
7. CRUD operations (updateCard, deleteCard, createCard)

**Refactor Strategy:**

```
useNarrativeSchema (current monolith)
    ↓ Split into:
useDEXRegistry (generic object store)
├── register(type, objects)
├── get(type, id)
├── update(type, id, updates)
├── delete(type, id)
├── filter(type, predicate)
└── subscribe(type, callback)

useDEXJourneys (domain hook)
├── journeys: DEXJourney[]
├── getJourney(id)
└── filterJourneys(query)

useDEXNodes (domain hook)
├── nodes: DEXNode[]
├── getNode(id)
└── filterNodes(journeyId, query)

useDEXSync (persistence hook)
├── save()
├── loading, saving, status
└── GitHub sync status
```

---

## Console Comparison Matrix

| Feature | NarrativeArchitect | KnowledgeVault | HealthDashboard | EngagementBridge | SproutQueue |
| --- | --- | --- | --- | --- | --- |
| Uses ThreeColumnLayout | ✅ (via Outlet) | ❌ | ❌ | ❌ | ✅ (via Outlet) |
| Uses FoundationUIContext | ✅ | ❌ | ❌ | ❌ | ✅ |
| Has Inspector | ✅ | ❌ | ❌ | ❌ | ✅ |
| Uses DataPanel | ✅ | ✅ | ✅ | ✅ | ❌ |
| Uses MetricCard | ✅ | ✅ | ✅ | ✅ | ✅ |
| Uses GlowButton | ✅ | ✅ | ✅ | ✅ | ❌ |
| Uses CollectionHeader | ✅ | ❌ | ❌ | ❌ | ✅ |
| Has Tab navigation | ❌ (ViewToggle) | ❌ | ✅ (internal) | ✅ (internal) | ✅ (filter tabs) |
| Lines | 571 | 223 | 540 | 333 | 146 |

---

## Extraction Plan

### Phase 1: Extract Component Grammar (No Breaking Changes)

**From NarrativeArchitect, extract:**

1. **ViewToggle → SegmentedControl**

```tsx
interface SegmentedControlProps<T extends string> {
  options: { id: T; label: string; icon?: string }[];
  value: T;
  onChange: (value: T) => void;
}
```

1. **JourneyList + PersonaList → ObjectList**

```tsx
interface ObjectListProps<T> {
  items: T[];
  selectedId: string | null;
  activeInspectorId: string | null;
  onSelect: (id: string) => void;
  renderItem: (item: T) => { label: string; count?: number; status?: 'active' | 'inactive' };
  emptyMessage?: string;
}
```

1. **NodeGrid + CardGrid → ObjectGrid**

```tsx
interface ObjectGridProps<T> {
  items: T[];
  activeInspectorId: string | null;
  searchQuery: string;
  onSelect: (id: string) => void;
  renderCard: (item: T) => { title: string; subtitle: string; badges: Badge[] };
  emptyMessage?: string;
  columns?: 2 | 3 | 4;
}
```

### Phase 2: Create DEXObject Type System

```tsx
// src/core/schema/dex.ts

/** Base interface for all DEX-compliant objects */
export interface DEXObject {
  id: string;
  type: DEXObjectType;
  label: string;
  description?: string;
  icon?: string;
  color?: string;
  status: 'draft' | 'active' | 'archived';
  
  // Versioning
  version: number;
  createdAt: string;
  updatedAt: string;
  
  // Kinetic metadata
  proposedBy?: 'human' | 'agent';
  approvedBy?: string;
  telemetryScore?: number;
  evolutionHistory?: DEXVersionEntry[];
}

export type DEXObjectType = 'lens' | 'journey' | 'node' | 'hub' | 'card' | 'sprout';

/** Extended types */
export interface DEXJourney extends DEXObject {
  type: 'journey';
  entryNodeId?: string;
  estimatedMinutes?: number;
  linkedHubId?: string;
}

export interface DEXNode extends DEXObject {
  type: 'node';
  query: string;
  journeyId: string;
  sequenceOrder?: number;
  primaryNext?: string;
  alternateNext?: string[];
  hubId?: string;
  sectionId?: string;
  contextSnippet?: string;
}

export interface DEXHub extends DEXObject {
  type: 'hub';
  tags: string[];
  priority: number;
  enabled: boolean;
  primarySource: string;
  supportingSources: string[];
  expertFraming: string;
  keyPoints: string[];
}

export interface DEXLens extends DEXObject {
  type: 'lens';
  enabled: boolean;
  toneGuidance: string;
  narrativeStyle: string;
  arcEmphasis: Record<string, number>;
  openingPhase: string;
  defaultThreadLength: number;
  entryPoints: string[];
  suggestedThread: string[];
}
```

### Phase 3: Create DEXRegistry

```tsx
// src/core/registry/DEXRegistry.ts

export interface DEXRegistry {
  // Read operations
  get<T extends DEXObject>(type: DEXObjectType, id: string): T | null;
  getAll<T extends DEXObject>(type: DEXObjectType): T[];
  filter<T extends DEXObject>(type: DEXObjectType, predicate: (item: T) => boolean): T[];
  
  // Write operations
  register<T extends DEXObject>(type: DEXObjectType, objects: Record<string, T>): void;
  update<T extends DEXObject>(type: DEXObjectType, id: string, updates: Partial<T>): void;
  delete(type: DEXObjectType, id: string): void;
  create<T extends DEXObject>(type: DEXObjectType, object: Omit<T, 'id' | 'version' | 'createdAt' | 'updatedAt'>): string;
  
  // Subscriptions
  subscribe(type: DEXObjectType, callback: (objects: DEXObject[]) => void): () => void;
  
  // Persistence
  hydrate(schema: NarrativeSchemaV2): void;
  dehydrate(): NarrativeSchemaV2;
}
```

---

## Migration Path

### Sprint 1: Extract & Unify (This Sprint)

**Deliverables:**

1. Extract `SegmentedControl`, `ObjectList`, `ObjectGrid` from NarrativeArchitect
2. Create `DEXObject` type system in `src/core/schema/dex.ts`
3. Create `useDEXRegistry` hook (React context-based)
4. Refactor `useNarrativeSchema` to use DEXRegistry internally
5. NarrativeArchitect continues working (no breaking changes)

**Success Criteria:**

- All existing tests pass
- NarrativeArchitect looks/works identical
- New components are documented in shared/
- DEXObject types are exported from @core/schema

### Sprint 2: Migrate Consoles

- Refactor SproutQueue to use ObjectGrid
- Add inspector to KnowledgeVault
- Unify tab patterns across consoles

### Sprint 3: Agent Proposal Pipeline

- Add proposal queue to DEXRegistry
- Implement agent → proposal → human approval flow
- Add telemetry scoring hooks

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Breaking existing tests | Medium | High | Run tests continuously during refactor |
| Schema migration errors | Low | High | Add validation layer, keep V2.0 compat |
| Performance regression | Low | Medium | Benchmark before/after |
| Over-abstraction | Medium | Medium | Start minimal, add features as needed |

---

## Appendix: File Inventory

**Files to Modify:**

- `src/foundation/consoles/NarrativeArchitect.tsx` (571 lines)
- `src/foundation/hooks/useNarrativeSchema.ts` (337 lines)
- `data/narratives-schema.ts` (596 lines)

**Files to Create:**

- `src/core/schema/dex.ts` — DEXObject type system
- `src/core/registry/DEXRegistry.ts` — Central object store
- `src/core/registry/useDEXRegistry.ts` — React hook
- `src/shared/SegmentedControl.tsx` — View toggle
- `src/shared/ObjectList.tsx` — Generic list
- `src/shared/ObjectGrid.tsx` — Generic grid

**Files Unchanged:**

- All inspector components (already well-structured)
- ThreeColumnLayout, InspectorPanel (working as-is)
- DataPanel, MetricCard, GlowButton (keep as-is)

---

## Next Step

This analysis is complete. Proceed to Foundation Sprint Spec with clear scope:

1. **Extract component grammar** — 3 new shared components
2. **Create DEX types** — New schema file
3. **Create DEXRegistry** — Central store pattern
4. **Refactor useNarrativeSchema** — Internal change, API stable
5. **Update NarrativeArchitect** — Use new components

Estimated effort: **2-3 focused sessions** with Claude Code.

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.

---
**PROVENANCE & HISTORY NOTE**
- **Internal GUID:** 2d3780a78eef811fafbed07902ebc680
- **Original Filename:** Foundation Console Deep Dive Extraction vs Rewrite 2d3780a78eef811fafbed07902ebc680.md
- **Standardized Namespace:** DEEP_Foundation_Console_Extraction_Vs_Rewrite
- **Audit Date:** 2025-12-30T02:30:25.222Z

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.