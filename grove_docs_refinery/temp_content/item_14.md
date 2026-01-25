
# The Sprout System: Recursive Exploration Architecture

**Version:** 2.0 (Field-Aware)  
**Status:** Technical Specification  
**Date:** December 2024

## Abstract

The Sprout System enables explorers to capture and cultivate valuable agent outputs within bounded Fields (knowledge domains). By transforming ephemeral conversations into persistent artifacts that feed back into Grove's Knowledge Commons, the system creates recursive loops where exploration generates the maps for future discovery. This document specifies the architecture, distinguishes MVP implementation from future capabilities, and positions the system as a generalizable protocol for any exploration domain.

---

## 1. The Core Loop

### 1.1 From Ephemeral to Persistent

Traditional agent interactions waste discoveries:

```
Query → Agent Processing → Response → (Lost)
```

The Sprout System adds a capture point:

```
Query → Agent Processing → Response → [/sprout] → Persistent Artifact (Field-scoped)
```

The system preserves responses verbatim with full provenance—the query that generated it, the Field that scoped it, the Lens that shaped its voice, and the Journey context that framed the inquiry. This provenance chain enables attribution as knowledge propagates.

### 1.2 The Field-Scoped Recursive Loop

Published knowledge shapes future exploration within bounded Fields:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│    Field: "The Grove Foundation"                                │
│    ─────────────────────────────                                │
│                                                                 │
│    Knowledge Commons (Field-scoped)                             │
│         │                                                       │
│         ▼                                                       │
│    RAG Context ──────► Agent ──────► Response                  │
│    (grove docs)                       │                         │
│                                       │ /sprout                 │
│                                       ▼                         │
│                                   [Sprout]                      │
│                                   fieldId: grove-foundation     │
│                                       │                         │
│                                       │ validation              │
│                                       ▼                         │
│                               [Promoted Content]                │
│                                       │                         │
│                                       └──────► Field's          │
│                                                Knowledge        │
│                                                Commons          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

The system learns through use. Observers cultivate specific Fields through exploration.

---

## 2. The Botanical Lifecycle

Grove's terminology maps naturally to content lifecycle:

<table header-row="true">
	<tr>
		<td>Stage</td>
		<td>State</td>
		<td>Description</td>
	</tr>
	<tr>
		<td>**Seed**</td>
		<td>Ephemeral</td>
		<td>Raw agent output, lost when conversation ends</td>
	</tr>
	<tr>
		<td>**Sprout**</td>
		<td>Captured</td>
		<td>Preserved via `/sprout` with full provenance including `fieldId`</td>
	</tr>
	<tr>
		<td>**Sapling**</td>
		<td>Validated</td>
		<td>Human review confirms accuracy and value</td>
	</tr>
	<tr>
		<td>**Tree**</td>
		<td>Published</td>
		<td>Integrated into Field's Knowledge Commons</td>
	</tr>
	<tr>
		<td>**Grove**</td>
		<td>Propagated</td>
		<td>Network-wide adoption across Fields, credit flows to creators</td>
	</tr>
</table>

Each Field is soil where different plants grow. Legal insights grow in the Legal Field; technical architecture insights grow in the Grove Foundation Field.

---

## 3. Provenance: The Attribution Foundation

### 3.1 What Gets Preserved

Each Sprout captures Field context as primary provenance:

```typescript
interface Sprout {
  id: string;
  
  // ═══════════════════════════════════════════════════════════
  // FIELD CONTEXT (REQUIRED)
  // ═══════════════════════════════════════════════════════════
  fieldId: string;                 // The Field this Sprout belongs to
  fieldSlug: string;               // URL-friendly identifier
  fieldName: string;               // Denormalized for display
  
  // ═══════════════════════════════════════════════════════════
  // THE ARTIFACT (VERBATIM)
  // ═══════════════════════════════════════════════════════════
  content: string;                 // The captured response
  contentType: 'text' | 'card' | 'synthesis';
  
  // ═══════════════════════════════════════════════════════════
  // GENERATION PROVENANCE
  // ═══════════════════════════════════════════════════════════
  generatedFrom: {
    sessionId: string;             // Terminal session
    query: string;                 // Observer's question
    
    // Namespaced entity references
    lensId?: string;               // e.g., "grove.skeptic"
    lensNamespace?: string;        // "grove"
    journeyId?: string;            // e.g., "grove.architecture-deep-dive"
    journeyNamespace?: string;     // "grove"
    nodeId?: string;               // Specific card/node triggered
    
    // RAG sources with namespace tracking
    ragSources: {
      documentId: string;
      namespace: string;           // Which Field's docs contributed
      relevanceScore: number;
    }[];
  };
  
  // ═══════════════════════════════════════════════════════════
  // COMPOSITE FIELD CONTEXT (if applicable)
  // ═══════════════════════════════════════════════════════════
  compositeContext?: {
    sourceNamespaces: string[];    // ["legal", "grove"] if cross-domain
    primaryNamespace?: string;     // Dominant source
    canPromoteTo: string[];        // Parent Field IDs
    promotedTo?: {
      fieldId: string;
      promotedAt: Date;
    };
  };
  
  // ═══════════════════════════════════════════════════════════
  // ATTRIBUTION
  // ═══════════════════════════════════════════════════════════
  createdBy: string;               // Observer who captured
  createdAt: Date;
  
  // ═══════════════════════════════════════════════════════════
  // CURATION STATE
  // ═══════════════════════════════════════════════════════════
  status: 'pending' | 'approved' | 'rejected' | 'archived';
  curatedBy?: string;
  curatedAt?: Date;
  tags: string[];
}
```

### 3.2 Why Verbatim and Field-Scoped Matters

Preserving responses verbatim AND Field-scoped enables the attribution economy:

1. **Clear Provenance**: The original output exists exactly as generated, in its originating Field
2. **Field Integrity**: Legal insights stay in Legal Field; Grove insights stay in Grove Field
3. **Derivative Tracking**: Cross-domain insights can be captured in Composite Fields
4. **Credit Flow**: Attribution flows to the Field's creators and the capturing Observer
5. **Audit Trail**: The evolution of ideas becomes traceable across Field boundaries

### 3.3 Composite Field Sprouts

When exploring in a Composite Field (merged from parents), Sprouts have richer provenance:

```typescript
// Sprout captured in "Legal-Grove Governance" composite Field
{
  fieldId: "legal-grove-composite-id",
  fieldName: "Legal-Grove Governance",
  
  compositeContext: {
    // This insight drew from both parent Fields
    sourceNamespaces: ["legal", "grove"],
    primaryNamespace: "legal",  // Predominantly legal content
    
    // Could be promoted to either parent
    canPromoteTo: ["legal-field-id", "grove-field-id"],
  },
  
  generatedFrom: {
    ragSources: [
      { documentId: "contract-123", namespace: "legal", relevanceScore: 0.92 },
      { documentId: "whitepaper-section", namespace: "grove", relevanceScore: 0.78 }
    ]
  }
}
```

**Sprout Promotion Flow:**
1. Observer captures Sprout in composite exploration
2. Sprout tagged with source namespaces based on RAG retrieval
3. Observer can "promote" Sprout to a parent Field if insight is domain-specific
4. Promoted Sprout appears in parent Field's Sprout collection
5. Attribution: discovered in composite, value accrues to parent

---

## 4. The User Experience Flow

### 4.1 Capture (Zero Friction, Field-Aware)

The interaction pattern optimizes for speed while maintaining Field context:

```
[Field: The Grove Foundation]

Observer: "How does the Ratchet actually work?"

[Grove responds with clear explanation]

Observer: /sprout
```

Immediate feedback (2-second toast):
```
🌱 Sprout planted in The Grove Foundation! View in Cultivate
```

No modal, no form, no interruption to flow. Field is implicit from session context.

### 4.2 Cultivate View (Cross-Field with Filtering)

The Cultivate surface shows Sprouts across all Fields with filtering:

```
┌─────────────────────────────────────────────────────────────┐
│  MY SPROUTS                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Filters: [All Fields ▼] [All Status ▼] [Date Range]       │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ "Attribution chains enable sustainable..."          │   │
│  │ 🌱 The Grove Foundation • Pending • Dec 22         │   │
│  │ Lens: grove.strategist | Journey: None             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ "Section 4.2 precedent suggests..."                 │   │
│  │ ⚖️ Legal Corpus • Approved • Dec 21                │   │
│  │ Lens: legal.litigator | Journey: due-diligence     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ "Cross-domain governance implications..."           │   │
│  │ 🔀 Legal-Grove Governance • Pending • Dec 22       │   │
│  │ Sources: legal (78%), grove (22%)                  │   │
│  │ [Promote to Legal] [Promote to Grove]              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Statistics (Per-Field Breakdown)

```
┌─────────────────────────────────────────────────────────────┐
│  YOUR GARDEN                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  By Field                                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 🌱 The Grove Foundation                            │    │
│  │    12 sprouts │ 3 saplings │ 1 tree               │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ ⚖️ Legal Corpus                                    │    │
│  │    8 sprouts │ 2 saplings │ 0 trees               │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │ 🔀 Legal-Grove Governance (Composite)              │    │
│  │    3 sprouts │ 0 promoted                         │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
│  Network Impact (Future)                                    │
│  ├── ✨ 47 responses shaped by your trees                  │
│  └── 🔗 3 derivative contributions                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. The Protocol Perspective

### 5.1 Grove as Genesis Implementation

The Sprout System is implemented within Grove, but the architecture describes a **protocol** applicable to any knowledge base organized into Fields:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE SPROUT PROTOCOL                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Any Agent Interface            Any Knowledge Base (Fields)    │
│        │                               │                        │
│        │    capture + fieldId          │                        │
│        │  ───────────────────────►     │                        │
│        │                               │                        │
│        │                        ┌──────┴──────┐                 │
│        │                        │   STAGING   │                 │
│        │                        │   (Field-   │                 │
│        │                        │   scoped)   │                 │
│        │                        └──────┬──────┘                 │
│        │                               │                        │
│        │                          validation                    │
│        │                               │                        │
│        │                        ┌──────┴──────┐                 │
│        │                        │  KNOWLEDGE  │                 │
│        │                        │   COMMONS   │                 │
│        │                        │  (Field +   │                 │
│        │                        │  Namespace) │                 │
│        │                        └──────┬──────┘                 │
│        │                               │                        │
│        │       credit attribution      │                        │
│        ◄───────────────────────────────────────────────────────┘                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Generalization Opportunities

The Field-scoped pattern applies to:

- **University research commons**: Each department/project is a Field
- **Corporate knowledge bases**: Each team/domain is a Field
- **Open source documentation**: Each project is a Field
- **Learning platforms**: Each course/topic is a Field
- **Cross-institutional collaboration**: Composite Fields merge institutional knowledge

The core loop remains: capture → preserve Field provenance → validate → publish → attribute.

---

## 6. MVP vs. Future Capabilities

### 6.1 MVP Scope

<table header-row="true">
	<tr>
		<td>Capability</td>
		<td>Implementation</td>
	</tr>
	<tr>
		<td>Capture</td>
		<td>`/sprout` command</td>
	</tr>
	<tr>
		<td>Field Context</td>
		<td>`fieldId` on every Sprout (single Field: Grove Foundation)</td>
	</tr>
	<tr>
		<td>Storage</td>
		<td>localStorage (browser)</td>
	</tr>
	<tr>
		<td>Identity</td>
		<td>Anonymous session ID</td>
	</tr>
	<tr>
		<td>View</td>
		<td>Cultivate with Field indicator</td>
	</tr>
	<tr>
		<td>Lifecycle</td>
		<td>Sprout status only</td>
	</tr>
</table>

### 6.2 Future Phases

<table header-row="true">
	<tr>
		<td>Phase</td>
		<td>Capability</td>
		<td>Dependency</td>
	</tr>
	<tr>
		<td>2</td>
		<td>Multi-Field support</td>
		<td>Field architecture</td>
	</tr>
	<tr>
		<td>2</td>
		<td>Field filter in Cultivate</td>
		<td>Multi-Field</td>
	</tr>
	<tr>
		<td>2</td>
		<td>Grove ID integration</td>
		<td>Identity infrastructure</td>
	</tr>
	<tr>
		<td>3</td>
		<td>Server-side storage</td>
		<td>API development</td>
	</tr>
	<tr>
		<td>3</td>
		<td>Admin review workflow (per Field)</td>
		<td>Server storage</td>
	</tr>
	<tr>
		<td>3</td>
		<td>Composite Field Sprouts</td>
		<td>Composite Fields</td>
	</tr>
	<tr>
		<td>4</td>
		<td>Sprout promotion (composite → parent)</td>
		<td>Composite Fields</td>
	</tr>
	<tr>
		<td>4</td>
		<td>Network propagation</td>
		<td>Distributed infrastructure</td>
	</tr>
	<tr>
		<td>4</td>
		<td>Credit attribution</td>
		<td>Network sync</td>
	</tr>
</table>

---

## 7. Connection to Knowledge Commons Architecture

The Sprout System implements the Terminal interface to Grove's broader Knowledge Commons vision. Fields organize knowledge into bounded contexts; Sprouts capture insights within those contexts; the Knowledge Commons enables sharing across Fields with attribution.

Key alignments:

1. **Attribution Economy**: Sprouts carry Field + namespace provenance enabling credit flow
2. **Preprint Model**: Immediate availability with quality signals accumulating through adoption
3. **Derivative Innovation**: Verbatim preservation + Field scoping enables clear attribution
4. **Field Integrity**: Domain knowledge stays coherent within Field boundaries
5. **Cross-Domain Synthesis**: Composite Fields enable explicit cross-Field exploration

---

## 8. Research Questions

The Field-aware Sprout System creates conditions for studying:

1. **Contribution Patterns**: Do Observers capture more in focused Fields or composite Fields?
2. **Quality Signals**: Do Field-specific Sprouts have higher promotion rates?
3. **Cross-Domain Value**: What patterns emerge in composite Field Sprouts?
4. **Attribution Effects**: Does visible Field credit increase contribution?
5. **Recursive Learning**: How do promoted Sprouts shape future Field responses?
6. **Field Specialization**: Do Fields develop distinct "personalities" through Sprout accumulation?

---

## 9. Conclusion

The Sprout System transforms agent conversations from consumption to cultivation. By capturing valuable agent outputs with full Field-aware provenance, validating through community review, and propagating through attribution-preserving channels, the system creates conditions for exploration that rewards contribution.

Fields provide the bounded contexts that make this tractable. A legal insight belongs in a Legal Field; a technical architecture insight belongs in a Grove Field; a cross-domain governance insight belongs in a composite Field that acknowledges both parents.

Grove serves as the genesis implementation—the first knowledge base to demonstrate the Field-aware pattern. The protocol itself is domain-agnostic: any knowledge base organized into Fields can implement capture, provenance, validation, and attribution.

The recursive loop is complete: systems designed to let humans cultivate agents within bounded Fields are themselves cultivated by humans through use.

---

## Cross-References

- `FIELD_ARCHITECTURE.md` — Complete Field specification
- `TRELLIS.md` — DEX stack documentation
- `specs/dex-object-model.ts` — TypeScript schemas
- Grove Foundation White Paper, "Knowledge Commons" section

---

*Document: Sprout System Technical Specification*
*Version: 2.0 (Field-Aware)*
*Date: December 2024*
*Status: Technical Specification*