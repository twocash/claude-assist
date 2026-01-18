#!/usr/bin/env python3
"""
Grove Research Generator - Main Orchestrator

Orchestrates the research document generation pipeline:
1. Parse user direction from @atlas comment
2. Build structured prompt from draft + direction
3. Query LEANN RAG for context
4. Generate document with Chicago citations
5. Post draft to Notion for review
6. On completion trigger, validate and file
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

from .config import get_config, ResearchConfig


@dataclass
class ResearchRequest:
    """Parsed research request from Notion."""
    page_id: str
    draft_content: str
    user_direction: str
    topic: Optional[str] = None
    format: str = "blog"  # blog, whitepaper, deep_dive
    audience: str = "general"
    requested_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ResearchContext:
    """Context gathered from LEANN RAG."""
    primary_sources: List[Dict] = field(default_factory=list)
    related_sources: List[Dict] = field(default_factory=list)
    context_summary: str = ""

    def to_prompt_section(self) -> str:
        """Format context for inclusion in prompt."""
        if not self.primary_sources and not self.related_sources:
            return "No additional Grove context available."

        lines = ["## Grove Context (from RAG retrieval)", ""]

        if self.primary_sources:
            lines.append("### Primary Sources")
            for src in self.primary_sources[:5]:
                lines.append(f"- **{src.get('title', 'Untitled')}**: {src.get('snippet', '')[:200]}...")
            lines.append("")

        if self.related_sources:
            lines.append("### Related Sources")
            for src in self.related_sources[:5]:
                lines.append(f"- {src.get('title', 'Untitled')}: {src.get('snippet', '')[:100]}...")

        return "\n".join(lines)


@dataclass
class GeneratedDocument:
    """Output from document generation."""
    title: str
    content: str
    citations: List[Dict] = field(default_factory=list)
    bibliography: str = ""
    format: str = "blog"
    word_count: int = 0

    def to_markdown(self) -> str:
        """Format as complete markdown document."""
        lines = [
            f"# {self.title}",
            "",
            self.content,
        ]

        if self.bibliography:
            lines.extend([
                "",
                "---",
                "",
                "## Bibliography",
                "",
                self.bibliography,
            ])

        return "\n".join(lines)


@dataclass
class ValidationResult:
    """Result of document validation."""
    status: str  # PASS, REVISE, ESCALATE
    feedback: str = ""
    issues: List[str] = field(default_factory=list)
    destination: Optional[str] = None  # Where to file on PASS


class ResearchOrchestrator:
    """Main orchestrator for research document generation."""

    def __init__(self, config: Optional[ResearchConfig] = None):
        self.config = config or get_config()
        self.config.ensure_directories()

        # Lazy-loaded agents
        self._prompt_builder = None
        self._researcher = None
        self._writer = None
        self._reviewer = None

    @property
    def prompt_builder(self):
        """Lazy load prompt builder agent."""
        if self._prompt_builder is None:
            from .agents.prompt_builder import PromptBuilder
            self._prompt_builder = PromptBuilder(self.config)
        return self._prompt_builder

    @property
    def researcher(self):
        """Lazy load researcher agent."""
        if self._researcher is None:
            from .agents.researcher import Researcher
            self._researcher = Researcher(self.config)
        return self._researcher

    @property
    def writer(self):
        """Lazy load writer agent."""
        if self._writer is None:
            from .agents.writer import Writer
            self._writer = Writer(self.config)
        return self._writer

    @property
    def reviewer(self):
        """Lazy load reviewer agent."""
        if self._reviewer is None:
            from .agents.reviewer import Reviewer
            self._reviewer = Reviewer(self.config)
        return self._reviewer

    def parse_research_request(
        self,
        page_id: str,
        draft_content: str,
        comment_text: str,
    ) -> ResearchRequest:
        """Parse @atlas comment into structured research request."""
        # Extract format hints
        format_type = "blog"
        if "white paper" in comment_text.lower() or "whitepaper" in comment_text.lower():
            format_type = "whitepaper"
        elif "deep dive" in comment_text.lower():
            format_type = "deep_dive"

        # Extract topic if mentioned
        topic = None
        topic_match = re.search(r'about\s+([^,\.]+)', comment_text, re.IGNORECASE)
        if topic_match:
            topic = topic_match.group(1).strip()

        return ResearchRequest(
            page_id=page_id,
            draft_content=draft_content,
            user_direction=comment_text,
            topic=topic,
            format=format_type,
        )

    def generate_document(
        self,
        request: ResearchRequest,
        use_rag: bool = True,
    ) -> GeneratedDocument:
        """
        Main pipeline: generate research document from request.

        Steps:
        1. Build structured prompt
        2. Query LEANN RAG for context
        3. Generate document with citations
        """
        print(f"Generating {request.format} document...")

        # Step 1: Build structured prompt
        print("  Building structured prompt...")
        prompt = self.prompt_builder.build(request)

        # Step 2: Query LEANN RAG for context
        context = ResearchContext()
        if use_rag and self.config.leann_index_path:
            print("  Querying LEANN RAG for context...")
            context = self.researcher.get_context(request)

        # Step 3: Generate document
        print("  Generating document...")
        document = self.writer.generate(prompt, context, request)

        print(f"  Generated: {document.word_count} words")
        return document

    def validate_document(
        self,
        document: GeneratedDocument,
        request: ResearchRequest,
    ) -> ValidationResult:
        """Validate document against Grove standards."""
        print("  Validating document...")
        return self.reviewer.validate(document, request)

    def run_pipeline(
        self,
        page_id: str,
        draft_content: str,
        comment_text: str,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Run full pipeline from @atlas trigger to document generation.

        Returns dict with:
        - request: parsed ResearchRequest
        - document: GeneratedDocument
        - validation: ValidationResult (if not dry_run)
        """
        # Parse request
        request = self.parse_research_request(page_id, draft_content, comment_text)

        # Generate document
        document = self.generate_document(request)

        result = {
            "request": request,
            "document": document,
            "markdown": document.to_markdown(),
        }

        if not dry_run:
            # Validate
            validation = self.validate_document(document, request)
            result["validation"] = validation

        return result

    def handle_completion(
        self,
        page_id: str,
        final_content: str,
    ) -> Dict[str, Any]:
        """
        Handle @atlas completion trigger.

        Validates and files the final document.
        """
        # Create a minimal request for validation
        request = ResearchRequest(
            page_id=page_id,
            draft_content=final_content,
            user_direction="completion",
        )

        # Create document from final content
        document = GeneratedDocument(
            title=self._extract_title(final_content),
            content=final_content,
            word_count=len(final_content.split()),
        )

        # Validate
        validation = self.reviewer.validate(document, request)

        return {
            "document": document,
            "validation": validation,
            "status": validation.status,
        }

    def _extract_title(self, content: str) -> str:
        """Extract title from markdown content."""
        for line in content.split("\n"):
            if line.startswith("# "):
                return line[2:].strip()
        return "Untitled Document"
