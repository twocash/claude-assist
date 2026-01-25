#!/usr/bin/env python3
"""Debug: check what URLs are stored in Notion."""
import json
import os
import requests

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

    print(f"Found {len(pages)} pages\n")

    # Check URL property format
    for page in pages[:5]:
        props = page.get('properties', {})
        url_prop = props.get('userDefined:URL', {})
        print(f"Page ID: {page['id']}")
        print(f"  URL property type: {type(url_prop)}")
        print(f"  URL property value: {url_prop}")
        print(f"  Name: {props.get('Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'N/A')}")
        print()
else:
    print(f"Error: {response.status_code}")
    print(response.text)
