#!/usr/bin/env python3
"""
Grove Corpus Sync - Daily sync between Notion Documentation and local corpus.

Monitors The Grove > Documentation section in Notion for changes.
Updates the local refined corpus with any edits.
Maintains metadata and provenance tracking.

Usage:
    python notion_corpus_sync.py              # Full sync
    python notion_corpus_sync.py --check      # Preview only
    python notion_corpus_sync.py --category vision  # Sync specific category

Schedule via Task Scheduler or cron for daily execution.
"""

import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
NOTION_KEY = os.environ.get('NOTION_API_KEY')
REFINED_DIR = Path(__file__).parent / "refined"
SYNC_STATE_FILE = Path(__file__).parent / ".notion_sync_state.json"

# Notion page IDs
DOCUMENTATION_PAGE_ID = "2ed780a78eef81059f0ec7177f68f464"
CATEGORY_IDS = {
    "vision": "2ed780a78eef81dfb5acd6f4a24d66d3",
    "software": "2ed780a78eef81cf9ccffb7820e047a3",
    "blog": "2ed780a78eef817da309ebb7228ee053"
}

# Type mapping for filenames
TYPE_MAP = {
    "vision": "v",
    "software": "s",
    "blog": "b"
}

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}


def load_sync_state() -> Dict:
    """Load sync state from file."""
    if SYNC_STATE_FILE.exists():
        try:
            with open(SYNC_STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        'last_sync': None,
        'documents': {}  # page_id -> {last_edited, content_hash, local_file}
    }


def save_sync_state(state: Dict):
    """Save sync state to file."""
    with open(SYNC_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, default=str)


def get_child_pages(parent_id: str) -> List[Dict]:
    """Get all child pages of a parent page."""
    url = f'https://api.notion.com/v1/blocks/{parent_id}/children'
    pages = []

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        results = response.json().get('results', [])
        for block in results:
            if block.get('type') == 'child_page':
                page_id = block.get('id')
                title = block.get('child_page', {}).get('title', 'Untitled')
                pages.append({
                    'id': page_id,
                    'title': title
                })
    return pages


def get_page_content(page_id: str) -> Dict:
    """Get full page content and metadata."""
    # Get page properties
    page_url = f'https://api.notion.com/v1/pages/{page_id}'
    page_resp = requests.get(page_url, headers=HEADERS)

    if page_resp.status_code != 200:
        return None

    page_data = page_resp.json()
    last_edited = page_data.get('last_edited_time')

    # Get page blocks (content)
    blocks_url = f'https://api.notion.com/v1/blocks/{page_id}/children?page_size=100'
    blocks_resp = requests.get(blocks_url, headers=HEADERS)

    if blocks_resp.status_code != 200:
        return None

    blocks = blocks_resp.json().get('results', [])
    content = blocks_to_markdown(blocks)

    # Extract title
    title = "Untitled"
    props = page_data.get('properties', {})
    for prop_name, prop_val in props.items():
        if prop_val.get('type') == 'title':
            title_arr = prop_val.get('title', [])
            if title_arr:
                title = ''.join([t.get('plain_text', '') for t in title_arr])
            break

    return {
        'id': page_id,
        'title': title,
        'last_edited': last_edited,
        'content': content,
        'url': f"https://www.notion.so/{page_id.replace('-', '')}"
    }


def blocks_to_markdown(blocks: List[Dict]) -> str:
    """Convert Notion blocks to markdown."""
    lines = []

    for block in blocks:
        block_type = block.get('type')

        if block_type == 'paragraph':
            text = extract_rich_text(block.get('paragraph', {}).get('rich_text', []))
            lines.append(text)
            lines.append('')

        elif block_type == 'heading_1':
            text = extract_rich_text(block.get('heading_1', {}).get('rich_text', []))
            lines.append(f'# {text}')
            lines.append('')

        elif block_type == 'heading_2':
            text = extract_rich_text(block.get('heading_2', {}).get('rich_text', []))
            lines.append(f'## {text}')
            lines.append('')

        elif block_type == 'heading_3':
            text = extract_rich_text(block.get('heading_3', {}).get('rich_text', []))
            lines.append(f'### {text}')
            lines.append('')

        elif block_type == 'bulleted_list_item':
            text = extract_rich_text(block.get('bulleted_list_item', {}).get('rich_text', []))
            lines.append(f'- {text}')

        elif block_type == 'numbered_list_item':
            text = extract_rich_text(block.get('numbered_list_item', {}).get('rich_text', []))
            lines.append(f'1. {text}')

        elif block_type == 'code':
            code = extract_rich_text(block.get('code', {}).get('rich_text', []))
            lang = block.get('code', {}).get('language', '')
            lines.append(f'```{lang}')
            lines.append(code)
            lines.append('```')
            lines.append('')

        elif block_type == 'quote':
            text = extract_rich_text(block.get('quote', {}).get('rich_text', []))
            lines.append(f'> {text}')
            lines.append('')

        elif block_type == 'divider':
            lines.append('---')
            lines.append('')

        elif block_type == 'callout':
            text = extract_rich_text(block.get('callout', {}).get('rich_text', []))
            icon = block.get('callout', {}).get('icon', {}).get('emoji', '')
            lines.append(f'> {icon} {text}')
            lines.append('')

    return '\n'.join(lines)


def extract_rich_text(rich_text: List[Dict]) -> str:
    """Extract plain text from rich text array."""
    parts = []
    for item in rich_text:
        text = item.get('plain_text', '')
        annotations = item.get('annotations', {})

        if annotations.get('bold'):
            text = f'**{text}**'
        if annotations.get('italic'):
            text = f'*{text}*'
        if annotations.get('code'):
            text = f'`{text}`'

        parts.append(text)

    return ''.join(parts)


def generate_filename(title: str, category: str, date: str) -> str:
    """Generate standardized filename."""
    # Parse date
    try:
        dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
        date_code = dt.strftime('%y%m%d')
    except:
        date_code = datetime.now().strftime('%y%m%d')

    # Create slug
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:50]

    type_code = TYPE_MAP.get(category, 's')

    return f"{date_code}-{type_code}-{category}-{slug}.md--FINAL.md"


def generate_frontmatter(page: Dict, category: str) -> str:
    """Generate YAML frontmatter for document."""
    lines = ['---']
    lines.append(f'title: "{page["title"]}"')
    lines.append('author: "Jim Calhoun"')

    # Parse year from last_edited
    try:
        dt = datetime.fromisoformat(page['last_edited'].replace('Z', '+00:00'))
        year = dt.year
        date_str = dt.strftime('%Y-%m-%d')
    except:
        year = datetime.now().year
        date_str = datetime.now().strftime('%Y-%m-%d')

    lines.append(f'copyright: "{year} The Grove Foundation"')
    lines.append(f'date: "{date_str}"')
    lines.append(f'type: "{category}"')
    lines.append('status: "final"')
    lines.append(f'notion_url: "{page["url"]}"')
    lines.append(f'notion_id: "{page["id"]}"')
    lines.append(f'last_synced: "{datetime.now().isoformat()}"')
    lines.append('---')
    lines.append('')

    return '\n'.join(lines)


def content_hash(content: str) -> str:
    """Generate hash of content for change detection."""
    return hashlib.md5(content.encode()).hexdigest()


def sync_category(category: str, state: Dict, apply: bool = True) -> Dict:
    """Sync all documents in a category."""
    category_id = CATEGORY_IDS.get(category)
    if not category_id:
        return {'error': f'Unknown category: {category}'}

    results = {
        'category': category,
        'checked': 0,
        'updated': 0,
        'new': 0,
        'unchanged': 0,
        'documents': []
    }

    # Get child pages
    pages = get_child_pages(category_id)
    print(f"\n  Found {len(pages)} documents in {category}")

    for page_info in pages:
        page_id = page_info['id']
        results['checked'] += 1

        # Get full content
        page = get_page_content(page_id)
        if not page:
            continue

        current_hash = content_hash(page['content'])
        stored = state['documents'].get(page_id, {})

        doc_result = {
            'title': page['title'],
            'id': page_id,
            'status': 'unchanged'
        }

        if not stored:
            # New document
            doc_result['status'] = 'new'
            results['new'] += 1
        elif stored.get('content_hash') != current_hash:
            # Changed
            doc_result['status'] = 'updated'
            results['updated'] += 1
        else:
            # Unchanged
            results['unchanged'] += 1

        if apply and doc_result['status'] in ['new', 'updated']:
            # Generate file
            filename = stored.get('local_file') or generate_filename(
                page['title'], category, page['last_edited']
            )
            filepath = REFINED_DIR / filename

            # Write file with frontmatter
            frontmatter = generate_frontmatter(page, category)
            full_content = frontmatter + page['content']

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)

            doc_result['file'] = filename

            # Update state
            state['documents'][page_id] = {
                'last_edited': page['last_edited'],
                'content_hash': current_hash,
                'local_file': filename,
                'title': page['title']
            }

        results['documents'].append(doc_result)
        print(f"    [{doc_result['status'].upper():9}] {page['title'][:50]}")

    return results


def run_sync(categories: List[str] = None, apply: bool = True):
    """Run full sync."""
    if not NOTION_KEY:
        print("ERROR: NOTION_API_KEY not set")
        return

    print("=" * 60)
    print("GROVE CORPUS SYNC")
    print("=" * 60)
    print(f"Mode: {'APPLY' if apply else 'CHECK (preview)'}")
    print(f"Corpus: {REFINED_DIR}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    state = load_sync_state()
    last_sync = state.get('last_sync', 'never')
    print(f"Last sync: {last_sync}")

    categories = categories or list(CATEGORY_IDS.keys())

    total_stats = {'checked': 0, 'updated': 0, 'new': 0, 'unchanged': 0}

    for category in categories:
        result = sync_category(category, state, apply)
        for key in ['checked', 'updated', 'new', 'unchanged']:
            total_stats[key] += result.get(key, 0)

    if apply:
        state['last_sync'] = datetime.now().isoformat()
        save_sync_state(state)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Checked:   {total_stats['checked']}")
    print(f"  New:       {total_stats['new']}")
    print(f"  Updated:   {total_stats['updated']}")
    print(f"  Unchanged: {total_stats['unchanged']}")

    if not apply:
        print("\nRun without --check to apply changes.")


def main():
    import sys
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print(__doc__)
        return

    apply = '--check' not in args

    categories = None
    if '--category' in args:
        idx = args.index('--category')
        if idx + 1 < len(args):
            categories = [args[idx + 1]]

    run_sync(categories=categories, apply=apply)


if __name__ == '__main__':
    main()
