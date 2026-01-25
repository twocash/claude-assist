"""
Batch pull all documents from Grove Corpus to local refined/ folder.
"""

from .api import get_api
from .pull import PullManager

# Grove Corpus database ID
GROVE_CORPUS_DB_ID = '00ea815de6fa40daa79bf5dd29b85a29'


def pull_all_documents(force: bool = False):
    """
    Pull all documents from Grove Corpus database.

    Args:
        force: If True, overwrite existing files
    """
    api = get_api()
    manager = PullManager(api=api)

    print("Fetching all documents from Grove Corpus...")
    pages = api.query_database(GROVE_CORPUS_DB_ID)
    print(f"Found {len(pages)} documents\n")

    results = {
        'created': [],
        'updated': [],
        'skipped': [],
        'errors': []
    }

    for i, page in enumerate(pages, 1):
        page_id = page['id'].replace('-', '')

        # Get title for display
        props = page.get('properties', {})
        title_prop = props.get('Title', {})
        title = ''
        if title_prop.get('type') == 'title':
            title = ''.join(t.get('plain_text', '') for t in title_prop.get('title', []))

        print(f"[{i}/{len(pages)}] {title[:50]}...")

        try:
            result = manager.pull_page(page_id, force=force)
            action = result.get('action', 'unknown')

            if action in results:
                results[action].append(result)
            else:
                results['created'].append(result)

            print(f"  -> {action}: {result.get('file', 'unknown')}\n")

        except Exception as e:
            error_info = {'page_id': page_id, 'title': title, 'error': str(e)}
            results['errors'].append(error_info)
            print(f"  -> ERROR: {e}\n")

    # Summary
    print("\n" + "=" * 60)
    print("BATCH PULL COMPLETE")
    print("=" * 60)
    print(f"Created: {len(results['created'])}")
    print(f"Updated: {len(results['updated'])}")
    print(f"Skipped: {len(results['skipped'])}")
    print(f"Errors:  {len(results['errors'])}")

    if results['errors']:
        print("\nErrors:")
        for err in results['errors']:
            print(f"  - {err['title']}: {err['error']}")

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Pull all docs from Grove Corpus')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')

    args = parser.parse_args()
    pull_all_documents(force=args.force)


if __name__ == '__main__':
    main()
