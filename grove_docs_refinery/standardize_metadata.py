#!/usr/bin/env python3
"""
Grove Corpus Metadata Standardizer

Adds YAML frontmatter to refined Grove documents with consistent metadata:
- title, author, date, type, domain, status, tags, source (if known)

Usage:
    python standardize_metadata.py --check          # Preview changes
    python standardize_metadata.py --apply          # Apply changes
    python standardize_metadata.py --single FILE    # Process one file
"""

import re
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

REFINED_DIR = Path(__file__).parent / "refined"

# Type codes: v=vision, s=spec/system, r=research
TYPE_MAP = {
    'v': 'vision',
    's': 'spec',
    'r': 'research'
}

# Domain mappings from filename patterns
DOMAIN_MAP = {
    'econ': 'economics',
    'arch': 'architecture',
    'method': 'methodology',
    'edge': 'edge-computing',
    'engage': 'engagement',
    'ratchet': 'ratchet-thesis',
    'pattern': 'patterns',
    'research': 'research'
}


def parse_filename(filename: str) -> Dict:
    """Extract metadata from filename pattern: YYMMDD-{type}-{domain}-{title}.md--FINAL.md"""
    metadata = {}

    # Remove --FINAL.md suffix
    base = filename.replace('--FINAL.md', '').replace('.md', '')

    # Pattern: 251200-v-econ-title-here
    match = re.match(r'^(\d{6})-([vsr])-([a-z]+)-(.+)$', base)
    if match:
        date_code, type_code, domain_code, title_slug = match.groups()

        # Parse date (YYMMDD)
        try:
            year = 2000 + int(date_code[:2])
            month = int(date_code[2:4])
            day = int(date_code[4:6]) or 1
            metadata['date'] = f"{year}-{month:02d}-{day:02d}"
        except:
            metadata['date'] = datetime.now().strftime('%Y-%m-%d')

        metadata['type'] = TYPE_MAP.get(type_code, type_code)
        metadata['domain'] = DOMAIN_MAP.get(domain_code, domain_code)
        metadata['title_slug'] = title_slug

    return metadata


def extract_inline_metadata(content: str) -> Dict:
    """Extract metadata from inline patterns like **Author:** or **Version:**"""
    metadata = {}

    # Author patterns
    author_match = re.search(r'\*\*Author[:\s]*\*\*\s*(.+?)(?:\n|$)', content, re.I)
    if author_match:
        metadata['author'] = author_match.group(1).strip()

    # Version patterns
    version_match = re.search(r'\*\*Version[:\s]*\*\*\s*(.+?)(?:\n|$)', content, re.I)
    if version_match:
        metadata['version'] = version_match.group(1).strip()

    # Status patterns
    status_match = re.search(r'\*\*Status[:\s]*\*\*\s*(.+?)(?:\n|$)', content, re.I)
    if status_match:
        metadata['status'] = status_match.group(1).strip()

    return metadata


def extract_title(content: str) -> Optional[str]:
    """Extract title from first H1 heading"""
    match = re.search(r'^#\s+(.+?)(?:\n|$)', content, re.M)
    if match:
        return match.group(1).strip()
    return None


def has_frontmatter(content: str) -> bool:
    """Check if content already has YAML frontmatter"""
    return content.strip().startswith('---')


def generate_frontmatter(metadata: Dict) -> str:
    """Generate YAML frontmatter block"""
    lines = ['---']

    if metadata.get('title'):
        lines.append(f'title: "{metadata["title"]}"')

    # Always Jim Calhoun as author
    lines.append('author: "Jim Calhoun"')

    # Copyright year based on document date
    if metadata.get('date'):
        year = metadata['date'][:4]
        lines.append(f'copyright: "{year} The Grove Foundation"')
        lines.append(f'date: "{metadata["date"]}"')
    else:
        lines.append('copyright: "2026 The Grove Foundation"')
    if metadata.get('type'):
        lines.append(f'type: "{metadata["type"]}"')
    if metadata.get('domain'):
        lines.append(f'domain: "{metadata["domain"]}"')

    lines.append('status: "final"')

    if metadata.get('tags'):
        lines.append('tags:')
        for tag in metadata['tags']:
            lines.append(f'  - {tag}')

    if metadata.get('source'):
        lines.append(f'source: "{metadata["source"]}"')

    lines.append('---')
    lines.append('')

    return '\n'.join(lines)


def process_file(filepath: Path, apply: bool = False) -> Dict:
    """Process a single file and return metadata/changes"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    result = {
        'file': filepath.name,
        'has_frontmatter': has_frontmatter(content),
        'changes': []
    }

    if result['has_frontmatter']:
        result['status'] = 'already_has_frontmatter'
        return result

    # Extract metadata from various sources
    filename_meta = parse_filename(filepath.name)
    inline_meta = extract_inline_metadata(content)
    title = extract_title(content)

    # Merge metadata (inline takes precedence)
    metadata = {**filename_meta, **inline_meta}
    if title:
        metadata['title'] = title

    # Generate tags from domain
    if metadata.get('domain'):
        metadata['tags'] = [metadata['domain']]

    # Generate frontmatter
    frontmatter = generate_frontmatter(metadata)
    new_content = frontmatter + content

    result['metadata'] = metadata
    result['status'] = 'needs_update'

    if apply:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        result['status'] = 'updated'

    return result


def main():
    args = sys.argv[1:]

    if '--help' in args or '-h' in args:
        print(__doc__)
        return

    apply = '--apply' in args
    check = '--check' in args or not apply

    # Single file mode
    if '--single' in args:
        idx = args.index('--single')
        if idx + 1 < len(args):
            filepath = Path(args[idx + 1])
            if not filepath.exists():
                filepath = REFINED_DIR / args[idx + 1]
            result = process_file(filepath, apply=apply)
            print(f"{result['file']}: {result['status']}")
            if result.get('metadata'):
                for k, v in result['metadata'].items():
                    print(f"  {k}: {v}")
            return

    # Process all files
    files = sorted(REFINED_DIR.glob('*.md'))

    stats = {'already_has': 0, 'needs_update': 0, 'updated': 0}

    print(f"\n{'=' * 60}")
    print(f"Grove Corpus Metadata Standardizer")
    print(f"{'=' * 60}")
    print(f"Mode: {'APPLY' if apply else 'CHECK (preview)'}")
    print(f"Directory: {REFINED_DIR}")
    print(f"Files found: {len(files)}")
    print(f"{'=' * 60}\n")

    for filepath in files:
        if filepath.name == '.gitkeep':
            continue

        result = process_file(filepath, apply=apply)

        if result['status'] == 'already_has_frontmatter':
            stats['already_has'] += 1
            print(f"[OK] {result['file']} (already has frontmatter)")
        elif result['status'] == 'needs_update':
            stats['needs_update'] += 1
            print(f"[ ] {result['file']} (needs update)")
            if result.get('metadata'):
                print(f"    title: {result['metadata'].get('title', 'N/A')[:50]}")
                print(f"    type: {result['metadata'].get('type', 'N/A')}")
                print(f"    domain: {result['metadata'].get('domain', 'N/A')}")
        elif result['status'] == 'updated':
            stats['updated'] += 1
            print(f"[OK] {result['file']} (updated)")

    print(f"\n{'=' * 60}")
    print(f"Summary:")
    print(f"  Already has frontmatter: {stats['already_has']}")
    print(f"  Needs update: {stats['needs_update']}")
    print(f"  Updated: {stats['updated']}")

    if check and stats['needs_update'] > 0:
        print(f"\nRun with --apply to update files.")


if __name__ == '__main__':
    main()
