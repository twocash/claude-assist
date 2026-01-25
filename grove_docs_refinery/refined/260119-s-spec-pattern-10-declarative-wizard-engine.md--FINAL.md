---
author: Jim Calhoun
date: '2026-01-19'
domain: spec
last_synced: '2026-01-19T22:07:22.705394'
local_file: 260119-s-spec-pattern-10-declarative-wizard-engine.md--FINAL.md
notion_id: 2ed780a7-8eef-816d-a7d8-f158b9aa8534
notion_url: https://www.notion.so/Pattern-10-Declarative-Wizard-Engine-2ed780a78eef816da7d8f158b9aa8534
status: final
title: 'Pattern 10: Declarative Wizard Engine'
type: software
---

# Pattern 10: Declarative Wizard Engine

**Status:** Proposed
**Derived From:** CustomLensWizard analysis
**Sprint:** TBD (wizard-engine-v1)

## Problem Statement

Grove's exploration architecture requires personalized content flows through multi-step user experiences:
- **Custom Lenses** — Persona-based content filtering (live in Terminal)
- **Custom Journeys** — Observer-defined exploration paths (planned)
- **Onboarding Flows** — Guided first-time experience (planned)
- **Preference Wizards** — Settings configuration (future)
Currently, CustomLensWizard hard-codes its flow logic in TypeScript. Each new wizard would require:
- New React components per step
- Duplicate state management
- Separate analytics integration
- Repeated flow logic
This violates **Declarative Sovereignty**—domain experts cannot create new wizards without engineering involvement.

## Solution: Declarative Wizard Engine

Separate wizard *definition* (JSON schema) from wizard *execution* (React engine).

```plain text
┌─────────────────────────────────────────────────────────────────┐
│                    DECLARATIVE WIZARD ARCHITECTURE               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  wizard-schema.json          WizardEngine.tsx                    │
│  ┌──────────────────┐       ┌────────────────────────────────┐  │
│  │ {                │       │ function WizardEngine({        │  │
│  │   "id": "...",   │──────▶│   schema,                      │  │
│  │   "steps": [...] │       │   onComplete,                  │  │
│  │ }                │       │   onCancel                     │  │
│  └──────────────────┘       │ }) { ... }                     │  │
│                             └────────────────────────────────┘  │
│                                         │                        │
│                    ┌────────────────────┼────────────────────┐  │
│                    ▼                    ▼                    ▼  │
│           ┌──────────────┐    ┌──────────────┐    ┌───────────┐│
│           │ ConsentStep  │    │ ChoiceStep   │    │ TextStep  ││
│           └──────────────┘    └──────────────┘    └───────────┘│
│           ┌──────────────┐    ┌──────────────┐    ┌───────────┐│
│           │GenerationStep│    │SelectionStep │    │ConfirmStep││
│           └──────────────┘    └──────────────┘    └───────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Current State Analysis

The existing CustomLensWizard already has **semi-declarative structure**. In `InputStep.tsx`:

```typescript
const STEPCONFIG: Record<string, {
  question: string;
  subtext?: string;
  options: OptionConfig[];
  inputKey: keyof UserInputs;
  otherKey?: keyof UserInputs;
  progress: number;
}> = {
  'input-motivation': {
    question: 'What brings you to thinking about AI infrastructure?',
    options: MOTIVATIONOPTIONS,
    inputKey: 'motivation',
    otherKey: 'motivationOther',
    progress: 1
  },
  // ... more steps
};
```

**What works:** Config-driven step rendering, option arrays, progress tracking.
**What's missing:** Flow logic still hard-coded in component (`handleInputComplete` with conditionals), step types mixed together, no schema separation.

## Wizard Schema Specification

### Top-Level Structure

```typescript
interface WizardSchema {
  id: string;                    // Unique wizard identifier
  version: string;               // Schema version
  title: string;                 // Shown in header
  description?: string;          // Optional subtitle

  steps: WizardStepSchema[];     // Ordered step definitions
  initialStep: string;           // First step ID

  generation?: {                 // AI generation config (if applicable)
    endpoint: string;
    method: 'POST';
    inputMapping: Record<string, string>;
    outputKey: string;
  };

  output: {
    type: string;                // Output type name
    transform?: string;          // Transform function name
  };

  analytics?: {
    startEvent: string;
    stepEvent: string;
    completeEvent: string;
    abandonEvent: string;
  };

  theme?: {
    primaryColor: string;
    accentColor: string;
  };
}
```

### Step Types

```typescript
type WizardStepSchema =
  | ConsentStepSchema
  | ChoiceStepSchema
  | TextStepSchema
  | GenerationStepSchema
  | SelectionStepSchema
  | ConfirmationStepSchema;

// Base fields all steps share
interface BaseStepSchema {
  id: string;
  type: string;
  title?: string;
  progress?: number;
}

// Consent/Privacy step
interface ConsentStepSchema extends BaseStepSchema {
  type: 'consent';
  headline: string;
  guarantees: Array<{
    icon: string;
    title: string;
    description: string;
  }>;
  acceptLabel: string;
  acceptAction: StepAction;
  cancelLabel?: string;
}

// Single choice step
interface ChoiceStepSchema extends BaseStepSchema {
  type: 'choice';
  question: string;
  subtext?: string;
  options: Array<{
    value: string;
    label: string;
    description?: string;
  }>;
  inputKey: string;
  allowOther?: boolean;
  otherKey?: string;
  next: ConditionalAction;
}

// Free text step
interface TextStepSchema extends BaseStepSchema {
  type: 'text';
  question: string;
  subtext?: string;
  inputKey: string;
  placeholder?: string;
  maxLength?: number;
  optional?: boolean;
  next: StepAction;
}

// AI generation step
interface GenerationStepSchema extends BaseStepSchema {
  type: 'generation';
  loadingMessage: string;
  errorMessage: string;
  retryLabel: string;
  next: StepAction;
}

// Selection from generated options
interface SelectionStepSchema extends BaseStepSchema {
  type: 'selection';
  headline: string;
  subtext?: string;
  optionsKey: string;
  outputKey: string;
  cardRenderer: string;
  refineLabel?: string;
  refineAction?: StepAction;
  next: StepAction;
}

// Confirmation step
interface ConfirmationStepSchema extends BaseStepSchema {
  type: 'confirmation';
  headline: string;
  displayKey: string;
  benefits: string[];
  privacyReminder?: string;
  confirmLabel: string;
  next: { complete: true };
}
```

### Flow Actions

```typescript
type StepAction =
  | { next: string }      // Go to step by ID
  | { complete: true }    // Finish wizard
  | { exit: true };       // Cancel wizard

interface ConditionalAction {
  conditions?: Array<{
    if: string;           // Expression: "motivation === 'worried'"
    then: string;         // Step ID
  }>;
  default: string;        // Fallback step ID
}
```

## Example: Custom Lens Wizard Schema

```json
{
  "id": "custom-lens-wizard",
  "version": "1.0",
  "title": "Create Your Personal Lens",

  "steps": [
    {
      "id": "privacy",
      "type": "consent",
      "headline": "Before we begin — a promise",
      "guarantees": [
        {
          "icon": "lock",
          "title": "Everything stays in your browser",
          "description": "Your answers are encrypted locally. We never see them."
        },
        {
          "icon": "lock",
          "title": "No accounts. No tracking.",
          "description": "Your lens is stored only in this browser."
        },
        {
          "icon": "sparkles",
          "title": "AI generates, you control",
          "description": "We'll create 3 options for you to choose from."
        }
      ],
      "acceptLabel": "I understand — let's build my lens",
      "acceptAction": { "next": "motivation" }
    },
    {
      "id": "motivation",
      "type": "choice",
      "question": "What brings you to thinking about AI infrastructure?",
      "inputKey": "motivation",
      "allowOther": true,
      "otherKey": "motivationOther",
      "options": [
        { "value": "worried-about-ai", "label": "I'm worried about where AI is heading" },
        { "value": "researching-distributed-systems", "label": "I'm researching distributed systems" },
        { "value": "someone-sent-link", "label": "Someone sent me this link" },
        { "value": "investment-opportunities", "label": "I'm looking for investment opportunities" },
        { "value": "just-curious", "label": "Just curious" },
        { "value": "other", "label": "Something else..." }
      ],
      "next": {
        "conditions": [
          { "if": "motivation === 'worried-about-ai'", "then": "concerns" }
        ],
        "default": "outlook"
      },
      "progress": 1
    },
    {
      "id": "concerns",
      "type": "choice",
      "question": "What conc
// ... (truncated)
```

## Example: Custom Journey Wizard (New Capability)

```json
{
  "id": "custom-journey-wizard",
  "version": "1.0",
  "title": "Design Your Exploration Path",

  "steps": [
    {
      "id": "intro",
      "type": "consent",
      "headline": "Create a journey that fits your curiosity",
      "guarantees": [
        {
          "icon": "compass",
          "title": "Your path, your pace",
          "description": "Choose what to explore and in what order."
        },
        {
          "icon": "bookmark",
          "title": "Save your progress",
          "description": "Pick up where you left off anytime."
        }
      ],
      "acceptLabel": "Let's design my journey",
      "acceptAction": { "next": "goal" }
    },
    {
      "id": "goal",
      "type": "choice",
      "question": "What do you want to understand about Grove?",
      "inputKey": "goal",
      "options": [
        { "value": "how-it-works", "label": "How the technology works" },
        { "value": "why-it-matters", "label": "Why this matters for AI's future" },
        { "value": "how-to-participate", "label": "How I can participate" },
        { "value": "investment-case", "label": "The investment opportunity" },
        { "value": "compare-alternatives", "label": "How it compares to alternatives" }
      ],
      "next": { "default": "depth" },
      "progress": 1
    },
    {
      "id": "depth",
      "type": "choice",
      "question": "How deep do you want to go?",
      "inputKey": "depth",
      "options": [
        { "value": "overview", "label": "Quick overview (10 min)" },
        { "value": "moderate", "label": "Solid understanding (30 min)" },
        { "value": "deep", "label": "Deep dive (60+ min)" }
      ],
      "next": { "default": "generating" },
      "progress": 2
    },
    {
      "id": "generating",
      "type": "generation",
      "loadingMessage": "Mapping your exploration path...",
      "errorMessage": "Couldn't generate jou
// ... (truncated)
```

## Implementation Architecture

### File Structure

```plain text
src/
├── core/
│   └── wizard/
│       ├── schema.ts           # TypeScript types
│       ├── engine.ts           # State machine logic
│       └── evaluator.ts        # Condition expression evaluator
│
├── surface/
│   └── components/
│       └── Wizard/
│           ├── WizardEngine.tsx      # Main orchestrator
│           ├── WizardProgress.tsx    # Progress bar
│           ├── WizardHeader.tsx      # Header with back/close
│           ├── steps/
│           │   ├── ConsentStep.tsx
│           │   ├── ChoiceStep.tsx
│           │   ├── TextStep.tsx
│           │   ├── GenerationStep.tsx
│           │   ├── SelectionStep.tsx
│           │   └── ConfirmationStep.tsx
│           └── hooks/
│               └── useWizardState.ts
│
└── data/
    └── wizards/
        ├── custom-lens.wizard.json
        ├── custom-journey.wizard.json
        └── onboarding.wizard.json
```

### WizardEngine Component

```typescript
interface WizardEngineProps<T> {
  schema: WizardSchema;
  onComplete: (result: T) => void;
  onCancel: () => void;
  initialInputs?: Record<string, unknown>;
}

export function WizardEngine<T>({
  schema,
  onComplete,
  onCancel,
  initialInputs
}: WizardEngineProps<T>) {
  const {
    state,
    currentStep,
    goToStep,
    updateInputs,
    getProgress
  } = useWizardState(schema, initialInputs);

  const handleStepComplete = (action: StepAction) => {
    if ('complete' in action && action.complete) {
      const result = transformOutput(state, schema.output);
      onComplete(result);
    } else if ('next' in action) {
      goToStep(action.next);
    }
  };

  const stepSchema = schema.steps.find(s => s.id === currentStep);

  return (
    <div className="wizard-container">
      <WizardHeader title={schema.title} onCancel={onCancel} />
      <WizardProgress current={getProgress()} total={getTotalSteps()} />
      <StepRenderer
        schema={stepSchema}
        inputs={state.inputs}
        onComplete={handleStepComplete}
      />
    </div>
  );
}
```

## DEX Compliance

**Declarative Sovereignty ✓** — Domain experts create wizards via JSON. No code changes for new questions, flow changes, or analytics events.
**Capability Agnosticism ✓** — Engine works regardless of AI model. Generation step calls configurable endpoint.
**Provenance ✓** — Every completion creates artifact with wizard ID, version, all inputs, timestamps.
**Organic Scalability ✓** — New wizards require only JSON schema file + optional card renderer.

## Migration Path

| Phase | Work | Risk |
|---|---|---|
| 1. Create Engine | New WizardEngine, step renderers, useWizardState | Low (additive) |
| 2. Extract Schema | Convert CustomLensWizard logic to JSON | Medium (parity) |
| 3. Replace | Swap CustomLensWizard to use engine | Medium (regression) |
| 4. Extend | Create custom-journey.wizard.json | Low (new feature) |

## Open Questions

1. **Expression Language:** JS expressions or safer DSL for conditions?
1. **Card Renderers:** Registry pattern or inline component references?
1. **Validation:** Schema-level or engine-level input validation?
1. **Theming:** How much styling should be schema-configurable?
