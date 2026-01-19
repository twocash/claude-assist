#!/usr/bin/env python3
"""
Atlas Startup Routine - Chief of Staff Task Capture System
Scans Notion for @Atlas mentions and creates tasks in the Atlas Tasks database.

Usage:
    python atlas_startup.py [--api-key KEY] [--task-db DB_ID]

Environment variables:
    NOTION_ATLAS_API_KEY      - Notion API key for Atlas integration
    NOTION_ATLAS_TASK_DATABASE_ID - Database ID for creating tasks
    NOTION_ATLAS_DATABASES    - Comma-separated database IDs to scan
"""
import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Optional, List, Dict, Any

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - support both naming conventions
NOTION_KEY = os.environ.get('NOTION_ATLAS_API_KEY', '') or os.environ.get('NOTION_API_KEY', '')
TASK_DB_ID = os.environ.get('NOTION_ATLAS_TASK_DATABASE_ID', '')
DB_IDS_ENV = os.environ.get('NOTION_ATLAS_DATABASES', '')
INBOX_DB_ID = os.environ.get('NOTION_ATLAS_INBOX_ID', 'c298b60934d248beb2c50942436b8bfe')

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# Priority keywords mapping
PRIORITY_KEYWORDS = {
    'P0': ['urgent', 'asap', 'p0', 'critical', 'blocker', 'emergency', 'immediately'],
    'P1': ['important', 'p1', 'high priority', 'soon', 'this week'],
    'P2': ['normal', 'p2', 'medium', 'whenever'],
    'P3': ['low', 'p3', 'nice to have', 'sometime', 'backlog']
}

# Task patterns to match
TASK_PATTERNS = [
    re.compile(r'@Atlas\s*(?:task)?[:\s]+(.+)', re.IGNORECASE),
    re.compile(r'@Atlas\s+(?:research|review|todo|fix|update|create|add|write)\s+(.+)', re.IGNORECASE),
    re.compile(r'\[?\s*\]\s*(.+?)\s*@Atlas', re.IGNORECASE),
    re.compile(r'TODO[:\s]+(.+)', re.IGNORECASE),
    re.compile(r'atlas,?\s+(?:please|would you|can you)\s+(.+)', re.IGNORECASE),
    re.compile(r'task[:\s]+(.+)', re.IGNORECASE),
]

# Disposition patterns - for actioning content via comments
DISPOSITION_PATTERNS = {
    'approved': re.compile(r'@atlas\s+approved?', re.IGNORECASE),
    'published': re.compile(r'@atlas\s+(?:published?|publish)', re.IGNORECASE),
    'complete': re.compile(r'@atlas\s+(?:complete|done|finished|ready)', re.IGNORECASE),
    'revise': re.compile(r'@atlas\s+(?:revise|revision|needs? work)', re.IGNORECASE),
    'reject': re.compile(r'@atlas\s+(?:reject|rejected|decline)', re.IGNORECASE),
    'archive': re.compile(r'@atlas\s+(?:archive|file|store)', re.IGNORECASE),
    'canon': re.compile(r'@atlas\s+(?:canon|canonical|add to (?:the )?(?:technical )?canon)', re.IGNORECASE),
}


def get_atlas_user_id() -> Optional[str]:
    """Get Atlas bot's user ID by fetching self info."""
    url = 'https://api.notion.com/v1/users/me'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('id')
    return None


def get_shared_databases() -> List[str]:
    """Get all databases shared with the Atlas integration."""
    if DB_IDS_ENV:
        return [db.strip() for db in DB_IDS_ENV.split(',') if db.strip()]

    url = 'https://api.notion.com/v1/search'
    payload = {
        "filter": {"property": "object", "value": "database"},
        "page_size": 100
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        results = response.json().get('results', [])
        return [r['id'] for r in results]
    return []


def get_all_pages() -> List[Dict]:
    """Get all pages accessible to Atlas (search)."""
    url = 'https://api.notion.com/v1/search'
    payload = {
        "filter": {"property": "object", "value": "page"},
        "page_size": 100
    }
    all_pages = []

    while url:
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code != 200:
            break

        data = response.json()
        all_pages.extend(data.get('results', []))
        url = data.get('next_url', None)
        time.sleep(0.25)  # Rate limit

    return all_pages


def get_page_content(page_id: str) -> str:
    """Get the content of a page as text."""
    url = f'https://api.notion.com/v1/blocks/{page_id}/children'
    content_parts = []

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break

        data = response.json()
        for block in data.get('results', []):
            content_parts.append(block_to_text(block))

        url = data.get('next_url', None)
        time.sleep(0.25)

    return '\n'.join(content_parts)


def block_to_text(block: Dict) -> str:
    """Convert a Notion block to text."""
    block_type = block.get('type', '')
    content = ''

    if block_type == 'paragraph':
        content = rich_text_to_text(block.get('paragraph', {}).get('rich_text', []))
    elif block_type == 'heading_1':
        content = '# ' + rich_text_to_text(block.get('heading_1', {}).get('rich_text', []))
    elif block_type == 'heading_2':
        content = '## ' + rich_text_to_text(block.get('heading_2', {}).get('rich_text', []))
    elif block_type == 'heading_3':
        content = '### ' + rich_text_to_text(block.get('heading_3', {}).get('rich_text', []))
    elif block_type == 'bulleted_list_item':
        content = '- ' + rich_text_to_text(block.get('bulleted_list_item', {}).get('rich_text', []))
    elif block_type == 'numbered_list_item':
        content = '1. ' + rich_text_to_text(block.get('numbered_list_item', {}).get('rich_text', []))
    elif block_type == 'to_do':
        checked = block.get('to_do', {}).get('checked', False)
        content = f"[{'x' if checked else ' '}] " + rich_text_to_text(block.get('to_do', {}).get('rich_text', []))
    elif block_type == 'code':
        content = '```\n' + rich_text_to_text(block.get('code', {}).get('rich_text', [])) + '\n```'
    elif block_type == 'quote':
        content = '> ' + rich_text_to_text(block.get('quote', {}).get('rich_text', []))
    elif block_type == 'callout':
        content = '> ' + rich_text_to_text(block.get('callout', {}).get('rich_text', []))

    return content


def rich_text_to_text(rich_text: List[Dict]) -> str:
    """Convert Notion rich_text array to plain text."""
    return ''.join([
        t.get('plain_text', '') or t.get('text', {}).get('content', '')
        for t in rich_text
    ])


def get_page_comments(page_id: str) -> List[Dict]:
    """Get all comments on a page."""
    url = f'https://api.notion.com/v1/comments?block_id={page_id}'
    all_comments = []

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break

        data = response.json()
        all_comments.extend(data.get('results', []))
        url = data.get('next_url', None)

    return all_comments


def extract_atlas_mentions(text: str) -> List[str]:
    """Extract @Atlas mention patterns from text."""
    mentions = []

    for pattern in TASK_PATTERNS:
        matches = pattern.findall(text)
        mentions.extend([m.strip() for m in matches if m.strip()])

    # Also look for @Atlas specifically
    atlas_pattern = re.compile(r'@Atlas', re.IGNORECASE)
    if atlas_pattern.search(text):
        # Try to get context after @Atlas
        context_match = re.search(r'@Atlas[:\s]+(.+)', text, re.IGNORECASE)
        if context_match:
            mentions.append(context_match.group(1).strip())

    return mentions


def extract_disposition_command(text: str) -> Optional[Dict[str, str]]:
    """Extract disposition command from comment text.

    Returns dict with 'action' and 'full_text' if found, None otherwise.
    """
    for action, pattern in DISPOSITION_PATTERNS.items():
        if pattern.search(text):
            return {
                'action': action,
                'full_text': text.strip()
            }
    return None


def get_pending_dispositions() -> List[Dict]:
    """Scan all pages for pending @atlas disposition commands in comments."""
    print("  Scanning for disposition comments...")

    all_pages = get_all_pages()
    dispositions = []

    for page in all_pages:
        page_id = page['id']
        page_title = get_page_title(page)
        page_url = f"https://www.notion.so/{page_id.replace('-', '')}"

        # Get comments on this page
        comments = get_page_comments(page_id)

        for comment in comments:
            comment_text = rich_text_to_text(comment.get('rich_text', []))
            disposition = extract_disposition_command(comment_text)

            if disposition:
                # Get comment author
                author = comment.get('created_by', {})
                author_name = author.get('name', 'Unknown')
                author_id = author.get('id', '')

                # Get comment timestamp
                created_time = comment.get('created_time', '')

                dispositions.append({
                    'page_id': page_id,
                    'page_title': page_title,
                    'page_url': page_url,
                    'comment_id': comment.get('id', ''),
                    'action': disposition['action'],
                    'full_text': disposition['full_text'],
                    'author': author_name,
                    'author_id': author_id,
                    'created_time': created_time
                })

        time.sleep(0.1)  # Rate limit

    return dispositions


def determine_priority(task_text: str) -> str:
    """Determine priority based on keywords in task text."""
    text_lower = task_text.lower()

    for priority, keywords in PRIORITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return priority

    return 'P2'  # Default priority


def determine_tags(task_text: str) -> List[str]:
    """Determine tags based on task content."""
    tags = []
    text_lower = task_text.lower()

    tag_keywords = {
        'research': ['research', 'investigate', 'find', 'search', 'look into'],
        'code': ['code', 'fix', 'bug', 'refactor', 'implement', 'add', 'create'],
        'docs': ['doc', 'document', 'write', 'update docs', 'readme'],
        'system': ['system', 'config', 'setup', 'install', 'deploy'],
        'grove': ['grove', 'sprint', 'foundation'],
        'review': ['review', 'check', 'audit', 'verify'],
        'refactor': ['refactor', 'clean up', 'improve', 'optimize']
    }

    for tag, keywords in tag_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                if tag not in tags:
                    tags.append(tag)
                break

    return tags if tags else ['system']


def create_task_in_database(task: Dict, source_page_url: str = '') -> bool:
    """Create a task item in the Atlas Tasks database."""
    if not TASK_DB_ID:
        print("  WARNING: NOTION_ATLAS_TASK_DATABASE_ID not set!")
        return False

    url = 'https://api.notion.com/v1/pages'

    priority = determine_priority(task['content'])
    tags = determine_tags(task['content'])

    # Clean up task content - remove task markers
    content = task['content']
    for marker in ['[ ]', 'Task:', 'TODO:', 'atlas, ', 'Atlas, ']:
        content = re.sub(rf'^{re.escape(marker)}\s*', '', content, flags=re.IGNORECASE).strip()

    payload = {
        "parent": {"database_id": TASK_DB_ID},
        "properties": {
            "title": {
                "title": [{"text": {"content": content[:100]}}]
            },
            "Status": {
                "status": {"name": "To-do"}
            },
            "Priority": {
                "select": {"name": priority}
            },
            "Tags": {
                "multi_select": [{"name": tag} for tag in tags]
            },
            "ATLAS Notes": {
                "rich_text": [{"text": {"content": f"Source: {source_page_url}"}}]
            }
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code in [200, 201]:
        return True
    else:
        print(f"  ERROR creating task: {response.status_code} - {response.text[:100]}")
        return False


def scan_page_for_tasks(page: Dict) -> List[Dict]:
    """Scan a page for @Atlas mentions and extract tasks."""
    tasks = []
    page_id = page['id']
    page_title = get_page_title(page)
    page_url = f"https://www.notion.so/{page_id.replace('-', '')}"

    # Check page content
    content = get_page_content(page_id)
    mentions = extract_atlas_mentions(content)

    for mention in mentions:
        tasks.append({
            'content': mention,
            'page_id': page_id,
            'page_title': page_title,
            'page_url': page_url,
            'source': 'page_content'
        })

    # Check comments
    comments = get_page_comments(page_id)
    for comment in comments:
        comment_text = rich_text_to_text(comment.get('rich_text', []))
        mentions = extract_atlas_mentions(comment_text)

        for mention in mentions:
            tasks.append({
                'content': mention,
                'page_id': page_id,
                'page_title': page_title,
                'page_url': page_url,
                'source': 'comment'
            })

    return tasks


def get_page_title(page: Dict) -> str:
    """Extract title from a Notion page."""
    title_prop = page.get('properties', {}).get('title', {})
    if title_prop and title_prop.get('title'):
        return rich_text_to_text(title_prop['title'])

    # Try 'Name' property
    name_prop = page.get('properties', {}).get('Name', {})
    if name_prop and name_prop.get('title'):
        return rich_text_to_text(name_prop['title'])

    # Try 'Title' property (Atlas Inbox uses this)
    title_prop2 = page.get('properties', {}).get('Title', {})
    if title_prop2 and title_prop2.get('title'):
        return rich_text_to_text(title_prop2['title'])

    return 'Untitled'


def get_pending_plans() -> List[Dict]:
    """Get pending plans from Atlas Inbox that need approval."""
    if not INBOX_DB_ID:
        return []

    url = f'https://api.notion.com/v1/databases/{INBOX_DB_ID}/query'
    payload = {
        "filter": {
            "and": [
                {"property": "Status", "status": {"equals": "Pending"}},
                {"property": "Disposition", "select": {"equals": "Action Required"}}
            ]
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        results = response.json().get('results', [])
        plans = []
        for page in results:
            props = page.get('properties', {})
            title = ''
            if props.get('Title', {}).get('title'):
                title = rich_text_to_text(props['Title']['title'])

            priority = props.get('Priority', {}).get('select', {})
            priority_name = priority.get('name', 'P2') if priority else 'P2'

            plans.append({
                'id': page['id'],
                'title': title,
                'priority': priority_name,
                'url': f"https://www.notion.so/{page['id'].replace('-', '')}"
            })
        return plans
    return []


def main():
    print("=" * 60)
    print("ATLAS CHIEF OF STAFF - STARTUP ROUTINE")
    print("=" * 60)

    # Check API key
    if not NOTION_KEY:
        print("\nERROR: NOTION_ATLAS_API_KEY not set!")
        print("Set it via environment variable or .env file")
        sys.exit(1)

    print(f"\n[1/7] Authenticating Atlas...")
    atlas_user_id = get_atlas_user_id()
    if not atlas_user_id:
        print("  Failed to authenticate. Check API key.")
        sys.exit(1)
    print(f"  Atlas authenticated successfully")

    print(f"\n[2/7] Checking for pending plans awaiting approval...")
    pending_plans = get_pending_plans()
    if pending_plans:
        print(f"  Found {len(pending_plans)} pending plan(s):")
        for plan in pending_plans:
            print(f"    [{plan['priority']}] {plan['title'][:50]}")
        print(f"\n  These plans need approval before execution.")
    else:
        print(f"  No pending plans. Clear to execute.")

    print(f"\n[3/7] Scanning for disposition comments (@atlas approved/published/etc)...")
    pending_dispositions = get_pending_dispositions()
    if pending_dispositions:
        print(f"  Found {len(pending_dispositions)} disposition command(s):")
        for disp in pending_dispositions:
            print(f"    [{disp['action'].upper()}] {disp['page_title'][:40]}")
            print(f"      Comment: {disp['full_text'][:60]}...")
    else:
        print(f"  No pending dispositions.")

    print(f"\n[4/7] Finding databases to scan...")
    databases = get_shared_databases()
    print(f"  Found {len(databases)} databases")

    if not TASK_DB_ID:
        print(f"\n  WARNING: NOTION_ATLAS_TASK_DATABASE_ID not set")
        print("  Tasks will be counted but not created")

    print(f"\n[5/7] Scanning all pages for @Atlas task mentions...")
    all_pages = get_all_pages()
    print(f"  Found {len(all_pages)} accessible pages")

    all_tasks = []
    for i, page in enumerate(all_pages, 1):
        if i % 50 == 0:
            print(f"  Scanning page {i}/{len(all_pages)}...")
        tasks = scan_page_for_tasks(page)
        all_tasks.extend(tasks)
        time.sleep(0.25)  # Rate limit

    # Remove duplicates based on content + page_id
    seen = set()
    unique_tasks = []
    for task in all_tasks:
        key = (task['content'].lower(), task['page_id'])
        if key not in seen:
            seen.add(key)
            unique_tasks.append(task)

    print(f"\n  Found {len(unique_tasks)} unique task mentions")

    if unique_tasks:
        print(f"\n[6/7] Creating tasks in Atlas Tasks database...")
        created_count = 0
        for task in unique_tasks:
            # Check if this looks like a task (not just a casual mention)
            content = task['content'].lower()
            if any(marker in content for marker in ['task', 'todo', 'research', 'review', 'fix', 'update', 'create', 'please']):
                success = create_task_in_database(task, task['page_url'])
                if success:
                    created_count += 1
                    print(f"  Created: {task['content'][:50]}...")

        print(f"\n  Created {created_count} tasks in Notion")

        print(f"\n[7/7] Summary:")
        print(f"  Tasks: {len(unique_tasks)}")
        for task in unique_tasks[:3]:
            priority = determine_priority(task['content'])
            print(f"    [{priority}] {task['content'][:50]}...")
        if len(unique_tasks) > 3:
            print(f"    ... and {len(unique_tasks) - 3} more")
    else:
        print(f"\n[6/7] No tasks to create")
        print(f"\n[7/7] Summary:")

    # Summary of dispositions
    if pending_dispositions:
        print(f"\n  Dispositions awaiting action: {len(pending_dispositions)}")
        for disp in pending_dispositions[:3]:
            print(f"    [{disp['action'].upper()}] {disp['page_title'][:40]}")
        if len(pending_dispositions) > 3:
            print(f"    ... and {len(pending_dispositions) - 3} more")

    print("\n" + "=" * 60)
    print("ATLAS STARTUP COMPLETE")
    print(f"Tasks: {len(unique_tasks)} | Dispositions: {len(pending_dispositions)} | Plans: {len(pending_plans)}")
    print("=" * 60)

    # Output for consumption by other scripts
    print("\n## ATLAS_STARTUP_JSON_START##")
    print(json.dumps({
        'pending_plans': [{'title': p['title'], 'priority': p['priority'], 'url': p['url']} for p in pending_plans],
        'pending_dispositions': [{
            'action': d['action'],
            'page_title': d['page_title'],
            'page_url': d['page_url'],
            'page_id': d['page_id'],
            'comment': d['full_text']
        } for d in pending_dispositions],
        'task_count': len(unique_tasks),
        'tasks': [{'content': t['content'], 'priority': determine_priority(t['content'])} for t in unique_tasks[:10]]
    }))
    print("## ATLAS_STARTUP_JSON_END##")


if __name__ == "__main__":
    main()
