"""Helper to get a single item from the MCP update queue."""
import json
import sys
from pathlib import Path

QUEUE_FILE = Path(__file__).parent / 'mcp_update_queue.json'
OUTPUT_DIR = Path(__file__).parent / 'temp_content'

def get_item(index: int, write_content: bool = False):
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = json.load(f)

    if index >= len(queue):
        print(f"ERROR: Index {index} out of range (max {len(queue)-1})")
        return

    item = queue[index]
    print(f"NOTION_ID: {item['notion_id']}")
    print(f"FILENAME: {item['filename']}")
    print(f"TABLES: {item['tables_count']}")

    if write_content:
        OUTPUT_DIR.mkdir(exist_ok=True)
        out_file = OUTPUT_DIR / f"item_{index}.md"
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(item['converted_content'])
        print(f"CONTENT_FILE: {out_file}")

def list_queue():
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = json.load(f)

    for i, item in enumerate(queue):
        print(f"{i}: {item['notion_id']} ({item['tables_count']} tables) - {item['filename'][:50]}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python get_queue_item.py <index> [--write] OR python get_queue_item.py --list")
        sys.exit(1)

    if sys.argv[1] == '--list':
        list_queue()
    else:
        idx = int(sys.argv[1])
        write = '--write' in sys.argv
        get_item(idx, write)
