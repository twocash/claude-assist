#!/usr/bin/env python3
"""
Batch update all Notion entries with standardized titles and tags.
Uses Notion API directly (not SDK) for more reliable access.
"""
import json
import os
import time

import requests

NOTION_KEY = os.environ.get('NOTION_API_KEY', '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')
DB_ID = 'efbdb5df36ed475eaf7ab28b25711c0c'

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def query_database():
    """Query all pages in the database."""
    url = f'https://api.notion.com/v1/databases/{DB_ID}/query'
    all_results = []

    while True:
        payload = {}
        if all_results and all_results[-1].get('next_cursor'):
            # Use the last start_cursor if we have results
            payload['start_cursor'] = all_results[-1].get('next_cursor')

        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            all_results.extend(results)

            # Check for next_cursor in the response, not in results
            if data.get('has_more'):
                print(f"  Fetched {len(all_results)} pages, continuing...")
                time.sleep(0.5)  # Rate limit
            else:
                break
        else:
            print(f"Error querying database: {response.status_code}")
            print(response.text)
            break

    return all_results

def update_page(page_id: str, entry: dict) -> bool:
    """Update a single page with standardized data."""
    url = f'https://api.notion.com/v1/pages/{page_id}'

    short_name = entry['original_name'].split('/')[-1] if '/' in entry['original_name'] else entry['original_name']
    new_title = f"{entry['title']} ({short_name})"

    # Truncate description if too long
    desc = entry.get('description', '')[:1900]

    payload = {
        'properties': {
            'Name': {
                'title': [{'text': {'content': new_title}}]
            },
            'Thought': {
                'rich_text': [{'text': {'content': entry.get('structured_thought', '')}}]
            },
            'Description': {
                'rich_text': [{'text': {'content': desc}}]
            }
        }
    }

    response = requests.patch(url, headers=HEADERS, json=payload)

    if response.status_code in [200, 201]:
        return True
    else:
        print(f"  Error updating {entry['original_name']}: {response.status_code}")
        return False

def main():
    print("BATCH UPDATING NOTION ENTRIES")
    print("=" * 60)

    # Load standardized entries
    with open('standardized_repos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    entries = data['entries']

    # Add structured thought to each entry
    for entry in entries:
        entry['structured_thought'] = (
            f"[{entry['category'].upper()}] "
            f"Class: {entry['class']} | "
            f"Feature: {entry['feature']} | "
            f"Benefit: {entry['benefit']} | "
            f"Tags: {entry['platform']}/{entry['cost']}/{entry['type']}/{entry['maturity']}"
        )

    print(f"Loaded {len(entries)} standardized entries")

    # Query database
    print("\nFetching pages from Notion...")
    pages = query_database()
    print(f"Found {len(pages)} pages in database")

    # Build URL to page_id mapping - property name is 'URL' not 'userDefined:URL'
    url_to_page = {}
    for page in pages:
        props = page.get('properties', {})
        url_prop = props.get('URL', {})
        if isinstance(url_prop, dict):
            url = url_prop.get('url', '')
        else:
            url = str(url_prop)
        if url:
            url_to_page[url] = page['id']

    print(f"Matched {len(url_to_page)} URLs")

    # Show sample URLs for debugging
    print("\nSample URLs in Notion:")
    for url in list(url_to_page.keys())[:5]:
        print(f"  {url}")

    print("\nSample URLs in standardized_repos.json:")
    for entry in entries[:5]:
        print(f"  {entry['url']}")

    # Update entries
    updated = 0
    errors = 0
    unmatched = []

    print("\nUpdating entries...")
    for i, entry in enumerate(entries, 1):
        url = entry['url']
        if url in url_to_page:
            page_id = url_to_page[url]
            short_title = entry['title'][:40] + '...' if len(entry['title']) > 40 else entry['title']
            print(f"{i:2d}. {short_title}")

            if update_page(page_id, entry):
                updated += 1
            else:
                errors += 1

            time.sleep(0.3)  # Rate limiting
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
        for u in unmatched[:10]:
            print(f"  - {u}")

if __name__ == "__main__":
    main()
