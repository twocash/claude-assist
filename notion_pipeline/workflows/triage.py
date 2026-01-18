"""
Triage Workflow.

Scans a Notion workspace section and generates a triage inventory.
Useful for cleanup and reorganization projects.
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..client import NotionClient


class TriageWorkflow:
    """
    Scan pages and generate triage recommendations.

    Categories:
    - Keep: Active, valuable content
    - Archive: Valuable but stale
    - Delete: Empty or obsolete
    - Review: Needs human decision
    """

    def __init__(self, client: Optional[NotionClient] = None):
        self.client = client or NotionClient()

    def scan_page_recursively(
        self,
        page_id: str,
        max_depth: int = 3,
        current_depth: int = 0
    ) -> List[Dict]:
        """
        Recursively scan a page and its children.

        Returns list of page metadata for triage.
        """
        if current_depth > max_depth:
            return []

        results = []

        # Get page info
        try:
            page = self.client.get_page(page_id)
            page_info = self._extract_page_info(page, current_depth)
            results.append(page_info)

            # Get children (blocks)
            # Note: Getting child pages requires blocks API
            # For now, we'll use search to find related pages

        except Exception as e:
            print(f"Error scanning {page_id}: {e}")

        return results

    def _extract_page_info(self, page: Dict, depth: int = 0) -> Dict:
        """Extract triage-relevant info from a page."""
        last_edited = page.get('last_edited_time', '')
        created = page.get('created_time', '')

        # Calculate staleness
        if last_edited:
            last_dt = datetime.fromisoformat(last_edited.replace('Z', '+00:00'))
            age_days = (datetime.now(last_dt.tzinfo) - last_dt).days
        else:
            age_days = 999

        return {
            'id': page['id'],
            'title': self.client.extract_title(page),
            'url': page.get('url', ''),
            'last_edited': last_edited[:10] if last_edited else '',
            'created': created[:10] if created else '',
            'age_days': age_days,
            'depth': depth,
            'recommendation': self._recommend(age_days)
        }

    def _recommend(self, age_days: int) -> str:
        """Generate triage recommendation based on age."""
        if age_days < 30:
            return 'Keep'
        elif age_days < 180:
            return 'Review'
        elif age_days < 365:
            return 'Archive'
        else:
            return 'Delete'

    def scan_database(
        self,
        database_id: str,
        recommendation_filter: Optional[str] = None
    ) -> List[Dict]:
        """
        Scan all pages in a database and generate triage info.

        Args:
            database_id: Database to scan
            recommendation_filter: Only return pages with this recommendation
        """
        pages = self.client.query_database(database_id)

        results = []
        for page in pages:
            info = self._extract_page_info(page)
            if recommendation_filter is None or info['recommendation'] == recommendation_filter:
                results.append(info)

        return results

    def generate_report(self, items: List[Dict]) -> str:
        """Generate markdown triage report."""
        lines = [
            "# Triage Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"Total items: {len(items)}",
            "",
            "## Summary",
        ]

        # Count by recommendation
        counts = {}
        for item in items:
            rec = item['recommendation']
            counts[rec] = counts.get(rec, 0) + 1

        for rec, count in sorted(counts.items()):
            lines.append(f"- **{rec}**: {count}")

        lines.extend(["", "## Items by Recommendation", ""])

        # Group by recommendation
        by_rec = {}
        for item in items:
            rec = item['recommendation']
            if rec not in by_rec:
                by_rec[rec] = []
            by_rec[rec].append(item)

        for rec in ['Delete', 'Archive', 'Review', 'Keep']:
            if rec in by_rec:
                lines.append(f"### {rec}")
                for item in by_rec[rec][:20]:  # Limit to 20 per category
                    lines.append(f"- [{item['title']}]({item['url']}) - {item['age_days']} days old")
                if len(by_rec[rec]) > 20:
                    lines.append(f"  ... and {len(by_rec[rec]) - 20} more")
                lines.append("")

        return '\n'.join(lines)
