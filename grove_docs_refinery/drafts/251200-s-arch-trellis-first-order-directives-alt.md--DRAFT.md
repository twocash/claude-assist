## Rewrite: 251200-s-arch-trellis-first-order-directives-alt.md
### Diagnosis Summary
Source document contains solid architectural thinking but uses legacy terminology ("DEX" vs current "exploration architecture") and needs alignment with current Grove positioning. The core technical concepts are sound but require voice tightening and strategic framing updates.

### Key Changes Made
- Updated "DEX" terminology to "exploration architecture" throughout
- Replaced "Models are seeds" framing with current "Models are seeds, architecture is soil" positioning
- Strengthened the separation of concerns explanations
- Updated Field examples to reflect current Grove focus areas
- Tightened prose by removing redundant explanations and buzzwords
- Aligned terminology with checkpoint (Credits, Terminal, Foundation, etc.)
- Preserved technical accuracy while improving accessibility

### Flags for Review
- Field-specific configuration examples may need validation against current implementation
- Implementation roadmap phases should be verified against current development priorities
- Cross-reference documents mentioned may need updating to match new terminology

---
# The Trellis Architecture: First Order Directives

**Implementing Exploration Architecture Standards**

Author: Jim Calhoun  
Version: 2.0 (Field-Aware)  
Status: Living Constitution  
Context: The Grove Foundation

---

## 1. The Core Philosophy

**Models are seeds. Architecture is soil. The Trellis is the support structure.**

We reject the "Model Maximalist" thesis that assumes value resides solely in LLM scale. Instead, we embrace the exploration architecture thesis: Value comes from the *structure of discovery*.

We are building the **Trellis**—the support framework that enables organic intelligence (human and artificial) to climb, branch, and bear fruit without collapsing into chaos.

*Exploration architecture is to the age of AI what information architecture was to the early web. Information architecture made chaotic web content navigable. Exploration architecture makes AI capability productive.*

---

## 2. The First Order Directive

**Separation of Exploration Logic from Execution Capability.**

- **Exploration Logic (The Trellis):** The declarative definition of *how* we search, *what* constitutes valid insight, and *where* connections form. Domain experts own this logic and define it through configuration (JSON/YAML).

- **Execution Capability (The Vine):** Raw processing power (LLM, RAG, Code Interpreter) that traverses the structure. This component is interchangeable and ephemeral.

**For Engineers & Agents:** Never hard-code exploration paths. If you write imperative code to define a journey, you violate the architecture. Build the *engine* that reads the map; don't build the map into the engine.

---

## 3. The Exploration Architecture Standards

Contributing to Grove means building on these four pillars:

### I. Declarative Sovereignty

- **The Rule:** Domain expertise belongs in configuration, not code.
- **The Test:** Can a non-technical lawyer, doctor, or historian alter refinement engine behavior by editing a schema file, without recompiling? If no, the feature is incomplete.

### II. Capability Agnosticism

- **The Rule:** Architecture must never assume underlying model capability. Today's frontier model becomes tomorrow's local script.
- **The Test:** Does the system break when models hallucinate? The Trellis must catch errors. Architecture functions as the "Superposition Collapse" mechanism—rigid frame that forces probabilistic noise into validated signal.

### III. Provenance as Infrastructure

- **The Rule:** A fact without origin is a bug.
- **The Test:** Every "Sprout" (insight) maintains unbroken attribution back to source—including the Field that scoped its generation. We store *what* is known, *how* it became known (the specific human-AI interaction that collapsed possibility into certainty), and *where* (the Field context).

### IV. Organic Scalability (The Trellis Principle)

- **The Rule:** Structure precedes growth without inhibiting it.
- **The Test:** The system supports "serendipitous connection." A trellis doesn't dictate exact leaf placement but guides general direction. Architecture enables "guided wandering" rather than rigid tunnels.

---

## 4. The Three-Layer Abstraction

The Trellis separates concerns into distinct layers:

### Layer 1: The Engine (The Trellis Frame)

**Status:** Fixed Infrastructure | **Change Velocity:** Low

The engine implements invariant system physics. It doesn't know *what* it refines, only *how* to refine.

- **Superposition Collapse:** Human attention transforms probabilistic AI outputs into validated insights
- **Sprout/Card Mechanics:** Atomic units of insight capture
- **Attribution Chains:** Provenance tracking linking every output to its origin
- **Field Routing:** Scoping all operations to active Field context
- **Memory Persistence:** Accumulated context turning isolated sessions into a "Grove"

### Layer 2: The Field (The Substrate)

**Status:** Variable Input | **Change Velocity:** Medium

Fields contain bounded knowledge domains. Each Field is self-contained workspace with RAG collection, exploration tools, and accumulated insights. The Trellis plants in any Field:

| Field Type | Content | Value Proposition |
|------------|---------|-------------------|
| Grove Research | White papers, specs, architecture | Coherent project knowledge |
| Legal Corpus | Depositions, contracts, case law | Case theory development |
| Academic Literature | Papers, preprints, citations | Synthesis & gap identification |
| Enterprise Knowledge | Slack, Docs, Email archives | Institutional memory preservation |
| Composite Field | Merged from 2+ parent Fields | Cross-domain synthesis |

**Key Field Properties:**
- Self-contained RAG collection (vector-indexed documents)
- Namespaced entities (`legal.contract-clause`, `grove.strategic-insight`)
- Scoped Sprouts (insights belong to originating Field)
- Attribution metadata (creator, contributors, fork lineage)
- Visibility controls (private, organizational, public)

See `FIELD_ARCHITECTURE.md` for complete Field specification.

### Layer 3: The Configuration (The Conditions)

**Status:** Declarative | **Change Velocity:** High

This layer defines "growing conditions" *per Field*. A legal analyst defines "Contradiction" card types; a biologist defines "Replication Error" card types. Configurations are Field-scoped.

- **Declarative Configuration:** Non-developers define behavior through structured data
- **Field-Scoped Configuration:** Each Field can have different Lenses, Journeys, Card Definitions
- **Logic Isolation:** Changing domains (Fields) doesn't require engine code changes

---

## 5. The Configuration Schemas

The Trellis is shaped by four interconnected schemas—the "genetic code" of specific Field deployments:

### A. Card Definition Schema
Defines "Fruit" types—what insights can be harvested in this Field?
- `cardTypes[]` — Valid categories (e.g., "Strategic Insight", "Legal Privilege")
- `validationRules{}` — Logic defining valid cards
- `displayTemplates{}` — UI rendering instructions
- **Namespace:** `{field-slug}.{card-type-id}`

### B. Relationship Schema
Defines "Branching" rules—how nodes connect within Fields?
- `relationTypes[]` — "Supports", "Refutes", "Extends", "Causes"
- `directionality{}` — Directed vs. bi-directional graph edges
- `autoDetection{}` — Prompts for LLM to suggest connections

### C. Journey Schema
Defines "Growth Paths"—curated exploration sequences through Field knowledge.
- `journeys[]` — Ordered node sequences with narrative structure
- `entryConditions{}` — When to suggest each journey
- `completionCriteria{}` — What constitutes journey completion
- **Namespace:** `{field-slug}.{journey-id}`

### D. Lens Schema
Defines "Perspectives"—how Fields speak to different audiences.
- `lenses[]` — Persona configurations with tone and emphasis
- `arcEmphasis{}` — Narrative arc weighting per lens
- `conversionPaths{}` — Next steps appropriate to each lens
- **Namespace:** `{field-slug}.{lens-id}`

---

## 6. Field-Aware Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              THE GROVE PLATFORM                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    LAYER 1: ENGINE (Fixed)                          │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │   │
│  │  │ Sprout   │ │ Session  │ │ RAG      │ │ LLM      │ │ Attrib   │  │   │
│  │  │ Manager  │ │ Manager  │ │ Engine   │ │ Router   │ │ Tracker  │  │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘  │   │
│  └────────────────────────────────┬────────────────────────────────────┘   │
│                                   │                                         │
│                          fieldId required                                   │
│                                   │                                         │
│  ┌────────────────────────────────┼────────────────────────────────────┐   │
│  │                    LAYER 2: FIELDS (Variable)                       │   │
│  │                                │                                    │   │
│  │  ┌──────────────────┐  ┌──────┴───────┐  ┌──────────────────┐      │   │
│  │  │ Grove Foundation │  │ Legal Corpus │  │ Academic Lit     │      │   │
│  │  │ ─────────────────│  │ ─────────────│  │ ─────────────────│      │   │
│  │  │ RAG: grove-docs  │  │ RAG: legal   │  │ RAG: papers      │      │   │
│  │  │ Lenses: 6        │  │ Lenses: 4    │  │ Lenses: 3        │      │   │
│  │  │ Journeys: 5      │  │ Journeys: 8  │  │ Journeys: 12     │      │   │
│  │  │ Sprouts: 127     │  │ Sprouts: 89  │  │ Sprouts: 234     │      │   │
│  │  └──────────────────┘  └──────────────┘  └──────────────────┘      │   │
│  │                                                                     │   │
│  │  ┌──────────────────────────────────────────────────────────┐      │   │
│  │  │ Legal-Grove Composite (merged)                           │      │   │
│  │  │ ─────────────────────────────────────────────────────────│      │   │
│  │  │ RAG: merged legal + grove                                │      │   │
│  │  │ Inherited: legal.*, grove.* entities                     │      │   │
│  │  │ Native: legal-grove.* entities                           │      │   │
│  │  └──────────────────────────────────────────────────────────┘      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                 LAYER 3: CONFIGURATION (Per Field)                  │   │
│  │                                                                     │   │
│  │  Field: grove-foundation                                            │   │
│  │  ├── grove.strategist-lens          (Lens config)                  │   │
│  │  ├── grove.skeptic-lens             (Lens config)                  │   │
│  │  ├── grove.architecture-journey     (Journey config)               │   │
│  │  ├── grove.strategic-insight        (Card Definition)              │   │
│  │  └── grove.technical-deep-dive      (Card Definition)              │   │
│  │                                                                     │   │
│  │  Field: legal-corpus                                                │   │
│  │  ├── legal.litigator-lens           (Lens config)                  │   │
│  │  ├── legal.compliance-journey       (Journey config)               │   │
│  │  ├── legal.contract-clause          (Card Definition)              │   │
│  │  └── legal.precedent-summary        (Card Definition)              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Implementation Roadmap

### Phase 1: Reference Implementation (Current)
*Grove Terminal as single-Field deployment*

Grove Terminal demonstrates exploration architecture mechanics using the "Grove Foundation" Field.
- Validates Sprout/Card lifecycle with Field context
- Proves "Superposition Collapse" user experience
- Schema supports multi-Field (single Field populated)

### Phase 2: Multi-Field Support

Enable multiple Fields per user/organization.
- Field creation flow
- Field switching (clean break = new session)
- Field selector in Terminal interface

### Phase 3: Composite Fields

Enable cross-domain synthesis through explicit Field merging.
- Merge interface for selecting parent Fields
- Namespaced entity inheritance
- Sprout promotion to parent Fields

### Phase 4: Knowledge Commons Integration

Connect Fields to shared marketplace.
- Publish Fields/Lenses/Journeys to marketplace
- Fork public Fields with attribution
- Credit economy for adoption

### Phase 5: Federation

Enable cross-instance Field discovery.
- University A explores University B's public Fields
- Attribution flows across federation boundaries

---

## 8. Terminology Reference

| Term | Definition |
|------|------------|
| **Trellis** | Structural framework (architecture) supporting exploration |
| **Exploration Architecture** | Methodology separating intent from inference |
| **Field** | Bounded knowledge domain with RAG collection and exploration tools |
| **Namespace** | Prefix identifying entity origin (e.g., `legal.`, `grove.`) |
| **Composite Field** | Field created by merging 2+ parent Fields |
| **Trellis Frame** | Engine layer — fixed infrastructure, low change velocity |
| **Substrate** | Field layer — variable input, medium change velocity |
| **Conditions** | Configuration layer — declarative definitions, high change velocity |
| **Vine** | Execution capability (LLM, RAG) — interchangeable and ephemeral |
| **Sprout** | Atomic unit of captured insight, scoped to a Field |
| **Grove** | The platform; also accumulated, refined knowledge across Fields |
| **Observer** | Human applying judgment (pruning) to AI-generated possibilities |
| **Superposition Collapse** | Human attention transforming AI outputs into validated insights |

---

## 9. Cross-References

- **Field Architecture:** See `FIELD_ARCHITECTURE.md` for complete Field specification
- **Sprout System:** See `SPROUT_SYSTEM.md` for insight capture lifecycle
- **Data Models:** See `specs/exploration-object-model.ts` for TypeScript schemas

---

## 10. Conclusion: The Infrastructure of Thought

Grove is infrastructure for exploration. We build the **Trellis Protocol** to create new connections between vast knowledge stores and information types.

Fields are the soil where this protocol grows. Each Field is bounded context—knowledge domain with RAG collection, exploration tools, and accumulated insights. Trellis architecture enables Fields to support organic growth without chaos.

Information Architecture organized the static web. **Exploration Architecture** organizes knowledge in the generative age for productive refinement. By separating exploration logic from execution capability, and by scoping exploration to Fields, we ensure that as models improve and knowledge domains multiply, our Trellis bears better fruit.

---

**Build the Trellis. Plant the Fields. The community brings the seeds.**