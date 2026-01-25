#!/usr/bin/env python3
"""
Atlas Inbox Scanner - Comprehensive view of inbox items with comments.
Run this to see everything awaiting triage or with @atlas mentions.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

NOTION_KEY = os.environ.get('NOTION_API_KEY')
INBOX_DB_ID = os.environ.get('NOTION_ATLAS_INBOX_ID', 'c298b60934d248beb2c50942436b8bfe')

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def query_inbox():
    """Query all pages in the Atlas Inbox."""
    url = f'https://api.notion.com/v1/databases/{INBOX_DB_ID}/query'
    all_results = []
    start_cursor = None

    while True:
        payload = {}
        if start_cursor:
            payload['start_cursor'] = start_cursor

        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get('results', []))

            if data.get('has_more'):
                start_cursor = data.get('next_cursor')
            else:
                break
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

    return all_results

def get_comments(page_id):
    """Get comments for a page."""
    url = f'https://api.notion.com/v1/comments?block_id={page_id}'
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json().get('results', [])
    return []

def extract_property(prop):
    """Extract value from Notion property."""
    if not prop:
        return ''

    prop_type = prop.get('type', '')

    if prop_type == 'title':
        return ''.join([t.get('plain_text', '') for t in prop.get('title', [])])
    elif prop_type == 'rich_text':
        return ''.join([t.get('plain_text', '') for t in prop.get('rich_text', [])])
    elif prop_type == 'select':
        select = prop.get('select')
        return select.get('name', '') if select else ''
    elif prop_type == 'multi_select':
        return ', '.join([s.get('name', '') for s in prop.get('multi_select', [])])
    elif prop_type == 'url':
        return prop.get('url', '') or ''

    return str(prop)

def extract_comment_text(comment):
    """Extract plain text from comment."""
    rich_text = comment.get('rich_text', [])
    return ''.join([t.get('plain_text', '') for t in rich_text])

def main():
    print("=" * 80)
    print("ATLAS INBOX SCAN")
    print("=" * 80)

    pages = query_inbox()

    # Separate by status
    pending = []
    triaged = []
    complete = []

    for page in pages:
        props = page.get('properties', {})
        status = extract_property(props.get('Status', {}))

        if status == 'Complete':
            complete.append(page)
        elif status == 'Triaged':
            triaged.append(page)
        else:
            pending.append(page)

    print(f"\nTotal: {len(pages)} items")
    print(f"  - Pending: {len(pending)}")
    print(f"  - Triaged: {len(triaged)}")
    print(f"  - Complete: {len(complete)}")

    def print_item(page, idx):
        props = page.get('properties', {})
        page_id = page['id']

        title = extract_property(props.get('Title', {}))
        status = extract_property(props.get('Status', {}))
        pillar = extract_property(props.get('Pillar', {}))
        priority = extract_property(props.get('Priority', {}))
        disposition = extract_property(props.get('Disposition', {}))
        source = extract_property(props.get('Source', {}))
        notes = extract_property(props.get('Atlas Notes', {}))
        tags = extract_property(props.get('Tags', {}))

        print(f"\n  [{idx}] {title[:65]}{'...' if len(title) > 65 else ''}")
        print(f"      ID: {page_id}")
        print(f"      Status: {status or 'NONE'} | Pillar: {pillar or 'NONE'} | Priority: {priority or 'NONE'}")
        print(f"      Disposition: {disposition or 'NONE'} | Tags: {tags or 'NONE'}")

        if source:
            print(f"      Source: {source[:60]}{'...' if len(source) > 60 else ''}")
        if notes:
            print(f"      Notes: {notes[:60]}{'...' if len(notes) > 60 else ''}")

        # Get comments
        comments = get_comments(page_id)
        if comments:
            print(f"      ** COMMENTS ({len(comments)}):")
            for c in comments:
                text = extract_comment_text(c)
                # Check for @atlas mentions
                has_atlas = '@atlas' in text.lower()
                prefix = "  >> @ATLAS: " if has_atlas else "     "
                print(f"        {prefix}{text[:70]}{'...' if len(text) > 70 else ''}")

    if pending:
        print("\n" + "=" * 80)
        print("PENDING (needs triage)")
        print("=" * 80)
        for i, page in enumerate(pending, 1):
            print_item(page, i)

    if triaged:
        print("\n" + "=" * 80)
        print("TRIAGED (awaiting action)")
        print("=" * 80)
        for i, page in enumerate(triaged, 1):
            print_item(page, i)

    if complete:
        print("\n" + "=" * 80)
        print("COMPLETE (for reference)")
        print("=" * 80)
        for i, page in enumerate(complete, 1):
            print_item(page, i)

    print("\n" + "=" * 80)
    print("END OF INBOX SCAN")
    print("=" * 80)

if __name__ == "__main__":
    main()
