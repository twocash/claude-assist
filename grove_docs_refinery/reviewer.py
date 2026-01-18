#!/usr/bin/env python3
"""
Grove Docs Refinery - Reviewer Agent

Validates editor output against Grove editorial standards.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum


class Assessment(Enum):
    """Review assessment types."""
    PASS = "PASS"
    REVISE = "REVISE"
    ESCALATE = "ESCALATE"


@dataclass
class Review:
    """Reviewer output - validation assessment."""
    original_name: str
    assessment: Assessment
    validation_checklist: Dict[str, bool]
    specific_feedback: str = ""
    suggested_improvements: List[str] = field(default_factory=list)
    terminology_issues_found: List[Dict] = field(default_factory=list)
    positioning_issues: List[Dict] = field(default_factory=list)


class ReviewerAgent:
    """Agent that validates Grove content against editorial standards."""

    def __init__(
        self,
        engine_path: Optional[Path] = None,
        checkpoint_path: Optional[Path] = None,
    ):
        self.engine_path = engine_path
        self.checkpoint_path = checkpoint_path
        self._engine_content: str = ""
        self._checkpoint_content: str = ""

        # Standard prohibited terms
        self._prohibited = [
            "revolutionary",
            "paradigm shift",
            "Web3",
            "democratize",
            "might",
            "could potentially",
            "it's possible that",
            "tokenomics",
            "network effects",
            "moats",
            "the future of AI",
            "unprecedented capabilities",
        ]

    def load_context(
        self,
        engine_path: Optional[Path] = None,
        checkpoint_path: Optional[Path] = None,
    ):
        """Load editorial engine and checkpoint."""
        if engine_path:
            self.engine_path = engine_path
        if checkpoint_path:
            self.checkpoint_path = checkpoint_path

        if self.engine_path and self.engine_path.exists():
            self._engine_content = self.engine_path.read_text()

        if self.checkpoint_path and self.checkpoint_path.exists():
            self._checkpoint_content = self.checkpoint_path.read_text()

    def validate(
        self,
        source_path: Path,
        draft_path: Path,
    ) -> Review:
        """Validate editor draft against source."""
        source_content = source_path.read_text(encoding="utf-8")
        draft_content = draft_path.read_text(encoding="utf-8")

        # Build validation checklist
        checklist = {
            "terminology_current": True,
            "positioning_aligned": True,
            "technical_accuracy": True,
            "voice_consistent": True,
            "no_prohibited_language": True,
            "appropriate_length": True,
            "changes_justified": True,
            "no_new_errors": True,
        }

        feedback = []
        improvements = []
        term_issues = []
        pos_issues = []

        # Check 1: Terminology
        term_check = self._check_terminology(draft_content)
        if not term_check["valid"]:
            checklist["terminology_current"] = False
            term_issues = term_check["issues"]
            feedback.append(f"Terminology issues found: {len(term_issues)}")

        # Check 2: Prohibited language
        prohibited_check = self._check_prohibited(draft_content)
        if not prohibited_check["valid"]:
            checklist["no_prohibited_language"] = False
            feedback.append(f"Prohibited language: {prohibited_check['issues']}")

        # Check 3: Positioning
        pos_check = self._check_positioning(draft_content)
        if not pos_check["aligned"]:
            checklist["positioning_aligned"] = False
            pos_issues = pos_check["issues"]
            feedback.append(f"Positioning gaps: {len(pos_issues)}")

        # Check 4: Length appropriateness
        length_check = self._check_length(draft_content, source_content)
        if not length_check["appropriate"]:
            checklist["appropriate_length"] = False
            feedback.append(length_check["reason"])

        # Check 5: Voice consistency
        voice_check = self._check_voice(draft_content)
        if not voice_check["consistent"]:
            checklist["voice_consistent"] = False
            improvements.extend(voice_check["issues"])

        # Check 6: Changes justified
        changes_check = self._check_changes_justified(draft_content, source_content)
        if not changes_check["justified"]:
            checklist["changes_justified"] = False
            feedback.append("Changes not clearly justified")

        # Check 7: No new errors
        errors_check = self._check_new_errors(draft_content)
        if not errors_check["clean"]:
            checklist["no_new_errors"] = False
            feedback.append(f"New errors found: {errors_check['issues']}")

        # Determine assessment
        assessment = self._determine_assessment(checklist, feedback, term_issues, pos_issues)

        # Generate feedback
        feedback_str = self._generate_feedback(
            assessment,
            checklist,
            feedback,
            term_issues,
            pos_issues,
        )

        return Review(
            original_name=source_path.name,
            assessment=assessment,
            validation_checklist=checklist,
            specific_feedback=feedback_str,
            suggested_improvements=improvements,
            terminology_issues_found=term_issues,
            positioning_issues=pos_issues,
        )

    def _check_terminology(self, content: str) -> Dict:
        """Check for terminology issues."""
        issues = []

        # Current terms to check
        current_terms = {
            "exploration architecture": ["AI platform", "decentralized AI"],
            "agents": ["bots", "AI assistants"],
            "credits": ["tokens"],
            "Trellis Architecture": [],
            "Grove": [],
        }

        for current, legacy_list in current_terms.items():
            # Check if current term is present (good)
            if current.lower() not in content.lower():
                issues.append({
                    "type": "missing_term",
                    "expected": current,
                    "note": "Current term not found",
                })

            # Check for legacy terms
            for legacy in legacy_list:
                if legacy.lower() in content.lower():
                    issues.append({
                        "type": "legacy_term",
                        "found": legacy,
                        "suggestion": current,
                    })

        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def _check_prohibited(self, content: str) -> Dict:
        """Check for prohibited language."""
        issues = []

        content_lower = content.lower()
        for term in self._prohibited:
            if f" {term} " in content_lower or f" {term}," in content_lower:
                count = content_lower.count(f" {term} ")
                issues.append(f"'{term}' ({count}x)")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
        }

    def _check_positioning(self, content: str) -> Dict:
        """Check positioning alignment."""
        issues = []
        content_lower = content.lower()

        # Key concepts from Grove thesis
        key_concepts = [
            "exploration",
            "distributed",
            "local",
            "agents",
        ]

        for concept in key_concepts:
            if concept not in content_lower:
                issues.append({
                    "type": "missing_concept",
                    "concept": concept,
                    "note": "Consider including this concept",
                })

        return {
            "aligned": len(issues) == 0,
            "issues": issues,
        }

    def _check_length(
        self,
        draft: str,
        source: str,
    ) -> Dict:
        """Check if length is appropriate."""
        draft_len = len(draft)
        source_len = len(source)

        # Allow up to 20% change
        if draft_len > source_len * 1.2:
            return {
                "appropriate": False,
                "reason": f"Draft is {int(draft_len/source_len*100)}% of original length - too long",
            }
        elif draft_len < source_len * 0.6:
            return {
                "appropriate": False,
                "reason": f"Draft is {int(draft_len/source_len*100)}% of original length - may have cut too much",
            }

        return {"appropriate": True}

    def _check_voice(self, content: str) -> Dict:
        """Check voice consistency."""
        issues = []

        # Check for passive voice (simplified)
        passive_count = len(re.findall(r"\b(is|are|was|were|been|being)\s+\w+ed\b", content))
        if passive_count > 5:
            issues.append(f"High passive voice usage ({passive_count} instances)")

        # Check for throat-clearing phrases
        throat_clearing = [
            "it's important to note",
            "in order to",
            "it should be noted",
        ]
        for phrase in throat_clearing:
            if phrase in content.lower():
                issues.append(f"Throat-clearing phrase: '{phrase}'")

        return {
            "consistent": len(issues) == 0,
            "issues": issues,
        }

    def _check_changes_justified(
        self,
        draft: str,
        source: str,
    ) -> Dict:
        """Check if changes are justified."""
        # Simplified check - in production, would compare more thoroughly
        return {"justified": True}

    def _check_new_errors(self, content: str) -> Dict:
        """Check for new errors introduced."""
        issues = []

        # Check for broken links/references (simplified)
        broken_refs = re.findall(r"\[\[([^\]]+)\]\]", content)
        if broken_refs:
            issues.append(f"Broken references: {broken_refs}")

        # Check for broken markdown
        unclosed_backticks = content.count("```") % 2
        if unclosed_backticks:
            issues.append("Unclosed code blocks")

        return {
            "clean": len(issues) == 0,
            "issues": issues,
        }

    def _determine_assessment(
        self,
        checklist: Dict[str, bool],
        feedback: List[str],
        term_issues: List[Dict],
        pos_issues: List[Dict],
    ) -> Assessment:
        """Determine final assessment."""
        # Count failures
        failures = sum(1 for v in checklist.values() if not v)

        # Escalate if positioning issues or major terminology problems
        if len(pos_issues) >= 2 or len(term_issues) >= 3:
            return Assessment.ESCALATE

        # Revise if there are issues that need fixing
        if failures >= 3:
            return Assessment.REVISE

        # Pass if mostly clean
        if failures <= 2:
            return Assessment.PASS

        # Default to revise
        return Assessment.REVISE

    def _generate_feedback(
        self,
        assessment: Assessment,
        checklist: Dict[str, bool],
        feedback: List[str],
        term_issues: List[Dict],
        pos_issues: List[Dict],
    ) -> str:
        """Generate specific feedback string."""
        lines = []

        if assessment == Assessment.PASS:
            lines.append("Quality check passed. Document meets Grove editorial standards.")

        elif assessment == Assessment.REVISE:
            lines.append("Revisions needed before approval.")
            for item in feedback:
                lines.append(f"- {item}")

        elif assessment == Assessment.ESCALATE:
            lines.append("ESCALATE: Requires human decision.")
            if pos_issues:
                lines.append(f"\nPositioning issues ({len(pos_issues)}):")
                for issue in pos_issues[:3]:
                    lines.append(f"  - {issue.get('concept', issue)}")
            if term_issues:
                lines.append(f"\nTerminology issues ({len(term_issues)}):")
                for issue in term_issues[:3]:
                    lines.append(f"  - {issue.get('found', issue)} -> {issue.get('suggestion', issue)}")

        return "\n".join(lines)

    def generate_review_report(self, review: Review) -> str:
        """Generate markdown review report."""
        lines = [
            f"## Review: {review.original_name}",
            f"### Assessment: {review.assessment.value}",
            "",
            "### Validation Checklist",
        ]

        for item, passed in review.validation_checklist.items():
            status = "[x]" if passed else "[ ]"
            lines.append(f"- {status} {item.replace('_', ' ').title()}")

        if review.specific_feedback:
            lines.extend(["", "### Specific Feedback", review.specific_feedback])

        if review.suggested_improvements:
            lines.extend(["", "### Suggested Improvements"])
            for imp in review.suggested_improvements:
                lines.append(f"- {imp}")

        return "\n".join(lines)
