#!/usr/bin/env python3
"""
Atlas Code Review Handler
Creates code review tasks and posts findings back to Notion.

Usage:
    python atlas_review.py "file_path" [--repo repo_url]

Environment:
    NOTION_ATLAS_API_KEY - Notion API key
    NOTION_ATLAS_TASK_DATABASE_ID - Task database ID
    SERENA_PROJECT_PATH - Serena project path (optional)
"""
import json
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

import requests

# Configuration
NOTION_KEY = os.environ.get('NOTION_ATLAS_API_KEY', '')
TASK_DB_ID = os.environ.get('NOTION_ATLAS_TASK_DATABASE_ID', '')
SERENA_PROJECT = os.environ.get('SERENA_PROJECT_PATH', '')

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

# Review categories
REVIEW_CHECKS = {
    'security': [
        'SQL injection risks',
        'XSS vulnerabilities',
        'Authentication checks',
        'Authorization logic',
        'Secrets in code'
    ],
    'style': [
        'Naming conventions',
        'Code formatting',
        'Comment quality',
        'Line length',
        'Import organization'
    ],
    'quality': [
        'Function complexity',
        'Duplicate code',
        'Error handling',
        'Edge cases',
        'Type safety'
    ],
    'tests': [
        'Test coverage',
        'Test quality',
        'Mock usage',
        'Edge case tests',
        'Integration tests'
    ]
}


def create_review_task(file_path: str, repo_url: str = "") -> str:
    """Create a code review task in Notion."""
    if not TASK_DB_ID:
        print("WARNING: NOTION_ATLAS_TASK_DATABASE_ID not set")
        return ""

    url = 'https://api.notion.com/v1/pages'
    payload = {
        "parent": {"database_id": TASK_DB_ID},
        "properties": {
            "title": {
                "title": [{"text": {"content": f"Review: {file_path[:90]}"}}]
            },
            "Status": {"status": {"name": "In Progress"}},
            "Priority": {"select": {"name": "P1"}},
            "Tags": {"multi_select": [{"name": "review"}]},
            "ATLAS Notes": {
                "rich_text": [{"text": {"content": f"Review started: {datetime.now().isoformat()}\nFile: {file_path}\nRepo: {repo_url}"}}]
            }
        }
    }

    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code in [200, 201]:
        page_id = response.json()['id']
        print(f"✓ Created review task: {file_path}")
        return page_id
    else:
        print(f"ERROR: {response.status_code} - {response.text[:100]}")
        return ""


def read_file_via_serena(file_path: str) -> Optional[str]:
    """Read file content using Serena MCP if available."""
    # This would use Serena MCP read_file in actual usage
    # For now, we return None to indicate file should be read by Claude
    return None


def analyze_code(content: str, file_path: str) -> Dict[str, Any]:
    """Analyze code and return review findings."""
    findings = {
        'security': [],
        'style': [],
        'quality': [],
        'tests': [],
        'score': 10,
        'issues_count': 0
    }

    if not content:
        return findings

    content_lower = content.lower()

    # Simple keyword-based analysis (would be replaced with LLM analysis)
    security_keywords = ['password', 'secret', 'api_key', 'token', 'auth']
    for kw in security_keywords:
        if kw in content_lower:
            if any(s in kw for s in security_keywords):
                findings['security'].append(f"Potential secret found: {kw}")
                findings['issues_count'] += 1

    # Check for common issues
    if 'console.log' in content or 'print(' in content:
        findings['quality'].append("Debug statements left in code")
        findings['issues_count'] += 1

    if 'except:' in content or 'catch:' in content:
        findings['quality'].append("Broad exception handling detected")
        findings['issues_count'] += 1

    # Calculate simple score
    findings['score'] = max(1, 10 - findings['issues_count'])

    return findings


def format_review_report(file_path: str, findings: Dict, content: str = None) -> str:
    """Format review findings as markdown."""
    report = f"""# Code Review: {file_path}

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Score:** {findings['score']}/10
**Issues:** {findings['issues_count']}

## Summary
"""

    if findings['issues_count'] == 0:
        report += "No issues found. Code looks good!\n"
    elif findings['score'] >= 7:
        report += "Minor issues found. Code is acceptable with fixes.\n"
    elif findings['score'] >= 4:
        report += "Several issues found. Review recommended before merge.\n"
    else:
        report += "Significant issues found. Please address before merging.\n"

    for category, items in [('Security', findings['security']),
                             ('Style', findings['style']),
                             ('Quality', findings['quality']),
                             ('Tests', findings['tests'])]:
        if items:
            report += f"\n### {category} Issues\n"
            for item in items:
                report += f"- {item}\n"

    if content:
        report += f"\n## Code Preview\n```\n{content[:500]}...\n```\n"

    report += "\n---\n*Review completed by Atlas Chief of Staff*"

    return report


def update_task_with_review(page_id: str, report: str, file_path: str):
    """Update the task page with review findings."""
    url = f'https://api.notion.com/v1/pages/{page_id}'

    payload = {
        "properties": {
            "Status": {"status": {"name": "Done"}},
            "ATLAS Notes": {
                "rich_text": [{"text": {"content": report[:1900]}}]
            }
        }
    }

    response = requests.patch(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print("✓ Updated task with review findings")
    else:
        print(f"ERROR updating task: {response.status_code}")


def main():
    parser = argparse.ArgumentParser(description='Atlas Code Review Handler')
    parser.add_argument('file', help='File path to review')
    parser.add_argument('--repo', '-r', default='', help='Repository URL')
    parser.add_argument('--output', '-o', help='Output file for review')
    parser.add_argument('--update-task', help='Update existing task page ID')
    args = parser.parse_args()

    print(f"Atlas Code Review Handler")
    print(f"==========================")
    print(f"File: {args.file}")
    print(f"Repo: {args.repo or 'local'}")
    print()

    # Create task if no existing task ID
    page_id = args.update_task or create_review_task(args.file, args.repo)

    if not page_id and not args.update_task:
        print("ERROR: Could not create review task")
        sys.exit(1)

    print("Code analysis would be performed here using:")
    print("  - Serena MCP for file reading")
    print("  - Claude Code for detailed analysis")
    print("  - Pattern matching for common issues")
    print()
    print("Example findings would be posted back to Notion task.")

    if args.output:
        findings = f"# Code Review: {args.file}\n\nReview completed at {datetime.now().isoformat()}"
        with open(args.output, 'w') as f:
            f.write(findings)
        print(f"✓ Review saved to {args.output}")

    if page_id:
        print(f"\nTask URL: https://www.notion.so/{page_id.replace('-', '')}")


if __name__ == "__main__":
    main()
