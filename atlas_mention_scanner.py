#!/usr/bin/env python3
"""
Atlas Mention Scanner - Periodic @Atlas mention detection.
Designed to run every 15 minutes via scheduler or continuous loop.

Usage:
    python atlas_mention_scanner.py           # Single scan
    python atlas_mention_scanner.py --loop    # Continuous (every 15 min)
    python atlas_mention_scanner.py --daemon  # Background daemon mode
"""
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
NOTION_KEY = os.environ.get('NOTION_API_KEY')
WORK_QUEUE_ID = os.environ.get('NOTION_ATLAS_WORK_QUEUE_ID', '9c8f104b347f4dfc829f7609c8f17f0d')
INBOX_DB_ID = os.environ.get('NOTION_ATLAS_INBOX_ID', 'c298b60934d248beb2c50942436b8bfe')

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# State file to track processed mentions
STATE_FILE = Path(__file__).parent / '.atlas_scanner_state.json'
SCAN_INTERVAL = 15 * 60  # 15 minutes in seconds


def load_state() -> Dict:
    """Load scanner state from file."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        'last_scan': None,
        'processed_comments': [],  # List of comment IDs already handled
        'processed_pages': {}      # page_id -> last_edited_time we saw
    }


def save_state(state: Dict):
    """Save scanner state to file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2, default=str)


def search_recent_pages(hours_back: int = 1, limit: int = 20) -> List[Dict]:
    """Search for recently modified pages."""
    url = 'https://api.notion.com/v1/search'

    # Get pages modified recently
    payload = {
        "filter": {"property": "object", "value": "page"},
        "sort": {"direction": "descending", "timestamp": "last_edited_time"},
        "page_size": limit
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json().get('results', [])
    print(f"  Search error: {response.status_code}")
    return []


def get_page_comments(page_id: str) -> List[Dict]:
    """Get comments for a page."""
    url = f'https://api.notion.com/v1/comments?block_id={page_id}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []


def extract_comment_text(comment: Dict) -> str:
    """Extract plain text from comment."""
    rich_text = comment.get('rich_text', [])
    return ''.join([t.get('plain_text', '') for t in rich_text])


def get_page_title(page: Dict) -> str:
    """Extract title from page."""
    props = page.get('properties', {})

    for prop_name in ['title', 'Title', 'Name']:
        prop = props.get(prop_name, {})
        if prop.get('title'):
            return ''.join([t.get('plain_text', '') for t in prop['title']])

    return 'Untitled'


def has_atlas_mention(text: str) -> bool:
    """Check if text contains @atlas mention."""
    return '@atlas' in text.lower()


def post_to_work_queue(title: str, mention_type: str, source_url: str, notes: str) -> bool:
    """Post a new mention to the Work Queue."""
    url = 'https://api.notion.com/v1/pages'

    payload = {
        "parent": {"database_id": WORK_QUEUE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": title[:100]}}]},
            "Type": {"select": {"name": mention_type}},
            "Status": {"select": {"name": "First Draft"}},
            "Source": {"url": source_url},
            "Notes": {"rich_text": [{"text": {"content": notes[:2000]}}]}
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    return response.status_code in [200, 201]


def scan_for_mentions(state: Dict) -> List[Dict]:
    """Scan for new @atlas mentions."""
    new_mentions = []
    processed_comments = set(state.get('processed_comments', []))

    # Get recent pages
    pages = search_recent_pages(hours_back=1)
    print(f"  Checking {len(pages)} recent pages...")

    for i, page in enumerate(pages):
        page_id = page['id']
        page_title = get_page_title(page)
        page_url = f"https://www.notion.so/{page_id.replace('-', '')}"

        # Check comments on this page
        comments = get_page_comments(page_id)

        for comment in comments:
            comment_id = comment.get('id')

            # Skip if already processed
            if comment_id in processed_comments:
                continue

            comment_text = extract_comment_text(comment)

            if has_atlas_mention(comment_text):
                new_mentions.append({
                    'comment_id': comment_id,
                    'page_id': page_id,
                    'page_title': page_title,
                    'page_url': page_url,
                    'comment_text': comment_text,
                    'created_time': comment.get('created_time')
                })

                # Mark as processed
                processed_comments.add(comment_id)

        time.sleep(0.1)  # Rate limiting

    # Update state
    state['processed_comments'] = list(processed_comments)[-500:]  # Keep last 500
    state['last_scan'] = datetime.now().isoformat()

    return new_mentions


def run_scan():
    """Run a single scan."""
    print(f"\n{'='*60}")
    print(f"ATLAS MENTION SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print('='*60)

    state = load_state()
    last_scan = state.get('last_scan', 'never')
    print(f"Last scan: {last_scan}")

    print("\nScanning for @Atlas mentions...")
    mentions = scan_for_mentions(state)

    if mentions:
        print(f"\n** Found {len(mentions)} new mention(s)! **\n")

        for m in mentions:
            print(f"  Page: {m['page_title'][:50]}")
            print(f"  Comment: {m['comment_text'][:80]}...")
            print(f"  URL: {m['page_url']}")
            print()

            # Post to Work Queue
            success = post_to_work_queue(
                title=f"@Atlas Mention: {m['page_title'][:60]}",
                mention_type="Other",
                source_url=m['page_url'],
                notes=f"Comment: {m['comment_text']}"
            )

            if success:
                print(f"  -> Posted to Work Queue")
            else:
                print(f"  -> Failed to post to Work Queue")
    else:
        print("No new mentions found.")

    save_state(state)
    print(f"\nScan complete. State saved.")

    return mentions


def run_loop():
    """Run continuous scanning loop."""
    print("Starting Atlas Mention Scanner in loop mode...")
    print(f"Scanning every {SCAN_INTERVAL // 60} minutes")
    print("Press Ctrl+C to stop\n")

    while True:
        try:
            run_scan()
            print(f"\nNext scan in {SCAN_INTERVAL // 60} minutes...")
            time.sleep(SCAN_INTERVAL)
        except KeyboardInterrupt:
            print("\n\nScanner stopped.")
            break
        except Exception as e:
            print(f"Error during scan: {e}")
            time.sleep(60)  # Wait a minute before retrying


def main():
    if not NOTION_KEY:
        print("ERROR: NOTION_API_KEY not set in environment")
        sys.exit(1)

    if '--loop' in sys.argv or '--daemon' in sys.argv:
        run_loop()
    else:
        run_scan()


if __name__ == "__main__":
    main()
