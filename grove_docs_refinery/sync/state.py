"""
Enhanced sync state management.

Tracks document relationships between local files and Notion pages,
including timestamps for conflict detection.
"""

import os
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List, Any
from dataclasses import dataclass, asdict


@dataclass
class DocumentState:
    """State of a single synced document."""
    notion_id: str
    local_file: str
    title: str
    notion_last_edited: Optional[str] = None
    local_last_modified: Optional[str] = None
    last_synced: Optional[str] = None
    content_hash: Optional[str] = None
    sync_status: str = 'unknown'  # synced, modified_local, modified_notion, conflict, orphan

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'DocumentState':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class SyncState:
    """
    Enhanced sync state management with conflict detection.

    State is stored in a JSON file with the structure:
    {
        "last_sync": "ISO timestamp",
        "notion_workspace": "Documentation page ID",
        "categories": {
            "vision": "page_id",
            "software": "page_id",
            "blog": "page_id"
        },
        "documents": {
            "notion-uuid": { DocumentState fields }
        }
    }
    """

    DEFAULT_STATE_FILE = '.notion_sync_state.json'

    def __init__(self, state_file: Optional[str] = None, refined_dir: Optional[str] = None):
        self.state_file = Path(state_file or self.DEFAULT_STATE_FILE)
        self.refined_dir = Path(refined_dir or 'grove_docs_refinery/refined')
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load state from file or create default."""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        return {
            'last_sync': None,
            'notion_workspace': None,
            'categories': {},
            'documents': {}
        }

    def save(self):
        """Persist state to file."""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    # ========================================================================
    # Configuration
    # ========================================================================

    def set_workspace(self, page_id: str):
        """Set the root Documentation page ID."""
        self.state['notion_workspace'] = page_id
        self.save()

    def set_category(self, category: str, page_id: str):
        """Set the page ID for a document category."""
        self.state.setdefault('categories', {})[category] = page_id
        self.save()

    def get_category_id(self, category: str) -> Optional[str]:
        """Get the page ID for a category."""
        return self.state.get('categories', {}).get(category)

    # ========================================================================
    # Document State Management
    # ========================================================================

    def get_document(self, notion_id: str) -> Optional[DocumentState]:
        """Get document state by Notion ID."""
        doc_data = self.state.get('documents', {}).get(notion_id)
        if doc_data:
            return DocumentState.from_dict(doc_data)
        return None

    def get_document_by_file(self, filename: str) -> Optional[DocumentState]:
        """Get document state by local filename."""
        for notion_id, doc_data in self.state.get('documents', {}).items():
            if doc_data.get('local_file') == filename:
                return DocumentState.from_dict(doc_data)
        return None

    def get_document_by_title(self, title: str) -> Optional[DocumentState]:
        """Get document state by title."""
        for notion_id, doc_data in self.state.get('documents', {}).items():
            if doc_data.get('title') == title:
                return DocumentState.from_dict(doc_data)
        return None

    def set_document(self, doc: DocumentState):
        """Update or create document state."""
        self.state.setdefault('documents', {})[doc.notion_id] = doc.to_dict()
        self.save()

    def remove_document(self, notion_id: str):
        """Remove a document from state."""
        self.state.get('documents', {}).pop(notion_id, None)
        self.save()

    def list_documents(self) -> List[DocumentState]:
        """List all tracked documents."""
        return [
            DocumentState.from_dict(data)
            for data in self.state.get('documents', {}).values()
        ]

    # ========================================================================
    # Sync Operations
    # ========================================================================

    def update_last_sync(self):
        """Update global last sync timestamp."""
        self.state['last_sync'] = datetime.now().isoformat()
        self.save()

    def get_last_sync(self) -> Optional[str]:
        """Get global last sync timestamp."""
        return self.state.get('last_sync')

    def mark_synced(self, notion_id: str, local_file: str, title: str,
                    notion_edited: str, content_hash: str):
        """Mark a document as successfully synced."""
        local_path = self.refined_dir / local_file
        local_modified = None
        if local_path.exists():
            local_modified = datetime.fromtimestamp(
                local_path.stat().st_mtime
            ).isoformat()

        doc = DocumentState(
            notion_id=notion_id,
            local_file=local_file,
            title=title,
            notion_last_edited=notion_edited,
            local_last_modified=local_modified,
            last_synced=datetime.now().isoformat(),
            content_hash=content_hash,
            sync_status='synced'
        )
        self.set_document(doc)

    # ========================================================================
    # Conflict Detection
    # ========================================================================

    def compute_hash(self, content: str) -> str:
        """Compute MD5 hash of content for change detection."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def check_status(self, notion_id: str, notion_edited: str,
                     local_content: Optional[str] = None) -> str:
        """
        Check sync status for a document.

        Returns:
            'synced' - No changes
            'modified_notion' - Notion changed since last sync
            'modified_local' - Local changed since last sync
            'conflict' - Both changed
            'new' - Not tracked yet
        """
        doc = self.get_document(notion_id)

        if not doc:
            return 'new'

        notion_changed = False
        local_changed = False

        # Check Notion changes
        if doc.notion_last_edited and notion_edited:
            if notion_edited > doc.notion_last_edited:
                notion_changed = True

        # Check local changes
        if doc.local_file and local_content:
            current_hash = self.compute_hash(local_content)
            if current_hash != doc.content_hash:
                local_changed = True
        elif doc.local_file:
            # Check file modification time
            local_path = self.refined_dir / doc.local_file
            if local_path.exists():
                local_mtime = datetime.fromtimestamp(
                    local_path.stat().st_mtime
                ).isoformat()
                if doc.local_last_modified and local_mtime > doc.local_last_modified:
                    local_changed = True

        if notion_changed and local_changed:
            return 'conflict'
        if notion_changed:
            return 'modified_notion'
        if local_changed:
            return 'modified_local'

        return 'synced'

    def find_orphans(self) -> Dict[str, List]:
        """
        Find orphaned documents.

        Returns dict with:
            'local_orphans': Files without Notion page
            'notion_orphans': Tracked pages not in local
        """
        local_orphans = []
        notion_orphans = []

        # Check for tracked docs missing locally
        for doc in self.list_documents():
            local_path = self.refined_dir / doc.local_file
            if not local_path.exists():
                notion_orphans.append(doc)

        # Check for local files not tracked
        tracked_files = {doc.local_file for doc in self.list_documents()}
        if self.refined_dir.exists():
            for file in self.refined_dir.glob('*--FINAL.md'):
                if file.name not in tracked_files:
                    local_orphans.append(file.name)

        return {
            'local_orphans': local_orphans,
            'notion_orphans': notion_orphans
        }

    # ========================================================================
    # Reporting
    # ========================================================================

    def summary(self) -> Dict:
        """Get sync state summary."""
        docs = self.list_documents()
        status_counts = {}
        for doc in docs:
            status = doc.sync_status
            status_counts[status] = status_counts.get(status, 0) + 1

        return {
            'last_sync': self.get_last_sync(),
            'total_documents': len(docs),
            'status_counts': status_counts,
            'categories': list(self.state.get('categories', {}).keys())
        }

    def get_changes_since(self, since: str) -> Dict[str, List[DocumentState]]:
        """
        Get documents changed since a timestamp.

        Returns dict with 'modified_notion', 'modified_local', 'conflict' keys.
        """
        result = {
            'modified_notion': [],
            'modified_local': [],
            'conflict': []
        }

        for doc in self.list_documents():
            if doc.last_synced and doc.last_synced > since:
                if doc.sync_status in result:
                    result[doc.sync_status].append(doc)

        return result


# ============================================================================
# Utility Functions
# ============================================================================

def get_state(state_file: Optional[str] = None) -> SyncState:
    """Get a configured SyncState instance."""
    return SyncState(state_file)


def migrate_old_state(old_state_file: str, new_state: SyncState):
    """
    Migrate from old sync state format to new format.

    The old format stores documents by title rather than notion_id.
    """
    if not Path(old_state_file).exists():
        return

    with open(old_state_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)

    # Migrate documents
    for key, data in old_data.get('documents', {}).items():
        notion_id = data.get('notion_id') or key
        doc = DocumentState(
            notion_id=notion_id,
            local_file=data.get('local_file', ''),
            title=data.get('title', ''),
            notion_last_edited=data.get('notion_last_edited'),
            local_last_modified=data.get('local_last_modified'),
            last_synced=data.get('last_synced'),
            content_hash=data.get('content_hash'),
            sync_status='unknown'
        )
        new_state.set_document(doc)

    # Migrate categories if present
    for category, page_id in old_data.get('categories', {}).items():
        new_state.set_category(category, page_id)

    new_state.update_last_sync()
