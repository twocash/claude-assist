#!/usr/bin/env python3
"""
Grove Docs Refinery - Checkpoint Manager

Loads and manages the editorial checkpoint (dynamic state).
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime


class EditorialCheckpoint:
    """Manages the Grove Editorial Checkpoint - dynamic state for current terminology/positioning."""

    def __init__(self, checkpoint_path: Optional[Path] = None):
        self.checkpoint_path = checkpoint_path
        self._content: str = ""
        self._data: Dict[str, Any] = {}
        self._loaded: bool = False

    def load(self, path: Optional[Path] = None) -> 'EditorialCheckpoint':
        """Load checkpoint from file."""
        if path:
            self.checkpoint_path = path

        if self.checkpoint_path and self.checkpoint_path.exists():
            self._content = self.checkpoint_path.read_text()
            self._parse()
            self._loaded = True

        return self

    def _parse(self):
        """Parse checkpoint content into structured data."""
        self._data = {
            "strategic_positioning": "",
            "terminology": {},
            "claims": [],
            "terminology_mapping": {},
            "current_terms": [],
            "legacy_terms": [],
        }

        # Extract strategic positioning (between ### The Core Frame and ### Key Strategic Claims)
        core_frame_match = re.search(
            r"### The Core Frame\s*\n\s*(.+?)(?=\n###|\Z)",
            self._content,
            re.DOTALL,
        )
        if core_frame_match:
            self._data["strategic_positioning"] = core_frame_match.group(1).strip()

        # Extract thesis
        thesis_match = re.search(
            r"### The Thesis \(One Paragraph\)\s*\n\s*(.+?)(?=\n###|\Z)",
            self._content,
            re.DOTALL,
        )
        if thesis_match:
            self._data["thesis"] = thesis_match.group(1).strip()

        # Parse terminology mapping table
        mapping_section = re.search(
            r"### Current Terms \(Use These\).*?\n\n(.*?)(?=\n###|\Z)",
            self._content,
            re.DOTALL,
        )
        if mapping_section:
            table_content = mapping_section.group(1)
            # Parse markdown table
            rows = re.findall(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", table_content)
            for row in rows:
                term = row[0].strip()
                definition = row[1].strip()
                self._data["terminology"][term] = definition
                self._data["current_terms"].append(term)

        # Parse legacy terms
        legacy_section = re.search(
            r"### Legacy Terms \(Avoid\)\s*\n\n(.*?)(?=\n###|\Z)",
            self._content,
            re.DOTALL,
        )
        if legacy_section:
            table_content = legacy_section.group(1)
            rows = re.findall(r"\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", table_content)
            for row in rows:
                legacy = row[0].strip()
                current = row[1].strip()
                self._data["terminology_mapping"][legacy] = current
                self._data["legacy_terms"].append(legacy)

        # Extract strategic claims
        claims_section = re.search(
            r"### Key Strategic Claims\s*\n\n(.*?)(?=\n###|\Z)",
            self._content,
            re.DOTALL,
        )
        if claims_section:
            claims_content = claims_section.group(1)
            self._data["claims"] = [
                line.strip().lstrip("123. ")
                for line in claims_content.split("\n")
                if line.strip() and line[0].isdigit()
            ]

    def is_loaded(self) -> bool:
        """Check if checkpoint is loaded."""
        return self._loaded

    @property
    def strategic_positioning(self) -> str:
        """Get core strategic positioning."""
        return self._data.get("strategic_positioning", "")

    @property
    def thesis(self) -> str:
        """Get the Grove thesis."""
        return self._data.get("thesis", "")

    @property
    def claims(self) -> List[str]:
        """Get key strategic claims."""
        return self._data.get("claims", [])

    @property
    def current_terms(self) -> Dict[str, str]:
        """Get current terminology mapping."""
        return self._data.get("terminology", {})

    @property
    def terminology_mapping(self) -> Dict[str, str]:
        """Get legacy to current term mappings."""
        return self._data.get("terminology_mapping", {})

    @property
    def last_updated(self) -> Optional[datetime]:
        """Get last update timestamp."""
        match = re.search(
            r"Last Updated:\s*(.+?)[\n\*]",
            self._content,
        )
        if match:
            try:
                return datetime.strptime(match.group(1).strip(), "%B %Y")
            except ValueError:
                pass
        return None

    def validate_term(self, term: str) -> Tuple[bool, Optional[str]]:
        """
        Validate a term against the checkpoint.

        Returns: (is_valid, suggestion_if_not)
        """
        term_lower = term.lower()

        # Check if it's a current term
        for current in self._data.get("current_terms", {}):
            if current.lower() == term_lower:
                return True, None

        # Check if it's a legacy term with a suggestion
        for legacy, current in self._data.get("terminology_mapping", {}).items():
            if legacy.lower() == term_lower:
                return False, current

        return True, None  # Unknown terms are assumed valid

    def find_issues(self, content: str) -> List[Dict[str, Any]]:
        """
        Find terminology and positioning issues in content.

        Returns list of issues found.
        """
        issues = []

        # Check for legacy terms
        for legacy, current in self.terminology_mapping.items():
            if legacy.lower() in content.lower():
                issues.append({
                    "type": "legacy_term",
                    "term": legacy,
                    "suggestion": current,
                    "context": self._find_context(content, legacy),
                })

        # Check for prohibited language (from original content)
        prohibited = [
            "revolutionary", "paradigm shift", "Web3", "democratize",
            "might", "could potentially", "tokenomics", "network effects",
            "moats", "the future of AI", "unprecedented capabilities",
        ]
        for term in prohibited:
            if term.lower() in content.lower():
                issues.append({
                    "type": "prohibited",
                    "term": term,
                    "suggestion": "Remove or rephrase",
                    "context": self._find_context(content, term),
                })

        return issues

    def _find_context(self, content: str, term: str, window: int = 50) -> str:
        """Find context around a term."""
        idx = content.lower().find(term.lower())
        if idx == -1:
            return ""
        start = max(0, idx - window)
        end = min(len(content), idx + len(term) + window)
        return content[start:end]

    def check_positioning(self, content: str) -> Dict[str, Any]:
        """Check content against current strategic positioning."""
        result = {
            "aligned": True,
            "issues": [],
            "suggestions": [],
        }

        # Check for presence of key concepts from thesis
        thesis_concepts = [
            "exploration",
            "distributed",
            "local",
            "agents",
            "discovery",
        ]

        content_lower = content.lower()
        missing = []
        for concept in thesis_concepts:
            if concept not in content_lower:
                missing.append(concept)

        if missing:
            result["issues"].append({
                "type": "missing_concept",
                "missing": missing,
                "note": "Consider including exploration/distributed concepts",
            })

        return result

    def get_validation_checklist(self) -> Dict[str, Any]:
        """Get the standard validation checklist from checkpoint."""
        return {
            "terminology_current": True,
            "positioning_aligned": True,
            "technical_accuracy": True,
            "voice_consistent": True,
            "no_prohibited_language": True,
            "appropriate_length": True,
        }


def load_checkpoint(path: Optional[Path] = None) -> EditorialCheckpoint:
    """Load an editorial checkpoint."""
    checkpoint = EditorialCheckpoint(path)
    checkpoint.load()
    return checkpoint
