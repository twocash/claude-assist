"""
Configuration for Notion Pipeline.
Loads from environment or .env file.
"""
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DatabaseConfig:
    """Known database IDs for quick reference."""
    # Grove inventory
    GROVE_SCATTERED_INVENTORY = '973d0191d4554f4f8aa218555ed01f67'
    GROVE_INVENTORY_DATA_SOURCE = '6dc99884-32c9-477f-9a23-ecff6cadb2f9'

    # Atlas feed
    ATLAS_FEED = '3e8867d58aa5495780c2860dada8c993'
    ATLAS_FEED_DATA_SOURCE = '3baa11e8-6dac-437c-9d56-f10a6404b215'

    # Deletion queue (page, not database)
    DELETION_QUEUE = '2ec780a78eef8072b788f7307f98e843'

    # GitHub stars
    GITHUB_STARS = 'efbdb5df36ed475eaf7ab28b25711c0c'


class Config:
    """Load configuration from environment."""

    def __init__(self):
        self._load_env_file()

        # Primary Notion API key
        self.notion_api_key = os.environ.get('NOTION_API_KEY') or \
                             os.environ.get('NOTION_ATLAS_API_KEY')

        if not self.notion_api_key:
            raise ValueError("NOTION_API_KEY not found in environment")

        # Database shortcuts
        self.databases = DatabaseConfig()

    def _load_env_file(self):
        """Load .env file if present."""
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ.setdefault(key.strip(), value.strip())
