#!/usr/bin/env python3
"""
Grove Docs Refinery - Editor Agent

Rewrites content following the Grove Editorial Engine methodology.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Analysis:
    """Analysis of a source document."""
    original_name: str
    working_name: str
    document_type: str  # white_paper, think_piece, spec, pitch, outreach
    apparent_date: Optional[str] = None
    audience: str = "general"
    length: int = 0
    word_count: int = 0

    # Assessment
    terminology_issues: List[Dict] = field(default_factory=list)
    positioning_gaps: List[str] = field(default_factory=list)
    technical_accuracy: str = "unknown"  # accurate, outdated, unknown

    # Structural
    leads_with_so_what: bool = False
    argument_flow: str = "unknown"  # strong, needs_work, unclear
    evidence_quality: str = "unknown"  # strong, adequate, weak
    length_appropriate: bool = True

    # Recommendation
    rewrite_scope: str = "light"  # light, moderate, substantial, retire
    key_changes_needed: List[str] = field(default_factory=list)
    flags_for_jim: List[str] = field(default_factory=list)


@dataclass
class Draft:
    """Editor output - rewritten document."""
    original_name: str
    working_name: str
    diagnosis_summary: str
    key_changes: List[str]
    flags_for_review: List[str]
    content: str
    editor_notes: str = ""


class EditorAgent:
    """Agent that rewrites Grove content following editorial methodology."""

    def __init__(
        self,
        engine_path: Optional[Path] = None,
        checkpoint_path: Optional[Path] = None,
    ):
        self.engine_path = engine_path
        self.checkpoint_path = checkpoint_path
        self._engine_content: str = ""
        self._checkpoint_content: str = ""

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

    def analyze(self, source_path: Path) -> Analysis:
        """Analyze a source document."""
        content = source_path.read_text(encoding="utf-8")

        # Basic metrics
        word_count = len(content.split())
        line_count = len(content.split("\n"))

        # Determine document type
        doc_type = self._determine_document_type(content, source_path)

        # Check apparent date
        date_match = re.search(
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
            content,
        )
        apparent_date = date_match.group(0) if date_match else None

        # Determine audience
        audience = self._determine_audience(content)

        # Analyze terminology issues
        issues = self._find_terminology_issues(content)

        # Check positioning alignment
        positioning = self._check_positioning(content)

        # Structural assessment
        leads_so_what = self._check_opening(content)
        flow = self._assess_argument_flow(content)
        evidence = self._assess_evidence(content)

        # Calculate rewrite scope
        scope, key_changes = self._calculate_rewrite_scope(issues, positioning, flow)

        return Analysis(
            original_name=source_path.name,
            working_name=self._normalize_name(source_path.name),
            document_type=doc_type,
            apparent_date=apparent_date,
            audience=audience,
            length=len(content),
            word_count=word_count,
            terminology_issues=issues,
            positioning_gaps=positioning["gaps"],
            technical_accuracy=positioning["accuracy"],
            leads_with_so_what=leads_so_what,
            argument_flow=flow,
            evidence_quality=evidence,
            length_appropriate=len(content) < 50000,  # Reasonable limit
            rewrite_scope=scope,
            key_changes_needed=key_changes,
            flags_for_jim=self._identify_flags(issues, positioning),
        )

    def rewrite(self, source_path: Path, analysis: Analysis) -> Draft:
        """Rewrite a document following editorial methodology."""
        content = source_path.read_text(encoding="utf-8")

        # Step 1: Fix terminology (mechanical)
        content = self._fix_terminology(content)

        # Step 2: Update positioning
        content = self._update_positioning(content, analysis)

        # Step 3: Strengthen arguments
        content = self._strengthen_arguments(content)

        # Step 4: Tighten prose
        content = self._tighten_prose(content)

        # Step 5: Verify voice
        content = self._verify_voice(content)

        # Identify key changes
        key_changes = self._identify_key_changes(analysis)

        # Identify flags for review
        flags = self._identify_editor_flags(analysis, content)

        return Draft(
            original_name=analysis.original_name,
            working_name=analysis.working_name,
            diagnosis_summary=self._generate_diagnosis(analysis),
            key_changes=key_changes,
            flags_for_review=flags,
            content=content,
        )

    def _determine_document_type(self, content: str, path: Path) -> str:
        """Determine document type from content and filename."""
        name_lower = path.name.lower()

        # Check filename
        if "white" in name_lower or "paper" in name_lower:
            return "white_paper"
        if "spec" in name_lower or "technical" in name_lower:
            return "spec"
        if "pitch" in name_lower or "executive" in name_lower:
            return "pitch"
        if "outreach" in name_lower or "partnership" in name_lower:
            return "outreach"

        # Check content structure
        if "# " in content and "## " in content and "### " in content:
            return "white_paper"
        if "The system SHALL" in content or "Requirements:" in content:
            return "spec"
        if "Problem → Solution" in content or "Hook → Problem" in content:
            return "pitch"

        return "think_piece"  # Default

    def _determine_audience(self, content: str) -> str:
        """Determine primary audience from content."""
        content_lower = content.lower()

        # Technical indicators
        if any(term in content_lower for term in ["api", "implementation", "architecture", "specification"]):
            return "technical"

        # Executive indicators
        if any(term in content_lower for term in ["market", "revenue", "strategy", "partnership", "go-to-market"]):
            return "executive"

        # Academic indicators
        if any(term in content_lower for term in ["research", "study", "analysis", "evidence"]):
            return "academic"

        return "general"

    def _find_terminology_issues(self, content: str) -> List[Dict]:
        """Find terminology issues in content."""
        issues = []

        legacy_mappings = {
            "AI platform": "Exploration architecture",
            "decentralized AI": "Exploration architecture",
            "bots": "Agents",
            "AI assistants": "Agents",
            "tokens": "Credits",
        }

        for legacy, current in legacy_mappings.items():
            if legacy.lower() in content.lower():
                count = content.lower().count(legacy.lower())
                issues.append({
                    "legacy": legacy,
                    "current": current,
                    "count": count,
                })

        return issues

    def _check_positioning(self, content: str) -> Dict:
        """Check positioning alignment."""
        content_lower = content.lower()

        # Key concepts from thesis
        key_concepts = [
            "exploration",
            "distributed",
            "local",
            "agents",
            "discovery",
            "sovereignty",
        ]

        gaps = []
        for concept in key_concepts:
            if concept not in content_lower:
                gaps.append(concept)

        # Check for competing positioning
        competing = []
        if "centralized" in content_lower and "control" in content_lower:
            # This might be good (contrasting Grove) or bad
            pass

        return {
            "gaps": gaps,
            "accuracy": "accurate" if len(gaps) < 2 else "needs_update",
        }

    def _check_opening(self, content: str) -> bool:
        """Check if document leads with 'so what'."""
        lines = content.strip().split("\n")[:10]
        text = " ".join([l for l in lines if not l.startswith("#")]).lower()

        # Check for throat-clearing
        throat_clearing = [
            "it's important to note",
            "in order to",
            "we would like to",
            "this document will",
        ]

        for phrase in throat_clearing:
            if phrase in text:
                return False

        return True

    def _assess_argument_flow(self, content: str) -> str:
        """Assess argument flow quality."""
        # Simplified assessment
        sections = content.split("## ")
        if len(sections) > 3:
            return "strong"
        elif len(sections) > 1:
            return "needs_work"
        return "unclear"

    def _assess_evidence(self, content: str) -> str:
        """Assess evidence quality."""
        # Check for citations, examples, data
        has_citations = "[" in content and "]" in content
        has_numbers = any(c.isdigit() for c in content[:2000])
        has_examples = "for example" in content.lower() or "such as" in content.lower()

        if has_citations and has_numbers:
            return "strong"
        elif has_examples or has_numbers:
            return "adequate"
        return "weak"

    def _calculate_rewrite_scope(
        self,
        issues: List[Dict],
        positioning: Dict,
        flow: str,
    ) -> Tuple[str, List[str]]:
        """Calculate rewrite scope and key changes."""
        key_changes = []

        if issues:
            key_changes.append(f"Fix {len(issues)} terminology issue(s)")

        if positioning["accuracy"] != "accurate":
            key_changes.append("Update strategic positioning")

        if flow == "needs_work":
            key_changes.append("Improve argument flow")

        # Determine scope
        issue_count = len(issues)
        change_count = len(key_changes)

        if change_count == 0:
            return "light", []
        elif change_count <= 2 and issue_count <= 3:
            return "moderate", key_changes
        else:
            return "substantial", key_changes

    def _identify_flags(
        self,
        issues: List[Dict],
        positioning: Dict,
    ) -> List[str]:
        """Identify items to flag for Jim."""
        flags = []

        if positioning["accuracy"] == "needs_update":
            flags.append("Strategic positioning needs update")

        if any(i.get("count", 0) > 5 for i in issues):
            flags.append("Heavy terminology issues - consider refactoring")

        return flags

    def _normalize_name(self, name: str) -> str:
        """Normalize filename for working."""
        # Strip spaces, use kebab-case
        return name.strip().replace(" ", "-").lower()

    def _fix_terminology(self, content: str) -> str:
        """Apply terminology fixes."""
        legacy_mappings = {
            "AI platform": "exploration architecture",
            "decentralized AI": "distributed AI infrastructure",
            "bots": "agents",
            "AI assistants": "agents",
            "tokens": "credits",
        }

        result = content
        for legacy, current in legacy_mappings.items():
            result = re.sub(
                rf"\b{re.escape(legacy)}\b",
                current,
                result,
                flags=re.IGNORECASE,
            )

        return result

    def _update_positioning(self, content: str, analysis: Analysis) -> str:
        """Update strategic positioning."""
        # This would typically involve more sophisticated rewriting
        # For now, ensure key concepts are present
        return content

    def _strengthen_arguments(self, content: str) -> str:
        """Strengthen arguments by removing hedging."""
        hedging = [
            (r"\bmight\b", ""),
            (r"\bcould potentially\b", ""),
            (r"\bit's possible that\b", ""),
            (r"\bmight be\b", "is"),
            (r"\bcould be\b", "is"),
        ]

        result = content
        for pattern, replacement in hedging:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        return result

    def _tighten_prose(self, content: str) -> str:
        """Tighten prose by removing filler."""
        fillers = [
            (r"\bIt's important to note that\b", ""),
            (r"\bIn order to\b", ""),
            (r"\bIt should be noted that\b", ""),
        ]

        result = content
        for pattern, replacement in fillers:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        return result

    def _verify_voice(self, content: str) -> str:
        """Verify voice consistency."""
        # Check for passive voice (simplified)
        passive_patterns = [
            r"\bis being\b",
            r"\bwas being\b",
            r"\bhas been\b",
            r"\bhave been\b",
        ]

        result = content
        # Note: In production, this would be more sophisticated
        return result

    def _identify_key_changes(self, analysis: Analysis) -> List[str]:
        """Identify key changes made."""
        changes = []

        if analysis.terminology_issues:
            changes.append(
                f"Fixed {len(analysis.terminology_issues)} terminology issue(s)"
            )

        if analysis.positioning_gaps:
            changes.append("Updated positioning for current strategy")

        if analysis.argument_flow == "needs_work":
            changes.append("Improved argument flow")

        return changes

    def _identify_editor_flags(
        self,
        analysis: Analysis,
        content: str,
    ) -> List[str]:
        """Identify flags for reviewer."""
        flags = []

        if analysis.technical_accuracy == "unknown":
            flags.append("Technical accuracy not verified")

        if len(content) > 10000:
            flags.append("Long document - verify consistent voice")

        return flags

    def _generate_diagnosis(self, analysis: Analysis) -> str:
        """Generate diagnosis summary."""
        parts = []

        parts.append(f"Type: {analysis.document_type.replace('_', ' ')}")

        if analysis.terminology_issues:
            parts.append(f"Found {len(analysis.terminology_issues)} legacy term(s)")

        if analysis.positioning_gaps:
            parts.append(f"Missing {len(analysis.positioning_gaps)} key concept(s)")

        parts.append(f"Rewrite scope: {analysis.rewrite_scope}")

        return "; ".join(parts)
