#!/usr/bin/env python3
"""
Grove Research Document Generator

Transforms blog posts into technical documents by combining:
- Blog post structure/outline
- Source paper analysis
- Grove voice standards

Usage:
    # From Notion blog post + arXiv paper
    python research_generator.py \
        --blog-url "https://notion.so/page-id" \
        --paper-url "https://arxiv.org/abs/2510.20809" \
        --output-type deep-dive

    # From local file + paper
    python research_generator.py \
        --blog-file "./blog-post.md" \
        --paper-url "https://arxiv.org/abs/2510.20809" \
        --output-type technical-brief

    # Just generate, don't run through refinery
    python research_generator.py \
        --blog-url "..." \
        --paper-url "..." \
        --no-refinery
"""

import os
import re
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')

# Paths
SCRIPT_DIR = Path(__file__).parent
PROMPTS_DIR = SCRIPT_DIR / "prompts"
INPUT_DIR = SCRIPT_DIR / "input"
OUTPUT_DIR = SCRIPT_DIR / "research_output"

# Document types
DOCUMENT_TYPES = {
    "deep-dive": {
        "name": "Deep Dive",
        "description": "Comprehensive technical analysis with full citations",
        "target_length": "3000-5000 words",
        "style": "Academic but accessible",
    },
    "technical-brief": {
        "name": "Technical Brief",
        "description": "Focused technical summary for practitioners",
        "target_length": "1500-2500 words",
        "style": "Dense, practical, implementation-focused",
    },
    "research-note": {
        "name": "Research Note",
        "description": "Quick synthesis connecting paper to Grove thesis",
        "target_length": "800-1200 words",
        "style": "Insight-focused, conversational",
    },
}


@dataclass
class ResearchContext:
    """Context for document generation."""
    blog_content: str
    blog_title: str
    paper_content: str
    paper_title: str
    paper_url: str
    output_type: str
    additional_context: Optional[str] = None


def fetch_arxiv_paper(arxiv_url: str) -> Dict[str, str]:
    """Fetch arXiv paper abstract and metadata."""
    # Extract paper ID
    # Handles: arxiv.org/abs/2510.20809, arxiv.org/pdf/2510.20809
    match = re.search(r'(\d{4}\.\d{4,5})', arxiv_url)
    if not match:
        raise ValueError(f"Could not parse arXiv ID from: {arxiv_url}")

    paper_id = match.group(1)

    # Fetch from arXiv API
    api_url = f"http://export.arxiv.org/api/query?id_list={paper_id}"
    response = requests.get(api_url)
    response.raise_for_status()

    # Parse XML response
    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)

    # arXiv uses Atom namespace
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    entry = root.find('atom:entry', ns)
    if entry is None:
        raise ValueError(f"Paper not found: {paper_id}")

    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
    abstract = entry.find('atom:summary', ns).text.strip()

    # Get authors
    authors = []
    for author in entry.findall('atom:author', ns):
        name = author.find('atom:name', ns).text
        authors.append(name)

    # Get published date
    published = entry.find('atom:published', ns).text[:10]

    # Try to get PDF content (basic extraction)
    pdf_url = f"https://arxiv.org/pdf/{paper_id}.pdf"

    return {
        "id": paper_id,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "published": published,
        "url": f"https://arxiv.org/abs/{paper_id}",
        "pdf_url": pdf_url,
        "content": f"""# {title}

**Authors:** {', '.join(authors)}
**Published:** {published}
**arXiv:** {paper_id}

## Abstract

{abstract}

---
*Full paper available at: {pdf_url}*
"""
    }


def fetch_notion_page(page_url: str) -> Dict[str, str]:
    """Fetch content from a Notion page."""
    if not NOTION_API_KEY:
        raise ValueError("NOTION_API_KEY not set")

    # Extract page ID from URL
    # Handles: notion.so/Page-Title-abc123def456
    match = re.search(r'([a-f0-9]{32}|[a-f0-9-]{36})$', page_url.replace('-', ''))
    if not match:
        # Try to find ID in the URL path
        match = re.search(r'-([a-f0-9]{32})(?:\?|$)', page_url)
        if not match:
            raise ValueError(f"Could not parse Notion page ID from: {page_url}")

    page_id = match.group(1)

    # Format with dashes if needed
    if len(page_id) == 32:
        page_id = f"{page_id[:8]}-{page_id[8:12]}-{page_id[12:16]}-{page_id[16:20]}-{page_id[20:]}"

    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }

    # Get page properties
    page_resp = requests.get(
        f'https://api.notion.com/v1/pages/{page_id}',
        headers=headers
    )
    page_resp.raise_for_status()
    page_data = page_resp.json()

    # Extract title
    title = "Untitled"
    props = page_data.get('properties', {})
    for prop_name, prop_val in props.items():
        if prop_val.get('type') == 'title':
            title_arr = prop_val.get('title', [])
            if title_arr:
                title = title_arr[0].get('plain_text', 'Untitled')
            break

    # Get page content (blocks)
    blocks_resp = requests.get(
        f'https://api.notion.com/v1/blocks/{page_id}/children?page_size=100',
        headers=headers
    )
    blocks_resp.raise_for_status()
    blocks_data = blocks_resp.json()

    # Convert blocks to markdown
    content_parts = [f"# {title}\n"]

    for block in blocks_data.get('results', []):
        block_type = block.get('type')
        block_content = block.get(block_type, {})

        if block_type == 'paragraph':
            text = extract_rich_text(block_content.get('rich_text', []))
            if text:
                content_parts.append(text)
        elif block_type == 'heading_1':
            text = extract_rich_text(block_content.get('rich_text', []))
            content_parts.append(f"# {text}")
        elif block_type == 'heading_2':
            text = extract_rich_text(block_content.get('rich_text', []))
            content_parts.append(f"## {text}")
        elif block_type == 'heading_3':
            text = extract_rich_text(block_content.get('rich_text', []))
            content_parts.append(f"### {text}")
        elif block_type == 'bulleted_list_item':
            text = extract_rich_text(block_content.get('rich_text', []))
            content_parts.append(f"- {text}")
        elif block_type == 'numbered_list_item':
            text = extract_rich_text(block_content.get('rich_text', []))
            content_parts.append(f"1. {text}")
        elif block_type == 'quote':
            text = extract_rich_text(block_content.get('rich_text', []))
            content_parts.append(f"> {text}")
        elif block_type == 'code':
            text = extract_rich_text(block_content.get('rich_text', []))
            lang = block_content.get('language', '')
            content_parts.append(f"```{lang}\n{text}\n```")
        elif block_type == 'divider':
            content_parts.append("---")

    return {
        "title": title,
        "content": "\n\n".join(content_parts),
        "url": page_url,
    }


def extract_rich_text(rich_text_arr: list) -> str:
    """Extract plain text from Notion rich text array."""
    return ''.join(rt.get('plain_text', '') for rt in rich_text_arr)


def load_local_file(file_path: Path) -> Dict[str, str]:
    """Load content from a local markdown file."""
    content = file_path.read_text(encoding='utf-8')

    # Try to extract title from first heading
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file_path.stem

    return {
        "title": title,
        "content": content,
        "path": str(file_path),
    }


def load_system_prompt(output_type: str) -> str:
    """Load the research generator system prompt."""
    prompt_path = PROMPTS_DIR / "research_system.md"

    if prompt_path.exists():
        base_prompt = prompt_path.read_text(encoding='utf-8')
    else:
        base_prompt = DEFAULT_RESEARCH_PROMPT

    # Add document type specifics
    doc_type = DOCUMENT_TYPES.get(output_type, DOCUMENT_TYPES["deep-dive"])

    type_section = f"""
## Document Type: {doc_type['name']}

**Description:** {doc_type['description']}
**Target Length:** {doc_type['target_length']}
**Style:** {doc_type['style']}
"""

    return base_prompt + type_section


def generate_research_document(context: ResearchContext) -> str:
    """Generate the technical document using Claude."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set")

    system_prompt = load_system_prompt(context.output_type)

    user_prompt = f"""## Source Blog Post

**Title:** {context.blog_title}

{context.blog_content}

---

## Source Paper

**Title:** {context.paper_title}
**URL:** {context.paper_url}

{context.paper_content}

---

## Task

Transform the blog post into a **{DOCUMENT_TYPES[context.output_type]['name']}** that:

1. Uses the blog post's structure and key insights as a foundation
2. Incorporates technical details and analysis from the source paper
3. Adds proper Chicago-style footnote citations
4. Maintains Grove voice standards (strategic, concrete, honest)
5. Expands on the connections between the paper and Grove's thesis

{f"Additional context: {context.additional_context}" if context.additional_context else ""}

Generate the full document now.
"""

    # Call Claude API
    response = requests.post(
        'https://api.anthropic.com/v1/messages',
        headers={
            'x-api-key': ANTHROPIC_API_KEY,
            'content-type': 'application/json',
            'anthropic-version': '2023-06-01',
        },
        json={
            'model': 'claude-sonnet-4-20250514',
            'max_tokens': 8000,
            'system': system_prompt,
            'messages': [
                {'role': 'user', 'content': user_prompt}
            ]
        }
    )
    response.raise_for_status()

    result = response.json()
    return result['content'][0]['text']


def add_frontmatter(content: str, context: ResearchContext) -> str:
    """Add YAML frontmatter to the document."""
    date_str = datetime.now().strftime('%Y-%m-%d')

    # Determine type code
    type_map = {
        "deep-dive": "vision",
        "technical-brief": "software",
        "research-note": "vision",
    }
    doc_type = type_map.get(context.output_type, "vision")

    frontmatter = f"""---
title: "{context.paper_title} - Technical Analysis"
author: "Jim Calhoun"
copyright: "2026 The Grove Foundation"
date: "{date_str}"
type: "{doc_type}"
domain: "research"
status: "draft"
source_paper: "{context.paper_url}"
source_blog: "{context.blog_title}"
---
"""

    return frontmatter + content


def main():
    parser = argparse.ArgumentParser(
        description="Generate technical documents from blog posts + papers"
    )

    # Blog source (one required)
    blog_group = parser.add_mutually_exclusive_group(required=True)
    blog_group.add_argument('--blog-url', help='Notion page URL for blog post')
    blog_group.add_argument('--blog-file', type=Path, help='Local markdown file')

    # Paper source
    parser.add_argument('--paper-url', required=True, help='arXiv or paper URL')

    # Output options
    parser.add_argument(
        '--output-type',
        choices=list(DOCUMENT_TYPES.keys()),
        default='deep-dive',
        help='Type of document to generate'
    )
    parser.add_argument('--output-file', type=Path, help='Output file path')
    parser.add_argument('--no-refinery', action='store_true',
                       help='Skip refinery pass')
    parser.add_argument('--context', help='Additional context/instructions')

    args = parser.parse_args()

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=" * 60)
    print("GROVE RESEARCH DOCUMENT GENERATOR")
    print("=" * 60)

    # Fetch blog content
    print("\n[1/4] Fetching blog post...")
    if args.blog_url:
        blog_data = fetch_notion_page(args.blog_url)
        print(f"  Title: {blog_data['title']}")
    else:
        blog_data = load_local_file(args.blog_file)
        print(f"  File: {args.blog_file}")

    # Fetch paper
    print("\n[2/4] Fetching source paper...")
    if 'arxiv.org' in args.paper_url:
        paper_data = fetch_arxiv_paper(args.paper_url)
        print(f"  Title: {paper_data['title']}")
        print(f"  Authors: {', '.join(paper_data['authors'][:3])}...")
    else:
        # For non-arXiv, just store the URL
        paper_data = {
            "title": "External Paper",
            "content": f"Paper URL: {args.paper_url}",
            "url": args.paper_url,
        }
        print(f"  URL: {args.paper_url}")

    # Build context
    context = ResearchContext(
        blog_content=blog_data['content'],
        blog_title=blog_data['title'],
        paper_content=paper_data['content'],
        paper_title=paper_data['title'],
        paper_url=paper_data.get('url', args.paper_url),
        output_type=args.output_type,
        additional_context=args.context,
    )

    # Generate document
    print(f"\n[3/4] Generating {DOCUMENT_TYPES[args.output_type]['name']}...")
    document = generate_research_document(context)

    # Add frontmatter
    document = add_frontmatter(document, context)

    # Determine output path
    if args.output_file:
        output_path = args.output_file
    else:
        # Generate filename from paper title
        slug = re.sub(r'[^a-z0-9]+', '-', paper_data['title'].lower())[:50]
        date_prefix = datetime.now().strftime('%y%m%d')
        type_code = 'v' if args.output_type != 'technical-brief' else 's'
        output_path = OUTPUT_DIR / f"{date_prefix}-{type_code}-research-{slug}.md"

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding='utf-8')
    print(f"  Saved: {output_path}")

    # Optionally run through refinery
    if not args.no_refinery:
        print("\n[4/4] Running through refinery...")
        # Copy to input directory for refinery
        refinery_input = INPUT_DIR / output_path.name
        refinery_input.write_text(document, encoding='utf-8')
        print(f"  Copied to refinery input: {refinery_input}")
        print("  Run: python -m grove_docs_refinery.refinery --single", refinery_input)
    else:
        print("\n[4/4] Skipping refinery (--no-refinery)")

    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"Output: {output_path}")
    print(f"Words: ~{len(document.split())}")

    return output_path


# Default prompt if file doesn't exist
DEFAULT_RESEARCH_PROMPT = """# Grove Research Document Generator

You are generating a technical research document for The Grove Foundation.

## Voice Standards

1. **Strategic, not smug** — Confidence without arrogance
2. **Concrete over abstract** — Specific mechanisms, not vague claims
3. **Honest about uncertainty** — "This is our hypothesis" beats false certainty
4. **8th-grade accessibility, graduate-level thinking** — Simple sentences, sophisticated ideas

## Citation Style

Use Chicago-style footnotes:

```
The paper demonstrates significant efficiency gains.¹

---
¹ Author Name, "Paper Title," arXiv:XXXX.XXXXX (Month Year), https://arxiv.org/abs/XXXX.XXXXX.
```

## Structure

1. **Opening** — State the core insight (the "so what")
2. **Context** — What problem does this address?
3. **Analysis** — Technical breakdown with paper citations
4. **Grove Connection** — How this relates to Grove's thesis
5. **Implications** — What this means going forward

## Terminology

- **Exploration architecture** (not "AI platform")
- **Agents** (not "bots" or "AI assistants")
- **Trellis Architecture** (the standard), **Grove** (the implementation)
- **Foundation** (the organization), **Terminal** (the interface)

## What to Avoid

- Buzzwords: "revolutionary," "paradigm shift," "democratize"
- Hedging: "might," "could potentially"
- Crypto signaling: "tokenomics," "network effects," "moats"
- Generic AI hype: "the future of AI," "unprecedented"
"""


if __name__ == '__main__':
    main()
