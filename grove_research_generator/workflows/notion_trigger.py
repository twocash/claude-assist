#!/usr/bin/env python3
"""
Notion Trigger Workflow

Full implementation of the @atlas research pipeline:
1. Detect @atlas research requests
2. Generate documents with Claude + RAG
3. Post drafts to Notion
4. Detect @atlas completion triggers
5. Analyze diffs and learn from edits
6. File completed documents
"""

import re
import os
from typing import List, Optional, Dict
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_config, ResearchConfig, DatabaseConfig
from draft_storage import DraftStorage
from agents.learning import LearningAgent


class NotionTriggerWorkflow:
    """
    Full workflow for @atlas research requests.

    Handles the complete lifecycle:
    - Research request detection
    - Document generation
    - Notion posting
    - Completion detection
    - Editorial learning
    """

    def __init__(self, config: Optional[ResearchConfig] = None):
        self.config = config or get_config()
        self.draft_storage = DraftStorage()
        self.learning_agent = LearningAgent()

        # Will be initialized when needed
        self._notion_client = None
        self._orchestrator = None

    @property
    def notion_client(self):
        """Lazy load Notion client from notion_pipeline."""
        if self._notion_client is None:
            try:
                pipeline_path = Path(__file__).parent.parent.parent / "notion_pipeline"
                sys.path.insert(0, str(pipeline_path))
                from notion_pipeline import NotionClient
                self._notion_client = NotionClient()
            except ImportError as e:
                print(f"notion_pipeline not available: {e}")
                self._notion_client = None
        return self._notion_client

    @property
    def orchestrator(self):
        """Lazy load the research orchestrator."""
        if self._orchestrator is None:
            from orchestrator import ResearchOrchestrator
            self._orchestrator = ResearchOrchestrator()
        return self._orchestrator

    # =========================================================================
    # Research Request Detection
    # =========================================================================

    def check_for_research_requests(self, page_ids: Optional[List[str]] = None) -> List[Dict]:
        """
        Scan pages for @atlas research triggers.

        Args:
            page_ids: Optional list of page IDs to check. If None, scans recent activity.

        Returns:
            List of dicts with:
            - page_id: Notion page ID
            - comment_text: The trigger comment
            - draft_content: Page content to transform
        """
        if not self.notion_client:
            print("Notion client not available")
            return []

        requests = []

        # If no specific pages, check The Grove page for recent comments
        if page_ids is None:
            page_ids = [DatabaseConfig.THE_GROVE_PAGE]

        for page_id in page_ids:
            try:
                # Get comments on this page
                comments = self._get_page_comments(page_id)

                for comment in comments:
                    if self._matches_research_pattern(comment.get('text', '')):
                        # Found a research request
                        content = self._get_page_content(page_id)
                        requests.append({
                            'page_id': page_id,
                            'comment_id': comment.get('id'),
                            'comment_text': comment.get('text'),
                            'draft_content': content,
                            'detected_at': datetime.now().isoformat()
                        })

            except Exception as e:
                print(f"Error checking page {page_id}: {e}")

        return requests

    def check_for_completion_triggers(self) -> List[Dict]:
        """
        Scan pending drafts for @atlas completion triggers.

        Returns:
            List of dicts with:
            - page_id: Notion page ID
            - original_content: The original AI-generated draft
            - edited_content: Current page content (human-edited)
        """
        if not self.notion_client:
            print("Notion client not available")
            return []

        completions = []

        # Check all pending drafts
        pending = self.draft_storage.get_pending_drafts()

        for page_id in pending:
            try:
                comments = self._get_page_comments(page_id)

                for comment in comments:
                    if self._matches_completion_pattern(comment.get('text', '')):
                        # Found a completion trigger
                        stored = self.draft_storage.get_draft(page_id)
                        edited = self._get_page_content(page_id)

                        if stored:
                            completions.append({
                                'page_id': page_id,
                                'original_content': stored.original_content,
                                'edited_content': edited,
                                'topic': stored.topic,
                                'format': stored.format
                            })

            except Exception as e:
                print(f"Error checking completion for {page_id}: {e}")

        return completions

    # =========================================================================
    # Document Generation & Posting
    # =========================================================================

    def process_research_request(self, request: Dict, dry_run: bool = False) -> Dict:
        """
        Process a research request through the full pipeline.

        Args:
            request: Dict with page_id, comment_text, draft_content
            dry_run: If True, don't post to Notion

        Returns:
            Dict with generation results
        """
        page_id = request['page_id']
        comment_text = request['comment_text']
        draft_content = request.get('draft_content', '')

        print(f"Processing research request for page {page_id}")
        print(f"Direction: {comment_text}")

        # Run the orchestrator
        result = self.orchestrator.run_pipeline(
            page_id=page_id,
            draft_content=draft_content,
            comment_text=comment_text,
            dry_run=dry_run
        )

        if result.get('status') == 'success' and not dry_run:
            document = result.get('document', '')
            topic = result.get('topic', 'Research Document')

            # Store the original draft for later comparison
            self.draft_storage.store_draft(
                page_id=page_id,
                content=document,
                topic=topic,
                format=result.get('format', 'blog')
            )

            # Post to Notion
            posted = self.post_draft_to_page(page_id, document)
            result['posted'] = posted

            if posted:
                self.add_completion_comment(
                    page_id,
                    "Draft ready! Edit directly in the page, then comment '@atlas this is complete' when done."
                )

        return result

    def post_draft_to_page(self, page_id: str, markdown: str) -> bool:
        """
        Post generated draft to Notion page.

        Args:
            page_id: The Notion page ID
            markdown: The markdown content to post

        Returns:
            True if successful
        """
        if not self.notion_client:
            print("Notion client not available")
            return False

        try:
            # Use notion_pipeline's update method
            self.notion_client.update_page_content(page_id, markdown)
            print(f"Posted draft to page {page_id} ({len(markdown)} chars)")
            return True
        except Exception as e:
            print(f"Error posting to Notion: {e}")
            return False

    def add_completion_comment(self, page_id: str, message: str) -> bool:
        """Add comment to page indicating draft is ready."""
        if not self.notion_client:
            print("Notion client not available")
            return False

        try:
            self.notion_client.add_comment(page_id, message)
            print(f"Added comment to page {page_id}")
            return True
        except Exception as e:
            print(f"Error adding comment: {e}")
            return False

    # =========================================================================
    # Completion & Learning
    # =========================================================================

    def process_completion(self, completion: Dict) -> Dict:
        """
        Process a completion trigger - analyze diffs and learn.

        Args:
            completion: Dict with page_id, original_content, edited_content

        Returns:
            Dict with learning results
        """
        page_id = completion['page_id']
        original = completion['original_content']
        edited = completion['edited_content']
        topic = completion.get('topic', 'Unknown')

        print(f"Processing completion for {page_id}")

        # Mark draft as complete
        self.draft_storage.mark_complete(page_id, edited)

        # Analyze diff and learn
        source_doc = f"{topic} ({page_id})"
        analysis = self.learning_agent.analyze_diff(original, edited, source_doc)

        # Update editorial memory
        if analysis.total_changes > 0:
            self.learning_agent.update_memory(analysis)
            print(f"Extracted {analysis.total_changes} learnings from edits")

        # Mark as analyzed
        self.draft_storage.mark_analyzed(page_id, analysis.total_changes)

        # Add confirmation comment
        if self.notion_client:
            msg = f"Document complete! Extracted {analysis.total_changes} editorial learnings."
            self.add_completion_comment(page_id, msg)

        return {
            'status': 'success',
            'page_id': page_id,
            'learnings_extracted': analysis.total_changes,
            'terminology_changes': len(analysis.terminology_changes),
            'voice_changes': len(analysis.voice_changes),
            'added_concepts': len(analysis.added_concepts),
            'structural_changes': len(analysis.structural_changes),
            'phrasing_changes': len(analysis.phrasing_changes)
        }

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _get_page_comments(self, page_id: str) -> List[Dict]:
        """Get comments from a Notion page."""
        if not self.notion_client:
            return []

        try:
            return self.notion_client.get_comments(page_id)
        except Exception as e:
            print(f"Error getting comments: {e}")
            return []

    def _get_page_content(self, page_id: str) -> str:
        """Get content from a Notion page."""
        if not self.notion_client:
            return ""

        try:
            return self.notion_client.get_page_content(page_id)
        except Exception as e:
            print(f"Error getting page content: {e}")
            return ""

    def _matches_research_pattern(self, text: str) -> bool:
        """Check if text matches research trigger patterns."""
        for pattern in self.config.research_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def _matches_completion_pattern(self, text: str) -> bool:
        """Check if text matches completion trigger patterns."""
        for pattern in self.config.completion_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    # =========================================================================
    # Full Workflow Run
    # =========================================================================

    def run_full_cycle(self, dry_run: bool = False) -> Dict:
        """
        Run a full cycle: check requests, generate, check completions, learn.

        Args:
            dry_run: If True, don't post to Notion

        Returns:
            Summary of actions taken
        """
        results = {
            'research_requests_found': 0,
            'research_requests_processed': 0,
            'completions_found': 0,
            'completions_processed': 0,
            'learnings_extracted': 0
        }

        # Check for new research requests
        print("Checking for research requests...")
        requests = self.check_for_research_requests()
        results['research_requests_found'] = len(requests)

        for request in requests:
            try:
                self.process_research_request(request, dry_run=dry_run)
                results['research_requests_processed'] += 1
            except Exception as e:
                print(f"Error processing request: {e}")

        # Check for completions
        print("\nChecking for completion triggers...")
        completions = self.check_for_completion_triggers()
        results['completions_found'] = len(completions)

        for completion in completions:
            try:
                result = self.process_completion(completion)
                results['completions_processed'] += 1
                results['learnings_extracted'] += result.get('learnings_extracted', 0)
            except Exception as e:
                print(f"Error processing completion: {e}")

        return results


# =============================================================================
# CLI Entry Points
# =============================================================================

def run_trigger_check():
    """CLI entry point for trigger checking."""
    workflow = NotionTriggerWorkflow()

    print("Checking for research requests...")
    requests = workflow.check_for_research_requests()
    print(f"Found {len(requests)} research requests")

    for req in requests:
        print(f"  - Page: {req['page_id']}")
        print(f"    Direction: {req['comment_text'][:80]}...")

    print("\nChecking for completion triggers...")
    completions = workflow.check_for_completion_triggers()
    print(f"Found {len(completions)} completion triggers")


def run_full_cycle(dry_run: bool = True):
    """Run a full workflow cycle."""
    workflow = NotionTriggerWorkflow()
    results = workflow.run_full_cycle(dry_run=dry_run)

    print("\n=== Cycle Complete ===")
    print(f"Research requests: {results['research_requests_processed']}/{results['research_requests_found']}")
    print(f"Completions: {results['completions_processed']}/{results['completions_found']}")
    print(f"Learnings extracted: {results['learnings_extracted']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Notion trigger workflow")
    parser.add_argument('--check', action='store_true', help='Check for triggers only')
    parser.add_argument('--run', action='store_true', help='Run full cycle')
    parser.add_argument('--live', action='store_true', help='Post to Notion (default: dry run)')

    args = parser.parse_args()

    if args.run:
        run_full_cycle(dry_run=not args.live)
    else:
        run_trigger_check()
