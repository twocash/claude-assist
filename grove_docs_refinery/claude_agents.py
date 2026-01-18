#!/usr/bin/env python3
"""
Grove Docs Refinery - Claude-Powered Agents

Drop-in replacement for rules-based editor/reviewer using Claude API.
Prompts are loaded from external files for easy tuning.
"""

import yaml
from pathlib import Path
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from enum import Enum

import anthropic

# Import dataclasses from original modules to maintain compatibility
from editor import Analysis, Draft
from reviewer import Review, Assessment


# Paths
PROMPTS_DIR = Path(__file__).parent / "prompts"
REFINERY_DIR = Path(__file__).parent


def load_prompt(name: str) -> str:
    """Load a prompt from the prompts directory."""
    path = PROMPTS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def load_settings() -> Dict:
    """Load Claude settings from YAML."""
    settings_path = PROMPTS_DIR / "settings.yaml"
    if settings_path.exists():
        return yaml.safe_load(settings_path.read_text(encoding="utf-8"))
    # Defaults
    return {
        "writer": {"model": "claude-sonnet-4-20250514", "max_tokens": 16000},
        "reviewer": {"model": "claude-sonnet-4-20250514", "max_tokens": 4000},
    }


class ClaudeEditorAgent:
    """Claude-powered editor that follows Grove editorial methodology.

    Drop-in replacement for EditorAgent with same interface.
    """

    def __init__(
        self,
        engine_path: Optional[Path] = None,
        checkpoint_path: Optional[Path] = None,
    ):
        self.engine_path = engine_path
        self.checkpoint_path = checkpoint_path
        self._engine_content: str = ""
        self._checkpoint_content: str = ""
        self._client = anthropic.Anthropic()
        self._settings = load_settings()

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
            self._engine_content = self.engine_path.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(f"Editorial engine not found: {self.engine_path}")

        if self.checkpoint_path and self.checkpoint_path.exists():
            self._checkpoint_content = self.checkpoint_path.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(f"Editorial checkpoint not found: {self.checkpoint_path}")

        print(f"Loaded editorial engine ({len(self._engine_content):,} chars)")
        print(f"Loaded editorial checkpoint ({len(self._checkpoint_content):,} chars)")

    def analyze(self, source_path: Path) -> Analysis:
        """Analyze a source document.

        For Claude-powered editor, analysis is lightweight since
        Claude will do the real analysis during rewrite.
        """
        content = source_path.read_text(encoding="utf-8")
        word_count = len(content.split())

        # Basic analysis - Claude does the heavy lifting in rewrite
        return Analysis(
            original_name=source_path.name,
            working_name=self._normalize_name(source_path.name),
            document_type="unknown",  # Claude will determine
            word_count=word_count,
            length=len(content),
            rewrite_scope="claude",  # Indicates Claude will handle
        )

    def rewrite(self, source_path: Path, analysis: Analysis) -> Draft:
        """Rewrite a document using Claude."""
        source_content = source_path.read_text(encoding="utf-8")
        source_name = source_path.name

        # Load system prompt from file
        system_prompt = load_prompt("writer_system")

        # Build user message with full context
        user_message = f"""## Grove Editorial Engine (Methodology)

{self._engine_content}

---

## Grove Editorial Checkpoint (Current State)

{self._checkpoint_content}

---

## Source Document to Rewrite

**Filename:** {source_name}

{source_content}

---

Please rewrite this document following the methodology and checkpoint above.
Remember to preserve intentional honesty in sections about caveats, risks, and uncertainties.
"""

        print(f"  Calling Claude to rewrite {source_name}...")
        print(f"    Source: {len(source_content):,} chars")

        settings = self._settings.get("writer", {})
        response = self._client.messages.create(
            model=settings.get("model", "claude-sonnet-4-20250514"),
            max_tokens=settings.get("max_tokens", 16000),
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        raw_response = response.content[0].text
        print(f"    Response: {len(raw_response):,} chars")

        return self._parse_response(source_name, raw_response)

    def _parse_response(self, source_name: str, raw_response: str) -> Draft:
        """Parse Claude's response into Draft structure."""
        diagnosis = ""
        key_changes = []
        flags = []
        content = ""

        lines = raw_response.split("\n")
        current_section = None
        content_started = False
        content_lines = []

        for line in lines:
            if "### Diagnosis Summary" in line:
                current_section = "diagnosis"
                continue
            elif "### Key Changes Made" in line:
                current_section = "changes"
                continue
            elif "### Flags for Review" in line:
                current_section = "flags"
                continue
            elif line.strip() == "---" and current_section == "flags":
                content_started = True
                current_section = "content"
                continue
            elif content_started and line.strip() == "---":
                break

            if current_section == "diagnosis" and line.strip():
                diagnosis += line.strip() + " "
            elif current_section == "changes" and line.strip().startswith("-"):
                key_changes.append(line.strip()[1:].strip())
            elif current_section == "flags" and line.strip().startswith("-"):
                flags.append(line.strip()[1:].strip())
            elif current_section == "content":
                content_lines.append(line)

        content = "\n".join(content_lines).strip()

        # Fallback if parsing failed
        if not content:
            parts = raw_response.split("---")
            if len(parts) >= 3:
                content = "---".join(parts[2:]).strip()
            else:
                content = raw_response

        return Draft(
            original_name=source_name,
            working_name=self._normalize_name(source_name),
            diagnosis_summary=diagnosis.strip(),
            key_changes=key_changes,
            flags_for_review=flags,
            content=content,
            editor_notes=f"Processed by Claude ({self._settings.get('writer', {}).get('model', 'unknown')})",
        )

    def _normalize_name(self, name: str) -> str:
        """Normalize filename."""
        return name.strip().replace(" ", "-").lower()


class ClaudeReviewerAgent:
    """Claude-powered reviewer that validates against Grove standards.

    Drop-in replacement for ReviewerAgent with same interface.
    """

    def __init__(
        self,
        engine_path: Optional[Path] = None,
        checkpoint_path: Optional[Path] = None,
    ):
        self.engine_path = engine_path
        self.checkpoint_path = checkpoint_path
        self._engine_content: str = ""
        self._checkpoint_content: str = ""
        self._client = anthropic.Anthropic()
        self._settings = load_settings()

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
            self._engine_content = self.engine_path.read_text(encoding="utf-8")

        if self.checkpoint_path and self.checkpoint_path.exists():
            self._checkpoint_content = self.checkpoint_path.read_text(encoding="utf-8")

    def validate(self, original_path: Path, draft_path: Path) -> Review:
        """Review a rewritten document."""
        original_content = original_path.read_text(encoding="utf-8")
        draft_content = draft_path.read_text(encoding="utf-8")
        doc_name = original_path.name

        # Load system prompt from file
        system_prompt = load_prompt("reviewer_system")

        user_message = f"""## Grove Editorial Engine (Methodology)

{self._engine_content}

---

## Grove Editorial Checkpoint (Current State)

{self._checkpoint_content}

---

## Original Source Document

**Filename:** {doc_name}

{original_content}

---

## Writer's Rewritten Draft

{draft_content}

---

Please review this rewrite against Grove standards.
Pay special attention to whether intentional honesty in "Honest Assessment" sections was preserved.
"""

        print(f"  Calling Claude to review {doc_name}...")

        settings = self._settings.get("reviewer", {})
        response = self._client.messages.create(
            model=settings.get("model", "claude-sonnet-4-20250514"),
            max_tokens=settings.get("max_tokens", 4000),
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )

        raw_response = response.content[0].text
        print(f"    Response: {len(raw_response):,} chars")

        return self._parse_response(doc_name, raw_response)

    def _parse_response(self, doc_name: str, raw_response: str) -> Review:
        """Parse Claude's response into Review structure."""
        # Determine assessment
        assessment = Assessment.REVISE  # Default
        if "### Assessment: PASS" in raw_response:
            assessment = Assessment.PASS
        elif "### Assessment: ESCALATE" in raw_response:
            assessment = Assessment.ESCALATE
        elif "### Assessment: REVISE" in raw_response:
            assessment = Assessment.REVISE

        # Parse checklist
        checklist = {}
        checklist_items = [
            "Terminology current",
            "Positioning aligned",
            "Technical accuracy",
            "Voice consistency",
            "No prohibited language",
            "Intentional honesty preserved",
            "Appropriate length",
            "Changes justified",
            "No new errors",
        ]
        for item in checklist_items:
            if f"[x] {item}" in raw_response or f"[X] {item}" in raw_response:
                checklist[item] = True
            else:
                checklist[item] = False

        # Extract feedback sections
        specific_feedback = ""
        suggested_improvements = []

        if "### Specific Feedback" in raw_response:
            start = raw_response.find("### Specific Feedback")
            end = raw_response.find("### Suggested Improvements", start)
            if end == -1:
                end = raw_response.find("---", start + 1)
            if end == -1:
                end = len(raw_response)
            specific_feedback = raw_response[start:end].replace("### Specific Feedback", "").strip()

        if "### Suggested Improvements" in raw_response:
            start = raw_response.find("### Suggested Improvements")
            end = raw_response.find("---", start)
            if end == -1:
                end = len(raw_response)
            improvements_text = raw_response[start:end].replace("### Suggested Improvements", "").strip()
            # Parse bullet points
            for line in improvements_text.split("\n"):
                if line.strip().startswith("-"):
                    suggested_improvements.append(line.strip()[1:].strip())

        return Review(
            original_name=doc_name,
            assessment=assessment,
            validation_checklist=checklist,
            specific_feedback=specific_feedback,
            suggested_improvements=suggested_improvements,
        )

    def generate_review_report(self, review: Review) -> str:
        """Generate human-readable review report."""
        lines = [
            f"## Review: {review.original_name}",
            f"### Assessment: {review.assessment.value}",
            "",
            "### Validation Checklist",
        ]

        for item, passed in review.validation_checklist.items():
            mark = "[x]" if passed else "[ ]"
            lines.append(f"- {mark} {item}")

        lines.extend([
            "",
            "### Specific Feedback",
            review.specific_feedback,
        ])

        if review.suggested_improvements:
            lines.extend([
                "",
                "### Suggested Improvements",
            ])
            for improvement in review.suggested_improvements:
                lines.append(f"- {improvement}")

        return "\n".join(lines)
