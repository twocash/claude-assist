#!/usr/bin/env python3
"""
Enrich Grove Scattered Content Inventory with source URLs, dates, and summaries.
Searches Notion for matching pages and updates inventory entries.
"""
import json
import os
import re
import time
from datetime import datetime

import requests

NOTION_KEY = os.environ.get('NOTION_API_KEY', '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')
INVENTORY_DB_ID = '973d0191d4554f4f8aa218555ed01f67'  # Database ID (not data source)

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# Category keywords for auto-classification
CATEGORY_KEYWORDS = {
    'ARCH': ['architecture', 'technical', 'system design', 'infrastructure'],
    'METHOD': ['methodology', 'process', 'workflow', 'foundation loop', 'sprout'],
    'THESIS': ['thesis', 'vision', 'world-changing', 'philosophy', 'obsolescence'],
    'ECON': ['economics', 'credit', 'pricing', 'market', 'revenue'],
    'RATCHET': ['ratchet', 'capability', 'propagation'],
    'SPEC': ['specification', 'spec', 'roadmap', 'mvp', 'checklist'],
    'RESEARCH': ['research', 'analysis', 'validation', 'nvidia', 'arxiv'],
    'PATTERN': ['pattern', 'design pattern', 'observer', 'configurator'],
    'EXEC': ['execution', 'prompt', 'sprint', 'handoff'],
    'SIMULATION': ['simulation', 'event loop'],
    'CONSOLE': ['console', 'bedrock', 'state management'],
    'SPROUT': ['sprout', 'terminal', 'cultivation'],
    'AGENT': ['agent', 'gardener', 'pruning'],
    'STRAT': ['strategy', 'strategic', 'framing'],
}

def query_inventory():
    """Query all pages in the inventory database."""
    url = f'https://api.notion.com/v1/databases/{INVENTORY_DB_ID}/query'
    all_results = []
    start_cursor = None

    while True:
        payload = {}
        if start_cursor:
            payload['start_cursor'] = start_cursor

        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            all_results.extend(results)

            if data.get('has_more'):
                start_cursor = data.get('next_cursor')
                print(f"  Fetched {len(all_results)} entries, continuing...")
                time.sleep(0.5)
            else:
                break
        else:
            print(f"Error querying database: {response.status_code}")
            print(response.text)
            break

    return all_results

def search_notion(query: str):
    """Search Notion for pages matching the query."""
    url = 'https://api.notion.com/v1/search'
    payload = {
        'query': query,
        'filter': {'property': 'object', 'value': 'page'},
        'page_size': 10
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"  Search error: {response.status_code}")
        return []

def get_page_content(page_id: str):
    """Get page content blocks."""
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'

    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def extract_text_from_blocks(blocks, max_chars=500):
    """Extract text from page blocks for summary."""
    text_parts = []
    chars = 0

    for block in blocks:
        block_type = block.get('type', '')

        if block_type in ['paragraph', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item']:
            rich_text = block.get(block_type, {}).get('rich_text', [])
            for rt in rich_text:
                plain_text = rt.get('plain_text', '')
                text_parts.append(plain_text)
                chars += len(plain_text)
                if chars >= max_chars:
                    break

        if chars >= max_chars:
            break

    summary = ' '.join(text_parts)[:max_chars]
    if len(summary) == max_chars:
        summary = summary.rsplit(' ', 1)[0] + '...'

    return summary

def infer_category(title: str, summary: str) -> str:
    """Infer category from title and summary content."""
    text = (title + ' ' + summary).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return category

    return None  # No match

def get_page_title(page):
    """Extract title from a Notion page."""
    props = page.get('properties', {})

    for prop_name, prop_value in props.items():
        if prop_value.get('type') == 'title':
            title_array = prop_value.get('title', [])
            if title_array:
                return title_array[0].get('plain_text', '')

    return ''

def update_inventory_entry(page_id: str, updates: dict) -> bool:
    """Update an inventory entry with enrichment data."""
    url = f'https://api.notion.com/v1/pages/{page_id}'

    properties = {}

    if updates.get('source_url'):
        properties['Source URL'] = {'url': updates['source_url']}

    if updates.get('summary'):
        properties['Summary'] = {
            'rich_text': [{'text': {'content': updates['summary'][:2000]}}]
        }

    if updates.get('last_updated'):
        properties['Last Updated'] = {
            'date': {'start': updates['last_updated']}
        }

    if updates.get('category'):
        properties['Category'] = {'select': {'name': updates['category']}}

    if not properties:
        return False

    payload = {'properties': properties}

    response = requests.patch(url, headers=HEADERS, json=payload)

    return response.status_code in [200, 201]

def main():
    print("GROVE INVENTORY ENRICHMENT")
    print("=" * 60)

    # Query inventory
    print("\nFetching inventory entries...")
    entries = query_inventory()
    print(f"Found {len(entries)} entries")

    # Process entries
    enriched = 0
    skipped = 0
    errors = 0

    for i, entry in enumerate(entries, 1):
        page_id = entry['id']
        props = entry.get('properties', {})

        # Get title
        title_prop = props.get('Page Name', {})
        title_array = title_prop.get('title', [])
        title = title_array[0].get('plain_text', '') if title_array else ''

        # Check if already has Source URL
        source_url_prop = props.get('Source URL', {})
        existing_url = source_url_prop.get('url', '')

        # Check if already has Summary
        summary_prop = props.get('Summary', {})
        summary_text = summary_prop.get('rich_text', [])
        existing_summary = summary_text[0].get('plain_text', '') if summary_text else ''

        if existing_url and existing_summary:
            print(f"[{i}/{len(entries)}] {title[:40]}... - SKIP (already enriched)")
            skipped += 1
            continue

        print(f"[{i}/{len(entries)}] {title[:40]}...")

        # Search for matching page
        search_results = search_notion(title)
        time.sleep(0.3)  # Rate limit

        # Find best match (not the inventory entry itself)
        best_match = None
        for result in search_results:
            result_id = result.get('id', '').replace('-', '')
            if result_id != page_id.replace('-', ''):
                # Check if title matches
                result_title = get_page_title(result)
                if result_title.lower() == title.lower() or title.lower() in result_title.lower():
                    best_match = result
                    break

        if not best_match:
            # Try broader search with first few words
            words = title.split()[:3]
            if len(words) >= 2:
                search_results = search_notion(' '.join(words))
                time.sleep(0.3)

                for result in search_results:
                    result_id = result.get('id', '').replace('-', '')
                    if result_id != page_id.replace('-', ''):
                        best_match = result
                        break

        if best_match:
            source_url = best_match.get('url', '')
            last_edited = best_match.get('last_edited_time', '')[:10]  # Date only

            # Get content for summary
            blocks = get_page_content(best_match['id'])
            time.sleep(0.3)
            summary = extract_text_from_blocks(blocks, max_chars=400)

            # Infer category if not set
            category = None
            category_prop = props.get('Category', {})
            if not category_prop.get('select'):
                category = infer_category(title, summary)

            updates = {
                'source_url': source_url if not existing_url else None,
                'summary': summary if not existing_summary else None,
                'last_updated': last_edited,
                'category': category
            }

            if update_inventory_entry(page_id, updates):
                print(f"  -> Enriched: {source_url[:50]}...")
                enriched += 1
            else:
                print(f"  -> ERROR updating")
                errors += 1
        else:
            print(f"  -> No matching source found")
            errors += 1

        time.sleep(0.3)  # Rate limit between entries

        # Progress checkpoint
        if i % 20 == 0:
            print(f"\n--- Progress: {enriched} enriched, {skipped} skipped, {errors} errors ---\n")

    print("\n" + "=" * 60)
    print("ENRICHMENT COMPLETE")
    print(f"  Enriched: {enriched}")
    print(f"  Skipped:  {skipped}")
    print(f"  Errors:   {errors}")
    print(f"  Total:    {len(entries)}")

if __name__ == "__main__":
    main()
