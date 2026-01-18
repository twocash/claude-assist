# Grove Foundation Loop — Sprint Methodology

A structured approach to software development implementing **Grove's exploration architecture** principles. Produces 8 planning artifacts, embeds automated testing as continuous process, and enables clean handoff to execution agents.

## Core Principles

### 1. Grove Architecture Alignment

The Foundation Loop implements Grove's exploration architecture standards:

| Principle | Implementation |
|-----------|----------------|
| **Declarative Sovereignty** | Domain logic in config (JSON/YAML), not code |
| **Capability Agnosticism** | Structure provides validity, not the model |
| **Provenance as Infrastructure** | Attribution chains on all artifacts |
| **Organic Scalability** | Structure precedes growth but doesn't inhibit it |

**The First Order Directive:** *Separation of Exploration Logic from Execution Capability.*
- Build the engine that reads the map; do not build the map into the engine.
- If you're hardcoding domain behavior, you're violating the architecture.

### 2. Testing as Process (Not Phase)

Testing is not a phase at the end—it's a continuous process integrated throughout:

```
Code Change → Tests Run → Report to Health → Unified Dashboard
                                                    ↓
                                          Pass ✅ Ship / Fail 🚫 Block
```

**Key insight:** E2E tests verify behavior; Health system tracks data integrity. Both feed into a unified view of system health.

### 3. Grove Architecture Rules

**CRITICAL:** When working on Grove codebase, enforce these rules:

| Rule | Violation | Correct Approach |
|------|-----------|------------------|
| No new handlers | Adding `handleFoo()` callback | Declarative config triggers action |
| No hardcoded behavior | `if (lens === 'engineer')` | Config defines lens-specific behavior |
| Behavior tests | Testing `toHaveClass('translate-x-0')` | Testing `toBeVisible()` |
| State machines | Imperative state updates | XState declarative transitions |

See `references/grove-architecture-rules.md` for full guidance.