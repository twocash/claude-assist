
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

<table header-row="true">
	<tr>
		<td>**Corpus Type**</td>
		<td>**Content**</td>
		<td>**Value Proposition**</td>
	</tr>
	<tr>
		<td>**Grove Research**</td>
		<td>White papers, specs</td>
		<td>Coherent project architecture</td>
	</tr>
	<tr>
		<td>**Legal Discovery**</td>
		<td>Depositions, exhibits</td>
		<td>Case theory development</td>
	</tr>
	<tr>
		<td>**Academic Literature**</td>
		<td>Papers, preprints</td>
		<td>Synthesis &amp; gap identification</td>
	</tr>
	<tr>
		<td>**Enterprise Knowledge**</td>
		<td>Slack, Docs, Email</td>
		<td>Tribal knowledge preservation</td>
	</tr>
</table>

### **Layer 3: The Configuration (The Conditions)**

*Status: Declarative (DEX) | Change Velocity: High*
The **DEX Layer** defines growing conditions. A legal analyst defines "Contradiction" nutrients; a biologist defines "Replication Error" nutrients.
- **Configuration is Declarative:** Non-developers define behavior through structured data files.
- **Logic Isolation:** Changing domains doesn't require touching engine code.

## **3. The DEX Configuration Schemas**

Four interconnected schemas shape the Trellis—the genetic code of each deployment.

### **A. Annotation Schema**

Defines insight types that can be harvested.

<table header-row="true">
	<tr>
		<td>**Field**</td>
		<td>**Description**</td>
	</tr>
	<tr>
		<td>annotationTypes[]</td>
		<td>Valid categories (e.g., "Strategic Insight", "Legal Privilege")</td>
	</tr>
	<tr>
		<td>validationRules{}</td>
		<td>Logic defining valid annotations</td>
	</tr>
	<tr>
		<td>displayTemplates{}</td>
		<td>UI rendering instructions</td>
	</tr>
</table>

- **Example (Legal):** "Contradicts Testimony" (Requires citation + timestamp)
- **Example (Science):** "Methodology Gap" (Requires reference to control group)

### **B. Relationship Schema**

Defines how nodes connect.

<table header-row="true">
	<tr>
		<td>**Field**</td>
		<td>**Description**</td>
	</tr>
	<tr>
		<td>relationTypes[]</td>
		<td>"Supports", "Refutes", "Extends", "Causes"</td>
	</tr>
	<tr>
		<td>directionality{}</td>
		<td>Directed vs. Bi-directional graph edges</td>
	</tr>
	<tr>
		<td>autoDetection{}</td>
		<td>Prompts for AI to suggest connections</td>
	</tr>
</table>

### **C. Processing Flow Schema**

Defines the insight lifecycle.

<table header-row="true">
	<tr>
		<td>**Field**</td>
		<td>**Description**</td>
	</tr>
	<tr>
		<td>stages[]</td>
		<td>Sprout → Sapling → Tree → Grove</td>
	</tr>
	<tr>
		<td>transitions{}</td>
		<td>Rules for moving between stages (e.g., "Requires 2 Approvals")</td>
	</tr>
	<tr>
		<td>outputIntegration{}</td>
		<td>Where insights flow (Knowledge Commons, Case File)</td>
	</tr>
</table>

### **D. Display Schema**

Defines how the Trellis appears to the Observer.

<table header-row="true">
	<tr>
		<td>**Field**</td>
		<td>**Description**</td>
	</tr>
	<tr>
		<td>cardTemplates{}</td>
		<td>Visual layouts for content types</td>
	</tr>
	<tr>
		<td>densityLevels{}</td>
		<td>Information density (Compact vs. Detailed)</td>
	</tr>
	<tr>
		<td>visualizations[]</td>
		<td>Graph view, Timeline view, List view</td>
	</tr>
</table>

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
