"""
Pull (download) workflow: Notion -> Local

Downloads documents from Grove Corpus database to local refined/ folder.
Handles proper naming using document date (not sync date).

Safety features:
- Backup before overwrite (.bak files)
- Git status check warns about uncommitted changes
- Conflict detection when both local and Notion changed
- Dry-run mode to preview changes without writing
"""

import os
import re
import shutil
import subprocess
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from .api import NotionAPI, get_api
from .converter import block_to_markdown, blocks_to_markdown
from .state import SyncState, get_state


class PullManager:
    """
    Manages pull from Notion to local.

    Safety features:
    - Creates .bak backup before overwriting any file
    - Warns if git has uncommitted changes
    - Detects conflicts (both sides changed since last sync)
    - Dry-run mode for previewing changes
    """

    # Type codes for filename
    TYPE_CODES = {
        'vision': 'v',
        'software': 's',
        'blog': 'b',
    }

    def __init__(self, api: Optional[NotionAPI] = None,
                 state: Optional[SyncState] = None,
                 refined_dir: Optional[str] = None):
        self.api = api or get_api()
        self.state = state or get_state()
        self.refined_dir = Path(refined_dir or 'grove_docs_refinery/refined')
        self.refined_dir.mkdir(parents=True, exist_ok=True)
        self._git_warned = False  # Only warn once per session

    def _check_git_status(self) -> bool:
        """
        Check if there are uncommitted changes in the refined directory.
        Returns True if clean, False if dirty. Only warns once per session.
        """
        if self._git_warned:
            return True  # Already warned, don't spam

        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain', str(self.refined_dir)],
                capture_output=True,
                text=True,
                cwd=self.refined_dir.parent
            )
            if result.stdout.strip():
                print("[!]  WARNING: Uncommitted changes in refined/ directory!")
                print("   Consider committing before pulling to preserve your work.")
                self._git_warned = True
                return False
        except Exception:
            pass  # Git not available, skip check
        return True

    def _create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of an existing file before overwriting.
        Returns the backup path, or None if no backup was needed.
        """
        if not file_path.exists():
            return None

        # Create backup with timestamp to avoid overwriting previous backups
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = file_path.with_suffix(f'.{timestamp}.bak')

        shutil.copy2(file_path, backup_path)
        print(f"  [BACKUP] Created: {backup_path.name}")
        return backup_path

    def _check_conflict(self, page_id: str, notion_last_edited: str,
                        file_path: Path) -> Tuple[str, Optional[str]]:
        """
        Check sync status and detect conflicts.

        Returns:
            Tuple of (status, reason) where status is one of:
            - 'synced': No changes needed
            - 'notion_newer': Notion changed, safe to pull
            - 'local_newer': Local changed, should push instead
            - 'conflict': Both changed, needs manual resolution
            - 'new': New document, safe to create
        """
        status = self.state.check_status(page_id, notion_last_edited)

        # Map state.py statuses to our more descriptive statuses
        if status == 'synced':
            return ('synced', 'No changes since last sync')
        elif status == 'modified_notion':
            return ('notion_newer', 'Notion has updates')
        elif status == 'modified_local':
            return ('local_newer', 'Local file modified - consider pushing instead')
        elif status == 'conflict':
            return ('conflict', 'CONFLICT: Both local and Notion changed since last sync')
        elif status == 'new':
            return ('new', 'New document')
        else:
            return ('new', 'Unknown status, treating as new')

    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug."""
        # Lowercase and replace spaces with hyphens
        slug = text.lower().strip()
        # Remove special characters except hyphens
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        # Replace whitespace with hyphens
        slug = re.sub(r'[\s_]+', '-', slug)
        # Remove multiple consecutive hyphens
        slug = re.sub(r'-+', '-', slug)
        # Trim hyphens from ends
        slug = slug.strip('-')
        return slug

    def _generate_filename(self, properties: Dict) -> str:
        """
        Generate canonical filename from document properties.

        Format: YYMMDD-t-domain-title-slug.md--FINAL.md

        Where:
        - YYMMDD = document date (from Date property)
        - t = type code (v=vision, s=software, b=blog)
        - domain = from Domain property
        - title-slug = slugified title
        """
        # Get date (use document date, default to today)
        date_str = properties.get('date:Date:start', '')
        if date_str:
            try:
                date_obj = datetime.fromisoformat(date_str)
                date_prefix = date_obj.strftime('%y%m%d')
            except ValueError:
                date_prefix = datetime.now().strftime('%y%m%d')
        else:
            date_prefix = datetime.now().strftime('%y%m%d')

        # Get type code
        doc_type = properties.get('Type', 'vision').lower()
        type_code = self.TYPE_CODES.get(doc_type, 'v')

        # Get domain
        domain = properties.get('Domain', 'vision').lower()

        # Get title slug
        title = properties.get('Title', 'untitled')
        title_slug = self._slugify(title)

        # Combine
        return f"{date_prefix}-{type_code}-{domain}-{title_slug}.md--FINAL.md"

    def _blocks_to_markdown(self, blocks: List[Dict]) -> str:
        """Convert Notion blocks to markdown with semantic spacing.

        Rules:
        - Blank line before headings (always)
        - Blank line after headings (always)
        - No blank lines between consecutive paragraphs
        - Blank line before/after code blocks, tables, quotes
        """
        result = []
        prev_type = None

        # Block types that need blank line before them
        NEEDS_BLANK_BEFORE = {'heading_1', 'heading_2', 'heading_3',
                              'code', 'table', 'quote', 'callout', 'divider'}
        # Block types that need blank line after them
        NEEDS_BLANK_AFTER = {'heading_1', 'heading_2', 'heading_3',
                             'code', 'table', 'quote', 'callout'}

        for i, block in enumerate(blocks):
            block_type = block.get('type', 'paragraph')
            md = block_to_markdown(block)

            if not md or not md.strip():
                continue

            # Add blank line before if needed
            if result:  # Not first block
                needs_blank = (
                    block_type in NEEDS_BLANK_BEFORE or
                    prev_type in NEEDS_BLANK_AFTER
                )
                if needs_blank:
                    result.append('\n')

            # Add the content (strip trailing newline, we'll manage spacing)
            result.append(md.rstrip('\n'))
            result.append('\n')

            prev_type = block_type

        return ''.join(result)

    def _create_frontmatter(self, page: Dict, properties: Dict,
                            local_filename: str) -> str:
        """Create YAML frontmatter for the document."""
        notion_id = page.get('id', '')
        notion_url = page.get('url', '')

        frontmatter = {
            'title': properties.get('Title', 'Untitled'),
            'author': properties.get('Author', ''),
            'date': properties.get('date:Date:start', ''),
            'type': properties.get('Type', ''),
            'domain': properties.get('Domain', ''),
            'status': properties.get('Status', ''),
            'notion_id': notion_id,
            'notion_url': notion_url,
            'local_file': local_filename,
            'last_synced': datetime.now().isoformat(),
        }

        # Remove empty values
        frontmatter = {k: v for k, v in frontmatter.items() if v}

        return yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)

    def _extract_properties(self, page: Dict) -> Dict:
        """Extract properties from Notion page format."""
        raw_props = page.get('properties', {})
        result = {}

        for prop_name, prop_data in raw_props.items():
            prop_type = prop_data.get('type')

            if prop_type == 'title':
                title_array = prop_data.get('title', [])
                result['Title'] = ''.join(t.get('plain_text', '') for t in title_array)

            elif prop_type == 'rich_text':
                text_array = prop_data.get('rich_text', [])
                result[prop_name] = ''.join(t.get('plain_text', '') for t in text_array)

            elif prop_type == 'select':
                select_data = prop_data.get('select')
                result[prop_name] = select_data.get('name', '') if select_data else ''

            elif prop_type == 'date':
                date_data = prop_data.get('date')
                if date_data:
                    result[f'date:{prop_name}:start'] = date_data.get('start', '')
                    if date_data.get('end'):
                        result[f'date:{prop_name}:end'] = date_data['end']

        return result

    def pull_page(self, page_id: str, force: bool = False,
                  dry_run: bool = False) -> Dict:
        """
        Pull a single page from Notion to local.

        Args:
            page_id: Notion page ID (with or without dashes)
            force: If True, overwrite existing file even on conflict
            dry_run: If True, preview changes without writing

        Returns:
            Dict with 'action', 'file', 'title', etc.
        """
        # Normalize page ID
        page_id = page_id.replace('-', '')

        print(f"Fetching page {page_id[:8]}...")

        # Check git status before any writes
        if not dry_run:
            self._check_git_status()

        # Get page metadata and blocks
        content = self.api.get_page_content(page_id)
        page = content['page']
        blocks = content['blocks']

        print(f"  Found {content['block_count']} blocks")

        # Extract properties
        properties = self._extract_properties(page)
        title = properties.get('Title', 'Untitled')

        # Generate filename
        filename = self._generate_filename(properties)
        file_path = self.refined_dir / filename

        print(f"  Title: {title}")
        print(f"  File: {filename}")

        # Check conflict status
        notion_last_edited = page.get('last_edited_time', '')
        sync_status, sync_reason = self._check_conflict(
            page_id, notion_last_edited, file_path
        )
        print(f"  Sync status: {sync_status} ({sync_reason})")

        # Handle different sync statuses
        if sync_status == 'synced' and not force:
            print(f"  [OK] Already synced, skipping")
            return {
                'action': 'skipped',
                'file': filename,
                'title': title,
                'reason': sync_reason
            }

        if sync_status == 'conflict' and not force:
            print(f"  [!]  CONFLICT detected! Use --force to overwrite local")
            return {
                'action': 'conflict',
                'file': filename,
                'title': title,
                'reason': sync_reason
            }

        if sync_status == 'local_newer' and not force:
            print(f"  [!]  Local file is newer - consider pushing instead")
            return {
                'action': 'skipped',
                'file': filename,
                'title': title,
                'reason': sync_reason
            }

        # Convert blocks to markdown
        markdown_content = self._blocks_to_markdown(blocks)

        # Create frontmatter
        frontmatter = self._create_frontmatter(page, properties, filename)

        # Combine into final document
        full_content = f"---\n{frontmatter}---\n\n{markdown_content}"

        # Dry run - just report what would happen
        if dry_run:
            action = 'would_update' if file_path.exists() else 'would_create'
            print(f"  [DRY] DRY RUN: {action} ({len(full_content):,} chars)")
            return {
                'action': action,
                'file': filename,
                'title': title,
                'chars': len(full_content),
                'blocks': content['block_count'],
                'dry_run': True
            }

        # Create backup before overwriting (safety!)
        backup_path = self._create_backup(file_path)

        # Write file
        file_path.write_text(full_content, encoding='utf-8')

        action = 'updated' if backup_path else 'created'
        print(f"  [OK] {action.capitalize()}: {len(full_content):,} chars")

        # Update sync state
        from .state import DocumentState
        doc_state = DocumentState(
            notion_id=page.get('id', '').replace('-', ''),
            local_file=filename,
            title=title,
            notion_last_edited=page.get('last_edited_time', ''),
            local_last_modified=datetime.now().isoformat(),
            last_synced=datetime.now().isoformat(),
            sync_status='synced'
        )
        self.state.set_document(doc_state)
        self.state.save()

        return {
            'action': action,
            'file': filename,
            'title': title,
            'chars': len(full_content),
            'blocks': content['block_count'],
            'backup': str(backup_path) if backup_path else None
        }


def pull_document(page_id: str, force: bool = False, dry_run: bool = False) -> Dict:
    """Convenience function to pull a single document."""
    manager = PullManager()
    return manager.pull_page(page_id, force=force, dry_run=dry_run)


def main():
    """CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description='Pull docs from Notion')
    parser.add_argument('page_id', nargs='?', help='Notion page ID or URL')
    parser.add_argument('--force', action='store_true',
                        help='Overwrite even on conflict')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without writing')
    parser.add_argument('--refined-dir', type=str, help='Output directory')

    args = parser.parse_args()

    if not args.page_id:
        print("Usage: python -m grove_docs_refinery.sync.pull <page_id_or_url>")
        print("\nOptions:")
        print("  --dry-run    Preview changes without writing")
        print("  --force      Overwrite even on conflict")
        print("\nExample:")
        print("  python -m grove_docs_refinery.sync.pull 2ed780a78eef8103ad94ff897214dd1e")
        print("  python -m grove_docs_refinery.sync.pull --dry-run https://notion.so/...")
        return

    # Extract page ID from URL if needed
    page_id = args.page_id
    if 'notion.so' in page_id:
        # Extract ID from URL
        match = re.search(r'([a-f0-9]{32})', page_id.replace('-', ''))
        if match:
            page_id = match.group(1)

    manager = PullManager(refined_dir=args.refined_dir)
    result = manager.pull_page(page_id, force=args.force, dry_run=args.dry_run)

    print(f"\n=== Pull {'Preview' if args.dry_run else 'Complete'} ===")
    print(f"Action: {result['action']}")
    print(f"File: {result['file']}")
    if result.get('backup'):
        print(f"Backup: {result['backup']}")


if __name__ == '__main__':
    main()
