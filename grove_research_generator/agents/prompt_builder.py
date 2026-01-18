#!/usr/bin/env python3
"""
Prompt Builder Agent

Transforms draft content + user direction into structured research prompt.
"""

import re
from typing import Dict, List, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ..config import ResearchConfig
    from ..orchestrator import ResearchRequest


@dataclass
class StructuredPrompt:
    """Structured prompt for research document generation."""
    topic: str
    angle: str
    audience: str
    format: str
    length_guidance: str
    key_concepts: List[str]
    draft_summary: str
    user_direction: str
    voice_standards: List[str]

    def to_prompt(self) -> str:
        """Format as LLM prompt."""
        concepts_str = ", ".join(self.key_concepts) if self.key_concepts else "None identified"

        return f"""# Research Document Generation

## Assignment
Create a {self.format} about: **{self.topic}**

## Angle/Focus
{self.angle}

## Target Audience
{self.audience}

## Length Guidance
{self.length_guidance}

## Key Concepts to Address
{concepts_str}

## Source Material Summary
{self.draft_summary}

## User Direction
{self.user_direction}

## Voice Standards (Grove)
{chr(10).join(f"- {v}" for v in self.voice_standards)}

## Requirements
1. Use Chicago-style footnotes for citations
2. Include a bibliography at the end
3. Maintain Grove voice throughout
4. Ground claims in specific evidence
5. Acknowledge uncertainty where appropriate
"""


class PromptBuilder:
    """Builds structured prompts from draft content and user direction."""

    # Format-specific guidance
    FORMAT_GUIDANCE = {
        "blog": {
            "length": "800-1500 words",
            "style": "Conversational but informed, accessible to general readers",
            "structure": "Hook, context, main argument, examples, conclusion",
        },
        "whitepaper": {
            "length": "2000-4000 words",
            "style": "Technical depth with executive summary, evidence-heavy",
            "structure": "Abstract, problem statement, analysis, solution, implications",
        },
        "deep_dive": {
            "length": "3000-6000 words",
            "style": "Comprehensive exploration, thorough citations",
            "structure": "Introduction, multiple sections with subheadings, conclusion",
        },
    }

    # Grove voice standards
    VOICE_STANDARDS = [
        "Strategic, not smug",
        "Concrete over abstract",
        "Honest about uncertainty",
        "8th-grade accessibility, graduate-level thinking",
        "Active voice, present tense",
    ]

    def __init__(self, config: 'ResearchConfig' = None):
        self.config = config

    def build(self, request: 'ResearchRequest') -> StructuredPrompt:
        """Build structured prompt from research request."""
        # Extract key concepts from draft
        key_concepts = self._extract_concepts(request.draft_content)

        # Determine angle from user direction
        angle = self._extract_angle(request.user_direction)

        # Get format guidance
        format_info = self.FORMAT_GUIDANCE.get(request.format, self.FORMAT_GUIDANCE["blog"])

        # Summarize draft content
        draft_summary = self._summarize_draft(request.draft_content)

        return StructuredPrompt(
            topic=request.topic or self._infer_topic(request.draft_content, request.user_direction),
            angle=angle,
            audience=request.audience,
            format=request.format,
            length_guidance=format_info["length"],
            key_concepts=key_concepts,
            draft_summary=draft_summary,
            user_direction=request.user_direction,
            voice_standards=self.config.voice_standards if self.config else self.VOICE_STANDARDS,
        )

    def _extract_concepts(self, content: str) -> List[str]:
        """Extract key concepts from draft content."""
        concepts = []

        # Look for Grove-specific terminology
        grove_terms = [
            "Trellis", "Grove", "Foundation", "Terminal",
            "Observer", "Agent", "DEX", "Exploration",
            "Credits", "Ratchet", "Distributed Inference",
        ]

        content_lower = content.lower()
        for term in grove_terms:
            if term.lower() in content_lower:
                concepts.append(term)

        # Extract capitalized phrases (potential concepts)
        cap_phrases = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b', content)
        for phrase in cap_phrases[:5]:  # Limit to top 5
            if phrase not in concepts:
                concepts.append(phrase)

        return concepts[:10]  # Limit total

    def _extract_angle(self, direction: str) -> str:
        """Extract the angle/focus from user direction."""
        # Look for "focus on" pattern
        focus_match = re.search(r'focus on\s+([^,\.]+)', direction, re.IGNORECASE)
        if focus_match:
            return focus_match.group(1).strip()

        # Look for "about" pattern
        about_match = re.search(r'about\s+([^,\.]+)', direction, re.IGNORECASE)
        if about_match:
            return about_match.group(1).strip()

        # Default to the direction itself (cleaned up)
        cleaned = re.sub(r'@atlas\s*', '', direction, flags=re.IGNORECASE).strip()
        return cleaned[:200] if len(cleaned) > 200 else cleaned

    def _infer_topic(self, content: str, direction: str) -> str:
        """Infer topic from content and direction."""
        # Try to get from direction first
        about_match = re.search(r'about\s+([^,\.]+)', direction, re.IGNORECASE)
        if about_match:
            return about_match.group(1).strip()

        # Fall back to first heading in content
        heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if heading_match:
            return heading_match.group(1).strip()

        # Fall back to first sentence
        first_sentence = content.split('.')[0][:100] if content else "Untitled Topic"
        return first_sentence

    def _summarize_draft(self, content: str) -> str:
        """Create a summary of the draft content."""
        if not content:
            return "No draft content provided."

        # Word count
        word_count = len(content.split())

        # Extract headings
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)

        # First paragraph
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        first_para = paragraphs[0][:300] if paragraphs else ""

        summary_parts = [
            f"Draft contains {word_count} words.",
        ]

        if headings:
            summary_parts.append(f"Sections: {', '.join(headings[:5])}")

        if first_para:
            summary_parts.append(f"Opens with: \"{first_para}...\"")

        return " ".join(summary_parts)
