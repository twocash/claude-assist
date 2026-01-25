# Grove Docs Refinery - Pipeline Analysis

**Generated:** 2026-01-19
**Updated:** 2026-01-20
**Status:** Batch Processing Complete - 65 Documents Ready

---

## TL;DR - Current Status

1. **65 documents in refined/** - Ready for Notion sync
2. **34 docs successfully processed** with Opus (from original 42 REVISE docs)
3. **6 docs need re-run** (API credits ran out)
4. **2 docs still REVISE** (may need manual review)

---

## Current State Summary (POST-BATCH)

| Location | Count | Description |
|----------|-------|-------------|
| `input/` | 71 | Raw source documents (archive candidate) |
| `drafts/` | 74+ | Documents processed by Editor agent |
| `reviews/` | 74+ | Review verdicts from Reviewer agent |
| `refined/` | **65** | Final documents ready for Notion |

---

## Batch Run Results (2026-01-20)

**Re-ran 42 REVISE documents with Opus (claude-opus-4-20250514)**

| Result | Count | Notes |
|--------|-------|-------|
| **PASS** | 34 | Successfully processed and saved to refined/ |
| **REVISE** | 2 | May need manual editing |
| **ERROR** | 6 | API credits exhausted |
| **Total** | 42 | Runtime: 122.8 minutes |

### Documents Still Needing Work

**2 REVISE (need manual review):**
- `251200-V-THESIS-Grove World Changing Play V2 Draft.md`
- `251200-S-PATTERN-Hub Prefixes and Rules.md`

**6 ERRORS (API credits needed for re-run):**
- `260100-S-SPEC-DEX Master Code Hygiene Agent.md`
- `260100-S-EXEC-DEX Master Scan Prompt.md`
- `260105-S-SPEC-Exploration Architecture Self Validation.md`
- `251230-S-ARCH-Trellis Bedrock Addendum.md`
- `251200-V-ECON-Declining Take Rate Mechanism.md`
- `251200-V-ECON-Reverse Progressive Tax Model.md`

---

## Previous Review Verdicts (Before Batch)

| Verdict | Count | Action Required |
|---------|-------|-----------------|
| **PASS** | 33 | Moved to refined/ |
| **REVISE** | 36 | Re-run with Opus → 34 PASS, 2 still REVISE |
| **ESCALATE** | 5 | Technical failures, handled |

---

## Key Issues Identified

### Issue 1: Two Separate Document Populations
- **Refined (31 docs)**: Came FROM Notion via pull - these are edited/finalized
- **Input (71 docs)**: Local source files meant to go THROUGH refinery TO Notion

**Overlap exists** - e.g., "The Training Ratchet" exists in both:
- `refined/251217-v-research-the-training-ratchet.md--FINAL.md` (from Notion)
- `input/251200-V-RATCHET-Training Convergence.md` (local source)

### Issue 2: Editor Agent Failures
The REVISE and ESCALATE verdicts reveal a systematic problem:
- Editor produces metadata/summaries only, not actual rewritten content
- Reviewer correctly rejects these incomplete submissions

### Issue 3: No Deduplication Between Input and Notion
Documents added directly to Notion were never cross-referenced against input/ sources.

---

## Documents Requiring Action

### Category A: PASS verdicts not in refined/ (need upload)
These passed review but weren't moved to refined/Notion:

```
251200-v-research-world-models-memory-architectures.md
251200-v-edge-distributed-infrastructure-implications.md
251200-v-engage-terminal-deep-dive.md
251200-v-research-translation-emergence-in-llms.md
251200-v-engage-simulation-ethics-deep-dive.md
251200-v-econ-economics-deep-dive.md
251200-v-research-chinese-open-source-ratchet-evidence.md
251200-s-method-user-story-refinery.md
... (33 total)
```

### Category B: ESCALATE - Technical Failures (5 docs)
Need manual review/restart:

```
251200-v-strat-grove-as-everyday-ai.md
251230-s-draft-prompt-results-kitbash.md
251230-s-pattern-hub-naming-conventions.md
grove-vision-test.md
sprout_system.md
```

### Category C: REVISE - Incomplete Rewrites (36 docs)
Editor needs to re-run with proper output:

```
251200-s-arch-architecture-documentation-index.md
251200-s-arch-technical-architecture-reference.md
251200-s-method-sprout-system-cultivation.md
... (36 total)
```

### Category D: Already in Notion (overlap with input)
Need to identify and skip these to avoid duplicates.

---

## Recommended Action Plan

### Phase 1: Deduplication Analysis
1. Map refined/ titles to input/ sources
2. Mark input docs that already exist in Notion
3. Create skip list for those documents

### Phase 2: Process PASS Docs
1. For 33 PASS docs, check if already in Notion
2. Upload unique ones to Notion Grove Corpus
3. Move to refined/ with notion_id

### Phase 3: Re-run Failed Docs
1. Fix Editor agent prompt to produce complete content
2. Re-process 36 REVISE documents
3. Handle 5 ESCALATE cases manually

### Phase 4: Reconcile Remaining
1. Process any input docs that haven't been touched
2. Establish ongoing workflow for new documents

---

## Execution Plan

### Step 1: Map Input ↔ Notion (Skip Duplicates)

**Already in Notion (31 docs)** - these input files can be marked SKIP:

| Input File Pattern | Notion Title | Action |
|-------------------|--------------|--------|
| `V-RATCHET-Training Convergence` | The Training Ratchet | SKIP |
| `V-ECON-Asymptotic Convergence` | The Asymptotic Convergence... | SKIP |
| `V-RESEARCH-World Models Memory` | World Models and Memory... | SKIP |
| `V-STRAT-Grove Personal AI Village` | Grove: Your Personal AI Village | SKIP |
| `V-EDGE-Capability Trajectory` | Local AI Infrastructure... | SKIP |
| ... | (31 total) | SKIP |

### Step 2: Identify Truly New Documents (~40 docs)

Input docs NOT in Notion need processing:
- `251200-V-THESIS-Grove World Changing Play Full.md` (213KB - needs Opus)
- `251200-V-THESIS-Grove World Changing Play Condensed.md`
- `251200-V-THESIS-Grove World Changing Play V2 Draft.md`
- `251200-V-ENGAGE-Engagement Research Brief.md`
- `251200-V-ENGAGE-Journal System Architecture.md`
- `251200-V-ENGAGE-Knowledge Commons Deep Dive.md`
- `251200-V-RATCHET-Capability Propagation Thesis.md`
- `251200-V-RATCHET-Deep Dive.md`
- `251200-V-RATCHET-Quantitative Analysis.md`
- ... (more to inventory)

### Step 3: Process Long Documents with Opus

Documents over 30KB need special handling:

| Document | Size | Strategy |
|----------|------|----------|
| Grove World Changing Play Full | 213KB | Opus + chunking |
| Grove World Changing Play Condensed | 60KB | Opus |
| Asymptotic Convergence | 35KB | Already in Notion |
| Technical Architecture Reference | 35KB | Opus |
| Engagement Research Brief | 34KB | Opus |
| Research Agent Product Vision | 32KB | Already in Notion |

### Step 4: Re-run Refinery with Proper Model

For documents that failed REVISE:
1. Switch Editor to Opus or 200K context model
2. Re-process drafts that have incomplete content
3. Re-run Reviewer

### Step 5: Upload PASS Docs to Notion

33 documents with PASS verdicts:
1. Check if title already exists in Notion
2. If new: Upload to Grove Corpus database
3. If exists: Skip (Notion is authoritative)
4. Add notion_id to local frontmatter

---

## Document Triage by Size

### Tier 1: Small (<10KB) - Standard Processing
~30 documents - regular Sonnet processing

### Tier 2: Medium (10-30KB) - Needs Attention
~25 documents - may need Opus for reliability

### Tier 3: Large (30KB+) - Opus Required
~16 documents - must use Opus or chunking:
- Grove World Changing Play Full (213KB)
- Grove World Changing Play Condensed (60KB)
- Technical Architecture Reference (35KB)
- Engagement Research Brief (34KB)
- And 12 more...

---

## Questions for Jim

1. **Canonical source**: Should Notion or local files be the source of truth going forward?
2. **Duplicate handling**: For docs that exist in both input and Notion, keep Notion version?
3. **ESCALATE docs**: Are these test files that can be deleted, or real content?
4. **Date prefixes**: Should we update all to proper dates or keep 251200/260100 conventions?
