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

## Known Limitations

1. **Rules-based, not LLM-based**
   - The editor uses regex patterns, not Claude
   - Heavy rewriting requires manual review

2. **No Notion sync yet**
   - Final docs stay on filesystem
   - Manual push to Notion needed

3. **ESCALATE items need decisions**
   - These appear in the run manifest
   - Requires human judgment

---

## Next Steps (After Jim's Review)

1. [ ] Run full batch processing
2. [ ] Review ESCALATE items
3. [ ] Push refined docs to Notion
4. [ ] Rebuild RAG index with refined corpus
5. [ ] Share on web via RAG interface

---

**Ready when you are!**
