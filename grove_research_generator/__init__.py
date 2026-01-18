"""
Grove Research Generator

Automated research document pipeline triggered by @atlas mentions in Notion.
Generates polished research documents with Chicago-style citations,
informed by LEANN RAG context.
"""

from .config import get_config, ResearchConfig, DatabaseConfig
from .orchestrator import ResearchOrchestrator

__all__ = [
    'get_config',
    'ResearchConfig',
    'DatabaseConfig',
    'ResearchOrchestrator',
]
