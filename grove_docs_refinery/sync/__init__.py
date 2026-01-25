"""
Grove Docs Refinery - Sync Package

Bidirectional synchronization between local refined/ corpus and Notion Documentation.

Modules:
    api: Paginated Notion API client with child recursion
    converter: Markdown <-> Notion blocks conversion (with table support)
    state: Enhanced sync state management
    push: Upload workflow (local -> Notion)
    pull: Download workflow (Notion -> local)
"""

from .api import NotionAPI, get_api
from .state import SyncState, get_state
from .push import PushManager
from .converter import (
    blocks_to_markdown,
    markdown_to_blocks,
    notion_page_to_markdown,
    parse_frontmatter
)

__all__ = [
    'NotionAPI', 'get_api',
    'SyncState', 'get_state',
    'PushManager',
    'blocks_to_markdown', 'markdown_to_blocks',
    'notion_page_to_markdown', 'parse_frontmatter'
]
