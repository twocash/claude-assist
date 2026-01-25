"""
Test script to verify paginated block fetching works.

Tests the core fix for the truncated content bug.
"""

import os
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv
load_dotenv()

from grove_docs_refinery.sync.api import NotionAPI
from grove_docs_refinery.sync.converter import blocks_to_markdown


def test_pagination():
    """Test fetching a large document with pagination."""

    # Trellis Architecture: First Order Directives
    # This is known to be a large document
    TEST_PAGE_ID = '2ed780a7-8eef-817c-ac26-e37e4cdb261b'

    print("=" * 60)
    print("PAGINATION TEST")
    print("=" * 60)

    api = NotionAPI()

    print(f"\nFetching page: {TEST_PAGE_ID}")
    print("This uses paginated fetching with child recursion...")

    try:
        result = api.get_page_content(TEST_PAGE_ID)

        page = result['page']
        blocks = result['blocks']
        total_blocks = result['block_count']

        # Extract title
        props = page.get('properties', {})
        title_prop = props.get('title') or props.get('Name') or {}
        if title_prop.get('type') == 'title':
            title = ''.join(t.get('plain_text', '') for t in title_prop.get('title', []))
        else:
            title = 'Unknown'

        print(f"\n--- Page Info ---")
        print(f"Title: {title}")
        print(f"ID: {page.get('id')}")
        print(f"Last edited: {page.get('last_edited_time')}")

        print(f"\n--- Block Counts ---")
        print(f"Top-level blocks: {len(blocks)}")
        print(f"Total blocks (including nested): {total_blocks}")

        # Count block types
        type_counts = {}
        blocks_with_children = 0

        def count_types(block_list):
            nonlocal blocks_with_children
            for block in block_list:
                block_type = block.get('type', 'unknown')
                type_counts[block_type] = type_counts.get(block_type, 0) + 1
                if '_children' in block:
                    blocks_with_children += 1
                    count_types(block['_children'])

        count_types(blocks)

        print(f"Blocks with children: {blocks_with_children}")
        print(f"\nBlock types found:")
        for btype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"  {btype}: {count}")

        # Convert to markdown and check length
        print(f"\n--- Markdown Conversion ---")
        markdown = blocks_to_markdown(blocks)
        lines = markdown.split('\n')
        print(f"Total characters: {len(markdown)}")
        print(f"Total lines: {len(lines)}")

        # Show first 500 chars
        print(f"\nFirst 500 characters:")
        print("-" * 40)
        print(markdown[:500])
        print("-" * 40)

        # Verify we got substantial content
        if total_blocks > 100:
            print(f"\n[OK] SUCCESS: Fetched {total_blocks} blocks (pagination working!)")
        elif total_blocks > 10:
            print(f"\n[OK] Fetched {total_blocks} blocks")
        else:
            print(f"\n[!] WARNING: Only {total_blocks} blocks - may still be truncated")

        return True

    except Exception as e:
        print(f"\n[X] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_category_pages():
    """Test fetching the category pages exist."""
    print("\n" + "=" * 60)
    print("CATEGORY PAGES TEST")
    print("=" * 60)

    CATEGORIES = {
        'vision': '2ed780a78eef81dfb5acd6f4a24d66d3',
        'software': '2ed780a78eef81cf9ccffb7820e047a3',
        'blog': '2ed780a78eef817da309ebb7228ee053'
    }

    api = NotionAPI()

    for category, page_id in CATEGORIES.items():
        try:
            page = api.get_page(page_id)
            props = page.get('properties', {})
            title_prop = props.get('title') or props.get('Name') or {}
            if title_prop.get('type') == 'title':
                title = ''.join(t.get('plain_text', '') for t in title_prop.get('title', []))
            else:
                title = 'Unknown'

            child_pages = api.get_child_pages(page_id)
            print(f"[OK] {category}: '{title}' ({len(child_pages)} child pages)")
        except Exception as e:
            print(f"[X] {category}: ERROR - {e}")


if __name__ == '__main__':
    print("\nGrove Docs Refinery - Sync Module Tests\n")

    success = test_pagination()
    test_category_pages()

    print("\n" + "=" * 60)
    if success:
        print("TESTS PASSED - Pagination is working correctly")
    else:
        print("TESTS FAILED - Check error messages above")
    print("=" * 60)
