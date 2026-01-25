#!/usr/bin/env python3
"""
Atlas Research Handler
Creates research tasks and posts findings back to Notion.

Usage:
    python atlas_research.py "research topic" [--output file.md]

Environment:
    NOTION_ATLAS_API_KEY - Notion API key
    NOTION_ATLAS_TASK_DATABASE_ID - Task database ID
"""
import json
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any

import requests

# Configuration
NOTION_KEY = os.environ.get('NOTION_ATLAS_API_KEY', '')
TASK_DB_ID = os.environ.get('NOTION_ATLAS_TASK_DATABASE_ID', '')

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}


def create_research_task(topic: str) -> str:
    """Create a research task in Notion and return the page ID."""
    if not TASK_DB_ID:
        print("WARNING: NOTION_ATLAS_TASK_DATABASE_ID not set")
        return ""

    url = 'https://api.notion.com/v1/pages'
    payload = {
        "parent": {"database_id": TASK_DB_ID},
        "properties": {
            "title": {
                "title": [{"text": {"content": f"Research: {topic[:90]}"}}]
            },
            "Status": {"status": {"name": "In Progress"}},
            "Priority": {"select": {"name": "P1"}},
            "Tags": {"multi_select": [{"name": "research"}]},
            "ATLAS Notes": {
                "rich_text": [{"text": {"content": f"Research started: {datetime.now().isoformat()}"}}]
            }
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code in [200, 201]:
        page_id = response.json()['id']
        print(f"✓ Created research task: {topic}")
        return page_id
    else:
        print(f"ERROR: {response.status_code} - {response.text[:100]}")
        return ""


def update_task_with_findings(page_id: str, findings: str, sources: List[str] = None):
    """Update the task page with research findings."""
    url = f'https://api.notion.com/v1/pages/{page_id}'

    content = f"""# Research Findings: {datetime.now().strftime('%Y-%m-%d')}

## Summary
{findings}

## Sources
{sources if sources else 'Web search results'}

---
*Research completed by Atlas Chief of Staff*
"""

    payload = {
        "properties": {
            "Status": {"status": {"name": "Done"}},
            "ATLAS Notes": {
                "rich_text": [{"text": {"content": content[:1900]}}]
            }
        }
    }

    response = requests.patch(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("✓ Updated task with findings")
    else:
        print(f"ERROR updating task: {response.status_code}")


def web_search(query: str) -> Dict[str, Any]:
    """Perform web search using Claude Code's search capability."""
    # This would typically be called via Claude Code's MCP
    # For now, we'll structure the response format
    return {
        "query": query,
        "results": [],
        "timestamp": datetime.now().isoformat()
    }


def main():
    parser = argparse.ArgumentParser(description='Atlas Research Handler')
    parser.add_argument('topic', help='Research topic or query')
    parser.add_argument('--output', '-o', help='Output file for findings')
    parser.add_argument('--update-task', help='Update existing task page ID')
    args = parser.parse_args()

    print(f"Atlas Research Handler")
    print(f"======================")
    print(f"Topic: {args.topic}")
    print()

    # Create task if no existing task ID
    page_id = args.update_task or create_research_task(args.topic)

    if not page_id and not args.update_task:
        print("ERROR: Could not create research task")
        sys.exit(1)

    # Simulate research (in real usage, this would use Claude Code's tools)
    print("Research would be performed here using:")
    print("  - Web search for current information")
    print("  - Document analysis")
    print("  - Source verification")
    print()
    print("Example findings would be posted back to Notion task.")

    if args.output:
        findings = f"# Research: {args.topic}\n\nResearch completed at {datetime.now().isoformat()}"
        with open(args.output, 'w') as f:
            f.write(findings)
        print(f"✓ Findings saved to {args.output}")

    if page_id:
        print(f"\nTask URL: https://www.notion.so/{page_id.replace('-', '')}")


if __name__ == "__main__":
    main()
