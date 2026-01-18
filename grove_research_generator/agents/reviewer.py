#!/usr/bin/env python3
"""
Reviewer Agent

Validates research documents against Grove standards.
"""

import re
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..config import ResearchConfig
    from ..orchestrator import ResearchRequest, GeneratedDocument, ValidationResult


class Reviewer:
    """Validates research documents against Grove standards."""

    # Terms to avoid in Grove voice
    TERMS_TO_AVOID = [
        "revolutionary",
        "paradigm shift",
        "Web3",
        "democratize",
        "might",
        "could potentially",
        "it's possible that",
        "It's important to note that",
        "In order to",
        "tokenomics",
        "network effects",
        "moats",
        "the future of AI",
        "unprecedented capabilities",
        "game-changer",
        "disruptive",
        "synergy",
        "leverage",
        "utilize",
    ]

    # Required elements by format
    REQUIRED_ELEMENTS = {
        "blog": ["introduction", "conclusion"],
        "whitepaper": ["executive summary", "problem", "solution"],
        "deep_dive": ["overview", "deep dive", "conclusion"],
    }

    def __init__(self, config: 'ResearchConfig' = None):
        self.config = config

    def validate(
        self,
        document: 'GeneratedDocument',
        request: 'ResearchRequest',
    ) -> 'ValidationResult':
        """
        Validate document against Grove standards.

        Checks:
        1. Voice standards (avoid certain terms)
        2. Required structural elements
        3. Citation presence
        4. Word count guidelines
        """
        from ..orchestrator import ValidationResult

        issues = []

        # Check voice
        voice_issues = self._check_voice(document.content)
        issues.extend(voice_issues)

        # Check structure
        structure_issues = self._check_structure(document.content, request.format)
        issues.extend(structure_issues)

        # Check citations
        citation_issues = self._check_citations(document)
        issues.extend(citation_issues)

        # Check word count
        word_count_issues = self._check_word_count(document, request.format)
        issues.extend(word_count_issues)

        # Determine status
        critical_issues = [i for i in issues if i.startswith("[CRITICAL]")]
        warning_issues = [i for i in issues if i.startswith("[WARNING]")]

        if critical_issues:
            status = "ESCALATE"
        elif len(warning_issues) > 3:
            status = "REVISE"
        elif warning_issues:
            status = "PASS"  # Minor issues, still passable
        else:
            status = "PASS"

        # Determine destination based on format
        destination = self._determine_destination(request.format)

        feedback = self._generate_feedback(issues)

        return ValidationResult(
            status=status,
            feedback=feedback,
            issues=issues,
            destination=destination,
        )

    def _check_voice(self, content: str) -> List[str]:
        """Check for voice standard violations."""
        issues = []
        content_lower = content.lower()

        for term in self.TERMS_TO_AVOID:
            if term.lower() in content_lower:
                # Find the context
                idx = content_lower.find(term.lower())
                context = content[max(0, idx-20):idx+len(term)+20]
                issues.append(f"[WARNING] Avoid term '{term}': \"...{context}...\"")

        return issues

    def _check_structure(self, content: str, format_type: str) -> List[str]:
        """Check for required structural elements."""
        issues = []
        content_lower = content.lower()

        required = self.REQUIRED_ELEMENTS.get(format_type, [])
        for element in required:
            # Check for heading containing the element
            pattern = rf'#+\s+.*{element}.*'
            if not re.search(pattern, content_lower):
                issues.append(f"[WARNING] Missing section: {element}")

        return issues

    def _check_citations(self, document: 'GeneratedDocument') -> List[str]:
        """Check citation requirements."""
        issues = []

        # Check for footnote markers in content
        footnote_pattern = r'\[\^(\d+)\]'
        footnotes_in_content = re.findall(footnote_pattern, document.content)

        if not footnotes_in_content:
            issues.append("[WARNING] No citations found in document")

        # Check citation count aligns
        if len(document.citations) == 0 and len(footnotes_in_content) > 0:
            issues.append("[CRITICAL] Footnote markers present but no citations tracked")

        return issues

    def _check_word_count(self, document: 'GeneratedDocument', format_type: str) -> List[str]:
        """Check word count against guidelines."""
        issues = []

        # Guidelines by format
        guidelines = {
            "blog": (800, 1500),
            "whitepaper": (2000, 4000),
            "deep_dive": (3000, 6000),
        }

        min_words, max_words = guidelines.get(format_type, (500, 5000))

        if document.word_count < min_words:
            issues.append(
                f"[WARNING] Document too short: {document.word_count} words "
                f"(minimum {min_words} for {format_type})"
            )
        elif document.word_count > max_words:
            issues.append(
                f"[WARNING] Document too long: {document.word_count} words "
                f"(maximum {max_words} for {format_type})"
            )

        return issues

    def _determine_destination(self, format_type: str) -> str:
        """Determine filing destination based on format."""
        destinations = {
            "blog": "Grove Blog",
            "whitepaper": "Grove Research",
            "deep_dive": "Grove Documentation",
        }
        return destinations.get(format_type, "Grove Content")

    def _generate_feedback(self, issues: List[str]) -> str:
        """Generate human-readable feedback."""
        if not issues:
            return "Document passes all validation checks."

        lines = ["Validation found the following issues:", ""]

        critical = [i for i in issues if i.startswith("[CRITICAL]")]
        warnings = [i for i in issues if i.startswith("[WARNING]")]

        if critical:
            lines.append("**Critical Issues (must fix):**")
            for issue in critical:
                lines.append(f"- {issue.replace('[CRITICAL] ', '')}")
            lines.append("")

        if warnings:
            lines.append("**Warnings (should address):**")
            for issue in warnings:
                lines.append(f"- {issue.replace('[WARNING] ', '')}")

        return "\n".join(lines)
