# Grove Docs Refinery - Setup Status

**Date:** January 17, 2026
**Status:** Ready for batch processing

---

## What's Ready

### Input Corpus (71 files)
- **Source:** `C:\GitHub\the-grove-foundation\grove-documents`
- **Copied to:** `grove_docs_refinery/input/` (working copies)
- **Files excluded:** CROSSREF.md, INVENTORY_REPORT.md, RENAME_MANIFEST.md

### Processing Pipeline
The refinery runs a two-stage pipeline:

```
Input File → Editor Agent → Draft → Reviewer Agent → Assessment
                                                         ↓
                                              PASS → refined/
                                              REVISE → stays in drafts/
                                              ESCALATE → requires decision
```

### Tested Output
Single file test completed successfully:
- `251200-V-THESIS-Grove World Changing Play Summary.md` → **PASS**
- Located in: `refined/251200-v-thesis-grove-world-changing-play-summary.md--FINAL.md`

---

## How to Run

### Option 1: Full Batch Processing
```bash
cd C:\GitHub\claude-assist
python -m grove_docs_refinery.refinery
```
This processes all 71 files. Expect ~5-10 minutes depending on file sizes.

### Option 2: Single File
```bash
python -m grove_docs_refinery.refinery --single "grove_docs_refinery/input/FILENAME.md"
```

### Option 3: Custom Batch Size
```bash
python -m grove_docs_refinery.refinery --batch-size 10
```

---

## What the Editor Does

The Editor Agent applies rules-based transformations:

1. **Terminology Fixes** (automatic)
   - "AI platform" → "exploration architecture"
   - "decentralized AI" → "distributed AI infrastructure"
   - "bots" → "agents"
   - "tokens" → "credits"

2. **Hedging Removal** (automatic)
   - Removes: "might", "could potentially", "it's possible that"
   - Converts: "might be" → "is", "could be" → "is"

3. **Filler Removal** (automatic)
   - Removes: "It's important to note that", "In order to"

4. **Analysis** (reported in draft)
   - Document type classification
   - Audience identification
   - Argument flow assessment
   - Evidence quality check

---

## What the Reviewer Checks

The Reviewer Agent validates against Grove standards:

| Check | Pass Criteria |
|-------|---------------|
| Terminology | No legacy terms remaining |
| Positioning | Key concepts present (exploration, distributed, local, agents) |
| Technical Accuracy | No obvious errors introduced |
| Voice | No prohibited language |
| Length | Appropriate for document type |

### Assessment Outcomes
- **PASS:** Ready for use → moved to `refined/`
- **REVISE:** Needs editor revision → stays in `drafts/`
- **ESCALATE:** Requires human decision → logged in manifest

---

## Output Locations

| Stage | Path | Suffix |
|-------|------|--------|
| Working copies | `input/` | `.md` |
| Editor drafts | `drafts/` | `--DRAFT.md` |
| Reviewer reports | `reviews/` | `--REVIEW.md` |
| Final approved | `refined/` | `--FINAL.md` |
| Run logs | `logs/` | `refinery-run-YYYYMMDD-HHMMSS.json` |

---

## Integration with RAG

The GroveRAG system at `workspace/leann-evaluation/` can index refined documents:

```python
# After batch processing completes
# Copy refined docs to RAG corpus
# Rebuild index

from rag_engine import GroveRAG
rag = GroveRAG()
rag.load_model()
rag.load_documents()  # Will pick up new files
rag.build_index()
rag.save()
```

---

## Review Before Processing

**Jim:** Before running the full batch, you may want to:

1. **Spot-check a few files manually**
   ```bash
   python -m grove_docs_refinery.refinery --single "grove_docs_refinery/input/251200-S-ARCH-Trellis First Order Directives v2.md"
   ```

2. **Review the output**
   - Check `drafts/` for the rewritten version
   - Check `reviews/` for the assessment report
   - Check `refined/` if it passed

3. **Adjust config.yaml if needed**
   - Terminology mappings
   - Avoid terms list
   - Voice standards

---

## Notion Sync (NEW - January 2026)

**The sync module is now operational!**

### Current State
- **31 documents** in `refined/` are linked to Notion Grove Corpus
- Each file has `notion_id` and `notion_url` in YAML frontmatter
- Bidirectional sync available via `sync/` module

### Workflow
```
Jim edits in Notion  →  Sync pulls to refined/  →  Local canonical backup
     (source)              (atlas runs)              (versioned)
```

### Commands
```bash
# Pull all documents from Notion
python -m grove_docs_refinery.sync.pull_all

# Pull single document
python -c "from sync.pull import PullManager; from sync.api import get_api; PullManager(get_api()).pull_page('PAGE_ID')"

# Audit properties
python -m grove_docs_refinery.sync.audit_properties

# Update domains
python -m grove_docs_refinery.sync.update_domains --apply
```

### Linkage Verified
All refined files have notion_id linking them to Notion:
```yaml
---
notion_id: 2ed780a7-8eef-8103-ad94-ff897214dd1e
notion_url: https://www.notion.so/The-Training-Ratchet-...
last_synced: '2026-01-19T22:06:38.958698'
---
```

---

## Known Limitations

1. **Long documents may exceed context limits**
   - Documents over 30KB need Opus or chunking
   - REVISE verdicts often indicate context overflow

2. **ESCALATE items need decisions**
   - These appear in the run manifest
   - Requires human judgment

3. **Refinery drafts are not linked to Notion**
   - input/ → drafts/ → reviews/ pipeline is separate
   - For documents already in Notion, use sync instead

---

## Batch Processing Results (2026-01-20)

**Opus Batch Run Completed:**
- **34 documents processed successfully** using claude-opus-4-20250514
- **Total refined documents: 65** (up from 31)
- **Runtime: 122.8 minutes**

### Remaining Items
- **2 REVISE docs** - May need manual review:
  - `251200-V-THESIS-Grove World Changing Play V2 Draft.md`
  - `251200-S-PATTERN-Hub Prefixes and Rules.md`

- **6 ERROR docs** - API credits needed for re-run:
  - `260100-S-SPEC-DEX Master Code Hygiene Agent.md`
  - `260100-S-EXEC-DEX Master Scan Prompt.md`
  - `260105-S-SPEC-Exploration Architecture Self Validation.md`
  - `251230-S-ARCH-Trellis Bedrock Addendum.md`
  - `251200-V-ECON-Declining Take Rate Mechanism.md`
  - `251200-V-ECON-Reverse Progressive Tax Model.md`

---

## Next Steps

1. [x] Run batch processing with Opus ✓ (34/42 success)
2. [ ] Re-run 6 failed docs (when API credits available)
3. [ ] Review 2 REVISE docs manually
4. [ ] Push new refined docs to Notion
5. [ ] Archive legacy input/drafts/reviews folders
6. [ ] Establish Notion-first workflow

---

**65 documents ready for Notion sync!**
