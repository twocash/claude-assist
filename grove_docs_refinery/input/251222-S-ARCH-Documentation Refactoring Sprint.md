> [Original Source: Architecture Documentation Refactoring - Dec 22 2d1780a78eef80178eebdbc8d6acbadd.md]

# Architecture Documentation Refactoring - Dec 22

## Complete

### Documents Created/Updated

| Document | Lines | Status | Description |
| --- | --- | --- | --- |
| `architecture/FIELD_ARCHITECTURE.md` | 721 | ✅ New | Complete Field specification |
| `architecture/FIELD_QUICK_REFERENCE.md` | 88 | ✅ New | Sprint-ready summary |
| `architecture/INDEX.md` | 141 | ✅ New | Documentation roadmap |
| `architecture/TRELLIS.md` | 284 | ✅ Updated | DEX stack v2.0 (Field-aware) |
| `architecture/TRELLIS_FIRST_ORDER_DIRECTIVES.md` | 114 | ✅ Updated | Directives v2.0 (Field-aware) |
| `ARCHITECTURE.md` | 267 | ✅ Updated | Cognitive Engine v2.0 (Field-aware) |
| `SPROUT_SYSTEM.md` | 423 | ✅ Updated | Sprout System v2.0 (Field-aware) |
| `specs/dex-object-model.ts` | 786 | ✅ New | Unified TypeScript schemas |
| `specs/custom-lens-data-model.ts` | 195 | ✅ Updated | References unified model |

**Total:** ~3,019 lines of architecture documentation

---

### Key Changes

**1. Field as First-Class Entity**

- Every doc now references Field context
- `fieldId` required on Sprouts, Sessions, Lenses, Journeys
- Field switching = clean break (new session)

**2. Namespace Pattern**

- `{field-slug}.{local-id}` for all entities
- Composite Fields inherit parent namespaces
- Native composite entities get composite namespace

**3. Three-Layer Stack Updated**

`Layer 1: Engine (Fixed)     — Sprout Manager, Session Manager, RAG, Attribution
Layer 2: Field (Variable)   — Knowledge domains with RAG + tools
Layer 3: Config (Per-Field) — Lenses, Journeys, Card Definitions`

**4. Unified Type Definitions**

- `specs/dex-object-model.ts` is now authoritative source
- All types include Field context
- Helper functions for namespace operations

**5. Documentation Hierarchy**

`docs/
├── architecture/
│   ├── INDEX.md                         ← Start here
│   ├── FIELD_ARCHITECTURE.md            ← Core spec
│   ├── FIELD_QUICK_REFERENCE.md         ← Sprint rules
│   ├── TRELLIS.md                       ← DEX philosophy
│   └── TRELLIS_FIRST_ORDER_DIRECTIVES.md
├── ARCHITECTURE.md                       ← Terminal implementation
├── SPROUT_SYSTEM.md                      ← Insight capture
└── specs/
    ├── dex-object-model.ts              ← Unified types
    └── custom-lens-data-model.ts        ← Wizard types`

---

### MVP Requirements Encoded

From `FIELD_QUICK_REFERENCE.md`:

typescript

`// Every Sprout must have Field context
interface Sprout {
  fieldId: string;        // REQUIRED
  fieldSlug: string;      // For URL routing
  fieldName: string;      // Denormalized for display
}

// Every Session must be Field-scoped
interface TerminalSession {
  fieldId: string;        // REQUIRED, immutable per session
  fieldSlug: string;
  fieldName: string;
}

// Field switching = new session (clean break)`

**What NOT to Do:**

- ❌ Create Sprouts without `fieldId`
- ❌ Allow sessions to span multiple Fields
- ❌ Query across Fields without explicit composite
- ❌ Use entity IDs without namespace prefix

---

### Ready for Implementation

The architecture is now fully documented and ready for:

1. **Sprint 6** — Chat styling (Field indicator in header)
2. **Phase 2** — Multi-Field support
3. **Phase 2+** — Composite Fields, marketplace
4. **Phase 3** — Attribution credits, federation

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.

---
**PROVENANCE & HISTORY NOTE**
- **Internal GUID:** 2d1780a78eef80178eebdbc8d6acbadd
- **Original Filename:** Architecture Documentation Refactoring - Dec 22 2d1780a78eef80178eebdbc8d6acbadd.md
- **Standardized Namespace:** ARCH_Architecture_Documentation_Refactoring
- **Audit Date:** 2025-12-30T02:30:25.222Z

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.