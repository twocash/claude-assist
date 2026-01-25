#!/usr/bin/env python3
"""
Update Notion database with standardized titles and tags.
Pattern: {CAT} | {CLASS} | {FEATURE} | {BENEFIT}
Tags embedded in structured format.
"""
import json
import os
from notion_client import Client

# Load standardized entries
with open('standardized_repos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
entries = data['entries']

# Initialize Notion client
NOTION_KEY = os.environ.get('NOTION_API_KEY', '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')
notion = Client(auth=NOTION_KEY)
DB_ID = 'efbdb5df36ed475eaf7ab28b25711c0c'

def get_all_pages():
    """Get all pages in the database."""
    pages = []
    cursor = None

    while True:
        try:
            if cursor:
                response = notion.databases.query(
                    database_id=DB_ID,
                    start_cursor=cursor
                )
            else:
                response = notion.databases.query(database_id=DB_ID)
        except Exception as e:
            print(f"Query error: {e}")
            break

        pages.extend(response.get('results', []))

        if response.get('has_more'):
            cursor = response.get('next_cursor')
        else:
            break

    return pages

def update_page(page_id: str, entry: dict):
    """Update a page with standardized title and structured tags."""
    # Create structured thought with all metadata
    structured_thought = (
        f"[{entry['category'].upper()}] "
        f"Class: {entry['class']} | "
        f"Feature: {entry['feature']} | "
        f"Benefit: {entry['benefit']} | "
        f"Tags: {entry['platform']}/{entry['cost']}/{entry['type']}/{entry['maturity']}"
    )

    # Extract owner/repo from URL for display
    original = entry['original_name']
    short_name = original.split('/')[-1] if '/' in original else original

    try:
        # Update title to include original repo name for reference
        new_title = f"{entry['title']} ({short_name})"

        notion.pages.update(
            page_id=page_id,
            properties={
                'Name': {'title': [{'text': {'content': new_title}}]},
                'Thought': {'rich_text': [{'text': {'content': structured_thought}}]},
                'Description': {'rich_text': [{'text': {'content': entry['description'][:1900]}}]},
            }
        )
        return True
    except Exception as e:
        print(f"  Error: {str(e)[:80]}")
        return False

def main():
    print("UPDATING NOTION DATABASE")
    print("=" * 60)
    print(f"Pattern: {{CAT}} | {{CLASS}} | {{FEATURE}} | {{BENEFIT}}")
    print(f"Tags: platform/cost/type/maturity")
    print("=" * 60)

    # Get all pages
    print("\nFetching pages from Notion...")
    pages = get_all_pages()
    print(f"Found {len(pages)} pages in database")

    # Create URL to page mapping
    url_to_page = {}
    for page in pages:
        props = page.get('properties', {})
        url_prop = props.get('URL', {}) or props.get('userDefined:URL', {})
        url = url_prop.get('url', '') if isinstance(url_prop, dict) else str(url_prop)
        if url:
            url_to_page[url] = page

    # Match and update
    updated = 0
    errors = 0
    unmatched = []

    print("\nUpdating entries...")
    for i, entry in enumerate(entries, 1):
        url = entry['url']
        if url in url_to_page:
            page_id = url_to_page[url]['id']
            short_title = entry['title'][:45] + '...' if len(entry['title']) > 45 else entry['title']
            print(f"{i:2d}. {short_title}")
            if update_page(page_id, entry):
                updated += 1
            else:
                errors += 1
        else:
            unmatched.append(entry['original_name'])
            print(f"{i:2d}. [NOT FOUND] {entry['original_name']}")
            errors += 1

    print("\n" + "=" * 60)
    print(f"RESULTS:")
    print(f"  Updated: {updated}")
    print(f"  Errors/Unmatched: {errors}")
    print(f"  Total: {len(entries)}")

    if unmatched:
        print(f"\nNOT FOUND IN NOTION ({len(unmatched)}):")
        for u in unmatched[:5]:
            print(f"  - {u}")

if __name__ == "__main__":
    main()
