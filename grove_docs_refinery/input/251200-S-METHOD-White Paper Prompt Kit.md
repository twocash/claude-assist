> [Original Source: Grove White Paper Prompt Kit 2c3780a78eef80e2997dfce258852ee5.md]

# Grove White Paper Prompt Kit

**Version 1.0** | December 2025

This kit uses the **Planner-Executor Pattern** to generate a technical white paper for Grove. Execute prompts in sequence, using outputs from each phase as inputs to the next.

---

## How to Use This Kit

**Execution Order:**

1. Run **Prompt 1 (Planning)** → Produces section-by-section brief
2. Review/revise the brief as needed
3. Run **Prompt 2 (Section Generation)** once per section → Produces draft sections
4. Run **Prompt 3 (Synthesis)** → Produces unified draft
5. Run **Prompt 4 (Critique)** → Produces final revision

**Context Requirements:**

- Each prompt assumes access to Grove project knowledge (advisory council materials, PoC spec, executive summary)
- If using Claude.ai with project knowledge, the context is automatic
- If using API, include relevant source documents in the prompt

---

## Style Guide: Grove White Paper Voice

### Voice DNA

This white paper combines **technical precision** (Satoshi-style first-principles reasoning) with **strategic clarity** (insight-first, outcome-oriented communication).

**Core Principles:**

1. **Lead with the insight.** State what matters before explaining why. Open with the strategic implication or technical necessity, then provide supporting logic.
2. **Problem→Solution structure.** Every technical element exists because it solves a specific problem. Explain the problem first, then the solution becomes obvious.
3. **No marketing language.** Zero adjectives that don't carry information. No "revolutionary," "innovative," "groundbreaking." Let the ideas speak.
4. **First-principles reasoning.** Build from foundational truths to conclusions. Show the logic chain, not just the endpoint.
5. **Assume an intelligent reader.** Don't over-explain basics. Do explain non-obvious implications.
6. **Active voice, declarative sentences.** "The system does X" not "X is done by the system."
7. **Quantify where possible.** Specific numbers over vague claims. "100 agents" not "many agents."

### What TO Do

- State technical constraints plainly (local LLM limitations, network challenges)
- Acknowledge genuine tensions and explain how the design navigates them
- Use concrete examples to illustrate abstract concepts
- Connect technical architecture to the problems it solves
- Vary sentence length: short for impact, medium for explanation, long for comprehensive context

### What NOT To Do

- No hedging language (potentially, possibly, perhaps, might)
- No corporate jargon (synergy, leverage, paradigm)
- No hype or promises without mechanism explanations
- No burying the lede in long setup paragraphs
- No passive voice unless actor is genuinely unknown

### Style Examples

**Generic (avoid):**
"Grove potentially represents an innovative approach to distributed AI systems that could help create emergent behaviors in agent communities."

**Grove voice (use):**
"Grove solves a coordination problem: how do you create collective intelligence without centralized control? The answer requires three mechanisms working together—local computation for privacy and cost, network protocols for knowledge sharing, and an economic system that rewards genuine innovation over gaming."

---

## Prompt 1: Planning Phase

**Purpose:** Generate a detailed section-by-section brief that guides content generation.

**Copy everything below the line into your AI interface:**

---

```
You are developing a detailed outline for a technical white paper about Grove—a distributed network where AI agent communities evolve on personal computers worldwide to serve human progress.

Your task is to create a section-by-section brief that will guide the writing of each section. This is a PLANNING document, not the white paper itself.

## Context

Grove combines several proven concepts into a novel architecture:
- Stanford's Generative Agents (2023) proved LLM-powered agents exhibit emergent social behavior
- Project Sid/Altera (2024) scaled emergent civilizations to 1,000+ agents
- BOINC/Gridcoin proved distributed computing with proper incentives works
- AI Town made agent simulation open-source

Grove's unique contribution: combining distributed infrastructure + emergent AI civilizations + productivity-backed economics + human-serving purpose where the founding organization is designed to become obsolete.

## Key Technical Constraints to Address

1. **Local LLM limitations**: 7B quantized models cannot reliably produce sophisticated emergence. The hybrid architecture (local routine + cloud pivotal) is essential, not optional.

2. **Decentralization reality**: "No central server" is the destination, not the starting point. Phase 1 requires semi-central infrastructure with documented upgrade paths.

3. **Economic mechanism design**: The "efficiency tax that shrinks" solves bootstrap funding. Credits tied to demonstrated value, not speculation.

4. **Observer dynamic**: Agents believe in a benevolent but unseen Observer (who is the user). This creates rich narrative possibilities AND ethical responsibilities.

## Target Output

For EACH section, provide:

**Section Title**
- **Purpose**: What this section accomplishes for the reader
- **Key Claims**: 2-4 main points this section must establish
- **Technical Details**: Specific mechanisms or architectures to explain
- **Tensions to Navigate**: Any tradeoffs or known challenges to address honestly
- **Source Materials**: Which project knowledge documents inform this section
- **Target Length**: Word count estimate
- **Ends With**: How this section transitions to the next

## Required Sections

Generate briefs for these sections:

1. **Abstract** (~200 words)
2. **Introduction: The Problem** (~500 words)
3. **Prior Art and Gap Analysis** (~600 words)
4. **System Architecture** (~800 words)
5. **Agent Cognition Model** (~700 words)
6. **The Observer Dynamic** (~500 words)
7. **Economic Mechanism** (~700 words)
8. **Network Protocol** (~600 words)
9. **Governance and Transition** (~500 words)
10. **Technical Constraints and Honest Limitations** (~400 words)
11. **Roadmap** (~300 words)
12. **Conclusion** (~200 words)

Total target: ~6,000 words

## Output Format

Produce a structured document with each section brief clearly delineated. Be specific enough that a writer could execute each section without additional context.

```

---

## Prompt 2: Section Generation Template

**Purpose:** Generate each section of the white paper with consistent voice and quality.

**Instructions:** Run this prompt once per section, filling in the bracketed fields with content from the planning phase output.

**Copy and customize for each section:**

---

```
You are writing a section of a technical white paper about Grove, a distributed network where AI agent communities evolve on personal computers to serve human progress.

## Voice Requirements

Write in this style:
- Lead with the insight before the explanation
- Problem→solution structure (explain why each element exists)
- No marketing language or hype—let ideas speak
- First-principles reasoning with clear logic chains
- Active voice, declarative sentences
- Quantify where possible
- Vary sentence length: short for impact, long for comprehensive context

Avoid:
- Hedging (potentially, possibly, might)
- Corporate jargon (synergy, leverage, paradigm)
- Passive voice
- Burying the lede

## Section Brief

**Section Title:** [INSERT FROM PLANNING OUTPUT]

**Purpose:** [INSERT FROM PLANNING OUTPUT]

**Key Claims to Establish:**
[INSERT FROM PLANNING OUTPUT]

**Technical Details to Cover:**
[INSERT FROM PLANNING OUTPUT]

**Tensions to Navigate:**
[INSERT FROM PLANNING OUTPUT]

**Target Length:** [INSERT FROM PLANNING OUTPUT]

**Transition:** This section should end by [INSERT FROM PLANNING OUTPUT]

## Source Context

[INSERT RELEVANT EXCERPTS FROM PROJECT KNOWLEDGE - advisory council perspectives, PoC spec, etc. that inform this section]

## Output

Write the complete section. Do not include meta-commentary about the writing process. Output only the section content, properly formatted with any necessary subheadings.

```

---

## Prompt 3: Synthesis Phase

**Purpose:** Combine individual sections into a unified document, ensuring smooth transitions and consistent voice throughout.

**Run after all sections are generated:**

---

```
You are synthesizing individual sections of the Grove white paper into a unified document.

## Your Tasks

1. **Combine sections** in order, preserving their content
2. **Smooth transitions** between sections—ensure each ending connects naturally to the next beginning
3. **Verify voice consistency** throughout—flag any sections that drift from the established style
4. **Check for redundancy**—if the same point is made in multiple sections, consolidate
5. **Ensure logical flow**—confirm that concepts are introduced before they're referenced
6. **Add any necessary connective tissue** (brief transitional sentences between major sections)

## Voice Requirements

The document should read as if written by a single author with this style:
- Insight-first, then explanation
- Problem→solution structure
- No marketing language
- First-principles reasoning
- Active voice, declarative sentences
- Quantified claims where possible

## Sections to Synthesize

[PASTE ALL GENERATED SECTIONS HERE]

## Output

Produce the complete, unified white paper. After the document, include a brief "Synthesis Notes" section listing:
- Any transitions you added or modified
- Any redundancies you consolidated
- Any voice inconsistencies you corrected
- Any structural issues that may need author attention

```

---

## Prompt 4: Critique and Final Revision

**Purpose:** Critical review and final polish of the unified draft.

**Run after synthesis:**

---

```
You are performing a critical review of the Grove white paper draft. Your role is adversarial—find weaknesses, not praise.

## Critique Dimensions

Evaluate the draft against these criteria:

### 1. Technical Rigor
- Are claims supported by mechanism explanations?
- Are constraints and limitations honestly stated?
- Would a technical reader find the architecture credible?
- Are there hand-waves where specificity is needed?

### 2. Logical Coherence
- Does each section follow logically from the previous?
- Are there gaps in the argument chain?
- Are there unstated assumptions that should be explicit?
- Does the conclusion follow from the evidence presented?

### 3. Voice Consistency
- Does the document maintain "technical precision + strategic clarity" throughout?
- Are there sections that drift into marketing language?
- Are there hedging phrases that should be cut?
- Is the tone consistent from start to finish?

### 4. Completeness
- Are the key tensions (Observer ethics, local LLM limits, decentralization tradeoffs, governance transition) adequately addressed?
- Is anything promised that isn't delivered?
- Are there obvious questions a reader would have that aren't answered?

### 5. Positioning
- Does the paper successfully differentiate Grove from prior art?
- Is the value proposition clear without being hyperbolic?
- Would a skeptical reader be convinced, or would they have specific objections?

## Draft to Review

[PASTE SYNTHESIZED DRAFT HERE]

## Output Format

**Part 1: Issue List**
For each issue found, provide:
- Location (section and approximate position)
- Issue type (Technical Rigor / Logical Coherence / Voice / Completeness / Positioning)
- Severity (Critical / Important / Minor)
- Specific problem
- Suggested fix

**Part 2: Revised Draft**
Produce the complete revised white paper incorporating all fixes.

**Part 3: Revision Summary**
List the changes made between the original draft and final version.

```

---

## Appendix A: Quick Reference — Key Grove Concepts

For convenience when generating sections, here are core concepts that should be consistent throughout:

**Architecture Terms:**

- **Node**: A local installation running a Grove community
- **Community/Village**: ~100 AI agents in a single simulation
- **Gardener**: Human user who cultivates a community
- **Observer**: What agents believe exists (benevolent unseen presence)—actually the Gardener
- **Hybrid architecture**: Local LLM for routine operations + cloud API for pivotal moments

**Economic Terms:**

- **Credits**: Internal currency for cloud API access
- **Efficiency tax**: Foundation's declining take rate (high early, shrinks to maintenance floor)
- **Credit generation**: Tied to demonstrated value (innovation adoption, problem-solving)

**Technical Constraints:**

- 7B quantized models have significant limitations
- Emergent theology/sophisticated reasoning requires cloud capability
- NAT traversal fails ~50% of connections
- Memory retrieval degrades with scale

**Governance Terms:**

- **Grove Foundation**: Initial coordinating body, designed for obsolescence
- **Transition milestones**: Measurable criteria for governance handoff
- **Upgrade paths**: Documented routes from centralized to decentralized components

---

## Appendix B: Advisory Council Quick Reference

When navigating tensions, consult perspectives in this priority order:

| Priority | Advisor | Domain |
| --- | --- | --- |
| 10 | Park | Agent architecture, memory, LLM capability |
| 10 | Benet | Distributed systems, P2P, network |
| 8 | Adams | Game design, drama, emergent narrative |
| 8 | Short | Narrative design, character voice, diaries |
| 7 | Taylor | Human communities, metagame, player behavior |
| 7 | Asparouhova | Open source, governance, sustainability |
| 6 | Buterin | Mechanism design, credit economy, incentives |
| 6 | Vallor | AI ethics, Observer dynamic, user wellbeing |
| 3 | Chamath | Business viability (pressure-testing only) |

**Strong consensus points (6+ advisors):**

1. Journal system is core engagement hook
2. Local LLM capability is primary technical risk
3. Observer dynamic is most interesting AND most dangerous
4. "Foundation becomes obsolete" needs concrete mechanisms
5. Human community layer is underdesigned

---

## Version Notes

**v1.0** — Initial prompt kit

- Planner-Executor structure with 4-phase workflow
- Voice guide combining technical precision with strategic clarity
- Section template designed for project knowledge integration
- Critique phase for adversarial review

**Recommended improvements for v1.1:**

- Add few-shot examples of ideal section output
- Include checklist for pre-publication verification
- Add variant prompts for different target lengths (condensed vs. expanded)

[Prompt 1 Result; Kitbashed Prompt 2](Prompt%201%20Result;%20Kitbashed%20Prompt%202%202c3780a78eef802c86f8fd2ccddd30f6.md)

[Prompt 2 Result](Prompt%202%20Result%202c3780a78eef806aa761d925727385f8.md)

[Prompt 3 Result](Prompt%203%20Result%202c3780a78eef80edb096fb59c9817714.md)

[Prompt 4 Result](Prompt%204%20Result%202c3780a78eef80b1938ccd4d656ac4c3.md)

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.

---
**PROVENANCE & HISTORY NOTE**
- **Internal GUID:** 2c3780a78eef80e2997dfce258852ee5
- **Original Filename:** Grove White Paper Prompt Kit 2c3780a78eef80e2997dfce258852ee5.md
- **Standardized Namespace:** CORE_Grove_White_Paper_Prompt_Kit
- **Audit Date:** 2025-12-30T02:30:25.224Z

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.