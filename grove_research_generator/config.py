#!/usr/bin/env python3
"""
Grove Research Generator - Configuration Module

Configuration for research document generation pipeline.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Known Notion database IDs and page IDs."""
    ATLAS_FEED = '3e8867d58aa5495780c2860dada8c993'
    ATLAS_FEED_DATA_SOURCE = '3baa11e8-6dac-437c-9d56-f10a6404b215'
    GROVE_SCATTERED_INVENTORY = '973d0191d4554f4f8aa218555ed01f67'
    DELETION_QUEUE = '2ec780a78eef8072b788f7307f98e843'
    GITHUB_STARS = 'efbdb5df36ed475eaf7ab28b25711c0c'
    THE_GROVE_PAGE = '2eb780a78eef80ae8fd1f4abcb53c053'
    SAMPLE_BLOG_POST = '2ec780a78eef81e8b5b6f1091210aee1'


class ResearchConfig:
    """Configuration manager for Grove Research Generator."""

    _instance: Optional['ResearchConfig'] = None
    _generator_root: Path = Path(__file__).parent

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load configuration from environment and defaults."""
        self.databases = DatabaseConfig()

    def _resolve_path(self, path_str: str) -> Path:
        """Resolve path relative to generator root."""
        path = Path(path_str)
        if path.is_absolute():
            return path
        return self._generator_root / path

    @property
    def prompts_dir(self) -> Path:
        return self._generator_root / "prompts"

    @property
    def logs_dir(self) -> Path:
        return self._generator_root / "logs"

    @property
    def leann_index_path(self) -> Optional[Path]:
        """Path to LEANN index for Grove knowledge."""
        leann_path = os.environ.get("GROVE_LEANN_INDEX")
        if leann_path:
            return Path(leann_path)
        # Default location
        default = Path(__file__).parent.parent / "leann-repo" / "grove-knowledge.leann"
        return default if default.exists() else None

    @property
    def research_engine_path(self) -> Path:
        return self.prompts_dir / "research_engine.md"

    @property
    def research_checkpoint_path(self) -> Path:
        return self.prompts_dir / "research_checkpoint.md"

    @property
    def citation_guide_path(self) -> Path:
        return self.prompts_dir / "citation_guide.md"

    @property
    def max_retries(self) -> int:
        """Max auto-retries before waiting for feedback."""
        return 1

    @property
    def voice_standards(self) -> list:
        """Grove voice standards for research documents."""
        return [
            "Strategic, not smug",
            "Concrete over abstract",
            "Honest about uncertainty",
            "8th-grade accessibility, graduate-level thinking",
            "Active voice, present tense",
        ]

    @property
    def research_patterns(self) -> list:
        """Patterns that trigger research document generation."""
        return [
            r'@atlas.*(?:research|write|blog|document|draft)',
            r'@atlas.*turn this into',
            r'@atlas.*create a.*(?:post|article|paper)',
        ]

    @property
    def completion_patterns(self) -> list:
        """Patterns that trigger completion/filing."""
        return [
            r'@atlas.*(?:complete|done|finished|ready|publish)',
            r'@atlas.*(?:file|ship) (?:this|it)',
        ]

    def ensure_directories(self):
        """Ensure all output directories exist."""
        for directory in [self.prompts_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)


def get_config() -> ResearchConfig:
    """Get the research generator configuration instance."""
    return ResearchConfig()
