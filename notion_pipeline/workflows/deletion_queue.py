"""
Deletion Queue Workflow.

Finds items marked for deletion and moves them to a holding queue.
Weekly pruning can then permanently delete the queued items.
"""
from typing import List, Dict, Optional
from ..client import NotionClient


class DeletionQueueWorkflow:
    """
    Move items marked for deletion to a queue.

    Pattern:
    1. Query database for items with Delete checkbox = True
    2. Move each item to Deletion Queue page
    3. Optionally uncheck the Delete box after moving
    """

    def __init__(self, client: Optional[NotionClient] = None):
        self.client = client or NotionClient()

    def find_items_to_delete(
        self,
        database_id: str,
        checkbox_property: str = 'Delete'
    ) -> List[Dict]:
        """
        Find all items with Delete checkbox checked.

        Returns list of pages with their titles and IDs.
        """
        filter_spec = {
            'property': checkbox_property,
            'checkbox': {'equals': True}
        }

        results = self.client.query_database(database_id, filter=filter_spec)

        items = []
        for page in results:
            items.append({
                'id': page['id'],
                'title': self.client.extract_title(page),
                'url': page.get('url', ''),
                'last_edited': page.get('last_edited_time', '')
            })

        return items

    def move_to_queue(
        self,
        items: List[Dict],
        queue_page_id: str,
        uncheck_after_move: bool = True,
        checkbox_property: str = 'Delete'
    ) -> Dict[str, int]:
        """
        Move items to deletion queue.

        Returns stats: {'moved': N, 'errors': N}
        """
        stats = {'moved': 0, 'errors': 0}

        for item in items:
            try:
                # Move to queue
                self.client.move_page(item['id'], queue_page_id)

                # Optionally uncheck the Delete box
                if uncheck_after_move:
                    self.client.update_page(item['id'], {
                        checkbox_property: {'checkbox': False}
                    })

                stats['moved'] += 1
                print(f"  Moved: {item['title']}")

            except Exception as e:
                stats['errors'] += 1
                print(f"  ERROR moving {item['title']}: {e}")

        return stats

    def run(
        self,
        database_id: str,
        queue_page_id: str,
        checkbox_property: str = 'Delete',
        dry_run: bool = False
    ) -> Dict:
        """
        Full workflow: find and move items to deletion queue.

        Args:
            database_id: Source database to scan
            queue_page_id: Deletion queue page ID
            checkbox_property: Name of checkbox property (default: "Delete")
            dry_run: If True, only report what would be moved
        """
        print(f"Scanning for items marked '{checkbox_property}'...")
        items = self.find_items_to_delete(database_id, checkbox_property)

        print(f"Found {len(items)} items to delete:")
        for item in items:
            print(f"  - {item['title']}")

        if dry_run:
            print("\n[DRY RUN] No items moved.")
            return {'found': len(items), 'moved': 0, 'errors': 0}

        if not items:
            return {'found': 0, 'moved': 0, 'errors': 0}

        print(f"\nMoving to deletion queue...")
        stats = self.move_to_queue(items, queue_page_id, checkbox_property=checkbox_property)

        print(f"\nComplete: {stats['moved']} moved, {stats['errors']} errors")
        return {'found': len(items), **stats}


# CLI entry point
if __name__ == '__main__':
    import sys

    client = NotionClient()
    workflow = DeletionQueueWorkflow(client)

    # Default to Grove Scattered Content Inventory
    db_id = client.databases.GROVE_SCATTERED_INVENTORY
    queue_id = client.databases.DELETION_QUEUE

    # Check for --dry-run flag
    dry_run = '--dry-run' in sys.argv

    workflow.run(db_id, queue_id, dry_run=dry_run)
