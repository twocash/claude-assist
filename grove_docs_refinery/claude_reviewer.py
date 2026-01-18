#!/usr/bin/env python3
"""
Grove Docs Refinery - Claude-Powered Reviewer Agent

Uses Claude API to validate rewritten content against Grove standards.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from enum import Enum

import anthropic


# Paths to methodology files
REFINERY_DIR = Path(__file__).parent
ENGINE_PATH = REFINERY_DIR / "editorial-engine.md"
CHECKPOINT_PATH = REFINERY_DIR / "editorial-checkpoint.md"


class Assessment(Enum):
    PASS = "PASS"
    REVISE = "REVISE"
    ESCALATE = "ESCALATE"


@dataclass
class ReviewOutput:
    """Output from the reviewer agent."""
    document_name: str
    assessment: Assessment
    checklist: dict[str, bool]
    specific_feedback: str
    suggested_improvements: str
    raw_response: str


REVIEWER_SYSTEM_PROMPT = """You are the Reviewer Agent in Grove's editorial refinery.

You have been provided with:
1. The Grove Editorial Engine (methodology)
2. The Grove Editorial Checkpoint (current state)
3. The original source document
4. The writer's rewritten draft

Your task: Validate the writer's rewrite against Grove standards.

Assess against these criteria:
- [ ] All terminology is current (per checkpoint)
- [ ] Strategic positioning reflects current state
- [ ] Technical descriptions are accurate
- [ ] Voice is consistent throughout
- [ ] No buzzwords or prohibited language (EXCEPT in "Honest Assessment" type sections where hedging is intentional)
- [ ] Appropriate length for document type
- [ ] Writer's changes are justified
- [ ] No new errors introduced
- [ ] Intentional uncertainty preserved (sections about caveats/risks should KEEP their hedging)

CRITICAL: "Honest Assessment" sections, "Caveats", "What We Don't Know" - these SHOULD contain hedging like "might", "could". That's intentional intellectual honesty, not filler. Only flag hedging that is throat-clearing filler, not substantive uncertainty acknowledgment.

Output format:

---
## Review: [Document Title]

### Assessment: [PASS / REVISE / ESCALATE]

### Validation Checklist
- [x] or [ ] Terminology current
- [x] or [ ] Positioning aligned
- [x] or [ ] Technical accuracy
- [x] or [ ] Voice consistency
- [x] or [ ] No prohibited language (filler hedging)
- [x] or [ ] Intentional honesty preserved
- [x] or [ ] Appropriate length
- [x] or [ ] Changes justified
- [x] or [ ] No new errors

### Specific Feedback
[If PASS: brief confirmation of quality]
[If REVISE: specific changes needed, return to writer]
[If ESCALATE: decision needed from Jim, explain why]

### Suggested Improvements (Optional)
[Minor enhancements that don't require REVISE status]
---
"""


class ClaudeReviewer:
    """Claude-powered reviewer that validates against Grove standards."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.engine_content = ""
        self.checkpoint_content = ""

    def load_context(self):
        """Load editorial engine and checkpoint."""
        if ENGINE_PATH.exists():
            self.engine_content = ENGINE_PATH.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(f"Editorial engine not found: {ENGINE_PATH}")

        if CHECKPOINT_PATH.exists():
            self.checkpoint_content = CHECKPOINT_PATH.read_text(encoding="utf-8")
        else:
            raise FileNotFoundError(f"Editorial checkpoint not found: {CHECKPOINT_PATH}")

    def review(self, original_path: Path, draft_path: Path) -> ReviewOutput:
        """Review a rewritten document."""
        original_content = original_path.read_text(encoding="utf-8")
        draft_content = draft_path.read_text(encoding="utf-8")
        doc_name = original_path.name

        user_message = f"""## Grove Editorial Engine (Methodology)

{self.engine_content}

---

## Grove Editorial Checkpoint (Current State)

{self.checkpoint_content}

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

        print(f"Calling Claude to review {doc_name}...")

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=REVIEWER_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        raw_response = response.content[0].text
        print(f"  Response: {len(raw_response):,} chars")

        return self._parse_response(doc_name, raw_response)

    def _parse_response(self, doc_name: str, raw_response: str) -> ReviewOutput:
        """Parse Claude's response into structured output."""
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
        suggested_improvements = ""

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
            suggested_improvements = raw_response[start:end].replace("### Suggested Improvements", "").strip()

        return ReviewOutput(
            document_name=doc_name,
            assessment=assessment,
            checklist=checklist,
            specific_feedback=specific_feedback,
            suggested_improvements=suggested_improvements,
            raw_response=raw_response,
        )


def main():
    """Test the Claude reviewer."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python claude_reviewer.py <original-file> <draft-file>")
        sys.exit(1)

    original_path = Path(sys.argv[1])
    draft_path = Path(sys.argv[2])

    if not original_path.exists():
        print(f"Original not found: {original_path}")
        sys.exit(1)
    if not draft_path.exists():
        print(f"Draft not found: {draft_path}")
        sys.exit(1)

    reviewer = ClaudeReviewer()
    reviewer.load_context()

    output = reviewer.review(original_path, draft_path)

    print("\n" + "=" * 60)
    print("REVIEWER OUTPUT")
    print("=" * 60)
    print(f"Document: {output.document_name}")
    print(f"Assessment: {output.assessment.value}")
    print("\nChecklist:")
    for item, passed in output.checklist.items():
        mark = "[x]" if passed else "[ ]"
        print(f"  {mark} {item}")
    print(f"\nFeedback: {output.specific_feedback[:200]}...")

    # Save output
    output_path = REFINERY_DIR / "reviews" / f"{original_path.stem}--REVIEW-claude.md"
    output_path.write_text(output.raw_response, encoding="utf-8")
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
