# Grove Docs Refinery

A comprehensive document management system for Grove Foundation content. Includes batch content refactoring, Notion integration, and daily corpus synchronization.

## Quick Reference

| Task | Command |
|------|---------|
| Batch refine docs | `python -m grove_docs_refinery.refinery` |
| Generate research doc | `python research_generator.py --blog-url URL --paper-url URL` |
| Upload to Notion | `python upload_to_notion.py --apply` |
| Sync from Notion | `python notion_corpus_sync.py` |
| Check sync status | `python notion_corpus_sync.py --check` |
| Standardize metadata | `python standardize_metadata.py --apply` |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    GROVE DOCS REFINERY                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐        │
│   │   INPUT     │───►│   EDITOR    │───►│  REVIEWER   │        │
│   │   FILES     │    │   AGENT     │    │   AGENT     │        │
│   └─────────────┘    └─────────────┘    └──────┬──────┘        │
│                                                │               │
│                      ┌─────────────────────────┼─────┐         │
│                      │           │             │     │         │
│                      ▼           ▼             ▼     ▼         │
│                ┌─────────┐  ┌──────┐     ┌──────┐ ┌────────┐   │
│                │  PASS   │  │REVISE│     │REVISE│ │ESCALATE│   │
│                └────┬────┘  └──────┘     └──────┘ └───┬────┘   │
│                     │                                 │        │
│                     ▼                                 ▼        │
│                ┌─────────┐                      ┌────────┐     │
│                │ REFINED │                      │  JIM   │     │
│                │ CORPUS  │                      │DECISION│     │
│                └────┬────┘                      └────────┘     │
│                     │                                          │
│         ┌───────────┴───────────┐                              │
│         ▼                       ▼                              │
│   ┌───────────┐          ┌───────────┐                         │
│   │  NOTION   │◄────────►│  LOCAL    │                         │
│   │   DOCS    │  (sync)  │  CORPUS   │                         │
│   └───────────┘          └───────────┘                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Notion Documentation Structure

The canonical Grove documentation lives in Notion under **The Grove > 📚 Documentation**:

| Category | Notion Page ID | Description |
|----------|----------------|-------------|
| **📚 Documentation** | `2ed780a78eef81059f0ec7177f68f464` | Parent container |
| Vision | `2ed780a78eef81dfb5acd6f4a24d66d3` | Thesis, research, strategy |
| Software | `2ed780a78eef81cf9ccffb7820e047a3` | Architecture, protocols, specs |
| Blog Posts | `2ed780a78eef817da309ebb7228ee053` | Published articles |

**Notion is the source of truth.** Edit documents in Notion; the daily sync updates local corpus.

---

## Corpus Sync System

### Daily Sync (Notion → Local)

```bash
# Preview changes
python notion_corpus_sync.py --check

# Apply sync
python notion_corpus_sync.py

# Sync specific category
python notion_corpus_sync.py --category vision
```

### Automated Sync (Task Scheduler)

Use `run_corpus_sync.bat` for Windows Task Scheduler:

1. Open Task Scheduler (`taskschd.msc`)
2. Create Basic Task → "Grove Corpus Sync"
3. Trigger: Daily, 6:00 AM
4. Action: Start `run_corpus_sync.bat`
5. Start in: `C:\GitHub\claude-assist`

### Initial Upload (Local → Notion)

```bash
# Preview
python upload_to_notion.py --check

# Upload all refined docs
python upload_to_notion.py --apply
```

---

## Document Metadata

All refined documents include standardized YAML frontmatter:

```yaml
---
title: "Document Title"
author: "Jim Calhoun"
copyright: "2026 The Grove Foundation"
date: "2026-01-18"
type: "vision"          # vision | spec | blog
domain: "research"      # research | architecture | economics | etc.
status: "final"
notion_url: "https://www.notion.so/..."
notion_id: "uuid"
last_synced: "ISO timestamp"
tags:
  - tag1
  - tag2
---
```

### Standardize Metadata

```bash
# Preview
python standardize_metadata.py --check

# Apply to all files
python standardize_metadata.py --apply

# Single file
python standardize_metadata.py --single filename.md
```

---

## Components

### Core Refinery

| Component | File | Purpose |
|-----------|------|---------|
| Orchestrator | `refinery.py` | Main workflow orchestration |
| Editor | `editor.py` | Content rewriting agent |
| Reviewer | `reviewer.py` | Quality validation agent |
| Checkpoint | `checkpoint.py` | Dynamic state management |
| Config | `config.py` | Configuration loader |

### Research Generator

| Component | File | Purpose |
|-----------|------|---------|
| Generator | `research_generator.py` | Blog + Paper → Technical Doc |
| System Prompt | `prompts/research_system.md` | Grove voice + Chicago citations |

**Usage:**
```bash
# Deep dive from Notion blog + arXiv paper
python research_generator.py \
  --blog-url "https://notion.so/page-id" \
  --paper-url "https://arxiv.org/abs/2510.20809" \
  --output-type deep-dive

# Output types: deep-dive | technical-brief | research-note
```

### Notion Integration

| Component | File | Purpose |
|-----------|------|---------|
| Corpus Sync | `notion_corpus_sync.py` | Daily Notion → Local sync |
| Upload | `upload_to_notion.py` | Bulk Local → Notion upload |
| Metadata | `standardize_metadata.py` | Frontmatter standardization |
| Scheduler | `run_corpus_sync.bat` | Task Scheduler wrapper |

### Methodology Files

| File | Purpose |
|------|---------|
| `editorial-engine.md` | Stable methodology (how to rewrite) |
| `editorial-checkpoint.md` | Dynamic state (what's current) |

---

## Directory Structure

```
grove_docs_refinery/
├── __init__.py
├── refinery.py              # Main orchestrator
├── research_generator.py    # Blog + Paper → Technical Doc
├── editor.py                # Writer agent
├── reviewer.py              # Reviewer agent
├── checkpoint.py            # Checkpoint manager
├── config.py                # Configuration
├── notion_corpus_sync.py    # Notion → Local sync
├── upload_to_notion.py      # Local → Notion upload
├── standardize_metadata.py  # Metadata standardizer
├── run_corpus_sync.bat      # Task Scheduler wrapper
├── editorial-engine.md      # Methodology
├── editorial-checkpoint.md  # Current state
├── config.yaml              # Settings
├── .notion_sync_state.json  # Sync state tracking
├── prompts/                 # System prompts
│   ├── research_system.md   # Research doc generation
│   ├── writer_system.md     # Editor agent
│   └── reviewer_system.md   # Reviewer agent
├── input/                   # Source files (raw)
├── drafts/                  # Editor outputs
├── reviews/                 # Reviewer outputs
├── refined/                 # Final outputs (synced with Notion)
├── research_output/         # Generated research docs
└── logs/                    # Run manifests
```

---

## Workflow

### Document Lifecycle

1. **Draft** → Write/paste raw content
2. **Refinery** → Run through editor + reviewer agents
3. **Upload** → Push to Notion Documentation
4. **Edit** → Make changes in Notion (source of truth)
5. **Sync** → Daily sync updates local corpus
6. **Index** → LEANN RAG indexes local corpus

### File Naming Convention

| Stage | Pattern | Example |
|-------|---------|---------|
| Input | Raw filename | `grove-white-paper.md` |
| Draft | `--DRAFT.md` | `grove-white-paper--DRAFT.md` |
| Review | `--REVIEW.md` | `grove-white-paper--REVIEW.md` |
| Final | `YYMMDD-t-category-slug.md--FINAL.md` | `260118-v-vision-training-ratchet.md--FINAL.md` |

Type codes: `v` = vision, `s` = software/spec, `b` = blog

---

## Integration Points

### Atlas Comment Dispositions

Disposition content via Notion comments:

| Command | Effect |
|---------|--------|
| `@atlas approved` | Mark as approved |
| `@atlas published` | Mark as published, file to canon |
| `@atlas complete` | Mark workflow complete |
| `@atlas revise` | Request revision |
| `@atlas archive` | Archive/file content |

Atlas scans all pages for disposition comments at startup via `atlas_startup.py`.

### Atlas Inbox

Send research from Claude Desktop to Atlas:
- Say "send to Atlas" in Claude Desktop
- Content appears in Atlas Inbox for triage
- Processing commands: polish, refinery, blog post

### LEANN RAG

The refined corpus feeds the LEANN semantic search index:
```bash
leann build grove-knowledge \
  --docs ./refined \
  --embedding-model all-MiniLM-L6-v2
```

### Notion Provenance

Every synced document includes:
- `notion_id` - UUID for API operations
- `notion_url` - Direct link to Notion page
- `last_synced` - Timestamp of last sync

---

## Environment Setup

Required environment variables:

```bash
NOTION_API_KEY=secret_...
ANTHROPIC_API_KEY=sk-...  # For refinery agents
```

Python dependencies:
```bash
pip install requests python-dotenv pyyaml anthropic
```

---

## Assessment Types

| Status | Meaning | Action |
|--------|---------|--------|
| PASS | Ready for use | Upload to Notion |
| REVISE | Needs editor revision | Re-run through editor |
| ESCALATE | Requires human decision | Review manually |

---

**Owner:** Jim Calhoun
**Version:** 2.1
**Updated:** January 18, 2026
