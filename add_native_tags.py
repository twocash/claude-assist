#!/usr/bin/env python3
"""
Add tag properties to Notion database and generate pragmatic thoughts.
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

def update_database_schema():
    """Add tag properties to the database schema."""
    url = f'https://api.notion.com/v1/databases/{DB_ID}'

    properties = {
        "Platform": {
            "select": {
                "options": [
                    {"name": "cloud", "color": "blue"},
                    {"name": "local", "color": "green"},
                    {"name": "browser", "color": "yellow"},
                    {"name": "cli", "color": "gray"},
                    {"name": "gui", "color": "purple"},
                    {"name": "api", "color": "orange"},
                ]
            }
        },
        "Cost": {
            "select": {
                "options": [
                    {"name": "oss", "color": "green"},
                    {"name": "free", "color": "blue"},
                    {"name": "paid", "color": "red"},
                    {"name": "freemium", "color": "yellow"},
                ]
            }
        },
        "Type": {
            "select": {
                "options": [
                    {"name": "api", "color": "blue"},
                    {"name": "cli", "color": "gray"},
                    {"name": "gui", "color": "purple"},
                    {"name": "browser-ext", "color": "yellow"},
                    {"name": "library", "color": "green"},
                    {"name": "framework", "color": "orange"},
                ]
            }
        },
        "Maturity": {
            "select": {
                "options": [
                    {"name": "production", "color": "green"},
                    {"name": "beta", "color": "yellow"},
                    {"name": "experimental", "color": "red"},
                ]
            }
        },
    }

    response = requests.patch(url, headers=HEADERS, json={"properties": properties})

    if response.status_code in [200, 201]:
        print("Database schema updated with tag properties!")
        return True
    else:
        print(f"Error updating schema: {response.status_code}")
        print(response.text)
        return False

def query_database():
    """Query all pages in the database."""
    url = f'https://api.notion.com/v1/databases/{DB_ID}/query'
    all_results = []
    cursor = None

    while True:
        payload = {}
        if cursor:
            payload['start_cursor'] = cursor

        response = requests.post(url, headers=HEADERS, json=payload)

        if response.status_code == 200:
            data = response.json()
            all_results.extend(data.get('results', []))
            if data.get('has_more'):
                cursor = data.get('next_cursor')
                print(f"  Fetched {len(all_results)} pages, continuing...")
                time.sleep(0.5)
            else:
                break
        else:
            print(f"Error querying database: {response.status_code}")
            break

    return all_results

def update_page_with_tags(page_id: str, entry: dict, thought: str) -> bool:
    """Update a page with tag properties and new thought."""
    url = f'https://api.notion.com/v1/pages/{page_id}'

    short_name = entry['original_name'].split('/')[-1] if '/' in entry['original_name'] else entry['original_name']
    new_title = f"{entry['title']} ({short_name})"

    # Truncate description
    desc = entry.get('description', '')[:1900]

    payload = {
        'properties': {
            'Name': {
                'title': [{'text': {'content': new_title}}]
            },
            'Thought': {
                'rich_text': [{'text': {'content': thought}}]
            },
            'Description': {
                'rich_text': [{'text': {'content': desc}}]
            },
            'Platform': {
                'select': {'name': entry['platform']}
            },
            'Cost': {
                'select': {'name': entry['cost']}
            },
            'Type': {
                'select': {'name': entry['type']}
            },
            'Maturity': {
                'select': {'name': entry['maturity']}
            },
        }
    }

    response = requests.patch(url, headers=HEADERS, json=payload)

    if response.status_code in [200, 201]:
        return True
    else:
        print(f"  Error: {response.status_code}")
        return False

def generate_thought(entry: dict) -> str:
    """Generate a pragmatic thought about the repo."""
    # Use the standardized info to create a useful description
    class_lower = entry['class'].lower()
    feature_lower = entry['feature'].lower()
    benefit_lower = entry['benefit'].replace(' ', '-').lower()
    category = entry['category']
    original = entry['original_name']
    desc = entry.get('description', '')

    # Create pragmatic thoughts based on category and class
    thoughts = {
        ('Claude Code/Skills', 'Agent'): f"Claude-native autonomous agent for {feature_lower.replace('-', ' ')}. Use for {benefit_lower.replace('-', ' ')} coding workflows. Integrates directly with Claude Code CLI.",
        ('Claude Code/Skills', 'Skill'): f"Claude Code skill for {feature_lower.replace('-', ' ')}. Extends Claude's capabilities with {desc[:100] if desc else 'specialized functionality'}.",
        ('Claude Code/Skills', 'Workflow'): f"Claude Code workflow for {feature_lower.replace('-', ' ')}. Streamlines {benefit_lower.replace('-', ' ')} development processes.",
        ('AI Agents & Frameworks', 'Agent'): f"Autonomous {class_lower} for {feature_lower.replace('-', ' ')}. Ideal for {benefit_lower.replace('-', ' ')} AI applications. Supports multi-model deployment.",
        ('AI Agents & Frameworks', 'Framework'): f"{class_lower.title()} enabling {feature_lower.replace('-', ' ')}. Powers {benefit_lower.replace('-', ' ')} agent systems. Production-ready.",
        ('Browser & Web Automation', 'Agent'): f"Browser-based {class_lower} for {feature_lower.replace('-', ' ')}. Perfect for {benefit_lower.replace('-', ' ')} web scraping and automation tasks.",
        ('Browser & Web Automation', 'Browser'): f"In-browser {class_lower} enabling {feature_lower.replace('-', ' ')}. Runs locally for {benefit_lower.replace('-', ' ')} privacy.",
        ('Browser & Web Automation', 'Scraper'): f"Web {class_lower} for {feature_lower.replace('-', ' ')}. Extracts data at scale with {benefit_lower.replace('-', ' ')} reliability.",
        ('Memory & Knowledge', 'Agent'): f"Memory-augmented {class_lower} for {feature_lower.replace('-', ' ')}. Maintains context across sessions with {benefit_lower.replace('-', ' ')} persistence.",
        ('Memory & Knowledge', 'Knowledge'): f"Knowledge base {class_lower} for {feature_lower.replace('-', ' ')}. Stores and retrieves with {benefit_lower.replace('-', ' ')} accuracy.",
        ('Memory & Knowledge', 'Memory'): f"Persistent {class_lower} for {feature_lower.replace('-', ' ')}. Never lose context with {benefit_lower.replace('-', ' ')} memory store.",
        ('LLM/RAG/Vector DB', 'Agent'): f"LLM-powered {class_lower} for {feature_lower.replace('-', ' ')}. Optimized for {benefit_lower.replace('-', ' ')} inference.",
        ('LLM/RAG/Vector DB', 'Framework'): f"RAG {class_lower} enabling {feature_lower.replace('-', ' ')}. Powers {benefit_lower.replace('-', ' ')} retrieval-augmented generation.",
        ('LLM/RAG/Vector DB', 'Router'): f"LLM {class_lower} for {feature_lower.replace('-', ' ')}. Routes queries to optimal models with {benefit_lower.replace('-', ' ')} intelligence.",
        ('LLM/RAG/Vector DB', 'Vector DB'): f"Vector database {class_lower} for {feature_lower.replace('-', ' ')}. Stores embeddings with {benefit_lower.replace('-', ' ')} performance.",
        ('LLM/RAG/Vector DB', 'Chunking'): f"Text {class_lower} for {feature_lower.replace('-', ' ')}. Optimizes RAG pipelines with {benefit_lower.replace('-', ' ')} splitting.",
        ('Workflow & Automation', 'Workflow'): f"Automation {class_lower} for {feature_lower.replace('-', ' ')}. Enables {benefit_lower.replace('-', ' ')} workflows without code.",
        ('Workflow & Automation', 'Agent'): f"Automation {class_lower} for {feature_lower.replace('-', ' ')}. Achieves {benefit_lower.replace('-', ' ')} task completion.",
        ('Design & UI', 'Component'): f"UI {class_lower} for {feature_lower.replace('-', ' ')}. Build {benefit_lower.replace('-', ' ')} interfaces fast.",
        ('Design & UI', 'Design System'): f"Design system {class_lower} for {feature_lower.replace('-', ' ')}. Scale {benefit_lower.replace('-', ' ')} visual development.",
        ('Design & UI', 'Knowledge'): f"Design {class_lower} for {feature_lower.replace('-', ' ')}. Document and share {benefit_lower.replace('-', ' ')} patterns.",
        ('Privacy & Local-First', 'Framework'): f"Local-first {class_lower} for {feature_lower.replace('-', ' ')}. Your data stays with you with {benefit_lower.replace('-', ' ')} sovereignty.",
        ('Privacy & Local-First', 'Multi Agent'): f"Local {class_lower} system for {feature_lower.replace('-', ' ')}. Collaborate with {benefit_lower.replace('-', ' ')} privacy.",
        ('Image/Media/OCR', 'OCR'): f"OCR {class_lower} for {feature_lower.replace('-', ' ')}. Extract text with {benefit_lower.replace('-', ' ')} accuracy.",
        ('Image/Media/OCR', 'Image Gen'): f"Image generation {class_lower} for {feature_lower.replace('-', ' ')}. Create {benefit_lower.replace('-', ' ')} visuals.",
        ('Image/Media/OCR', 'Tool'): f"Media {class_lower} for {feature_lower.replace('-', ' ')}. Process images with {benefit_lower.replace('-', ' ')} efficiency.",
        ('Finance & Trading', 'Trading'): f"Trading {class_lower} for {feature_lower.replace('-', ' ')}. Execute {benefit_lower.replace('-', ' ')} strategies.",
        ('Finance & Trading', 'Backtest'): f"Backtesting {class_lower} for {feature_lower.replace('-', ' ')}. Validate {benefit_lower.replace('-', ' ')} trading strategies.",
        ('Finance & Trading', 'Agent'): f"Trading {class_lower} for {feature_lower.replace('-', ' ')}. Automate {benefit_lower.replace('-', ' ')} financial decisions.",
    }

    # Try to get a specific thought
    key = (category, entry['class'])
    if key in thoughts:
        return thoughts[key]

    # Generic fallback
    return f"{category} {class_lower} for {feature_lower.replace('-', ' ')}. Provides {benefit_lower.replace('-', ' ')} functionality. {desc[:100] if desc else 'Useful tool for developers.'}"

def main():
    print("UPDATING NOTION WITH NATIVE TAGS & BETTER THOUGHTS")
    print("=" * 60)

    # First, update database schema
    print("\n1. Adding tag properties to database...")
    update_database_schema()

    # Load standardized entries
    with open('standardized_repos.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    entries = data['entries']

    print(f"\n2. Loaded {len(entries)} entries")

    # Query database
    print("\n3. Fetching pages from Notion...")
    pages = query_database()
    print(f"   Found {len(pages)} pages")

    # Build URL to page_id mapping
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

    # Update entries
    updated = 0
    errors = 0

    print("\n4. Updating entries with native tags and new thoughts...")
    for i, entry in enumerate(entries, 1):
        url = entry['url']
        if url in url_to_page:
            page_id = url_to_page[url]

            # Generate new thought
            thought = generate_thought(entry)

            short_title = entry['title'][:35] + '...' if len(entry['title']) > 35 else entry['title']
            print(f"{i:2d}. {short_title}")

            if update_page_with_tags(page_id, entry, thought):
                updated += 1
            else:
                errors += 1

            time.sleep(0.3)

    print("\n" + "=" * 60)
    print(f"RESULTS:")
    print(f"  Updated: {updated}")
    print(f"  Errors: {errors}")
    print(f"  Total: {len(entries)}")

if __name__ == "__main__":
    main()
