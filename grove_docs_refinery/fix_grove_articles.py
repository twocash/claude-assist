#!/usr/bin/env python3
"""
Fix "Grove is/was/builds/etc." to "The Grove is/was/builds/etc."

Excludes cases like "your Grove", "their Grove", "a Grove" which are correct.
"""

import re
from pathlib import Path

REFINED_DIR = Path('C:/GitHub/claude-assist/grove_docs_refinery/refined')

# Verbs that follow "Grove" and should have "The" prepended
VERBS = r'(is|was|has|will|can|does|provides|enables|creates|builds|represents|combines|transforms|operates|uses|makes|demonstrates|defers|anticipates|captures|aggregates)'

# Pattern: "Grove <verb>" but NOT preceded by possessive/article words
# Negative lookbehind for: your, their, a, an, each, every, this, that, whose
PATTERN = re.compile(
    r'(?<![Yy]our )(?<![Tt]heir )(?<![Aa] )(?<![Ee]ach )(?<![Ee]very )(?<![Tt]his )(?<![Tt]hat )(?<![Ww]hose )'
    r'\bGrove ' + VERBS + r'\b',
    re.MULTILINE
)

def fix_file(filepath: Path, dry_run: bool = True) -> int:
    """Fix Grove article usage in a single file."""
    content = filepath.read_text(encoding='utf-8')

    # Find all matches first
    matches = list(PATTERN.finditer(content))

    if not matches:
        return 0

    # Replace "Grove <verb>" with "The Grove <verb>"
    def replacer(match):
        full_match = match.group(0)
        # Don't change if already preceded by "The "
        start = match.start()
        if start >= 4 and content[start-4:start] == 'The ':
            return full_match
        return 'The ' + full_match

    new_content = PATTERN.sub(replacer, content)

    changes = content != new_content
    if changes:
        if dry_run:
            print(f"\n{filepath.name}:")
            for m in matches:
                # Get context
                start = max(0, m.start() - 30)
                end = min(len(content), m.end() + 30)
                context = content[start:end].replace('\n', ' ')
                print(f"  ...{context}...")
        else:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"  Fixed: {filepath.name} ({len(matches)} changes)")

    return len(matches) if changes else 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Fix Grove article usage')
    parser.add_argument('--apply', action='store_true', help='Apply changes (default: dry run)')
    args = parser.parse_args()

    dry_run = not args.apply

    print("=" * 60)
    print("Grove Article Fixer")
    print("=" * 60)
    print(f"Mode: {'DRY RUN' if dry_run else 'APPLYING CHANGES'}")
    print()

    total_fixes = 0
    files_fixed = 0

    for filepath in sorted(REFINED_DIR.glob('*.md')):
        fixes = fix_file(filepath, dry_run)
        if fixes > 0:
            total_fixes += fixes
            files_fixed += 1

    print()
    print("=" * 60)
    print(f"Total: {total_fixes} fixes in {files_fixed} files")
    if dry_run:
        print("Run with --apply to make changes")
    print("=" * 60)


if __name__ == '__main__':
    main()
