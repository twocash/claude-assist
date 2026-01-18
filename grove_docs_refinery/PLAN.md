# Grove Docs Refinery - Operationalization Plan

**Created:** January 2026
**Status:** Ready for Implementation
**Owner:** Jim Calhoun

## Overview

This plan operationalizes the Grove Docs Refinery system as Python scripts that integrate with our ATLAS agent infrastructure. The refinery is a two-layer system for batch content refactoring:
- **Grove Editorial Engine** — Stable methodology (voice, terminology, rewrite process)
- **Grove Docs Refinery** — Orchestration for Claude CLI

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   REFINERY ORCHESTRATOR                      │
│                    (refinery.py)                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   INPUT     │───►│   EDITOR    │───►│  REVIEWER   │     │
│  │   FILES     │    │   AGENT     │    │   AGENT     │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
│                                               │             │
│                     ┌─────────────────────────┼─────┐       │
│                     │                         │     │       │
│                     ▼                         ▼     ▼       │
│               ┌─────────┐              ┌──────┐ ┌────────┐  │
│               │  PASS   │              │REVISE│ │ESCALATE│  │
│               └────┬────┘              └──┬───┘ └───┬────┘  │
│                    │                      │         │       │
│                    ▼                      │         ▼       │
│               ┌─────────┐                 │    ┌────────┐   │
│               │ REFINED │◄────────────────┘    │  JIM   │   │
│               │ OUTPUT  │                     │DECISION│   │
│               └─────────┘                     └────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
C:\github\claude-assist\
├── grove-docs-refinery/
│   ├── __init__.py
│   ├── refinery.py              # Main orchestrator
│   ├── editor.py                # Writer agent
│   ├── reviewer.py              # Reviewer agent
│   ├── checkpoint.py            # Checkpoint loader/manager
│   ├── manifest.py              # Run tracking
│   ├── editorial-engine.md      # Stable methodology
│   ├── editorial-checkpoint.md  # Dynamic state
│   ├── config.yaml              # Configuration
│   ├── input/                   # Source files
│   ├── drafts/                  # Editor outputs
│   ├── reviews/                 # Reviewer outputs
│   ├── refined/                 # Final outputs
│   └── logs/                    # Run logs
```

## Implementation Steps

### Step 1: Create Refinery Orchestrator (`refinery.py`)

**Purpose:** Main entry point that orchestrates the full workflow

**Functions:**
- `RefineryOrchestrator.run_batch(input_dir, output_dir, batch_size=5)`
- `RefineryOrchestrator.run_single(file_path)`
- `RefineryOrchestrator.resume_from_manifest(manifest_path)`

**Workflow:**
1. Load editorial engine and checkpoint
2. Scan input directory for files
3. Generate manifest
4. For each file:
   - Run Editor agent (analysis + rewrite)
   - Run Reviewer agent (validation)
   - Record PASS/REVISE/ESCALATE
5. Generate run summary
6. Present ESCALATE items to Jim

### Step 2: Create Editor Agent (`editor.py`)

**Purpose:** Rewrite content following editorial methodology

**Functions:**
- `EditorAgent.load_context(engine_skill, checkpoint)`
- `EditorAgent.analyze(source_file) -> Analysis`
- `EditorAgent.rewrite(source_file, analysis) -> Draft`

**Output Format:**
```markdown
## Rewrite: [Document Title]
### Diagnosis Summary
[2-3 sentences on source state]
### Key Changes Made
- [Change 1]
- [Change 2]
- [etc.]
### Flags for Review
- [Any uncertainties, decisions needed, or ESCALATE items]
---
[FULL REWRITTEN CONTENT]
```

### Step 3: Create Reviewer Agent (`reviewer.py`)

**Purpose:** Validate editor output against Grove standards

**Functions:**
- `ReviewerAgent.validate(source_file, draft) -> ReviewResult`
- `ReviewerAgent.check_terminology(draft, checkpoint)`
- `ReviewerAgent.check_positioning(draft, checkpoint)`

**Output Format:**
```markdown
## Review: [Document Title]
### Assessment: [PASS / REVISE / ESCALATE]
### Validation Checklist
- [x] Terminology current
- [x] Positioning aligned
- [ ] Technical accuracy
- [ ] Voice consistency
- [ ] No prohibited language
- [ ] Appropriate length
- [ ] Changes justified
- [ ] No new errors
### Specific Feedback
[If PASS: brief confirmation]
[If REVISE: specific changes needed]
[If ESCALATE: decision needed from Jim]
```

### Step 4: Checkpoint Manager (`checkpoint.py`)

**Purpose:** Load and manage editorial checkpoint state

**Functions:**
- `CheckpointManager.load() -> dict`
- `CheckpointManager.get_terminology_mapping() -> dict`
- `CheckpointManager.get_positioning() -> str`
- `CheckpointManager.get_voice_standards() -> list`
- `CheckpointManager.validate_term(term) -> (valid, suggestion)`

### Step 5: Manifest & Tracking (`manifest.py`)

**Purpose:** Track refinery runs and file status

**Functions:**
- `Manifest.create(input_files) -> dict`
- `Manifest.update_status(file, status, notes)`
- `Manifest.add_escalate(file, issue, options)`
- `Manifest.generate_summary() -> str`

**Manifest Format:**
```json
{
  "run_date": "2026-01-16",
  "files": [
    {
      "original_name": "grove-white-paper-v2.md",
      "working_name": "grove-white-paper-v2.md",
      "status": "PASS",
      "original_words": 3500,
      "refined_words": 3200,
      "notes": "Minor voice adjustments"
    }
  ],
  "escalate_items": [],
  "summary": {}
}
```

## Integration with ATLAS

### Agent Dispatch Integration

The refinery can leverage our existing `agents/` directory:

```
agents/
├── refinery-editor.py    # Editor agent wrapper
├── refinery-reviewer.py  # Reviewer agent wrapper
└── ...
```

**Dispatch flow:**
1. Refinery.py identifies file to process
2. Calls appropriate agent via dispatch system
3. Agent loads editorial context
4. Agent produces output
5. Refinery records result

### Skills Integration

The editorial engine and checkpoint can be:
- **Static files** in `grove-docs-refinery/`
- **Skills** in `skills/user/grove-editorial-engine/` for Claude Desktop

### Checkpoint Updates

If refinery reveals needed checkpoint changes:
1. Document the pattern
2. Propose checkpoint addition
3. Get Jim's approval
4. Update checkpoint
5. Note in manifest

## Configuration (`config.yaml`)

```yaml
refinery:
  input_dir: "grove-docs-refinery/input"
  output_dirs:
    drafts: "grove-docs-refinery/drafts"
    reviews: "grove-docs-refinery/reviews"
    refined: "grove-docs-refinery/refined"
  logs: "grove-docs-refinery/logs"
  batch_size: 5
  max_revisions: 2

editor:
  model: "sonnet"
  checkpoint_path: "grove-docs-refinery/editorial-checkpoint.md"
  engine_path: "grove-docs-refinery/editorial-engine.md"

reviewer:
  model: "sonnet"
  checkpoint_path: "grove-docs-refinery/editorial-checkpoint.md"
  engine_path: "grove-docs-refinery/editorial-engine.md"

# Grove standards
standards:
  voice:
    - "Strategic, not smug"
    - "Concrete over abstract"
    - "Honest about uncertainty"
  terminology:
    - "Exploration architecture" (not "AI platform")
    - "Agents" (not "bots")
    - "Credits" (not "tokens")
  avoid:
    - "revolutionary"
    - "paradigm shift"
    - "Web3"
    - "democratize"
    - "might", "could potentially"
```

## Folder Structure

```
grove-docs-refinery/
├── config.yaml              # Configuration
├── editorial-engine.md      # Stable methodology (from Notion)
├── editorial-checkpoint.md  # Dynamic state (from Notion)
├── refinery.py              # Main orchestrator
├── editor.py                # Editor agent
├── reviewer.py              # Reviewer agent
├── checkpoint.py            # Checkpoint manager
├── manifest.py              # Run tracking
├── input/                   # Source files (.md, .txt)
│   ├── grove-white-paper-v2.md
│   ├── grove-vision.md
│   └── architecture-spec.md
├── drafts/                  # Editor outputs
│   ├── grove-white-paper-v2--DRAFT.md
│   └── grove-vision--DRAFT.md
├── reviews/                 # Reviewer outputs
│   ├── grove-white-paper-v2--REVIEW.md
│   └── grove-vision--REVIEW.md
├── refined/                 # Final outputs
│   ├── grove-white-paper-v2--FINAL.md
│   └── grove-vision--FINAL.md
└── logs/
    ├── refinery-run-2026-01-16.json
    └── refinery-run-2026-01-16--SUMMARY.md
```

## File Naming Convention

| Original | Working Name | Draft | Review | Final |
|----------|-------------|-------|--------|-------|
| Grove White Paper v2.md | grove-white-paper-v2.md | grove-white-paper-v2--DRAFT.md | grove-white-paper-v2--REVIEW.md | grove-white-paper-v2--FINAL.md |
| Architecture Spec.md | architecture-spec.md | architecture-spec--DRAFT.md | architecture-spec--REVIEW.md | architecture-spec--FINAL.md |

## Quick Mode (Single File)

For processing one file without full batch infrastructure:

```bash
python -m grove-docs-refinery.refinery --single path/to/file.md
```

This will:
1. Load editorial engine and checkpoint
2. Run analysis
3. Confirm with Jim
4. Execute editor pass
5. Execute reviewer pass
6. Deliver refined output

## Pilot Test

**Files to process:** 2-3 test documents

**Test objectives:**
1. Validate editor produces quality rewrites
2. Validate reviewer catches issues
3. Test ESCALATE flow
4. Measure performance (words/minute)
5. Gather Jim's feedback

**Success criteria:**
- [ ] All 3 files complete pipeline
- [ ] At least 1 PASS, 1 ESCALATE
- [ ] Jim approves output quality
- [ ] Process takes <5 min per file

## Next Steps

1. **Create directory structure**
2. **Copy editorial engine and checkpoint from Notion**
3. **Implement Refinery Orchestrator**
4. **Implement Editor Agent**
5. **Implement Reviewer Agent**
6. **Implement Manifest & Tracking**
7. **Create CLI interface**
8. **Run pilot test**
9. **Iterate based on results**

---

*Plan created for Grove Docs Refinery operationalization*
