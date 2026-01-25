"""
Push (upload) workflow: Local -> Notion Database

Uploads refined documents as rows in the Grove Corpus database.
Each document = one database row with properties + content.
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


class DatabasePushManager:
    """
    Manages push to Grove Corpus database.
    """

    # Grove Corpus database
    DATABASE_ID = '00ea815de6fa40daa79bf5dd29b85a29'
    DATA_SOURCE_ID = 'ae082912-753f-442d-a844-1cb735d93eae'

    def __init__(self, api: Optional[NotionAPI] = None,
                 state: Optional[SyncState] = None,
                 refined_dir: Optional[str] = None):
        self.api = api or get_api()
        self.state = state or get_state()
        self.refined_dir = Path(refined_dir or 'grove_docs_refinery/refined')

    def _parse_local_file(self, file_path: Path) -> Tuple[Dict, List[Dict], str]:
        """Parse a local markdown file."""
        content = file_path.read_text(encoding='utf-8')
        frontmatter, blocks = markdown_file_to_notion(content)
        return frontmatter, blocks, content

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

        # No frontmatter - add new
        new_yaml = yaml.dump(updates, default_flow_style=False, allow_unicode=True)
        new_content = f'---\n{new_yaml}---\n\n{content}'
        file_path.write_text(new_content, encoding='utf-8')

    def _build_properties(self, frontmatter: Dict, file_path: Path) -> Dict:
        """Build Notion database properties from frontmatter."""
        props = {}

        # Title (required)
        title = frontmatter.get('title', file_path.stem)
        props['Title'] = title

        # Type (select)
        doc_type = frontmatter.get('type', 'vision').lower()
        if doc_type in ('vision', 'software', 'blog'):
            props['Type'] = doc_type
        elif doc_type == 'spec':
            props['Type'] = 'software'
        else:
            props['Type'] = 'vision'

        # Domain (select)
        domain = frontmatter.get('domain', '').lower()
        valid_domains = ('research', 'architecture', 'economics', 'strategy', 'protocol', 'spec')
        if domain in valid_domains:
            props['Domain'] = domain

        # Status (select)
        status = frontmatter.get('status', 'final').lower()
        if status in ('draft', 'review', 'final'):
            props['Status'] = status
        else:
            props['Status'] = 'final'

        # Author (text)
        author = frontmatter.get('author', '')
        if author:
            props['Author'] = author

        # Date
        date_str = frontmatter.get('date', '')
        if date_str:
            # Ensure proper format
            if isinstance(date_str, str) and len(date_str) >= 10:
                props['date:Date:start'] = date_str[:10]
                props['date:Date:is_datetime'] = 0

        # Local File (for sync tracking)
        props['Local File'] = file_path.name

        # Last Synced
        props['date:Last Synced:start'] = datetime.now().strftime('%Y-%m-%d')
        props['date:Last Synced:is_datetime'] = 0

        return props

    def find_existing_row(self, title: str, notion_id: Optional[str] = None) -> Optional[Dict]:
        """Find existing database row by ID or title."""
        # Strategy 1: Direct lookup by ID (only if it's a database row)
        if notion_id:
            try:
                formatted_id = self._format_notion_id(notion_id)
                uuid_with_dashes = f'{formatted_id[:8]}-{formatted_id[8:12]}-{formatted_id[12:16]}-{formatted_id[16:20]}-{formatted_id[20:]}'
                page = self.api.get_page(uuid_with_dashes)
                if page and not page.get('archived'):
                    # Check if this is a database row (has parent.database_id)
                    parent = page.get('parent', {})
                    if parent.get('type') == 'database_id':
                        return page
                    # Otherwise it's an old page, ignore it
            except Exception:
                pass

        # Strategy 2: Query database by title
        try:
            results = self.api.query_database(
                self.DATABASE_ID,
                filter_={
                    'property': 'Title',
                    'title': {'equals': title}
                }
            )
            if results:
                return results[0]
        except Exception:
            pass

        return None

    def create_row(self, frontmatter: Dict, blocks: List[Dict], file_path: Path) -> Dict:
        """Create a new database row."""
        props = self._build_properties(frontmatter, file_path)

        # Build Notion properties format
        notion_props = {}

        # Title
        notion_props['Title'] = {
            'title': [{'text': {'content': props.get('Title', 'Untitled')}}]
        }

        # Select properties
        for key in ('Type', 'Domain', 'Status'):
            if key in props:
                notion_props[key] = {'select': {'name': props[key]}}

        # Text properties
        for key in ('Author', 'Local File'):
            if key in props:
                notion_props[key] = {
                    'rich_text': [{'text': {'content': props[key]}}]
                }

        # Date properties
        if 'date:Date:start' in props:
            notion_props['Date'] = {
                'date': {'start': props['date:Date:start']}
            }
        if 'date:Last Synced:start' in props:
            notion_props['Last Synced'] = {
                'date': {'start': props['date:Last Synced:start']}
            }

        # Clean blocks for upload - handle tables specially
        # Tables MUST include their children (rows) when created
        clean_blocks = []

        for block in blocks:
            if block.get('type') == 'table':
                # Tables require children - include rows in the table block
                table_rows = block.get('_children', [])
                if table_rows:
                    # Clean rows
                    clean_rows = [{k: v for k, v in r.items() if k != '_children'}
                                  for r in table_rows]
                    clean_blocks.append({
                        'type': 'table',
                        'table': {
                            'table_width': block.get('table', {}).get('table_width', 2),
                            'has_column_header': block.get('table', {}).get('has_column_header', True),
                            'has_row_header': block.get('table', {}).get('has_row_header', False),
                            'children': clean_rows
                        }
                    })
                # Skip empty tables
            else:
                clean_blocks.append({k: v for k, v in block.items() if k != '_children'})

        # Create page in database
        parent = {'database_id': self.DATABASE_ID}
        page = self.api.create_page(parent, notion_props, clean_blocks)

        return page

    def update_row(self, page_id: str, frontmatter: Dict, blocks: List[Dict], file_path: Path) -> Dict:
        """Update existing database row."""
        props = self._build_properties(frontmatter, file_path)

        # Build Notion properties format for update
        notion_props = {}

        # Select properties
        for key in ('Type', 'Domain', 'Status'):
            if key in props:
                notion_props[key] = {'select': {'name': props[key]}}

        # Text properties
        for key in ('Author', 'Local File'):
            if key in props:
                notion_props[key] = {
                    'rich_text': [{'text': {'content': props[key]}}]
                }

        # Date properties
        if 'date:Date:start' in props:
            notion_props['Date'] = {
                'date': {'start': props['date:Date:start']}
            }
        notion_props['Last Synced'] = {
            'date': {'start': datetime.now().strftime('%Y-%m-%d')}
        }

        # Update properties
        self.api.update_page(page_id, notion_props)

        # Clear and replace content
        self.api.clear_page_content(page_id)

        # Clean blocks for upload - handle tables specially (same as create_row)
        clean_blocks = []
        for block in blocks:
            if block.get('type') == 'table':
                # Tables require children - include rows in the table block
                table_rows = block.get('_children', [])
                if table_rows:
                    clean_rows = [{k: v for k, v in r.items() if k != '_children'}
                                  for r in table_rows]
                    clean_blocks.append({
                        'type': 'table',
                        'table': {
                            'table_width': block.get('table', {}).get('table_width', 2),
                            'has_column_header': block.get('table', {}).get('has_column_header', True),
                            'has_row_header': block.get('table', {}).get('has_row_header', False),
                            'children': clean_rows
                        }
                    })
                # Skip empty tables
            else:
                clean_blocks.append({k: v for k, v in block.items() if k != '_children'})

        if clean_blocks:
            self.api.append_blocks(page_id, clean_blocks)

        return self.api.get_page(page_id)

    # Quality thresholds
    MIN_CONTENT_CHARS = 400  # Minimum chars after frontmatter
    MIN_BLOCKS = 5  # Minimum number of blocks

    def _quality_check(self, content: str, blocks: List[Dict], file_path: Path) -> Optional[str]:
        """
        Quality gate to prevent uploading stub/incomplete files.

        Returns error message if quality check fails, None if OK.
        """
        # Strip frontmatter to get actual content
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                body = parts[2].strip()
            else:
                body = content
        else:
            body = content

        # Check content length
        if len(body) < self.MIN_CONTENT_CHARS:
            return f"Content too short ({len(body)} chars < {self.MIN_CONTENT_CHARS})"

        # Check block count (excluding empty paragraphs)
        non_empty = [b for b in blocks if not (
            b.get('type') == 'paragraph' and
            not b.get('paragraph', {}).get('rich_text', [])
        )]
        if len(non_empty) < self.MIN_BLOCKS:
            return f"Too few content blocks ({len(non_empty)} < {self.MIN_BLOCKS})"

        return None  # Passed

    def push_file(self, file_path: Path, dry_run: bool = False, skip_quality_check: bool = False) -> Dict:
        """Push a single file to database."""
        result = {
            'file': str(file_path),
            'action': None,
            'page': None,
            'error': None
        }

        try:
            frontmatter, blocks, content = self._parse_local_file(file_path)

            # Quality gate
            if not skip_quality_check:
                quality_error = self._quality_check(content, blocks, file_path)
                if quality_error:
                    result['action'] = 'skipped_quality'
                    result['error'] = quality_error
                    return result

            title = frontmatter.get('title', file_path.stem)
            notion_id = frontmatter.get('notion_id')

            # Check for existing row
            existing = self.find_existing_row(title, notion_id)

            if dry_run:
                if existing:
                    result['action'] = 'would_update'
                    result['page'] = {'id': existing.get('id'), 'title': title}
                else:
                    result['action'] = 'would_create'
                    result['page'] = {'title': title}
                return result

            if existing:
                page_id = existing.get('id')
                page = self.update_row(page_id, frontmatter, blocks, file_path)
                result['action'] = 'updated'
            else:
                page = self.create_row(frontmatter, blocks, file_path)
                result['action'] = 'created'

            result['page'] = page

            # Update local frontmatter
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
            import traceback
            traceback.print_exc()

        return result

    def push_all(self, dry_run: bool = False, files: Optional[List[str]] = None) -> List[Dict]:
        """Push all refined documents to database."""
        results = []

        if files:
            file_paths = [self.refined_dir / f for f in files]
        else:
            file_paths = list(self.refined_dir.glob('*--FINAL.md'))

        print(f"Found {len(file_paths)} files to process")

        for i, file_path in enumerate(sorted(file_paths), 1):
            if not file_path.exists():
                results.append({
                    'file': str(file_path),
                    'action': 'not_found',
                    'error': 'File does not exist'
                })
                continue

            print(f"[{i}/{len(file_paths)}] {file_path.name[:50]}...")
            result = self.push_file(file_path, dry_run)
            results.append(result)

            if result['action'] == 'error':
                print(f"  ERROR: {result['error']}")
            else:
                action = result['action']
                page_id = result.get('page', {}).get('id', 'N/A')[:8]
                print(f"  {action} ({page_id}...)")

        if not dry_run:
            self.state.update_last_sync()

        return results

    def check_status(self) -> Dict:
        """Check sync status."""
        summary = {
            'total': 0,
            'would_create': 0,
            'would_update': 0,
            'files': []
        }

        file_paths = list(self.refined_dir.glob('*--FINAL.md'))
        summary['total'] = len(file_paths)

        for file_path in sorted(file_paths):
            content = file_path.read_text(encoding='utf-8')
            frontmatter, _ = parse_frontmatter(content)

            title = frontmatter.get('title', file_path.stem)
            notion_id = frontmatter.get('notion_id')
            doc_type = frontmatter.get('type', 'vision')

            existing = self.find_existing_row(title, notion_id)

            if existing:
                status = 'would_update'
                summary['would_update'] += 1
            else:
                status = 'would_create'
                summary['would_create'] += 1

            summary['files'].append({
                'file': file_path.name,
                'title': title,
                'type': doc_type,
                'status': status
            })

        return summary


def main():
    """CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description='Push docs to Grove Corpus database')
    parser.add_argument('--check', action='store_true', help='Check status')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes')
    parser.add_argument('--file', type=str, nargs='+', help='Specific files')
    parser.add_argument('--refined-dir', type=str, help='Refined directory path')

    args = parser.parse_args()

    manager = DatabasePushManager(refined_dir=args.refined_dir)

    if args.check:
        status = manager.check_status()
        print(f"\n=== Sync Status ===")
        print(f"Total: {status['total']}")
        print(f"Would create: {status['would_create']}")
        print(f"Would update: {status['would_update']}")
    else:
        results = manager.push_all(dry_run=args.dry_run, files=args.file)

        created = sum(1 for r in results if r['action'] == 'created')
        updated = sum(1 for r in results if r['action'] == 'updated')
        errors = sum(1 for r in results if r['action'] == 'error')

        print(f"\n=== Push Complete ===")
        print(f"Created: {created}")
        print(f"Updated: {updated}")
        print(f"Errors: {errors}")


if __name__ == '__main__':
    main()
