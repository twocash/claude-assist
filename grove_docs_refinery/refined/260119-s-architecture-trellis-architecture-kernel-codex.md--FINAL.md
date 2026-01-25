---
author: Jim Calhoun
date: '2026-01-19'
domain: architecture
last_synced: '2026-01-19T22:07:51.766594'
local_file: 260119-s-architecture-trellis-architecture-kernel-codex.md--FINAL.md
notion_id: 2ed780a7-8eef-81ab-9db1-ddf3a5cda584
notion_url: https://www.notion.so/Trellis-Architecture-Kernel-Codex-2ed780a78eef81ab9db1ddf3a5cda584
status: final
title: Trellis Architecture Kernel Codex
type: software
---

# Trellis Architecture Kernel Codex

# **Domain-Agnostic Information Refinement Engine**

*The Standard for Human-Guided Intelligence Augmentation*
December 21, 2025 | Architectural Specification v1.0
**Executive Summary**
The **Trellis Architecture** is a standard that makes any corpus of information navigable and refinable through human attention.
The core thesis: **Models are seeds, architecture is soil.**
Current AI investment focuses on building bigger models (better seeds). Trellis Architecture focuses on the environment that makes those models productive. It provides the **DEX (Declarative Exploration)** layer—the structural support that allows organic intelligence (human and artificial) to climb, branch, and bear fruit without collapsing into chaos.

### The DEX Directive

The architecture implements one First Order Directive: **Separation of Exploration Logic from Execution Capability.**
- **Exploration Logic (The Trellis):** Defined declaratively (JSON/YAML). Owned by domain experts. Sets the growing conditions.
- **Execution Capability (The Vine):** Performed by AI models and humans. Interchangeable and ephemeral.
*Exploration architecture is to the age of AI what information architecture was to the internet. Information architecture made the chaotic early web navigable. Exploration architecture makes AI capability productive.*

## **2. The Three-Layer Abstraction**

The Trellis separates concerns into three distinct layers, creating the standard **DEX Stack**:

### **Layer 1: The Engine (The Trellis Frame)**

*Status: Fixed Infrastructure | Change Velocity: Low*
The engine layer implements the invariant physics of the system. It processes any content type without knowing domain specifics.
- **Superposition Collapse:** Human attention transforms probabilistic AI outputs into validated insights.
- **Sprout/Card Mechanics:** Atomic units of insight capture.
- **Attribution Chains:** Provenance tracking that links every insight back to its source.
- **Memory Persistence:** Accumulated context that turns isolated sessions into persistent knowledge growth.

### **Layer 2: The Corpus (The Substrate)**

*Status: Variable Input | Change Velocity: Medium*
The corpus layer contains raw information. Trellis Architecture works with any substrate:

| **Corpus Type** | **Content** | **Value Proposition** |
|---|---|---|
| **Grove Research** | White papers, specs | Coherent project architecture |
| **Legal Discovery** | Depositions, exhibits | Case theory development |
| **Academic Literature** | Papers, preprints | Synthesis & gap identification |
| **Enterprise Knowledge** | Slack, Docs, Email | Tribal knowledge preservation |

### **Layer 3: The Configuration (The Conditions)**

*Status: Declarative (DEX) | Change Velocity: High*
The **DEX Layer** defines growing conditions. A legal analyst defines "Contradiction" nutrients; a biologist defines "Replication Error" nutrients.
- **Configuration is Declarative:** Non-developers define behavior through structured data files.
- **Logic Isolation:** Changing domains doesn't require touching engine code.

## **3. The DEX Configuration Schemas**

Four interconnected schemas shape the Trellis—the genetic code of each deployment.

### **A. Annotation Schema**

Defines insight types that can be harvested.

| **Field** | **Description** |
|---|---|
| annotationTypes[] | Valid categories (e.g., "Strategic Insight", "Legal Privilege") |
| validationRules{} | Logic defining valid annotations |
| displayTemplates{} | UI rendering instructions |

- **Example (Legal):** "Contradicts Testimony" (Requires citation + timestamp)
- **Example (Science):** "Methodology Gap" (Requires reference to control group)

### **B. Relationship Schema**

Defines how nodes connect.

| **Field** | **Description** |
|---|---|
| relationTypes[] | "Supports", "Refutes", "Extends", "Causes" |
| directionality{} | Directed vs. Bi-directional graph edges |
| autoDetection{} | Prompts for AI to suggest connections |

### **C. Processing Flow Schema**

Defines the insight lifecycle.

| **Field** | **Description** |
|---|---|
| stages[] | Sprout → Sapling → Tree → Grove |
| transitions{} | Rules for moving between stages (e.g., "Requires 2 Approvals") |
| outputIntegration{} | Where insights flow (Knowledge Commons, Case File) |

### **D. Display Schema**

Defines how the Trellis appears to the Observer.

| **Field** | **Description** |
|---|---|
| cardTemplates{} | Visual layouts for content types |
| densityLevels{} | Information density (Compact vs. Detailed) |
| visualizations[] | Graph view, Timeline view, List view |

## **4. Architectural Principles (The DEX Standard)**

Any contribution to the codebase must adhere to these First Order Directives.

### **Principle 1: Capability Agnosticism (The Vine is not the Trellis)**

The architecture never assumes specific AI capabilities. Today's frontier model is tomorrow's local script.
- *The Test:* If the model hallucinates, the Trellis contains it without breaking. Structure provides validity, not the model.

### **Principle 2: Declarative Sovereignty**

Domain expertise belongs in configuration, not code.
- *The Directive:* Never hard-code exploration paths. Build the engine that reads the map; don't build the map into the engine.

### **Principle 3: Provenance as Infrastructure**

In the Trellis, a fact without a root is a weed.
- *The Mechanism:* Attribution chains are mandatory. We track who collapsed the superposition and when.

### **Principle 4: Human-AI Symbiosis (The Observer)**

The system requires human-in-the-loop for Superposition Collapse.
- *The Role:* AI generates possibilities (growth); humans apply judgment (pruning). The Trellis supports both.

## **5. Implementation Roadmap**

### **Phase 1: Reference Implementation (The Grove Terminal)**

Current State
Grove Terminal serves as the reference Trellis implementation, demonstrating DEX mechanics using distributed AI research corpus.
- Validates Sprout/Card lifecycle.
- Proves Superposition Collapse UX.

### **Phase 2: Configuration Extraction (DEXification)**

Extract hardcoded behaviors into DEX Schemas.
- Convert types.ts definitions into schema.json files.
- Implement dynamic SchemaLoader.

### **Phase 3: The Trellis Builder (Admin UI)**

Enable non-technical experts to build their own Trellises.
- Visual editor for Annotation and Relationship schemas.
- No-code adjustment of processing flows.

### **Phase 4: Multi-Domain Deployment**

Deploy Trellis into new domains.
- **Legal Trellis:** Pilot with partner law firm.
- **Academic Trellis:** Pilot with university research group.
