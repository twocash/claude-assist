#!/usr/bin/env python3
"""
Export standardized repo entries to CSV for Notion import.
Format: {CAT} | {CLASS} | {FEATURE} | {BENEFIT}
With embedded tags for easy filtering.
"""
import json
import csv

with open('standardized_repos.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
entries = data['entries']

# Write CSV
with open('github_stars_standardized.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(['Name', 'Category', 'Class', 'Feature', 'Benefit', 'Platform', 'Cost', 'Type', 'Maturity', 'URL', 'Stars', 'Description'])

    for e in entries:
        writer.writerow([
            e['title'],
            e['category'],
            e['class'],
            e['feature'],
            e['benefit'],
            e['platform'],
            e['cost'],
            e['type'],
            e['maturity'],
            e['url'],
            e['stars'],
            e['description']
        ])

print(f"Exported {len(entries)} entries to github_stars_standardized.csv")
print()
print("TITLE PATTERN: {CAT} | {CLASS} | {FEATURE} | {BENEFIT}")
print()
print("SAMPLE TITLES:")
for e in entries[:10]:
    print(f"  {e['title']}")

print()
print("IMPORT TO NOTION:")
print("1. Open Notion: https://www.notion.so/efbdb5df36ed475eaf7ab28b25711c0c")
print("2. Click '...' menu > 'Import' > 'CSV'")
print("3. Select github_stars_standardized.csv")
print("4. Map columns to properties")
