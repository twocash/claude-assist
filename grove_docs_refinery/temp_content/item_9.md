
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

<table header-row="true">
	<tr>
		<td>Document</td>
		<td>Purpose</td>
		<td>Key Concepts</td>
	</tr>
	<tr>
		<td>[`architecture/FIELD_ARCHITECTURE.md`](architecture/FIELD_ARCHITECTURE.md)</td>
		<td>**START HERE** — Complete Field specification</td>
		<td>Fields, Namespaces, Composite Fields, Attribution</td>
	</tr>
	<tr>
		<td>[`architecture/FIELD_QUICK_REFERENCE.md`](architecture/FIELD_QUICK_REFERENCE.md)</td>
		<td>Sprint-ready Field summary</td>
		<td>Quick rules, MVP requirements</td>
	</tr>
	<tr>
		<td>[`architecture/TRELLIS.md`](architecture/TRELLIS.md)</td>
		<td>Declarative Exploration (DEX) stack philosophy and layers</td>
		<td>DEX principles, three-layer abstraction</td>
	</tr>
	<tr>
		<td>[`architecture/TRELLIS_FIRST_ORDER_DIRECTIVES.md`](architecture/TRELLIS_FIRST_ORDER_DIRECTIVES.md)</td>
		<td>DEX principles (condensed)</td>
		<td>Four pillars, terminology</td>
	</tr>
</table>

### Implementation

<table header-row="true">
	<tr>
		<td>Document</td>
		<td>Purpose</td>
		<td>Key Concepts</td>
	</tr>
	<tr>
		<td>[`ARCHITECTURE.md`](ARCHITECTURE.md)</td>
		<td>Cognitive Simulation Engine</td>
		<td>Entropy detection, journey routing, session state</td>
	</tr>
	<tr>
		<td>[`SPROUT_SYSTEM.md`](SPROUT_SYSTEM.md)</td>
		<td>Insight capture lifecycle</td>
		<td>Sprout provenance, botanical lifecycle, Knowledge Commons</td>
	</tr>
	<tr>
		<td>[`specs/dex-object-model.ts`](specs/dex-object-model.ts)</td>
		<td>TypeScript type definitions</td>
		<td>Field, Sprout, Session, Lens, Journey schemas</td>
	</tr>
</table>

### Supporting

<table header-row="true">
	<tr>
		<td>Document</td>
		<td>Purpose</td>
	</tr>
	<tr>
		<td>[`ARCHITECTURE_RAG.md`](ARCHITECTURE_RAG.md)</td>
		<td>RAG implementation details</td>
	</tr>
	<tr>
		<td>[`ARCHITECTURE_EVENT_DRIVEN.md`](ARCHITECTURE_EVENT_DRIVEN.md)</td>
		<td>Event bus architecture</td>
	</tr>
	<tr>
		<td>[`ENGAGEMENT_BUS_INTEGRATION.md`](ENGAGEMENT_BUS_INTEGRATION.md)</td>
		<td>Engagement system events</td>
	</tr>
</table>

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

<table header-row="true">
	<tr>
		<td>Date</td>
		<td>Change</td>
		<td>Documents Affected</td>
	</tr>
	<tr>
		<td>Dec 2024</td>
		<td>Field architecture introduced</td>
		<td>All architecture docs</td>
	</tr>
	<tr>
		<td>Dec 2024</td>
		<td>Namespace pattern defined</td>
		<td>FIELD_ARCHITECTURE, dex-object-model.ts</td>
	</tr>
	<tr>
		<td>Dec 2024</td>
		<td>Sprout System updated for Field context</td>
		<td>SPROUT_SYSTEM.md</td>
	</tr>
	<tr>
		<td>Dec 2024</td>
		<td>Declarative Exploration (DEX) stack updated for Field layer</td>
		<td>TRELLIS.md, TRELLIS_FIRST_ORDER_DIRECTIVES.md</td>
	</tr>
</table>