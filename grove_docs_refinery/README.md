# Grove Docs Refinery

A two-layer system for batch content refactoring of Grove documentation.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   REFINERY ORCHESTRATOR                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   INPUT     │───►│   EDITOR    │───►│  REVIEWER   │     │
│  │   FILES     │    │   AGENT     │    │   AGENT     │     │
│  └─────────────┘    └─────────────┘    └──────┬──────┘     │
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
└─────────────────────────────────────────────────────────────┘
```

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Orchestrator | `refinery.py` | Main workflow orchestration |
| Editor | `editor.py` | Content rewriting agent |
| Reviewer | `reviewer.py` | Quality validation agent |
| Checkpoint | `checkpoint.py` | Dynamic state management |
| Config | `config.py` | Configuration loader |

## Methodology Files

| File | Purpose |
|------|---------|
| `editorial-engine.md` | Stable methodology (how to rewrite) |
| `editorial-checkpoint.md` | Dynamic state (what's current) |

## Usage

### Batch Processing

```bash
python -m grove_docs_refinery.refinery
```

### Single File

```bash
python -m grove_docs_refinery.refinery --single path/to/file.md
```

### Python API

```python
from grove_docs_refinery import RefineryOrchestrator

orchestrator = RefineryOrchestrator()
orchestrator.initialize()
manifest = orchestrator.run_batch()

# Check results
print(f"Passed: {manifest.summary['passed']}")
print(f"Escalated: {len(manifest.escalate_items)}")
```

## Directory Structure

```
grove-docs-refinery/
├── __init__.py
├── refinery.py              # Main orchestrator
├── editor.py                # Writer agent
├── reviewer.py              # Reviewer agent
├── checkpoint.py            # Checkpoint manager
├── config.py                # Configuration
├── editorial-engine.md      # Methodology
├── editorial-checkpoint.md  # Current state
├── config.yaml              # Settings
├── input/                   # Source files
├── drafts/                  # Editor outputs
├── reviews/                 # Reviewer outputs
├── refined/                 # Final outputs
└── logs/                    # Run manifests
```

## Output Files

| Stage | Suffix | Example |
|-------|--------|---------|
| Draft | `--DRAFT.md` | `grove-white-paper--DRAFT.md` |
| Review | `--REVIEW.md` | `grove-white-paper--REVIEW.md` |
| Final | `--FINAL.md` | `grove-white-paper--FINAL.md` |

## Assessment Types

| Status | Meaning |
|--------|---------|
| PASS | Ready for use |
| REVISE | Needs editor revision |
| ESCALATE | Requires human decision |

## Integration

### With ATLAS

The refinery can integrate with ATLAS agent dispatch:
1. Refinery identifies file to process
2. Calls appropriate agent
3. Agent loads editorial context
4. Agent produces output
5. Refinery records result

### With Notion

- Final refined docs can sync to Notion
- Manifest can track in Notion database
- ESCALATE items become Notion tasks

---

**Owner:** Jim Calhoun
**Version:** 1.0
**Created:** January 2026
