# Grove Research Generator

Automated research document pipeline triggered by @atlas mentions in Notion.

## Overview

This system generates polished research documents (blog posts, whitepapers, deep dives) with:
- Claude API integration for intelligent generation
- LEANN RAG for Grove context retrieval
- Chicago-style citations
- Editorial learning loop (learns from your edits)

## Quick Start

```bash
# Test the system
python -m grove_research_generator test

# Generate a document
python -m grove_research_generator generate --topic "Trellis Architecture" --format blog

# Build the LEANN index
python -m grove_research_generator build-index
```

## Workflow

### For Jim (User Workflow)

1. **Request a document**: Comment `@atlas write a blog post about X, focusing on Y` on any Notion page
2. **Review draft**: Atlas posts the draft directly to the page
3. **Edit**: Make your changes directly in Notion
4. **Complete**: Comment `@atlas this is complete`
5. **Learn**: Atlas analyzes your edits and updates its editorial memory

### Trigger Patterns

**Research Requests:**
- `@atlas write a blog about...`
- `@atlas turn this into a whitepaper`
- `@atlas create a document about...`
- `@atlas research X and draft...`

**Completion:**
- `@atlas this is complete`
- `@atlas done`
- `@atlas publish this`

## Architecture

```
grove_research_generator/
├── config.py              # Configuration + database IDs
├── orchestrator.py        # Main pipeline coordinator
├── draft_storage.py       # Stores drafts for diff comparison
├── cli.py                 # Command-line interface
├── build_index.py         # LEANN index builder
├── editorial_memory.md    # Learned editorial preferences
├── agents/
│   ├── prompt_builder.py  # Structures prompts from direction
│   ├── researcher.py      # LEANN RAG queries
│   ├── writer.py          # Claude document generation
│   ├── reviewer.py        # Quality validation
│   └── learning.py        # Diff analyzer + memory updater
├── prompts/
│   ├── research_engine.md     # Writing methodology
│   ├── research_checkpoint.md # Grove terminology
│   └── citation_guide.md      # Chicago style rules
└── workflows/
    └── notion_trigger.py  # @atlas mention detection
```

## Editorial Learning Loop

The system learns from your edits:

1. **Store**: When Atlas posts a draft, the original is saved
2. **Compare**: When you mark it complete, Atlas diffs original vs edited
3. **Extract**: Patterns are categorized (terminology, voice, concepts, structure)
4. **Remember**: `editorial_memory.md` is updated with new learnings
5. **Apply**: Future generations load the memory into Claude's system prompt

### Current Learnings

See `editorial_memory.md` for accumulated preferences. Example:
- "The Grove" (not "Grove") - always use the article

## Document Formats

| Format | Length | Purpose |
|--------|--------|---------|
| `blog` | 800-1500 words | Accessible insights for general readers |
| `whitepaper` | 2000-4000 words | Technical depth with executive accessibility |
| `deep_dive` | 3000-6000 words | Comprehensive exploration for technical readers |

## Voice Standards

- **Strategic, not smug** - Show insight without condescension
- **Concrete over abstract** - Use specific examples
- **Honest about uncertainty** - Acknowledge what we don't know
- **8th-grade accessibility, graduate-level thinking**
- **Active voice, present tense**

## Configuration

Key database IDs are in `config.py`:
- `ATLAS_FEED` - Conversation log
- `THE_GROVE_PAGE` - Parent for research documents
- `SAMPLE_BLOG_POST` - Reference document

## Dependencies

- `anthropic` - Claude API
- `leann` - RAG (optional, falls back gracefully)
- Notion MCP server for posting

---

*Part of the Atlas AI Chief of Staff system*
