#!/usr/bin/env python3
"""
Writer Agent

Generates research documents with Chicago-style citations using Claude.
"""

import os
from typing import Dict, List, Optional, TYPE_CHECKING
from datetime import datetime
from pathlib import Path

if TYPE_CHECKING:
    from ..config import ResearchConfig
    from ..orchestrator import ResearchRequest, ResearchContext, GeneratedDocument
    from .prompt_builder import StructuredPrompt


class CitationManager:
    """Manages Chicago-style citations and bibliography."""

    def __init__(self):
        self.citations: List[Dict] = []
        self._counter = 0

    def add_citation(
        self,
        text: str,
        title: str,
        author: Optional[str] = None,
        url: Optional[str] = None,
        date: Optional[str] = None,
        source: Optional[str] = None,
    ) -> str:
        """
        Add a citation and return the footnote marker.

        Returns: Footnote number as superscript (e.g., "[^1]")
        """
        self._counter += 1
        self.citations.append({
            'number': self._counter,
            'text': text,
            'title': title,
            'author': author or "Grove Documentation",
            'url': url or "",
            'source': source or "",
            'date': date or datetime.now().strftime("%B %Y"),
        })
        return f"[^{self._counter}]"

    def add_from_rag_source(self, source: Dict) -> str:
        """Add citation from RAG search result."""
        return self.add_citation(
            text=source.get('snippet', '')[:100],
            title=source.get('title', 'Untitled'),
            author="Grove Documentation",
            url=source.get('url', ''),
            source=source.get('source', ''),
            date=source.get('date', ''),
        )

    def format_footnote(self, citation: Dict) -> str:
        """Format a single footnote in Chicago style."""
        parts = []

        # Author
        if citation.get('author'):
            parts.append(citation['author'])

        # Title in quotes
        parts.append(f'"{citation["title"]}"')

        # Source if available
        if citation.get('source'):
            parts.append(f"Grove Documentation ({citation['source']})")
        else:
            parts.append("Grove Documentation")

        # Date
        if citation.get('date'):
            parts.append(citation['date'])

        # URL
        if citation.get('url'):
            parts.append(citation['url'])

        return f"[^{citation['number']}]: {', '.join(filter(None, parts))}."

    def generate_footnotes(self) -> str:
        """Generate all footnotes section."""
        if not self.citations:
            return ""

        lines = ["", "---", "", "## Footnotes", ""]
        for citation in self.citations:
            lines.append(self.format_footnote(citation))

        return "\n".join(lines)

    def generate_bibliography(self) -> str:
        """Generate Chicago-style bibliography."""
        if not self.citations:
            return ""

        # Deduplicate by title
        seen_titles = set()
        unique_citations = []
        for c in self.citations:
            if c['title'] not in seen_titles:
                seen_titles.add(c['title'])
                unique_citations.append(c)

        # Sort by author/title
        sorted_citations = sorted(
            unique_citations,
            key=lambda c: (c.get('author', ''), c.get('title', ''))
        )

        lines = []
        for citation in sorted_citations:
            entry = []

            # Author
            author = citation.get('author', 'Grove Documentation')
            entry.append(author + ".")

            # Title in quotes
            entry.append(f'"{citation["title"]}."')

            # Source
            if citation.get('source'):
                entry.append(f"Grove Documentation ({citation['source']}),")
            else:
                entry.append("Grove Documentation,")

            # Date
            if citation.get('date'):
                entry.append(f"{citation['date']}.")

            # URL
            if citation.get('url'):
                entry.append(citation['url'])

            lines.append(" ".join(filter(None, entry)))

        return "\n\n".join(lines)


class Writer:
    """Generates research documents with citations using Claude."""

    def __init__(self, config: 'ResearchConfig' = None):
        self.config = config
        self.citation_manager = CitationManager()
        self._claude_client = None
        self._learning_agent = None

    @property
    def learning_agent(self):
        """Lazy load learning agent for editorial memory."""
        if self._learning_agent is None:
            try:
                from .learning import LearningAgent
                self._learning_agent = LearningAgent()
            except ImportError:
                self._learning_agent = None
        return self._learning_agent

    def _get_editorial_memory(self) -> str:
        """Get editorial memory summary for prompt injection."""
        if self.learning_agent:
            summary = self.learning_agent.get_memory_summary()
            if summary:
                return summary
        return ""

    @property
    def claude_client(self):
        """Lazy load Anthropic client."""
        if self._claude_client is None:
            try:
                import anthropic
                self._claude_client = anthropic.Anthropic()
            except ImportError:
                print("  anthropic package not installed")
                self._claude_client = None
            except Exception as e:
                print(f"  Failed to initialize Claude: {e}")
                self._claude_client = None
        return self._claude_client

    def generate(
        self,
        prompt: 'StructuredPrompt',
        context: 'ResearchContext',
        request: 'ResearchRequest',
    ) -> 'GeneratedDocument':
        """
        Generate research document from prompt and context.

        Uses Claude API if available, otherwise falls back to template.
        """
        from ..orchestrator import GeneratedDocument

        # Reset citation manager
        self.citation_manager = CitationManager()

        # Try Claude generation first
        if self.claude_client:
            print("  Using Claude for generation...")
            content = self._generate_with_claude(prompt, context, request)
        else:
            print("  Using template generation (Claude unavailable)...")
            content = self._generate_template(prompt, context, request)

        # Get footnotes and bibliography
        footnotes = self.citation_manager.generate_footnotes()
        bibliography = self.citation_manager.generate_bibliography()

        # Combine content with footnotes
        full_content = content
        if footnotes:
            full_content = content + footnotes

        title = request.topic or "Research Document"

        document = GeneratedDocument(
            title=title,
            content=full_content,
            citations=self.citation_manager.citations,
            bibliography=bibliography,
            format=request.format,
            word_count=len(full_content.split()),
        )

        return document

    def _generate_with_claude(
        self,
        prompt: 'StructuredPrompt',
        context: 'ResearchContext',
        request: 'ResearchRequest',
    ) -> str:
        """Generate document using Claude API."""

        # Load methodology
        methodology = self._load_methodology()

        # Load editorial memory (learned preferences from human edits)
        editorial_memory = self._get_editorial_memory()

        # Build context section from RAG results
        context_section = self._format_context_for_claude(context)

        # Build editorial guidance section
        editorial_section = ""
        if editorial_memory:
            editorial_section = f"""
## Editorial Preferences (Learned from Human Edits)
The following preferences have been learned from previous editorial feedback.
Apply these consistently:

{editorial_memory}
"""

        # Build the full prompt
        system_prompt = f"""You are an expert research writer for Grove, a distributed AI platform.

{methodology}

## Your Assignment
Generate a {request.format} document following the methodology above.

## Voice Standards
{chr(10).join(f"- {v}" for v in prompt.voice_standards)}
{editorial_section}
## Important
- Use Chicago-style footnotes for citations: [^1], [^2], etc.
- Include footnote definitions at the end
- Ground claims in the provided context
- Maintain Grove voice throughout
- Be concrete and specific, avoid buzzwords
"""

        user_prompt = f"""# Document Request

## Topic
{prompt.topic}

## Angle/Focus
{prompt.angle}

## Target Audience
{prompt.audience}

## Format
{request.format} ({prompt.length_guidance})

## Key Concepts to Address
{', '.join(prompt.key_concepts) if prompt.key_concepts else 'None specified'}

## Source Material
{prompt.draft_summary}

## User Direction
{prompt.user_direction}

{context_section}

---

Now write the {request.format} document. Start with the content directly (no preamble).
Include [^n] footnote markers for citations, and define them at the end.
"""

        try:
            response = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )

            content = response.content[0].text

            # Track citations from the generated content
            self._extract_citations_from_content(content, context)

            return content

        except Exception as e:
            print(f"  Claude API error: {e}")
            print("  Falling back to template...")
            return self._generate_template(prompt, context, request)

    def _load_methodology(self) -> str:
        """Load research methodology from prompts."""
        methodology_path = Path(__file__).parent.parent / "prompts" / "research_engine.md"
        if methodology_path.exists():
            return methodology_path.read_text(encoding="utf-8")
        return ""

    def _format_context_for_claude(self, context: 'ResearchContext') -> str:
        """Format RAG context for Claude prompt."""
        if not context.primary_sources and not context.related_sources:
            return "## Available Context\nNo additional Grove documentation context available."

        lines = ["## Available Context from Grove Documentation", ""]

        if context.primary_sources:
            lines.append("### Primary Sources")
            for i, src in enumerate(context.primary_sources[:5], 1):
                lines.append(f"\n**Source {i}: {src.get('title', 'Untitled')}**")
                lines.append(f"```")
                lines.append(src.get('snippet', '')[:400])
                lines.append(f"```")
            lines.append("")

        if context.related_sources:
            lines.append("### Related Sources")
            for i, src in enumerate(context.related_sources[:5], 1):
                lines.append(f"\n**Source {i}: {src.get('title', 'Untitled')}**")
                lines.append(f"```")
                lines.append(src.get('snippet', '')[:300])
                lines.append(f"```")

        return "\n".join(lines)

    def _extract_citations_from_content(self, content: str, context: 'ResearchContext') -> None:
        """Track citations referenced in generated content."""
        import re

        # Find all footnote markers
        footnotes = re.findall(r'\[\^(\d+)\]', content)
        used_numbers = set(int(n) for n in footnotes)

        # Map footnotes to sources
        all_sources = context.primary_sources + context.related_sources

        for num in sorted(used_numbers):
            if num <= len(all_sources):
                src = all_sources[num - 1]
                self.citation_manager.add_from_rag_source(src)
            else:
                # Generic citation if no matching source
                self.citation_manager.add_citation(
                    text="",
                    title=f"Reference {num}",
                    author="Grove Documentation",
                )

    def _generate_template(
        self,
        prompt: 'StructuredPrompt',
        context: 'ResearchContext',
        request: 'ResearchRequest',
    ) -> str:
        """Generate template document structure (fallback)."""
        lines = []

        # Introduction section
        lines.extend([
            "## Introduction",
            "",
            f"*[Draft introduction about {prompt.topic}]*",
            "",
            f"This {request.format} explores {prompt.angle}.",
            "",
        ])

        # Context from RAG (if available)
        if context.primary_sources:
            lines.extend([
                "## Background",
                "",
                "Drawing from Grove documentation:",
                "",
            ])
            for src in context.primary_sources[:3]:
                marker = self.citation_manager.add_from_rag_source(src)
                lines.append(f"- {src.get('snippet', '')[:200]}...{marker}")
            lines.append("")

        # Main content sections based on format
        if request.format == "blog":
            lines.extend(self._blog_template(prompt))
        elif request.format == "whitepaper":
            lines.extend(self._whitepaper_template(prompt))
        else:
            lines.extend(self._deep_dive_template(prompt))

        # Key concepts section
        if prompt.key_concepts:
            lines.extend([
                "## Key Concepts",
                "",
            ])
            for concept in prompt.key_concepts:
                lines.append(f"- **{concept}**: *[Define and explain]*")
            lines.append("")

        # Conclusion
        lines.extend([
            "## Conclusion",
            "",
            f"*[Summarize main points about {prompt.topic}]*",
            "",
        ])

        # Draft notes
        lines.extend([
            "---",
            "",
            "**Draft Notes (template mode - Claude unavailable):**",
            f"- Source material: {prompt.draft_summary}",
            f"- User direction: {prompt.user_direction}",
            f"- Target length: {prompt.length_guidance}",
            "",
        ])

        return "\n".join(lines)

    def _blog_template(self, prompt: 'StructuredPrompt') -> List[str]:
        """Template for blog post format."""
        return [
            "## The Core Insight",
            "",
            "*[Main argument or insight]*",
            "",
            "## Why This Matters",
            "",
            "*[Practical implications]*",
            "",
            "## What This Looks Like",
            "",
            "*[Concrete examples]*",
            "",
        ]

    def _whitepaper_template(self, prompt: 'StructuredPrompt') -> List[str]:
        """Template for whitepaper format."""
        return [
            "## Executive Summary",
            "",
            "*[Brief overview of findings]*",
            "",
            "## Problem Statement",
            "",
            "*[Define the problem being addressed]*",
            "",
            "## Analysis",
            "",
            "*[Detailed examination]*",
            "",
            "## Solution",
            "",
            "*[Proposed approach]*",
            "",
            "## Implications",
            "",
            "*[Broader impact]*",
            "",
        ]

    def _deep_dive_template(self, prompt: 'StructuredPrompt') -> List[str]:
        """Template for deep dive format."""
        return [
            "## Overview",
            "",
            "*[Set the stage]*",
            "",
            "## Historical Context",
            "",
            "*[How we got here]*",
            "",
            "## Technical Deep Dive",
            "",
            "*[Detailed exploration]*",
            "",
            "### Implementation Details",
            "",
            "*[Specifics]*",
            "",
            "### Trade-offs",
            "",
            "*[Considerations]*",
            "",
            "## Future Directions",
            "",
            "*[Where this leads]*",
            "",
        ]
