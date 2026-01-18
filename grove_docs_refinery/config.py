#!/usr/bin/env python3
"""
Grove Docs Refinery - Configuration Module

Loads configuration from config.yaml and provides access to settings.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class RefineryConfig:
    """Configuration manager for Grove Docs Refinery."""

    _instance: Optional['RefineryConfig'] = None
    _config: Dict[str, Any] = {}
    _refinery_root: Path = Path(__file__).parent

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """Load configuration from config.yaml."""
        config_path = self._find_config_file()
        if config_path and config_path.exists():
            with open(config_path, 'r') as f:
                self._config = yaml.safe_load(f) or {}
        else:
            # Default configuration
            self._config = self._default_config()

    def _find_config_file(self) -> Optional[Path]:
        """Find config.yaml in refinery directory."""
        # Check refinery directory
        current = self._refinery_root / "config.yaml"
        if current.exists():
            return current

        # Check GROVE_REFINERY_CONFIG env var
        if os.environ.get("GROVE_REFINERY_CONFIG"):
            return Path(os.environ["GROVE_REFINERY_CONFIG"])

        return None

    def _resolve_path(self, path_str: str) -> Path:
        """Resolve path relative to refinery root."""
        path = Path(path_str)
        if path.is_absolute():
            return path
        return self._refinery_root / path

    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        refinery_root = self._refinery_root
        return {
            "refinery": {
                "backend": "claude",  # "claude" or "rules"
                "input_dir": str(refinery_root / "input"),
                "output_dirs": {
                    "drafts": str(refinery_root / "drafts"),
                    "reviews": str(refinery_root / "reviews"),
                    "refined": str(refinery_root / "refined"),
                },
                "logs": str(refinery_root / "logs"),
                "batch_size": 5,
                "max_revisions": 2,
            },
            "editor": {
                "model": "sonnet",
                "checkpoint_path": str(refinery_root / "editorial-checkpoint.md"),
                "engine_path": str(refinery_root / "editorial-engine.md"),
            },
            "reviewer": {
                "model": "sonnet",
                "checkpoint_path": str(refinery_root / "editorial-checkpoint.md"),
                "engine_path": str(refinery_root / "editorial-engine.md"),
            },
            "standards": {
                "voice": [
                    "Strategic, not smug",
                    "Concrete over abstract",
                    "Honest about uncertainty",
                    "8th-grade accessibility, graduate-level thinking",
                    "Active voice, present tense",
                ],
                "terminology": {
                    "Exploration architecture": ["AI platform", "decentralized AI"],
                    "Agents": ["bots", "AI assistants"],
                    "The Observer": ["user"],
                    "Credits": ["tokens"],
                    "Trellis Architecture": [],
                    "Grove": [],
                    "Foundation": [],
                    "Terminal": [],
                },
                "avoid": [
                    "revolutionary",
                    "paradigm shift",
                    "Web3",
                    "democratize",
                    "might",
                    "could potentially",
                    "it's possible that",
                    "It's important to note that",
                    "In order to",
                    "tokenomics",
                    "network effects",
                    "moats",
                    "the future of AI",
                    "unprecedented capabilities",
                ],
            },
        }

    def get(self, *keys: str, default: Any = None) -> Any:
        """Get a config value by key path."""
        value = self._config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    @property
    def input_dir(self) -> Path:
        return self._resolve_path(self.get("refinery", "input_dir", default="input"))

    @property
    def drafts_dir(self) -> Path:
        return self._resolve_path(self.get("refinery", "output_dirs", "drafts", default="drafts"))

    @property
    def reviews_dir(self) -> Path:
        return self._resolve_path(self.get("refinery", "output_dirs", "reviews", default="reviews"))

    @property
    def refined_dir(self) -> Path:
        return self._resolve_path(self.get("refinery", "output_dirs", "refined", default="refined"))

    @property
    def logs_dir(self) -> Path:
        return self._resolve_path(self.get("refinery", "logs", default="logs"))

    @property
    def batch_size(self) -> int:
        return self.get("refinery", "batch_size", default=5)

    @property
    def max_revisions(self) -> int:
        return self.get("refinery", "max_revisions", default=2)

    @property
    def backend(self) -> str:
        """Backend to use: 'claude' or 'rules'."""
        return self.get("refinery", "backend", default="claude")

    @property
    def checkpoint_path(self) -> Path:
        return self._resolve_path(self.get("editor", "checkpoint_path", default="editorial-checkpoint.md"))

    @property
    def engine_path(self) -> Path:
        return self._resolve_path(self.get("editor", "engine_path", default="editorial-engine.md"))

    @property
    def terms_to_avoid(self) -> list:
        return self.get("standards", "avoid", default=[])

    @property
    def terminology_mapping(self) -> dict:
        return self.get("standards", "terminology", default={})

    @property
    def voice_standards(self) -> list:
        return self.get("standards", "voice", default=[])

    def ensure_directories(self):
        """Ensure all output directories exist."""
        for directory in [
            self.input_dir,
            self.drafts_dir,
            self.reviews_dir,
            self.refined_dir,
            self.logs_dir,
        ]:
            directory.mkdir(parents=True, exist_ok=True)


def get_config() -> RefineryConfig:
    """Get the refinery configuration instance."""
    return RefineryConfig()
