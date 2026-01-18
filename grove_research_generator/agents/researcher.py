#!/usr/bin/env python3
"""
Researcher Agent

Queries LEANN RAG for Grove context and synthesizes sources.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import ResearchConfig
    from ..orchestrator import ResearchRequest, ResearchContext

# Add LEANN to path
LEANN_PATH = Path(__file__).parent.parent.parent / "leann-repo" / "packages" / "leann-core" / "src"
if LEANN_PATH.exists():
    sys.path.insert(0, str(LEANN_PATH))


class Researcher:
    """Retrieves context from LEANN RAG for research documents."""

    # Grove terminology for concept extraction
    GROVE_TERMS = [
        "Trellis", "Trellis Architecture",
        "Grove", "Grove Foundation",
        "Foundation", "Terminal",
        "Observer", "Agent",
        "DEX", "Declarative Exploration",
        "Exploration Architecture",
        "Credits", "Ratchet",
        "Distributed Inference",
        "Foundation Loop",
    ]

    def __init__(self, config: 'ResearchConfig' = None):
        self.config = config
        self._searcher = None
        self._index_path = None

    @property
    def index_path(self) -> Optional[Path]:
        """Get the LEANN index path."""
        if self._index_path is None:
            # Try config first
            if self.config and self.config.leann_index_path:
                self._index_path = self.config.leann_index_path
            else:
                # Default location
                default = Path(__file__).parent.parent / "grove-knowledge.leann"
                if default.exists():
                    self._index_path = default
        return self._index_path

    @property
    def searcher(self):
        """Lazy load LEANN searcher."""
        if self._searcher is None and self.index_path:
            try:
                from leann import LeannSearcher
                self._searcher = LeannSearcher(str(self.index_path))
                print(f"  LEANN index loaded: {self.index_path}")
            except ImportError:
                print("  LEANN not installed - RAG disabled")
                self._searcher = None
            except Exception as e:
                print(f"  Failed to load LEANN index: {e}")
                self._searcher = None
        return self._searcher

    def get_context(self, request: 'ResearchRequest') -> 'ResearchContext':
        """
        Query LEANN for relevant Grove context.

        Returns ResearchContext with primary and related sources.
        """
        from ..orchestrator import ResearchContext

        context = ResearchContext()

        if not self.searcher:
            print("  No LEANN index available - skipping RAG")
            return context

        # Query for primary topic
        if request.topic:
            print(f"  Searching for: {request.topic}")
            primary_results = self._search(request.topic, top_k=10)
            context.primary_sources = self._format_results(primary_results)
            print(f"  Found {len(context.primary_sources)} primary sources")

        # Query for key concepts from draft
        concepts = self._extract_concepts(request.draft_content)
        if concepts:
            print(f"  Searching for concepts: {', '.join(concepts[:3])}")
            for concept in concepts[:3]:  # Limit queries
                related = self._search(concept, top_k=5)
                context.related_sources.extend(self._format_results(related))

        # Deduplicate related sources
        context.related_sources = self._deduplicate(context.related_sources)
        print(f"  Found {len(context.related_sources)} related sources")

        # Generate context summary
        context.context_summary = self._summarize_context(context)

        return context

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Direct search interface for external use.

        Returns list of dicts with title, snippet, url, score.
        """
        if not self.searcher:
            return []

        results = self._search(query, top_k)
        return self._format_results(results)

    def _search(self, query: str, top_k: int = 10) -> List:
        """Execute LEANN search."""
        if not self.searcher:
            return []

        try:
            results = self.searcher.search(query, top_k=top_k)
            return results
        except Exception as e:
            print(f"  Search error: {e}")
            return []

    def _format_results(self, results: List) -> List[Dict]:
        """Format LEANN results for context."""
        formatted = []
        for r in results:
            # Extract metadata
            metadata = getattr(r, 'metadata', {}) or {}

            formatted.append({
                'title': metadata.get('title', 'Untitled'),
                'source': metadata.get('source', ''),
                'path': metadata.get('path', ''),
                'url': self._generate_url(metadata),
                'date': metadata.get('date', ''),
                'snippet': getattr(r, 'text', '')[:500],
                'score': getattr(r, 'score', 0.0),
            })
        return formatted

    def _generate_url(self, metadata: Dict) -> str:
        """Generate URL/reference for a source."""
        if metadata.get('url'):
            return metadata['url']
        if metadata.get('source'):
            return f"grove://docs/{metadata['source']}"
        if metadata.get('path'):
            return f"file://{metadata['path']}"
        return ""

    def _deduplicate(self, sources: List[Dict]) -> List[Dict]:
        """Remove duplicate sources."""
        seen = set()
        unique = []
        for src in sources:
            # Use title + source as unique key
            key = (src.get('title', ''), src.get('source', ''))
            if key not in seen:
                seen.add(key)
                unique.append(src)
        return unique[:10]  # Limit total

    def _extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts for related queries."""
        concepts = []
        content_lower = content.lower()

        for term in self.GROVE_TERMS:
            if term.lower() in content_lower:
                concepts.append(term)

        # Also extract capitalized phrases
        cap_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b', content)
        for phrase in cap_phrases[:3]:
            if phrase not in concepts:
                concepts.append(phrase)

        return concepts[:5]

    def _summarize_context(self, context: 'ResearchContext') -> str:
        """Generate summary of retrieved context."""
        total = len(context.primary_sources) + len(context.related_sources)
        if total == 0:
            return "No additional context retrieved from Grove knowledge base."

        parts = []
        if context.primary_sources:
            titles = [s['title'] for s in context.primary_sources[:3]]
            parts.append(f"{len(context.primary_sources)} primary sources including: {', '.join(titles)}")
        if context.related_sources:
            parts.append(f"{len(context.related_sources)} related sources")

        return f"Retrieved {' and '.join(parts)} from Grove knowledge base."
