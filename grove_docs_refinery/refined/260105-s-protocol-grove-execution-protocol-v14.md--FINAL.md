---
author: Jim Calhoun
date: '2026-01-05'
domain: protocol
last_synced: '2026-01-20T17:17:49.706399'
local_file: 260105-s-protocol-grove-execution-protocol-v14.md--FINAL.md
notion_id: 2ee780a7-8eef-81bb-8488-eca6973c8fa1
notion_url: https://www.notion.so/Grove-Execution-Protocol-v1-4-2ee780a78eef81bb8488eca6973c8fa1
status: final
title: Grove Execution Protocol v1.4
type: software
---

*see codebase for current protocols, this is for illustrative purposes only: *[*https://www.github/twocash/the-grove-foundation*](https://www.github/twocash/the-grove-foundation)

# Grove Execution Protocol v1.4 (Skill)

**Purpose:** Execution contracts for Grove Foundation development. This protocol implements DEX/Trellis architecture principles with atomic verification gates.
**Philosophy:** This is an execution contract, not a planning methodology. Planning happens in conversation; execution follows this protocol.
**v1.4 Changes:**
- Added Constraint 10: REVIEW.html Completion Gate
- Added Constraint 7b: UI Slot Check — New Object Audit
- REVIEW.html must be complete with all screenshots before handoff
- Standardized handoff sequence with notification
- New objects must pass UI Slot decision tree before creating routes
**v1.3 Changes:**
- Added Constraint 2b: Playwright Visual Verification (replaces Chrome MCP)
- Playwright commands for deterministic screenshot capture
- E2E test file pattern for User Story smoke tests
**v1.2 Changes:**
- Added Constraint 8: Code-Simplifier Pre-Commit Gate
- Added Constraint 9: Sprint Documentation Commits
- Added DEX Compliance Gates as enforceable checkpoints
- Strengthened Constraint 2: Visual Verification enforcement

---

## The DEX Compass

Every decision passes through these four tests:

| Principle | Test Question | Failure Mode |
|---|---|---|
| **Declarative Sovereignty** | Can a domain expert change this behavior via config, not code? | Hardcoded domain logic |
| **Capability Agnosticism** | Does this work regardless of which LLM is attached? | Model-specific assumptions |
| **Provenance as Infrastructure** | Does every object track how it came to exist? | Orphaned facts |
| **Organic Scalability** | Does structure enable growth without code changes? | Brittle architecture |

**The Ultimate Test:** *"If we swapped the LLM tomorrow, would this still work?"*

---

## Hard Constraints (Inviolable)

### Constraint 1: Strangler Fig Zones

```javascript
FROZEN ZONE — DO NOT TOUCH
├── /terminal route
├── /foundation route (except Foundation consoles)
├── src/surface/components/Terminal/*
└── src/workspace/* (legacy GroveWorkspace)

ACTIVE BUILD ZONE — WHERE WE WORK
├── /explore route
├── /bedrock route
├── src/explore/*
├── src/bedrock/*
└── src/core/schema/*
```

**Any file edit in FROZEN ZONE = sprint failure. No exceptions.**
Before any edit, verify the file path is in ACTIVE BUILD ZONE.

---

### Constraint 2: Visual Verification Gates

**Screenshots are audit artifacts that prove features work. They are mandatory.**
Every sub-phase with UI changes ends with:

```javascript
┌────────────────────────────────────────────────────────────┐
│  SCREENSHOT VERIFICATION SEQUENCE (MANDATORY)              │
│                                                            │
│  1. npm run dev                                            │
│  2. Navigate to correct route (/explore or /bedrock/*)    │
│  3. Interact with the feature                             │
│  4. Take screenshot                                        │
│  5. SAVE TO PROJECT: docs/sprints/{sprint}/screenshots/   │
│  6. VERIFY FILE EXISTS (ls or dir the folder!)            │
│  7. Update DEVLOG.md with screenshot path                 │
│  8. Only then: commit (include screenshot in commit)      │
└────────────────────────────────────────────────────────────┘
```

**Screenshot File Requirements:**

| Requirement | Specification |
|---|---|
| **Location** | `docs/sprints/{sprint}/screenshots/` |
| **Filename** | `{phase}{subphase}-{description}.png` (e.g., `3a-card-grid.png`) |
| **Format** | PNG preferred, GIF for interactions |
| **Verification** | Run `ls docs/sprints/{sprint}/screenshots/` AFTER saving |

**FAILURE MODE:** Screenshots in browser memory or temp folders DO NOT count.
The file must exist at the specified path and be included in the git commit.
**If screenshot cannot be saved:**
1. STOP the phase
1. Report the issue
1. Do NOT proceed to commit
1. Do NOT claim visual verification is complete
**ENFORCEMENT:** Before ANY commit, verify screenshot count matches phase count:

```bash
ls docs/sprints/{sprint}/screenshots/ | wc -l
# Must equal or exceed current phase number
```

**No commit without visual evidence of working UI saved to the project.**

---

### Constraint 2b: Playwright Visual Verification

**Browser automation tools are unreliable for screenshots. Use Playwright for deterministic captures.**

```javascript
┌────────────────────────────────────────────────────────────┐
│  PLAYWRIGHT SCREENSHOT COMMANDS                            │
│                                                            │
│  # Basic screenshot                                        │
│  npx playwright screenshot http://localhost:3000/explore \ │
│    docs/sprints/{sprint}/screenshots/{name}.png           │
│                                                            │
│  # Full page screenshot                                    │
│  npx playwright screenshot --full-page \                   │
│    http://localhost:3000/explore \                        │
│    docs/sprints/{sprint}/screenshots/{name}.png           │
│                                                            │
│  # Wait for specific element before capture               │
│  npx playwright screenshot --wait-for-selector="[data-testid='garden-tray']" \ │
│    http://localhost:3000/explore \                        │
│    docs/sprints/{sprint}/screenshots/{name}.png           │
└────────────────────────────────────────────────────────────┘
```

**When to use Playwright vs Chrome MCP:**
- **Playwright:** Deterministic screenshots, E2E tests, visual regression
- **Chrome MCP:** Interactive exploration, debugging, human-in-loop tasks
**E2E Test Pattern for User Stories:**

```typescript
// tests/e2e/{feature}.spec.ts
const SCREENSHOTS_DIR = 'docs/sprints/{sprint}/screenshots'

test('US-{ID}: {Story Title}', async ({ page }) => {
  await page.goto('/explore')
  await page.waitForLoadState('networkidle')

  // Test the acceptance criteria
  const element = page.getByTestId('feature-element')
  await expect(element).toBeVisible()

  // Capture verification screenshot
  await page.screenshot({
    path: `${SCREENSHOTS_DIR}/us-{id}-{description}.png`,
    fullPage: false
  })
})
```

---

### Constraint 3: Contract File Requirements

Every sprint execution requires these files:

```javascript
docs/sprints/{sprint-name}/
├── SPEC.md           ← Execution contract (what we're building)
├── DEVLOG.md         ← Running execution log (what happened)
├── REVIEW.html       ← Visual proof of completion (v1.4)
└── screenshots/      ← Visual verification evidence
    ├── phase1a-*.png
    ├── phase2a-*.png
    └── ...
```

[**SPEC.md**](http://spec.md/)** required sections:**
- Live Status table (current phase, blocking issues)
- Attention Anchor (what we're building right now)
- Hard Constraints (strangler fig, DEX matrix)
- Execution Architecture (phases, sub-phases, gates)
- Success Criteria / Sprint Failed conditions
[**DEVLOG.md**](http://devlog.md/)** format:**

```markdown
## Phase N: {Name}
**Started:** {timestamp}
**Status:** {in-progress|complete|blocked}

### Sub-phase Na: {Description}
- What was done
- Files changed
- Screenshot: `screenshots/Na-description.png`
- Gate: ✅ PASSED / ❌ FAILED

### DEX Compliance (per phase)
- Declarative Sovereignty: ✅ {how it passes}
- Capability Agnosticism: ✅ {how it passes}
- Provenance: ✅ {how it passes}
- Organic Scalability: ✅ {how it passes}
```

---

### Constraint 4: Feature Flags Before Wiring

New code stays isolated until verified:
1. Component exists standalone (testable in isolation)
1. Feature flag controls execution path
1. `flag=false` verified (legacy behavior preserved)
1. `flag=true` verified (new behavior works)
1. Both paths coexist until explicit cutover

---

### Constraint 5: Behavior Tests, Not Implementation Tests

```typescript
// WRONG - tests implementation details
expect(element).toHaveClass('translate-x-0');
expect(component.state.isOpen).toBe(true);

// RIGHT - tests observable behavior
expect(element).toBeVisible();
expect(page.getByText('Welcome')).toBeInTheDocument();
```

Test what Observers see and experience, not internal state or CSS classes.

---

### Constraint 6: Test Routes — WHERE to Verify

**Always verify features at the CORRECT route:**

```javascript
✅ localhost:3000/explore           ← Kinetic stream features
✅ localhost:3000/bedrock/*         ← Bedrock consoles (Nursery, Garden, etc.)
❌ localhost:3000/                  ← LEGACY terminal (features won't appear!)
❌ localhost:3000/terminal          ← LEGACY terminal
```

Testing at `/` or `/terminal` makes features appear broken when they're actually in the FROZEN ZONE.

---

### Constraint 7: Bedrock Console Factory

**All Bedrock consoles use the factory pattern. No exceptions.**

```typescript
// CORRECT - using factory
import { createBedrockConsole } from '@/bedrock/createBedrockConsole'

export const NurseryConsole = createBedrockConsole<SproutPayload>({
  title: 'Nursery',
  icon: Seedling,
  endpoint: 'nursery',
  // ... config
})

// WRONG - custom implementation
export const NurseryConsole: React.FC = () => {
  // Custom code that bypasses factory
}
```

**Why this matters:**
- Consistency across all consoles
- Shared infrastructure (polling, error handling, styling)
- DEX compliance (Organic Scalability principle)
- Easier maintenance and updates
**When adding a new console:**
1. Check if `createBedrockConsole` supports the use case
1. If yes: use it
1. If no: extend the factory, don't bypass it

---

### Constraint 7b: UI Slot Check — New Object Audit

**Before creating ANY new UI route, console, or top-level navigation item: STOP and run the UI Slot Check.**

```javascript
┌────────────────────────────────────────────────────────────┐
│  UI SLOT CHECK — MANDATORY FOR NEW OBJECTS                │
│                                                            │
│  When a sprint spec introduces a new schema/object:        │
│                                                            │
│  1. DOES THIS NEED ITS OWN UI SLOT?                       │
│     Ask: "Can this live inside an existing console?"       │
│                                                            │
│     If YES → Use existing console (Experience, Bedrock)    │
│     If NO  → Document WHY in spec, get approval           │
│                                                            │
│  2. THE DEFAULT IS NO NEW SLOT                            │
│     Search, filter, and tagging handle most needs.         │
│     New routes are expensive (navigation, routing, tests).│
│                                                            │
│  3. IF OBJECT IS A "TYPE" OF SOMETHING:                    │
│     It belongs in a polymorphic console via registry.      │
│     Example: ResearchAgentConfig → Experience console      │
│              (NOT /research-config route)                  │
│                                                            │
│  4. API-FIRST MINDSET                                      │
│     The UI is a thin layer over the object model.         │
│     A messy object model = messy API = tech debt.         │
│     Get the objects right; UI follows.                     │
└────────────────────────────────────────────────────────────┘
```

**Decision Tree for New Objects:**

```javascript
New object in spec?
    │
    ├─► Is it a TYPE of existing concept?
    │       │
    │       ├─► YES → Register in type registry, use polymorphic console
    │       │         (e.g., ResearchConfig is Experience type)
    │       │
    │       └─► NO → Continue...
    │
    ├─► Does it have its own lifecycle independent of all other objects?
    │       │
    │       ├─► NO → Embed in parent object's UI
    │       │
    │       └─► YES → Continue...
    │
    ├─► Will users need to browse/search MANY of these?
    │       │
    │       ├─► NO → Detail view or modal, not console
    │       │
    │       └─► YES → Continue...
    │
    └─► ONLY NOW: Consider new console (requires justification in spec)
```

**Examples:**

| Object | UI Slot? | Why |
|---|---|---|
| ResearchAgentConfig | ❌ NO | It's an Experience type → Experience console |
| EvidenceBundle | ❌ NO | Output artifact → displayed inline in results |
| Sprout | ✅ YES | Own lifecycle, users browse many → Nursery console |
| Experience | ✅ YES | Core entity, users browse many → Experience console |
| User preferences | ❌ NO | Settings modal, not console |

**Spec Requirement:**
If a sprint creates a new top-level UI slot, [SPEC.md](http://spec.md/) includes:

```markdown
## UI Slot Justification

**New Route:** /bedrock/{new-console}

**Why existing consoles don't work:**
- {Reason 1}
- {Reason 2}

**Independent lifecycle:** {Yes/No + explanation}

**Browse/search pattern:** {Yes/No + explanation}

**Approved by:** {User approval required}
```

---

### Constraint 8: Code-Simplifier Pre-Commit Gate

**All sprint commits pass through code-simplifier agent before merge.**
The code-simplifier plugin (`code-simplifier@claude-plugins-official`) ensures:
- Clarity over cleverness (explicit code beats compact code)
- No nested ternary operators (use switch/if-else)
- Project-specific standards from [CLAUDE.md](http://claude.md/) applied
- Functionality preserved (never changes what code does)

```javascript
┌────────────────────────────────────────────────────────────┐
│  CODE-SIMPLIFIER PRE-COMMIT SEQUENCE                      │
│                                                            │
│  1. Complete feature implementation                        │
│  2. Run build gates: npm run build && npm run lint        │
│  3. Invoke code-simplifier agent on modified files:       │
│     /code-simplifier                                       │
│     OR use Task tool with subagent_type=code-simplifier   │
│  4. Review simplifications (preserve functionality!)      │
│  5. Apply approved changes                                │
│  6. Re-run build gates                                    │
│  7. Visual verification + screenshot                      │
│  8. Only then: commit                                     │
├────────────────────────────────────────────────────────────┤
│  CODE-SIMPLIFIER TARGETS:                                 │
│  ✅ Recently modified files in current sprint             │
│  ✅ New components and hooks                              │
│  ✅ Service layer changes                                 │
├────────────────────────────────────────────────────────────┤
│  SKIP CODE-SIMPLIFIER WHEN:                               │
│  ⏭️ Hotfixes under 10 lines                              │
│  ⏭️ Config-only changes (.config.ts, .json)              │
│  ⏭️ Documentation-only changes                           │
└────────────────────────────────────────────────────────────┘
```

**Integration with Sprint Workflow:**
- Phase completion = build gates + visual verification + code-simplifier
- Sprint completion = all phases pass + final code-simplifier sweep
- Code review = verify code-simplifier was applied (check commit history)

---

### Constraint 9: Sprint Documentation Commits

**Sprint documentation commits alongside code. No orphaned docs.**

```javascript
┌────────────────────────────────────────────────────────────┐
│  SPRINT DOCUMENTATION COMMIT PROTOCOL                      │
│                                                            │
│  DURING SPRINT:                                            │
│  After each phase: git add docs/sprints/{sprint}/DEVLOG.md│
│  Include DEVLOG updates in phase commits                  │
│                                                            │
│  FINAL COMMIT:                                             │
│  git add docs/sprints/{sprint}/                           │
│  (Includes SPEC.md, DEVLOG.md, REVIEW.html, screenshots/) │
│                                                            │
│  PRE-PUSH CHECKLIST:                                       │
│  git status docs/sprints/                                 │
│  → Must show NO untracked sprint folders                  │
│  → If untracked folders exist: git add them before push   │
└────────────────────────────────────────────────────────────┘
```

**Verification Command:**

```bash
# Run before every push - should return empty (no untracked sprint docs)
git status docs/sprints/ --porcelain | grep "^??"
```

---

### Constraint 10: REVIEW.html Completion Gate

**Before handoff, REVIEW.html is complete with all screenshots.**
The REVIEW.html provides visual proof of sprint completion. It's the Observer's primary interface for reviewing what was built.

```javascript
┌────────────────────────────────────────────────────────────┐
│  REVIEW.HTML REQUIRED SECTIONS                            │
│                                                            │
│  1. SUMMARY METRICS                                        │
│     - Phases Complete (e.g., 7/7)                         │
│     - Tests Passing (e.g., 23/23 E2E)                     │
│     - Screenshots captured (count)                        │
│     - Sprint Status (Complete/In Progress)                │
│                                                            │
│  2. USER STORIES TABLE                                    │
│     - Story ID, Title, Priority, Status                   │
│     - Links to Notion acceptance criteria                 │
│                                                            │
│  3. PHASE PROGRESS                                        │
│     - Each phase with status badge                        │
│     - Description of what was done                        │
│     - Embedded screenshots (<img> tags)                   │
│                                                            │
│  4. TEST RESULTS                                          │
│     - Unit test count and status                          │
│     - E2E test count and status                          │
│     - Coverage breakdown by user story                    │
│                                                            │
│  5. FILES CHANGED                                         │
│     - New files (green)                                   │
│     - Modified files (yellow)                             │
│     - Brief description of each                           │
│                                                            │
│  6. KEY FEATURES DELIVERED                                │
│     - Bullet list of capabilities                         │
│     - Links to relevant code/docs                         │
└────────────────────────────────────────────────────────────┘
```

**User Handoff Announcement (Required):**
When sprint is complete and REVIEW.html is ready:

```javascript
📋 Sprint Review Ready
Sprint: {sprint-name}
Status: ✅ Complete
Review File: docs/sprints/{sprint}/REVIEW.html

Open REVIEW.html in browser to see:
- Summary metrics and test results
- Screenshots of all completed features
- Phase-by-phase progress with visual evidence
```

**Screenshot Embedding:**

```html
<div class="media-item">
  <img src="screenshots/us-c001-tray-visible.png" alt="Feature description">
  <div class="media-caption">US-C001: Caption describing what this shows</div>
</div>
```

---

## DEX Compliance Gates

**DEX principles are gates, not guidelines. Violation blocks the sprint.**
Every feature passes these four tests before commit:

```javascript
┌────────────────────────────────────────────────────────────┐
│  DEX COMPLIANCE CHECKLIST (Required before commit)        │
│                                                            │
│  □ DECLARATIVE SOVEREIGNTY                                │
│    Can a domain expert change behavior via config?        │
│    ✅ Pass: Behavior in .config.ts or JSON               │
│    ❌ Fail: Hardcoded domain logic in components          │
│                                                            │
│  □ CAPABILITY AGNOSTICISM                                 │
│    Does this work regardless of which LLM is attached?    │
│    ✅ Pass: No model-specific code paths                  │
│    ❌ Fail: Code branches on model name/capabilities      │
│                                                            │
│  □ PROVENANCE AS INFRASTRUCTURE                           │
│    Does every object track how it came to exist?          │
│    ✅ Pass: createdAt, createdBy, source tracked          │
│    ❌ Fail: Orphaned facts with no origin                 │
│                                                            │
│  □ ORGANIC SCALABILITY                                    │
│    Does structure enable growth without code changes?     │
│    ✅ Pass: Factory patterns, registries, configs         │
│    ❌ Fail: One-off implementations, hardcoded lists      │
└────────────────────────────────────────────────────────────┘
```

**How to Document DEX Compliance:**
In [DEVLOG.md](http://devlog.md/) for each phase:

```markdown
### DEX Compliance
- Declarative Sovereignty: ✅ {how it passes}
- Capability Agnosticism: ✅ {how it passes}
- Provenance: ✅ {how it passes}
- Organic Scalability: ✅ {how it passes}
```

**The Ultimate Test:** *"If we swapped the LLM tomorrow, would this still work?"*

---

## Sprint Contract Templates

### [SPEC.md](http://spec.md/) Template

```markdown
# {Feature Name} Execution Contract

**Codename:** `{sprint-name}`
**Status:** Execution Contract for Claude Code CLI
**Protocol:** Grove Execution Protocol v1.4
**Baseline:** `main` (post {previous-sprint})
**Date:** {YYYY-MM-DD}

---

## Live Status

| Field | Value |
|-------|-------|
| **Current Phase** | Phase N - {Name} |
| **Status** | 🚀 Executing |
| **Blocking Issues** | None |
| **Last Updated** | {timestamp} |
| **Next Action** | {description} |

---

## Attention Anchor

**We are building:** {one-sentence description}

**Success looks like:** {observable outcome}

---

## Hard Constraints

### Strangler Fig Compliance
{copy from protocol}

### DEX Compliance Matrix
| Feature | Declarative | Agnostic | Provenance | Scalable |
|---------|-------------|----------|------------|----------|
| {name}  | ✅/❌ {why} | ✅/❌    | ✅/❌      | ✅/❌    |

---

## Execution Architecture

### Phases
{list phases with sub-phases and gates}

---

## Success Criteria

### Sprint Complete When:
- [ ] All phases completed with verification
- [ ] All DEX compliance gates pass
- [ ] All screenshots captured and embedded in REVIEW.html
- [ ] REVIEW.html complete with all sections
- [ ] Code-simplifier applied
- [ ] Build and lint pass
- [ ] User notified with REVIEW.html path

### Sprint Failed If:
- ❌ Any FROZEN ZONE file modified
- ❌ Any phase without screenshot evidence
- ❌ DEX compliance test fails
- ❌ REVIEW.html not created or incomplete
- ❌ User handoff without REVIEW.html

---

*This contract is binding. Deviation requires explicit human approval.*
```

---

## Common Pitfalls

| Pitfall | Prevention |
|---|---|
| Testing at wrong route | Always use `/explore` or `/bedrock/*`, never `/` or `/terminal` |
| Screenshots in temp folder | Save directly to `docs/sprints/{sprint}/screenshots/` |
| Custom console implementation | Use `createBedrockConsole` factory |
| Skipping code-simplifier | Always run before final commit |
| Orphaned sprint docs | Include `docs/sprints/` in every commit |
| No REVIEW.html | Create REVIEW.html before user handoff |
| Handoff without review path | Always tell user where REVIEW.html is |
| Editing FROZEN ZONE | Check file path before every edit |
| New route without UI Slot Check | Run decision tree before creating routes (Constraint 7b) |
| Object type as separate console | Register in type registry, use polymorphic console |

---

## Success Criteria Checklist

### Sprint Complete When:

- [ ] All phases completed with verification gates
- [ ] All DEX compliance matrix cells verified
- [ ] All build gates passing (`npm run build && npm run lint`)
- [ ] Screenshot evidence for all visual verifications
- [ ] FROZEN ZONE untouched
- [ ] [DEVLOG.md](http://devlog.md/) documents complete journey
- [ ] Code-simplifier pass applied
- [ ] DEX compliance documented in DEVLOG
- [ ] E2E smoke tests passing
- [ ] REVIEW.html complete with all screenshots
- [ ] User notified with REVIEW.html path

### Sprint Failed If:

- ❌ Any FROZEN ZONE file modified
- ❌ Any phase completed without screenshot
- ❌ DEX compliance test fails
- ❌ Code committed without code-simplifier pass
- ❌ Sprint documentation not committed with code
- ❌ REVIEW.html not created or missing screenshots
- ❌ User handoff without REVIEW.html notification

---

## When Stuck

```javascript
┌────────────────────────────────────────────────────────────┐
│  CHECKLIST WHEN BLOCKED                                    │
│                                                            │
│  □ Am I in the right directory? (pwd)                     │
│  □ Am I testing at the right route? (/explore, not /)     │
│  □ Did I run npm run build?                               │
│  □ Did I run npm run dev?                                 │
│  □ Is the dev server actually running?                    │
│  □ Am I editing a FROZEN ZONE file?                       │
│  □ Did I save the screenshot to the project folder?       │
│  □ Does the factory support my use case?                  │
│  □ Is REVIEW.html updated with latest screenshots?        │
│  □ Did I run code-simplifier before commit?               │
│                                                            │
│  If still stuck: Update DEVLOG.md with blocker details    │
│  and ask for guidance.                                    │
└────────────────────────────────────────────────────────────┘
```

---
*This protocol is binding for all Grove Foundation development. Deviation requires explicit human approval.*
