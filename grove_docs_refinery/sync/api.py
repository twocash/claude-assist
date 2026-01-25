"""
Notion API client with pagination and child block recursion.

Fixes the truncation bug in the original sync scripts by:
1. Handling pagination (has_more/next_cursor)
2. Recursively fetching child blocks (toggles, columns, etc.)
"""

import os
import time
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

load_dotenv()


class NotionAPI:
    """Paginated Notion API client with child recursion."""

    BASE_URL = 'https://api.notion.com/v1'
    MAX_DEPTH = 3  # Max recursion depth for nested blocks
    PAGE_SIZE = 100  # Notion API max
    RATE_LIMIT_DELAY = 0.35  # Seconds between requests to avoid rate limits

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('NOTION_API_KEY')
        if not self.api_key:
            raise ValueError("NOTION_API_KEY not found in environment")

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Notion-Version': '2022-06-28',
            'Content-Type': 'application/json'
        }
        self._last_request_time = 0

    def _rate_limit(self):
        """Ensure we don't exceed Notion's rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)
        self._last_request_time = time.time()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make a rate-limited request to the Notion API."""
        self._rate_limit()
        url = f'{self.BASE_URL}/{endpoint}'
        response = requests.request(method, url, headers=self.headers, **kwargs)

        if response.status_code == 429:
            # Rate limited - wait and retry
            retry_after = int(response.headers.get('Retry-After', 1))
            time.sleep(retry_after)
            return self._request(method, endpoint, **kwargs)

        response.raise_for_status()
        return response.json()

    def get_page(self, page_id: str) -> Dict:
        """Get a page's metadata."""
        return self._request('GET', f'pages/{page_id}')

    def get_database(self, database_id: str) -> Dict:
        """Get a database's metadata."""
        return self._request('GET', f'databases/{database_id}')

    def query_database(self, database_id: str, filter_: Optional[Dict] = None,
                       sorts: Optional[List] = None) -> List[Dict]:
        """Query a database with pagination."""
        all_results = []
        cursor = None

        while True:
            body = {'page_size': self.PAGE_SIZE}
            if cursor:
                body['start_cursor'] = cursor
            if filter_:
                body['filter'] = filter_
            if sorts:
                body['sorts'] = sorts

            data = self._request('POST', f'databases/{database_id}/query', json=body)
            all_results.extend(data.get('results', []))

            if not data.get('has_more'):
                break
            cursor = data.get('next_cursor')

        return all_results

    def get_block_children(self, block_id: str, depth: int = 0) -> List[Dict]:
        """
        Fetch all child blocks with pagination and recursion.

        This is the core fix for the truncated content bug.

        Args:
            block_id: The parent block (or page) ID
            depth: Current recursion depth (stops at MAX_DEPTH)

        Returns:
            List of blocks with nested '_children' for blocks that have children
        """
        all_blocks = []
        cursor = None

        while True:
            params = {'page_size': self.PAGE_SIZE}
            if cursor:
                params['start_cursor'] = cursor

            data = self._request('GET', f'blocks/{block_id}/children', params=params)

            for block in data.get('results', []):
                # Recursively fetch children if they exist and we haven't hit max depth
                if block.get('has_children') and depth < self.MAX_DEPTH:
                    block['_children'] = self.get_block_children(block['id'], depth + 1)
                all_blocks.append(block)

            if not data.get('has_more'):
                break
            cursor = data.get('next_cursor')

        return all_blocks

    def get_page_content(self, page_id: str) -> Dict:
        """
        Get a page's full content including metadata and all blocks.

        Returns:
            Dict with 'page' (metadata) and 'blocks' (full content with children)
        """
        page = self.get_page(page_id)
        blocks = self.get_block_children(page_id)

        return {
            'page': page,
            'blocks': blocks,
            'block_count': self._count_blocks(blocks)
        }

    def _count_blocks(self, blocks: List[Dict]) -> int:
        """Count total blocks including nested children."""
        count = len(blocks)
        for block in blocks:
            if '_children' in block:
                count += self._count_blocks(block['_children'])
        return count

    def create_page(self, parent: Dict, properties: Dict,
                    children: Optional[List[Dict]] = None) -> Dict:
        """Create a new page."""
        body = {
            'parent': parent,
            'properties': properties
        }
        if children:
            # Notion limits to 100 children per request
            body['children'] = children[:100]

        page = self._request('POST', 'pages', json=body)

        # If more than 100 children, append the rest
        if children and len(children) > 100:
            self.append_blocks(page['id'], children[100:])

        return page

    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """Update a page's properties."""
        return self._request('PATCH', f'pages/{page_id}', json={'properties': properties})

    def append_blocks(self, block_id: str, children: List[Dict]) -> Dict:
        """Append blocks to a page or block, handling the 100-block limit."""
        results = []

        # Batch in groups of 100
        for i in range(0, len(children), 100):
            batch = children[i:i + 100]
            result = self._request('PATCH', f'blocks/{block_id}/children',
                                   json={'children': batch})
            results.extend(result.get('results', []))

        return {'results': results}

    def delete_block(self, block_id: str) -> Optional[Dict]:
        """Archive/delete a block. Returns None if block doesn't exist."""
        try:
            return self._request('DELETE', f'blocks/{block_id}')
        except Exception:
            # Block may already be deleted or archived
            return None

    def clear_page_content(self, page_id: str) -> int:
        """
        Delete all blocks from a page.

        Used when updating a page's content completely.

        Returns:
            Number of blocks deleted
        """
        try:
            blocks = self.get_block_children(page_id, depth=0)  # Only top-level
        except Exception:
            return 0

        deleted = 0
        for block in blocks:
            if self.delete_block(block['id']) is not None:
                deleted += 1
        return deleted

    def get_child_pages(self, page_id: str) -> List[Dict]:
        """Get all child pages under a parent page."""
        blocks = self.get_block_children(page_id, depth=0)
        return [b for b in blocks if b['type'] == 'child_page']

    def search(self, query: str, filter_type: Optional[str] = None) -> List[Dict]:
        """
        Search for pages or databases.

        Args:
            query: Search query
            filter_type: 'page' or 'database' (optional)
        """
        all_results = []
        cursor = None

        while True:
            body = {'query': query, 'page_size': self.PAGE_SIZE}
            if cursor:
                body['start_cursor'] = cursor
            if filter_type:
                body['filter'] = {'property': 'object', 'value': filter_type}

            data = self._request('POST', 'search', json=body)
            all_results.extend(data.get('results', []))

            if not data.get('has_more'):
                break
            cursor = data.get('next_cursor')

        return all_results

    def find_page_by_title(self, title: str, parent_id: Optional[str] = None) -> Optional[Dict]:
        """
        Find a page by exact title match.

        Args:
            title: Page title to find
            parent_id: Optional parent page ID to narrow search

        Returns:
            Page object if found, None otherwise
        """
        results = self.search(title, filter_type='page')

        for page in results:
            # Extract title from properties
            props = page.get('properties', {})
            title_prop = props.get('title') or props.get('Name') or props.get('name')

            if title_prop:
                if title_prop.get('type') == 'title':
                    page_title = ''.join(
                        t.get('plain_text', '')
                        for t in title_prop.get('title', [])
                    )
                    if page_title.strip() == title.strip():
                        # If parent_id specified, verify parent
                        if parent_id:
                            parent = page.get('parent', {})
                            if parent.get('page_id') == parent_id:
                                return page
                        else:
                            return page

        return None


# Convenience function
def get_api() -> NotionAPI:
    """Get a configured NotionAPI instance."""
    return NotionAPI()
