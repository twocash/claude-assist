"""
Push (upload) workflow: Local -> Notion

Handles:
1. Initial upload to correct hierarchy (by type -> Vision/Software/Blog)
2. Update existing pages (for subsequent syncs)
3. Duplicate prevention via notion_id + title matching
4. Write notion_id back to local frontmatter after upload
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from .api import NotionAPI, get_api
from .converter import markdown_file_to_notion, parse_frontmatter
from .state import SyncState, DocumentState, get_state


# Category mappings from frontmatter type field
TYPE_TO_CATEGORY = {
    'vision': 'vision',
    'software': 'software',
    'spec': 'software',
    'blog': 'blog',
    'post': 'blog'
}

# Filename prefix mappings (YYMMDD-{letter}-{subtype}-...)
# s = software, v = vision
FILENAME_PREFIX_TO_CATEGORY = {
    's': 'software',  # s-arch, s-method, s-spec, s-pattern, s-exec, etc.
    'v': 'vision',    # v-thesis, v-econ, v-edge, v-engage, v-ratchet, v-research, v-strat
}

def infer_category_from_filename(filename: str) -> str:
    """
    Infer document category from filename pattern.

    Pattern: YYMMDD-{type_letter}-{subtype}-{name}.md--FINAL.md
    Examples:
        251200-s-arch-technical-architecture.md--FINAL.md -> software
        251200-v-thesis-grove-world-changing.md--FINAL.md -> vision
    """
    # Match pattern: 6 digits, dash, single letter, dash
    match = re.match(r'^\d{6}-([a-z])-', filename.lower())
    if match:
        letter = match.group(1)
        return FILENAME_PREFIX_TO_CATEGORY.get(letter, 'vision')
    return 'vision'  # Default to vision


def extract_title_from_content(content: str) -> str:
    """
    Extract title from markdown content.

    Looks for first H1 heading (# Title) in the content.
    Falls back to first non-empty line if no H1 found.
    """
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    # Fall back to first non-empty line
    for line in lines:
        line = line.strip()
        if line and not line.startswith('---'):
            return line[:100]  # Limit length
    return 'Untitled'


class PushManager:
    """
    Manages the push (upload) workflow from local to Notion.

    Uploads documents to the Grove Corpus database with proper properties.
    """

    # Grove Corpus database ID
    GROVE_CORPUS_DB = '00ea815d-e6fa-40da-a79b-f5dd29b85a29'

    # Legacy category page IDs (archived - kept for reference)
    DOCUMENTATION_PAGE = '2ed780a78eef81059f0ec7177f68f464'
    CATEGORY_PAGES = {
        'vision': '2ed780a78eef81dfb5acd6f4a24d66d3',
        'software': '2ed780a78eef81cf9ccffb7820e047a3',
        'blog': '2ed780a78eef817da309ebb7228ee053'
    }

    def __init__(self, api: Optional[NotionAPI] = None,
                 state: Optional[SyncState] = None,
                 refined_dir: Optional[str] = None):
        self.api = api or get_api()
        self.state = state or get_state()
        self.refined_dir = Path(refined_dir or 'grove_docs_refinery/refined')

        # Initialize state with category IDs
        for category, page_id in self.CATEGORY_PAGES.items():
            self.state.set_category(category, page_id)

    def _parse_local_file(self, file_path: Path) -> Tuple[Dict, List[Dict], str]:
        """
        Parse a local markdown file.

        Returns:
            Tuple of (frontmatter, blocks, full_content)
        """
        content = file_path.read_text(encoding='utf-8')
        frontmatter, blocks = markdown_file_to_notion(content)
        return frontmatter, blocks, content

    def _get_category_for_type(self, doc_type: str) -> str:
        """Map document type to category."""
        return TYPE_TO_CATEGORY.get(doc_type.lower(), 'vision')

    def _format_notion_id(self, uuid: str) -> str:
        """Format UUID for consistent comparison."""
        return uuid.replace('-', '').lower()

    def _update_frontmatter(self, file_path: Path, updates: Dict):
        """Update frontmatter in a local file."""
        content = file_path.read_text(encoding='utf-8')

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    frontmatter.update(updates)
                    new_yaml = yaml.dump(frontmatter, default_flow_style=False,
                                         allow_unicode=True)
                    new_content = f'---\n{new_yaml}---{parts[2]}'
                    file_path.write_text(new_content, encoding='utf-8')
                    return
                except yaml.YAMLError:
                    pass

        # No frontmatter or parse error - add new frontmatter
        new_yaml = yaml.dump(updates, default_flow_style=False, allow_unicode=True)
        new_content = f'---\n{new_yaml}---\n\n{content}'
        file_path.write_text(new_content, encoding='utf-8')

    def find_existing_page(self, title: str, notion_id: Optional[str] = None,
                           category: Optional[str] = None) -> Optional[Dict]:
        """
        Find an existing Notion page by ID or title.

        Strategy:
        1. If notion_id provided, try to fetch directly
        2. If not found, search by title within category
        """
        # Strategy 1: Direct lookup by ID
        if notion_id:
            try:
                formatted_id = self._format_notion_id(notion_id)
                # Add dashes for API call
                uuid_with_dashes = f'{formatted_id[:8]}-{formatted_id[8:12]}-{formatted_id[12:16]}-{formatted_id[16:20]}-{formatted_id[20:]}'
                page = self.api.get_page(uuid_with_dashes)
                if page and not page.get('archived'):
                    return page
            except Exception:
                pass  # Page not found, try title search

        # Strategy 2: Search by title
        parent_id = self.CATEGORY_PAGES.get(category) if category else None
        found = self.api.find_page_by_title(title, parent_id)
        return found

    def create_page(self, title: str, category: str, blocks: List[Dict],
                     local_file: Optional[str] = None) -> Dict:
        """
        Create a new page in the Grove Corpus database.

        Args:
            title: Document title
            category: Document type (vision/software/blog)
            blocks: Notion block content
            local_file: Local filename for linking
        """
        from datetime import datetime

        # Build properties for database page
        properties = {
            'Title': {
                'title': [{'text': {'content': title}}]
            },
            'Type': {
                'select': {'name': category}
            },
            'Status': {
                'select': {'name': 'final'}  # Coming from refined/
            },
            'Last Synced': {
                'date': {'start': datetime.now().isoformat()}
            }
        }

        # Add local file reference if provided
        if local_file:
            properties['Local File'] = {
                'rich_text': [{'text': {'content': local_file}}]
            }

        # Build parent (database, not page)
        parent = {'database_id': self.GROVE_CORPUS_DB}

        # Filter and clean blocks for API
        clean_blocks = []
        for block in blocks:
            if block.get('type') == 'table':
                # Tables need children (table_row blocks)
                table_data = block.get('table', {
                    'table_width': 2,
                    'has_column_header': True,
                    'has_row_header': False
                })
                # Include table row children
                table_children = block.get('_children', [])
                if table_children:
                    table_data['children'] = [
                        {k: v for k, v in row.items() if k != '_children'}
                        for row in table_children
                    ]
                clean_blocks.append({
                    'type': 'table',
                    'table': table_data
                })
            else:
                clean_blocks.append({k: v for k, v in block.items() if k != '_children'})

        # Create page in database
        page = self.api.create_page(parent, properties, clean_blocks)

        return page

    def update_page(self, page_id: str, blocks: List[Dict]) -> Dict:
        """Update an existing page's content."""
        # Clear existing content
        self.api.clear_page_content(page_id)

        # Filter blocks for upload
        clean_blocks = []
        for block in blocks:
            clean_blocks.append({k: v for k, v in block.items() if k != '_children'})

        # Append new content
        if clean_blocks:
            self.api.append_blocks(page_id, clean_blocks)

        # Get updated page
        return self.api.get_page(page_id)

    def push_file(self, file_path: Path, dry_run: bool = False) -> Dict:
        """
        Push a single file to Notion.

        Args:
            file_path: Path to the markdown file
            dry_run: If True, don't actually upload

        Returns:
            Dict with 'action' ('created'/'updated'/'skipped'), 'page', 'error'
        """
        result = {
            'file': str(file_path),
            'action': None,
            'page': None,
            'error': None
        }

        try:
            # Parse file
            frontmatter, blocks, content = self._parse_local_file(file_path)

            # Get title: frontmatter > H1 heading > filename stem
            title = frontmatter.get('title')
            if not title:
                title = extract_title_from_content(content)
            notion_id = frontmatter.get('notion_id')
            # Prefer frontmatter type, but fall back to filename inference
            doc_type = frontmatter.get('type')
            if doc_type:
                category = self._get_category_for_type(doc_type)
            else:
                category = infer_category_from_filename(file_path.name)

            # Check for existing page
            existing = self.find_existing_page(title, notion_id, category)

            if dry_run:
                if existing:
                    result['action'] = 'would_update'
                    result['page'] = {'id': existing.get('id'), 'title': title}
                else:
                    result['action'] = 'would_create'
                    result['page'] = {'title': title, 'category': category}
                return result

            if existing:
                # Update existing page
                page_id = existing.get('id')
                page = self.update_page(page_id, blocks)
                result['action'] = 'updated'
            else:
                # Create new page in Grove Corpus database
                page = self.create_page(title, category, blocks, local_file=file_path.name)
                result['action'] = 'created'

            result['page'] = page

            # Update local frontmatter with notion_id
            page_id = page.get('id', '').replace('-', '')
            page_url = page.get('url', '')

            self._update_frontmatter(file_path, {
                'notion_id': page_id,
                'notion_url': page_url,
                'last_synced': datetime.now().isoformat()
            })

            # Update sync state
            content_hash = self.state.compute_hash(content)
            self.state.mark_synced(
                notion_id=page_id,
                local_file=file_path.name,
                title=title,
                notion_edited=page.get('last_edited_time', ''),
                content_hash=content_hash
            )

        except Exception as e:
            result['error'] = str(e)
            result['action'] = 'error'

        return result

    def push_all(self, dry_run: bool = False, files: Optional[List[str]] = None) -> List[Dict]:
        """
        Push all refined documents to Notion.

        Args:
            dry_run: If True, preview without uploading
            files: Optional list of specific filenames to push

        Returns:
            List of result dicts
        """
        results = []

        # Get files to process
        if files:
            file_paths = [self.refined_dir / f for f in files]
        else:
            file_paths = list(self.refined_dir.glob('*--FINAL.md'))

        import sys
        print(f"Found {len(file_paths)} files to process", flush=True)

        for i, file_path in enumerate(sorted(file_paths)):
            if not file_path.exists():
                results.append({
                    'file': str(file_path),
                    'action': 'not_found',
                    'error': 'File does not exist'
                })
                continue

            print(f"[{i+1}/{len(file_paths)}] Processing: {file_path.name}", flush=True)
            result = self.push_file(file_path, dry_run)
            results.append(result)

            if result['action'] == 'error':
                print(f"  ERROR: {result['error']}", flush=True)
            else:
                print(f"  {result['action']}: {result.get('page', {}).get('id', 'N/A')}", flush=True)

        # Update global sync time
        if not dry_run:
            self.state.update_last_sync()

        return results

    def check_status(self) -> Dict:
        """
        Check sync status of all refined documents.

        Returns summary of what would be created/updated.
        """
        summary = {
            'total': 0,
            'would_create': 0,
            'would_update': 0,
            'synced': 0,
            'files': []
        }

        file_paths = list(self.refined_dir.glob('*--FINAL.md'))
        summary['total'] = len(file_paths)

        for file_path in sorted(file_paths):
            content = file_path.read_text(encoding='utf-8')
            frontmatter, _ = parse_frontmatter(content)

            # Get title: frontmatter > H1 heading > filename stem
            title = frontmatter.get('title')
            if not title:
                title = extract_title_from_content(content)
            notion_id = frontmatter.get('notion_id')
            # Prefer frontmatter type, but fall back to filename inference
            doc_type = frontmatter.get('type')
            if doc_type:
                category = self._get_category_for_type(doc_type)
            else:
                category = infer_category_from_filename(file_path.name)

            existing = self.find_existing_page(title, notion_id, category)

            if existing:
                # Check if content differs
                doc_state = self.state.get_document(
                    self._format_notion_id(existing.get('id', ''))
                )
                if doc_state:
                    current_hash = self.state.compute_hash(content)
                    if current_hash == doc_state.content_hash:
                        status = 'synced'
                        summary['synced'] += 1
                    else:
                        status = 'would_update'
                        summary['would_update'] += 1
                else:
                    status = 'would_update'
                    summary['would_update'] += 1
            else:
                status = 'would_create'
                summary['would_create'] += 1

            summary['files'].append({
                'file': file_path.name,
                'title': title,
                'category': category,
                'status': status
            })

        return summary


# ============================================================================
# CLI Interface
# ============================================================================

def safe_print(text: str):
    """Print text safely, handling encoding errors."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Fall back to ASCII with replacement
        print(text.encode('ascii', 'replace').decode('ascii'))


def main():
    """Command-line interface for push operations."""
    import argparse
    import sys
    import io

    # Fix Windows console encoding
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(description='Push local docs to Notion')
    parser.add_argument('--check', action='store_true',
                        help='Check status without uploading')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview what would be done')
    parser.add_argument('--file', type=str, nargs='+',
                        help='Specific files to push')
    parser.add_argument('--refined-dir', type=str,
                        help='Path to refined directory')

    args = parser.parse_args()

    manager = PushManager(refined_dir=args.refined_dir)

    if args.check:
        status = manager.check_status()
        print("\n=== Sync Status ===")
        print(f"Total files: {status['total']}")
        print(f"Would create: {status['would_create']}")
        print(f"Would update: {status['would_update']}")
        print(f"Already synced: {status['synced']}")
        print("\nDetails:")
        for f in status['files']:
            print(f"  {f['status']:15} {f['category']:10} {f['title'][:50]}")
    else:
        results = manager.push_all(dry_run=args.dry_run, files=args.file)

        # Summary
        created = sum(1 for r in results if r['action'] == 'created')
        updated = sum(1 for r in results if r['action'] == 'updated')
        errors = sum(1 for r in results if r['action'] == 'error')

        print(f"\n=== Push Complete ===")
        print(f"Created: {created}")
        print(f"Updated: {updated}")
        print(f"Errors: {errors}")


if __name__ == '__main__':
    main()
