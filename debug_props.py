#!/usr/bin/env python3
"""Debug: check all properties of a Notion page."""
import json
import os
import requests
import pprint

NOTION_KEY = os.environ.get('NOTION_API_KEY', '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')
DB_ID = 'efbdb5df36ed475eaf7ab28b25711c0c'

HEADERS = {
    'Authorization': f'Bearer {NOTION_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

url = f'https://api.notion.com/v1/databases/{DB_ID}/query'
response = requests.post(url, headers=HEADERS, json={})

if response.status_code == 200:
    data = response.json()
    pages = data.get('results', [])

    # Get first page details
    if pages:
        page_id = pages[0]['id']
        page_url = f'https://api.notion.com/v1/pages/{page_id}'
        page_resp = requests.get(page_url, headers=HEADERS)

        if page_resp.status_code == 200:
            page = page_resp.json()
            props = page.get('properties', {})

            print("All properties on first page:")
            print("=" * 60)
            for name, prop in props.items():
                print(f"\n{name}: {prop.get('type')}")
                if 'url' in prop:
                    print(f"  url: {prop['url']}")
                if 'rich_text' in prop:
                    rt = prop['rich_text']
                    if rt:
                        print(f"  rich_text: {rt[0].get('text', {}).get('content', 'N/A')}")
                if 'title' in prop:
                    tt = prop['title']
                    if tt:
                        print(f"  title: {tt[0].get('text', {}).get('content', 'N/A')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
