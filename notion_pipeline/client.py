"""
Notion API client with direct REST calls.
Bypasses MCP cache - always fresh reads.
"""
import time
from typing import Any, Dict, List, Optional
import requests

from .config import Config


class NotionClient:
    """
    Direct Notion API client.

    Key features:
    - Fresh reads (no caching)
    - Property filtering on queries
    - Built-in rate limiting
    """

    BASE_URL = 'https://api.notion.com/v1'

    def __init__(self, api_key: Optional[str] = None):
        config = Config()
        self.api_key = api_key or config.notion_api_key
        self.databases = config.databases

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }

        self._rate_limit_delay = 0.35  # seconds between requests
        self._last_request_time = 0

    def _rate_limit(self):
        """Respect Notion rate limits."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._rate_limit_delay:
            time.sleep(self._rate_limit_delay - elapsed)
        self._last_request_time = time.time()

    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make rate-limited request."""
        self._rate_limit()
        url = f'{self.BASE_URL}{endpoint}'
        response = requests.request(method, url, headers=self.headers, **kwargs)
        return response

    # ========== Database Operations ==========

    def query_database(
        self,
        database_id: str,
        filter: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        page_size: int = 100
    ) -> List[Dict]:
        """
        Query database with optional filtering.

        Example filter for checkbox:
            {"property": "Delete", "checkbox": {"equals": True}}

        Example filter for select:
            {"property": "Status", "select": {"equals": "Active"}}
        """
        endpoint = f'/databases/{database_id}/query'
        all_results = []
        start_cursor = None

        while True:
            payload = {'page_size': page_size}
            if filter:
                payload['filter'] = filter
            if sorts:
                payload['sorts'] = sorts
            if start_cursor:
                payload['start_cursor'] = start_cursor

            response = self._request('POST', endpoint, json=payload)

            if response.status_code != 200:
                raise Exception(f"Query failed: {response.status_code} - {response.text}")

            data = response.json()
            all_results.extend(data.get('results', []))

            if data.get('has_more'):
                start_cursor = data.get('next_cursor')
            else:
                break

        return all_results

    def get_database_schema(self, database_id: str) -> Dict:
        """Get database schema (properties)."""
        response = self._request('GET', f'/databases/{database_id}')

        if response.status_code != 200:
            raise Exception(f"Get database failed: {response.status_code} - {response.text}")

        return response.json()

    # ========== Page Operations ==========

    def get_page(self, page_id: str) -> Dict:
        """Get page by ID."""
        response = self._request('GET', f'/pages/{page_id}')

        if response.status_code != 200:
            raise Exception(f"Get page failed: {response.status_code} - {response.text}")

        return response.json()

    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """
        Update page properties.

        Example:
            {"Delete": {"checkbox": True}}
            {"Status": {"select": {"name": "Archived"}}}
        """
        response = self._request('PATCH', f'/pages/{page_id}', json={'properties': properties})

        if response.status_code not in [200, 201]:
            raise Exception(f"Update failed: {response.status_code} - {response.text}")

        return response.json()

    def move_page(self, page_id: str, new_parent_id: str, parent_type: str = 'page_id') -> Dict:
        """
        Move page to new parent.

        parent_type: 'page_id', 'database_id', or 'workspace'
        """
        if parent_type == 'workspace':
            parent = {'type': 'workspace', 'workspace': True}
        else:
            parent = {'type': parent_type, parent_type: new_parent_id}

        response = self._request('PATCH', f'/pages/{page_id}', json={'parent': parent})

        if response.status_code not in [200, 201]:
            raise Exception(f"Move failed: {response.status_code} - {response.text}")

        return response.json()

    def archive_page(self, page_id: str) -> Dict:
        """Archive (soft delete) a page."""
        response = self._request('PATCH', f'/pages/{page_id}', json={'archived': True})

        if response.status_code not in [200, 201]:
            raise Exception(f"Archive failed: {response.status_code} - {response.text}")

        return response.json()

    # ========== Search Operations ==========

    def search(
        self,
        query: str,
        filter_type: Optional[str] = None,  # 'page' or 'database'
        page_size: int = 20
    ) -> List[Dict]:
        """Search across workspace."""
        payload = {'query': query, 'page_size': page_size}
        if filter_type:
            payload['filter'] = {'property': 'object', 'value': filter_type}

        response = self._request('POST', '/search', json=payload)

        if response.status_code != 200:
            raise Exception(f"Search failed: {response.status_code} - {response.text}")

        return response.json().get('results', [])

    # ========== Utility Methods ==========

    def extract_title(self, page: Dict) -> str:
        """Extract title from page properties."""
        props = page.get('properties', {})
        for prop_name, prop_value in props.items():
            if prop_value.get('type') == 'title':
                title_array = prop_value.get('title', [])
                if title_array:
                    return title_array[0].get('plain_text', '')
        return ''

    def extract_checkbox(self, page: Dict, property_name: str) -> bool:
        """Extract checkbox value from page."""
        props = page.get('properties', {})
        prop = props.get(property_name, {})
        return prop.get('checkbox', False)

    def extract_select(self, page: Dict, property_name: str) -> Optional[str]:
        """Extract select value from page."""
        props = page.get('properties', {})
        prop = props.get(property_name, {})
        select = prop.get('select')
        return select.get('name') if select else None
