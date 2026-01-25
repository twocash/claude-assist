## Rewrite: 251200-s-arch-architecture-documentation-index.md
### Diagnosis Summary
Source document is a technical index from December 2024 describing Field-aware architecture. Written for developers, it uses some legacy terminology ("tokens" in implied credit economy) and could benefit from clearer positioning of architectural choices within Grove's exploration philosophy.

### Key Changes Made
- Updated terminology: "tokens" → "credits", clarified "DEX" as Declarative Exploration
- Reframed Fields as exploration domains rather than generic "knowledge domains"
- Added context connecting technical architecture to Grove's exploration mission
- Removed hedging language while preserving honest scope limitations in MVP section
- Strengthened voice to be more direct and concrete

### Flags for Review
- Kept technical depth appropriate for developer audience
- Maintained all technical specifications and implementation details
- Preserved the honest assessment of MVP limitations and phased approach

---
# Grove Architecture Documentation Index

**Version:** 2.0 (Field-Aware)  
**Last Updated:** December 2024

---

## Overview

This index maps Grove's architecture documentation. All documents reflect the Field-aware architecture introduced in December 2024.

**Core Principle:** All exploration happens within a Field. A Field is a bounded exploration domain with its own RAG collection, discovery tools, and accumulated insights.

---

## Architecture Documents

### Foundational

| Document | Purpose | Key Concepts |
|----------|---------|--------------|
| [`architecture/FIELD_ARCHITECTURE.md`](architecture/FIELD_ARCHITECTURE.md) | **START HERE** — Complete Field specification | Fields, Namespaces, Composite Fields, Attribution |
| [`architecture/FIELD_QUICK_REFERENCE.md`](architecture/FIELD_QUICK_REFERENCE.md) | Sprint-ready Field summary | Quick rules, MVP requirements |
| [`architecture/TRELLIS.md`](architecture/TRELLIS.md) | Declarative Exploration (DEX) stack philosophy and layers | DEX principles, three-layer abstraction |
| [`architecture/TRELLIS_FIRST_ORDER_DIRECTIVES.md`](architecture/TRELLIS_FIRST_ORDER_DIRECTIVES.md) | DEX principles (condensed) | Four pillars, terminology |

### Implementation

| Document | Purpose | Key Concepts |
|----------|---------|--------------|
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Cognitive Simulation Engine | Entropy detection, journey routing, session state |
| [`SPROUT_SYSTEM.md`](SPROUT_SYSTEM.md) | Insight capture lifecycle | Sprout provenance, botanical lifecycle, Knowledge Commons |
| [`specs/dex-object-model.ts`](specs/dex-object-model.ts) | TypeScript type definitions | Field, Sprout, Session, Lens, Journey schemas |

### Supporting

| Document | Purpose |
|----------|---------|
| [`ARCHITECTURE_RAG.md`](ARCHITECTURE_RAG.md) | RAG implementation details |
| [`ARCHITECTURE_EVENT_DRIVEN.md`](ARCHITECTURE_EVENT_DRIVEN.md) | Event bus architecture |
| [`ENGAGEMENT_BUS_INTEGRATION.md`](ENGAGEMENT_BUS_INTEGRATION.md) | Engagement system events |

---

## Key Architectural Decisions

### 1. Fields as First-Class Entities

Every exploration operation belongs to a Field:
- Sprouts carry `fieldId`
- Sessions carry `fieldId`
- Lenses, Journeys, Card Definitions belong to Fields
- Field switching creates new session (clean cognitive break)

### 2. Namespaced Entities

Entities within Fields use namespaced identifiers:
```
{field-slug}.{local-id}

Examples:
- grove.strategic-insight
- legal.contract-clause
- legal-grove.regulatory-risk (composite)
```

### 3. Composite Fields for Cross-Domain Exploration

Grove enforces explicit boundaries. Cross-domain exploration requires Composite Field creation:
- Merge 2+ parent Fields
- Inherited entities retain parent namespace
- Native entities receive composite namespace
- Sprouts promote to parent Fields when validated

### 4. Attribution Economy

All entities track provenance for the Knowledge Commons:
- Original creator
- Fork lineage
- Contributors
- Adoption metrics
- Credit flow (future implementation)

---

## Reading Order

**For understanding the architecture:**
1. `architecture/FIELD_ARCHITECTURE.md` — Start here
2. `architecture/TRELLIS.md` — Philosophy and layers
3. `specs/dex-object-model.ts` — Data structures
4. `SPROUT_SYSTEM.md` — Insight capture

**For implementing features:**
1. `architecture/FIELD_QUICK_REFERENCE.md` — Rules checklist
2. `specs/dex-object-model.ts` — TypeScript schemas
3. `ARCHITECTURE.md` — Terminal implementation
4. Sprint-specific docs in `sprints/`

---

## MVP Scope (December 2024)

**Implemented:**
- Field schema with all future-ready properties
- Single Field populated (The Grove Foundation)
- `fieldId` on all Sprouts and Sessions
- Field indicator in Terminal header

**Deferred:**
- Multi-Field switching (Phase 2)
- Field creation flow (Phase 2)
- Composite Field merging (Phase 2+)
- Knowledge Commons marketplace (Phase 3)
- Attribution credit economy (Phase 3+)

---

## Document Conventions

### Version Tags
- **2.0 (Field-Aware)** — Updated for Field architecture
- **1.0 (Genesis)** — Original pre-Field version

### Cross-References
All documents include a "Cross-References" section linking to related docs.

### TypeScript Schemas
Authoritative types live in `specs/dex-object-model.ts`. Implementation types conform to these schemas.

---

## Change Log

| Date | Change | Documents Affected |
|------|--------|-------------------|
| Dec 2024 | Field architecture introduced | All architecture docs |
| Dec 2024 | Namespace pattern defined | FIELD_ARCHITECTURE, dex-object-model.ts |
| Dec 2024 | Sprout System updated for Field context | SPROUT_SYSTEM.md |
| Dec 2024 | Declarative Exploration (DEX) stack updated for Field layer | TRELLIS.md, TRELLIS_FIRST_ORDER_DIRECTIVES.md |