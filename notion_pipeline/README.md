# Notion Pipeline

Direct Python API client for sophisticated Notion workflows. Bypasses MCP cache issues and enables property-based filtering.

## Why This Exists

The MCP Notion tools have limitations:
1. **Cache issues** - MCP returns stale data, even after updates
2. **No property filtering** - Can't query "checkbox = true" directly
3. **OAuth auth** - Different from Python API key auth

This pipeline uses direct REST API calls for:
- Fresh reads every time (no cache)
- Property-based database queries
- Batch operations with rate limiting

## Setup

### 1. Get a Notion API Key

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration (or use existing)
3. Copy the **Internal Integration Secret** (starts with `ntn_` or `secret_`)

### 2. Share Databases with Integration

For each database you want to access:
1. Open the database in Notion
2. Click **Share** (top right)
3. Search for your integration name
4. Click **Invite**

**Important:** The integration needs explicit access to each database. If you get 404 errors, the database isn't shared.

### 3. Configure Environment

Create `.env` in the project root:

```bash
NOTION_API_KEY=ntn_your_key_here
```

Or set the environment variable directly:

```bash
export NOTION_API_KEY=ntn_your_key_here
```

## Usage

### CLI Commands

```bash
# Test connection
python -m notion_pipeline test

# Find items marked for deletion (dry run)
python -m notion_pipeline deletion-queue --dry-run

# Actually move items to deletion queue
python -m notion_pipeline deletion-queue

# Generate triage report for a database
python -m notion_pipeline triage <database_id>
```

### Python API

```python
from notion_pipeline import NotionClient
from notion_pipeline.workflows import DeletionQueueWorkflow

# Create client
client = NotionClient()

# Query with filters
items = client.query_database(
    database_id='973d0191d4554f4f8aa218555ed01f67',
    filter={'property': 'Delete', 'checkbox': {'equals': True}}
)

# Run deletion workflow
workflow = DeletionQueueWorkflow(client)
workflow.run(
    database_id='973d0191d4554f4f8aa218555ed01f67',
    queue_page_id='2ec780a78eef8072b788f7307f98e843'
)
```

## Known Database IDs

```python
# Grove inventory
GROVE_SCATTERED_INVENTORY = '973d0191d4554f4f8aa218555ed01f67'

# Atlas feed
ATLAS_FEED = '3e8867d58aa5495780c2860dada8c993'

# Deletion queue (page)
DELETION_QUEUE = '2ec780a78eef8072b788f7307f98e843'

# GitHub stars
GITHUB_STARS = 'efbdb5df36ed475eaf7ab28b25711c0c'
```

## Filter Examples

```python
# Checkbox equals true
{'property': 'Delete', 'checkbox': {'equals': True}}

# Select equals value
{'property': 'Status', 'select': {'equals': 'Active'}}

# Text contains
{'property': 'Title', 'rich_text': {'contains': 'Grove'}}

# Date after
{'property': 'Created', 'date': {'after': '2024-01-01'}}

# Compound filter (AND)
{
    'and': [
        {'property': 'Delete', 'checkbox': {'equals': True}},
        {'property': 'Status', 'select': {'equals': 'Ready'}}
    ]
}
```

## Troubleshooting

### 404 Errors
The database isn't shared with your integration. Go to the database in Notion, click Share, and invite your integration.

### 401 Errors
Invalid API key. Check your `.env` file and ensure the key starts with `ntn_` or `secret_`.

### Rate Limiting
The client automatically rate-limits to ~3 requests/second. For bulk operations, this is handled internally.

## Architecture

```
notion_pipeline/
├── __init__.py          # Package exports
├── __main__.py          # CLI entry point
├── cli.py               # Command-line interface
├── client.py            # Notion API client
├── config.py            # Configuration loader
└── workflows/
    ├── deletion_queue.py  # Move to deletion queue
    └── triage.py          # Generate triage reports
```
