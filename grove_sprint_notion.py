#!/usr/bin/env python3
"""
Grove Sprint Notion Manager
===========================
Create and update sprint entries in the Grove Feature Roadmap database.

Usage:
    python grove_sprint_notion.py create S15-BD-FederationEditors-v1 --status in-progress --domain Bedrock
    python grove_sprint_notion.py update S15 --status complete
    python grove_sprint_notion.py list
    python grove_sprint_notion.py list --status in-progress

Environment:
    Reads NOTION_API_KEY from .env file or environment variable.
"""

import argparse
import os
import sys
from pathlib import Path

import requests

# Load .env if present
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.strip() and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip())

# Configuration
NOTION_KEY = os.environ.get('NOTION_API_KEY')
GROVE_ROADMAP_DB_ID = 'cb49453c-022c-477d-a35b-744531e7d161'

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# Valid values for select properties
VALID_STATUS = ['idea', 'draft-spec', 'needs-audit', 'ready', 'in-progress', 'complete', 'archived', 'blocked']
VALID_DOMAIN = ['Bedrock', 'Surface', 'Core', 'Infrastructure', 'Documentation']
VALID_EFFORT = ['tiny', 'small', 'medium', 'large', 'epic']


def list_sprints(status_filter=None, limit=50):
    """List sprints in the Grove Feature Roadmap."""
    url = f'https://api.notion.com/v1/databases/{GROVE_ROADMAP_DB_ID}/query'

    payload = {'page_size': limit}
    if status_filter:
        payload['filter'] = {
            'property': 'Status',
            'select': {'equals': status_filter}
        }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text[:200]}")
        return []

    results = response.json().get('results', [])
    sprints = []

    for r in results:
        props = r.get('properties', {})
        title = props.get('Feature', {}).get('title', [])
        title_text = title[0]['plain_text'] if title else 'No title'

        status = props.get('Status', {}).get('select', {})
        status_name = status.get('name', 'None') if status else 'None'

        domain = props.get('Domain', {}).get('select', {})
        domain_name = domain.get('name', '') if domain else ''

        sprints.append({
            'id': r['id'],
            'title': title_text,
            'status': status_name,
            'domain': domain_name,
            'url': r.get('url', '')
        })

    return sprints


def find_sprint(search_term):
    """Find a sprint by partial title match."""
    url = f'https://api.notion.com/v1/databases/{GROVE_ROADMAP_DB_ID}/query'
    payload = {
        'filter': {
            'property': 'Feature',
            'title': {'contains': search_term}
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return None

    results = response.json().get('results', [])
    return results[0] if results else None


def create_sprint(title, status='draft-spec', domain=None, effort=None, parent_spec=None):
    """Create a new sprint entry."""
    url = 'https://api.notion.com/v1/pages'

    properties = {
        'Feature': {
            'title': [{'text': {'content': title}}]
        },
        'Status': {
            'select': {'name': status}
        }
    }

    if domain:
        properties['Domain'] = {'select': {'name': domain}}
    if effort:
        properties['Effort'] = {'select': {'name': effort}}
    if parent_spec:
        properties['Parent Spec'] = {'rich_text': [{'text': {'content': parent_spec}}]}

    payload = {
        'parent': {'database_id': GROVE_ROADMAP_DB_ID},
        'properties': properties
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        data = response.json()
        return {
            'id': data['id'],
            'url': data['url'],
            'success': True
        }
    else:
        return {
            'success': False,
            'error': response.text[:300]
        }


def update_sprint(page_id, status=None, domain=None, effort=None):
    """Update an existing sprint entry."""
    url = f'https://api.notion.com/v1/pages/{page_id}'

    properties = {}
    if status:
        properties['Status'] = {'select': {'name': status}}
    if domain:
        properties['Domain'] = {'select': {'name': domain}}
    if effort:
        properties['Effort'] = {'select': {'name': effort}}

    if not properties:
        return {'success': False, 'error': 'No properties to update'}

    payload = {'properties': properties}

    response = requests.patch(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return {'success': True}
    else:
        return {'success': False, 'error': response.text[:300]}


def main():
    # Handle Windows encoding for emojis
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description='Manage Grove sprints in Notion')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # List command
    list_parser = subparsers.add_parser('list', help='List sprints')
    list_parser.add_argument('--status', choices=VALID_STATUS, help='Filter by status')
    list_parser.add_argument('--limit', type=int, default=25, help='Max results')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new sprint')
    create_parser.add_argument('title', help='Sprint title (e.g., S15-BD-FederationEditors-v1)')
    create_parser.add_argument('--status', choices=VALID_STATUS, default='draft-spec')
    create_parser.add_argument('--domain', choices=VALID_DOMAIN)
    create_parser.add_argument('--effort', choices=VALID_EFFORT)
    create_parser.add_argument('--parent', help='Parent spec name')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update a sprint')
    update_parser.add_argument('search', help='Sprint title search term')
    update_parser.add_argument('--status', choices=VALID_STATUS)
    update_parser.add_argument('--domain', choices=VALID_DOMAIN)
    update_parser.add_argument('--effort', choices=VALID_EFFORT)

    args = parser.parse_args()

    if not NOTION_KEY:
        print("Error: NOTION_API_KEY not set")
        print("Set it in .env or as environment variable")
        sys.exit(1)

    if args.command == 'list':
        sprints = list_sprints(args.status, args.limit)
        if not sprints:
            print("No sprints found")
            return

        print(f"\nGrove Feature Roadmap ({len(sprints)} entries):\n")
        for s in sprints:
            status_display = s['status'][:12].ljust(12)
            domain_display = f"[{s['domain']}]" if s['domain'] else ""
            print(f"  {status_display}  {s['title'][:50]} {domain_display}")

    elif args.command == 'create':
        print(f"Creating sprint: {args.title}")
        result = create_sprint(
            args.title,
            status=args.status,
            domain=args.domain,
            effort=args.effort,
            parent_spec=args.parent
        )
        if result['success']:
            print(f"  Created! URL: {result['url']}")
        else:
            print(f"  Error: {result['error']}")

    elif args.command == 'update':
        print(f"Searching for: {args.search}")
        sprint = find_sprint(args.search)
        if not sprint:
            print("  Sprint not found")
            return

        title = sprint['properties']['Feature']['title']
        title_text = title[0]['plain_text'] if title else 'Unknown'
        print(f"  Found: {title_text}")

        result = update_sprint(
            sprint['id'],
            status=args.status,
            domain=args.domain,
            effort=args.effort
        )
        if result['success']:
            print(f"  Updated successfully!")
        else:
            print(f"  Error: {result['error']}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
