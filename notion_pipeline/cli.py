#!/usr/bin/env python3
"""
Notion Pipeline CLI.

Usage:
    python -m notion_pipeline.cli deletion-queue [--dry-run]
    python -m notion_pipeline.cli triage <database_id>
    python -m notion_pipeline.cli test
"""
import argparse
import sys
from .client import NotionClient
from .workflows import DeletionQueueWorkflow, TriageWorkflow


def cmd_deletion_queue(args):
    """Run deletion queue workflow."""
    client = NotionClient()
    workflow = DeletionQueueWorkflow(client)

    db_id = args.database or client.databases.GROVE_SCATTERED_INVENTORY
    queue_id = args.queue or client.databases.DELETION_QUEUE

    print(f"Database: {db_id}")
    print(f"Queue: {queue_id}")
    print(f"Dry run: {args.dry_run}")
    print()

    workflow.run(db_id, queue_id, dry_run=args.dry_run)


def cmd_triage(args):
    """Run triage workflow."""
    client = NotionClient()
    workflow = TriageWorkflow(client)

    db_id = args.database
    items = workflow.scan_database(db_id)
    report = workflow.generate_report(items)
    print(report)


def cmd_test(args):
    """Test connection and basic operations."""
    print("Testing Notion Pipeline Connection...")
    print("=" * 50)

    try:
        client = NotionClient()
        print(f"API Key: ...{client.api_key[-8:]}")

        # Test search
        print("\nTesting search...")
        results = client.search("Grove", page_size=3)
        print(f"  Found {len(results)} results")
        for r in results[:3]:
            print(f"  - {r.get('properties', {})}")

        # Test database query
        print("\nTesting database query (Grove Inventory)...")
        db_id = client.databases.GROVE_SCATTERED_INVENTORY
        try:
            pages = client.query_database(db_id, page_size=3)
            print(f"  Found {len(pages)} pages (limited to 3)")
            for p in pages[:3]:
                title = client.extract_title(p)
                print(f"  - {title}")
        except Exception as e:
            print(f"  ERROR: {e}")
            print("  (Database may not be shared with integration)")

        print("\n" + "=" * 50)
        print("Test complete!")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Notion Pipeline CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # deletion-queue command
    del_parser = subparsers.add_parser('deletion-queue', help='Move items to deletion queue')
    del_parser.add_argument('--dry-run', action='store_true', help='Show what would be moved')
    del_parser.add_argument('--database', help='Database ID to scan')
    del_parser.add_argument('--queue', help='Queue page ID')
    del_parser.set_defaults(func=cmd_deletion_queue)

    # triage command
    triage_parser = subparsers.add_parser('triage', help='Generate triage report')
    triage_parser.add_argument('database', help='Database ID to scan')
    triage_parser.set_defaults(func=cmd_triage)

    # test command
    test_parser = subparsers.add_parser('test', help='Test connection')
    test_parser.set_defaults(func=cmd_test)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
