"""
Draft Storage - Persist original drafts for diff analysis.

When Atlas posts a draft to Notion, we save the original here.
When the user marks it complete, we can diff against the edited version.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict, field


@dataclass
class StoredDraft:
    """A draft stored for later comparison."""
    page_id: str
    original_content: str
    topic: str
    format: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"  # pending, complete, analyzed
    edited_content: Optional[str] = None
    analyzed_at: Optional[str] = None
    learnings_extracted: int = 0


class DraftStorage:
    """Manages draft persistence for the learning loop."""

    def __init__(self, storage_path: Optional[Path] = None):
        if storage_path is None:
            storage_path = Path(__file__).parent / "drafts"
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.index_file = self.storage_path / "index.json"
        self._load_index()

    def _load_index(self) -> None:
        """Load the draft index from disk."""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self._index = json.load(f)
        else:
            self._index = {"drafts": {}}

    def _save_index(self) -> None:
        """Persist the draft index to disk."""
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self._index, f, indent=2)

    def store_draft(self, page_id: str, content: str, topic: str, format: str = "blog") -> StoredDraft:
        """
        Store an original draft when posting to Notion.

        Args:
            page_id: The Notion page ID
            content: The original generated content
            topic: The document topic
            format: Document format (blog, whitepaper, deep_dive)

        Returns:
            The stored draft object
        """
        draft = StoredDraft(
            page_id=page_id,
            original_content=content,
            topic=topic,
            format=format
        )

        # Save the full content to a separate file
        draft_file = self.storage_path / f"{page_id}.md"
        with open(draft_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Update index
        self._index["drafts"][page_id] = {
            "topic": topic,
            "format": format,
            "created_at": draft.created_at,
            "status": "pending"
        }
        self._save_index()

        return draft

    def get_draft(self, page_id: str) -> Optional[StoredDraft]:
        """
        Retrieve a stored draft by page ID.

        Args:
            page_id: The Notion page ID

        Returns:
            The stored draft, or None if not found
        """
        if page_id not in self._index["drafts"]:
            return None

        meta = self._index["drafts"][page_id]
        draft_file = self.storage_path / f"{page_id}.md"

        if not draft_file.exists():
            return None

        with open(draft_file, 'r', encoding='utf-8') as f:
            content = f.read()

        return StoredDraft(
            page_id=page_id,
            original_content=content,
            topic=meta.get("topic", ""),
            format=meta.get("format", "blog"),
            created_at=meta.get("created_at", ""),
            status=meta.get("status", "pending"),
            edited_content=meta.get("edited_content"),
            analyzed_at=meta.get("analyzed_at"),
            learnings_extracted=meta.get("learnings_extracted", 0)
        )

    def mark_complete(self, page_id: str, edited_content: str) -> Optional[StoredDraft]:
        """
        Mark a draft as complete and store the edited version.

        Args:
            page_id: The Notion page ID
            edited_content: The human-edited version

        Returns:
            The updated draft object
        """
        if page_id not in self._index["drafts"]:
            return None

        # Save edited version
        edited_file = self.storage_path / f"{page_id}_edited.md"
        with open(edited_file, 'w', encoding='utf-8') as f:
            f.write(edited_content)

        # Update index
        self._index["drafts"][page_id]["status"] = "complete"
        self._index["drafts"][page_id]["edited_content"] = str(edited_file)
        self._save_index()

        return self.get_draft(page_id)

    def mark_analyzed(self, page_id: str, learnings_count: int) -> None:
        """
        Mark a draft as analyzed after learning extraction.

        Args:
            page_id: The Notion page ID
            learnings_count: Number of learnings extracted
        """
        if page_id in self._index["drafts"]:
            self._index["drafts"][page_id]["status"] = "analyzed"
            self._index["drafts"][page_id]["analyzed_at"] = datetime.now().isoformat()
            self._index["drafts"][page_id]["learnings_extracted"] = learnings_count
            self._save_index()

    def get_pending_drafts(self) -> List[str]:
        """Get page IDs of drafts awaiting completion."""
        return [
            page_id for page_id, meta in self._index["drafts"].items()
            if meta.get("status") == "pending"
        ]

    def get_completed_unanalyzed(self) -> List[str]:
        """Get page IDs of completed drafts not yet analyzed."""
        return [
            page_id for page_id, meta in self._index["drafts"].items()
            if meta.get("status") == "complete"
        ]

    def get_edited_content(self, page_id: str) -> Optional[str]:
        """
        Get the edited content for a draft.

        Args:
            page_id: The Notion page ID

        Returns:
            The edited content, or None if not available
        """
        if page_id not in self._index["drafts"]:
            return None

        edited_file = self.storage_path / f"{page_id}_edited.md"
        if not edited_file.exists():
            return None

        with open(edited_file, 'r', encoding='utf-8') as f:
            return f.read()

    def cleanup_old_drafts(self, days: int = 30) -> int:
        """
        Remove drafts older than specified days that have been analyzed.

        Args:
            days: Age threshold in days

        Returns:
            Number of drafts cleaned up
        """
        from datetime import timedelta

        cutoff = datetime.now() - timedelta(days=days)
        cleaned = 0

        for page_id, meta in list(self._index["drafts"].items()):
            if meta.get("status") != "analyzed":
                continue

            created = datetime.fromisoformat(meta.get("created_at", ""))
            if created < cutoff:
                # Remove files
                draft_file = self.storage_path / f"{page_id}.md"
                edited_file = self.storage_path / f"{page_id}_edited.md"

                if draft_file.exists():
                    draft_file.unlink()
                if edited_file.exists():
                    edited_file.unlink()

                # Remove from index
                del self._index["drafts"][page_id]
                cleaned += 1

        if cleaned > 0:
            self._save_index()

        return cleaned
