#!/usr/bin/env python3
"""
Grove Corpus Upload to Notion

Uploads refined documents to the Notion Documentation structure.
Reads YAML frontmatter and places docs in appropriate categories.

Usage:
    python upload_to_notion.py --check     # Preview what would be uploaded
    python upload_to_notion.py --apply     # Actually upload
"""

import os
import re
import yaml
import requests
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

# Configuration
NOTION_KEY = os.environ.get('NOTION_API_KEY')
REFINED_DIR = Path(__file__).parent / "refined"

# Category page IDs (created in Documentation structure)
CATEGORY_IDS = {
    "vision": "2ed780a78eef81dfb5acd6f4a24d66d3",
    "software": "2ed780a78eef81cf9ccffb7820e047a3",
    "spec": "2ed780a78eef81cf9ccffb7820e047a3",  # Same as software
    "blog": "2ed780a78eef817da309ebb7228ee053",
    "blog posts": "2ed780a78eef817da309ebb7228ee053"
}

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}


def parse_frontmatter(filepath: Path) -> Dict:
    """Extract YAML frontmatter from markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize line endings to LF
    content = content.replace('\r\n', '\n')

    if not content.startswith('---'):
        return {}

    # Find closing ---
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return {}

    yaml_str = content[3:end_match.start() + 3]
    try:
        return yaml.safe_load(yaml_str)
    except:
        return {}


def get_content_without_frontmatter(filepath: Path) -> str:
    """Get markdown content without YAML frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Normalize line endings to LF
    content = content.replace('\r\n', '\n')

    if not content.startswith('---'):
        return content

    # Find closing ---
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return content

    return content[end_match.end() + 3:].strip()


# Valid Notion code block languages
NOTION_LANGUAGES = {
    'typescript': 'typescript', 'tsx': 'typescript', 'ts': 'typescript',
    'javascript': 'javascript', 'jsx': 'javascript', 'js': 'javascript',
    'python': 'python', 'py': 'python',
    'bash': 'bash', 'shell': 'bash', 'sh': 'bash', 'zsh': 'bash',
    'json': 'json', 'yaml': 'yaml', 'yml': 'yaml',
    'html': 'html', 'css': 'css', 'sql': 'sql',
    'markdown': 'markdown', 'md': 'markdown',
    'rust': 'rust', 'go': 'go', 'java': 'java', 'c': 'c', 'cpp': 'c++',
    'ruby': 'ruby', 'php': 'php', 'swift': 'swift', 'kotlin': 'kotlin',
    '': 'plain text', 'text': 'plain text', 'txt': 'plain text'
}


def truncate_text(text: str, max_len: int = 1900) -> str:
    """Truncate text to fit Notion's 2000 char limit with buffer."""
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."


def markdown_to_notion_blocks(content: str) -> list:
    """Convert markdown to Notion blocks (simplified)."""
    blocks = []
    lines = content.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]

        # Headings
        if line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": truncate_text(line[4:])}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": truncate_text(line[3:])}}]
                }
            })
        elif line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": truncate_text(line[2:])}}]
                }
            })
        # Code blocks
        elif line.startswith('```'):
            lang = line[3:].strip().lower()
            # Map to valid Notion language
            notion_lang = NOTION_LANGUAGES.get(lang, 'plain text')
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_content = '\n'.join(code_lines)
            # Truncate very long code blocks
            if len(code_content) > 1900:
                code_content = code_content[:1900] + "\n// ... (truncated)"
            blocks.append({
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [{"type": "text", "text": {"content": code_content}}],
                    "language": notion_lang
                }
            })
        # Bullet lists
        elif line.startswith('- '):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": truncate_text(line[2:])}}]
                }
            })
        # Numbered lists
        elif re.match(r'^\d+\.\s', line):
            text = re.sub(r'^\d+\.\s', '', line)
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": truncate_text(text)}}]
                }
            })
        # Quotes
        elif line.startswith('> '):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": truncate_text(line[2:])}}]
                }
            })
        # Dividers
        elif line.strip() == '---':
            blocks.append({
                "object": "block",
                "type": "divider",
                "divider": {}
            })
        # Regular paragraphs
        elif line.strip():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": truncate_text(line)}}]
                }
            })

        i += 1

    return blocks


def create_notion_page(title: str, parent_id: str, blocks: list) -> Dict:
    """Create a new page in Notion under the given parent."""
    url = 'https://api.notion.com/v1/pages'

    # Notion limits to 100 blocks per request
    initial_blocks = blocks[:100]

    payload = {
        "parent": {"page_id": parent_id},
        "properties": {
            "title": {
                "title": [{"text": {"content": title}}]
            }
        },
        "children": initial_blocks
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        page_id = result['id']

        # Add remaining blocks if any
        if len(blocks) > 100:
            append_blocks(page_id, blocks[100:])

        return result
    else:
        return {"error": response.text, "status": response.status_code}


def append_blocks(page_id: str, blocks: list):
    """Append blocks to an existing page (handles >100 blocks)."""
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'

    # Process in batches of 100
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        response = requests.patch(url, headers=HEADERS, json={"children": batch})
        if response.status_code != 200:
            print(f"    Warning: Failed to append blocks batch: {response.text[:100]}")


def get_category_for_type(doc_type: str) -> Optional[str]:
    """Map document type to category ID."""
    doc_type_lower = doc_type.lower() if doc_type else ""
    return CATEGORY_IDS.get(doc_type_lower)


def process_file(filepath: Path, apply: bool = False) -> Dict:
    """Process a single file."""
    result = {
        'file': filepath.name,
        'status': 'pending'
    }

    # Parse frontmatter
    meta = parse_frontmatter(filepath)
    if not meta:
        result['status'] = 'no_frontmatter'
        return result

    title = meta.get('title', filepath.stem)
    doc_type = meta.get('type', '')

    result['title'] = title
    result['type'] = doc_type

    # Get category
    category_id = get_category_for_type(doc_type)
    if not category_id:
        result['status'] = 'unknown_type'
        return result

    result['category_id'] = category_id

    if apply:
        # Get content and convert to blocks
        content = get_content_without_frontmatter(filepath)
        blocks = markdown_to_notion_blocks(content)

        # Create page
        response = create_notion_page(title, category_id, blocks)

        if 'error' in response:
            result['status'] = 'error'
            result['error'] = response['error'][:200]
        else:
            result['status'] = 'uploaded'
            result['notion_id'] = response.get('id')
            result['url'] = response.get('url')
    else:
        result['status'] = 'would_upload'

    return result


def main():
    import sys
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print(__doc__)
        return

    if not NOTION_KEY:
        print("ERROR: NOTION_API_KEY not set")
        return

    apply = '--apply' in args

    print("=" * 60)
    print("GROVE CORPUS UPLOAD TO NOTION")
    print("=" * 60)
    print(f"Mode: {'APPLY' if apply else 'CHECK (preview)'}")
    print(f"Directory: {REFINED_DIR}")
    print("=" * 60)

    files = sorted(REFINED_DIR.glob('*--FINAL.md'))
    print(f"\nFound {len(files)} refined documents\n")

    stats = {'uploaded': 0, 'would_upload': 0, 'error': 0, 'skipped': 0}

    for filepath in files:
        result = process_file(filepath, apply=apply)

        status = result['status']
        title = result.get('title', filepath.name)[:50]
        doc_type = result.get('type', 'unknown')

        if status == 'uploaded':
            stats['uploaded'] += 1
            print(f"[OK] {title}")
            print(f"     Type: {doc_type} -> Notion ID: {result.get('notion_id', 'N/A')}")
        elif status == 'would_upload':
            stats['would_upload'] += 1
            print(f"[ ] {title}")
            print(f"     Type: {doc_type} -> Would upload to category")
        elif status == 'error':
            stats['error'] += 1
            print(f"[X] {title}")
            print(f"     Error: {result.get('error', 'Unknown')[:80]}")
        else:
            stats['skipped'] += 1
            print(f"[SKIP] {filepath.name} ({status})")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if apply:
        print(f"  Uploaded: {stats['uploaded']}")
        print(f"  Errors: {stats['error']}")
    else:
        print(f"  Would upload: {stats['would_upload']}")
        print(f"  Skipped: {stats['skipped']}")
        print("\nRun with --apply to upload documents.")


if __name__ == '__main__':
    main()
