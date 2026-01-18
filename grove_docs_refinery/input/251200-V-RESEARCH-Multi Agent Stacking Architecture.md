> [Original Source: Multi-Agent Stacking Architecture Research 2c7780a78eef81bfba94c37cbcefa0fe.md]

# Multi-Agent "Stacking" Architecture Research

**Source:** Long Hua Tu (@long.hua.tu on TikTok) - developer/content creator focusing on human-in-the-loop AI workflows

**Captured:** December 12, 2025

---

## The Core Concept

Using one AI (Gemini 2.0) to supervise and prompt another AI (coding agent) - known in research as **Multi-Agent Systems (MAS)** or **Hierarchical LLM Architectures**.

---

## Research Terms to Explore

### 1. Agentic Workflows & Orchestration

Direct mapping to "stacking" pattern:

**Orchestrator (Gemini 2.0):** Handles high-level reasoning, planning, visual context. Understands *what* needs to be done and *why*.

**Worker (Cursor/Windsurf):** Handles implementation details, syntax, file manipulation.

Research terms: "Orchestrator-Worker pattern" or "Agentic Design Patterns" (popularized by Andrew Ng)

### 2. Meta-Prompting

Technique where an AI generates the optimal prompt for another AI. Long Hua Tu asks Gemini to help "think through how to correctly prompt" the coding bot - reducing human error and ensuring unambiguous instructions.

Research terms: "Automated Prompt Optimization" or "Meta-Prompting"

### 3. Co-LLM / Collaborative LLMs

General-purpose model guides a specialized model:

- General model (Gemini): "world knowledge" + multimodal screen vision
- Specialized model: "domain knowledge" of specific codebase

"Stacking" leverages both strengths without context switching.

Research terms: "Co-LLM" or "Collaborative Multi-Agent Frameworks"

---

## Why This Pattern Works

User noted it felt like "having a developer over my shoulder" - effectively created a **Driver-Navigator pair programming setup**:

- **Navigator** (Gemini 2.0 + Human): Reviews screen, spots high-level issues, directs strategy
- **Driver** (Coding Agent): Focuses on writing code and syntax

---

## Grove Relevance

This pattern maps directly to several Grove design elements:

### Hybrid Architecture Parallel

Local 7B models (routine behaviors) + cloud frontier models (complex reasoning) mirrors the orchestrator-worker split. Park's technical constraints about when to invoke cloud compute align with this pattern.

### Agent Coordination Implications

How Grove agents might coordinate within civilizations - some agents developing orchestration capabilities while others specialize in execution.

### Human-Agent Interface Model

The Driver-Navigator paradigm could inform how Observers interact with their Grove civilizations - strategic oversight while agents handle implementation.

### Meta-Communication Potential

Agents potentially developing meta-prompting capabilities to coordinate more effectively with each other.

---

## Reference Video

"Future-Proof Coding Agents" - Bill Chen & Brian Fioca, OpenAI

Discusses "anatomy of a coding agent" and **harnesses** - structures allowing interchangeable sub-agents, similar to stacking workflow. Highly relevant to Grove's hybrid architecture design.

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.

---
**PROVENANCE & HISTORY NOTE**
- **Internal GUID:** 2c7780a78eef81bfba94c37cbcefa0fe
- **Original Filename:** Multi-Agent Stacking Architecture Research 2c7780a78eef81bfba94c37cbcefa0fe.md
- **Standardized Namespace:** RESEARCH_Multi_Agent_Stacking_Architecture
- **Audit Date:** 2025-12-30T02:30:25.223Z

*Note: This document was processed for an update, but no changes were made.*

---
© 2025 The Grove Foundation / Jim Calhoun. All rights reserved.