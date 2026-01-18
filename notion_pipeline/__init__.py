"""
Notion Pipeline - Direct API workflows for sophisticated Notion automation.

Key advantages over MCP tools:
- Fresh reads (no cache issues)
- Property filtering on queries
- Batch operations with rate limiting
"""

from .client import NotionClient
from .config import Config

__all__ = ['NotionClient', 'Config']
