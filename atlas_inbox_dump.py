#!/usr/bin/env python3
"""
Dump Atlas Inbox items with comments for triage.
"""
import os
import requests

from dotenv import load_dotenv
load_dotenv()

NOTION_KEY = os.environ.get('NOTION_API_KEY')
INBOX_DB_ID = 'c298b60934d248beb2c50942436b8bfe'

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
    print("=" * 70)
    print("ATLAS INBOX DUMP")
    print("=" * 70)

    pages = query_inbox()
    print(f"\nFound {len(pages)} items in inbox\n")

    for i, page in enumerate(pages, 1):
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

        print("-" * 70)
        print(f"#{i}: {title[:60]}{'...' if len(title) > 60 else ''}")
        print(f"    Status: {status or '-'} | Pillar: {pillar or '-'} | Priority: {priority or '-'}")
        print(f"    Disposition: {disposition or '-'} | Tags: {tags or '-'}")
        if source:
            print(f"    Source: {source[:70]}{'...' if len(source) > 70 else ''}")
        if notes:
            print(f"    Notes: {notes[:70]}{'...' if len(notes) > 70 else ''}")

        # Get comments
        comments = get_comments(page_id)
        if comments:
            print(f"    >> COMMENTS ({len(comments)}):")
            for c in comments:
                text = extract_comment_text(c)
                print(f"       -> {text[:100]}{'...' if len(text) > 100 else ''}")

        print()

    print("=" * 70)
    print("END OF INBOX")
    print("=" * 70)

if __name__ == "__main__":
    main()
