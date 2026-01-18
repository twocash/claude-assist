#!/usr/bin/env python3
"""
Grove Docs Refinery - Claude-Powered Editor Agent

Uses Claude API to intelligently rewrite Grove content following
the editorial methodology and checkpoint.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

import anthropic


# Paths to methodology files
REFINERY_DIR = Path(__file__).parent
ENGINE_PATH = REFINERY_DIR / "editorial-engine.md"
CHECKPOINT_PATH = REFINERY_DIR / "editorial-checkpoint.md"


@dataclass
class WriterOutput:
    """Output from the writer agent."""
    original_name: str
    working_name: str
    diagnosis_summary: str
    key_changes: list[str]
    flags_for_review: list[str]
    content: str
    raw_response: str


WRITER_SYSTEM_PROMPT = """You are the Writer Agent in Grove's editorial refinery.

You have been provided with:
1. The Grove Editorial Engine (methodology for how to rewrite)
2. The Grove Editorial Checkpoint (current strategic positioning and terminology)

Your task: Rewrite the provided document to reflect Grove's current positioning, terminology, and voice.

Follow the 5-step methodology:
1. Diagnose the source content
2. Align with checkpoint
3. Assess structure
4. Execute rewrite
5. Validate against checklist

CRITICAL GUIDELINES:
- Preserve INTENTIONAL honesty and uncertainty. Sections explicitly labeled "Honest Assessment", "Caveats", "What We Don't Know" etc. should KEEP their hedging language - that's the point.
- Only remove hedging that is filler/throat-clearing, not substantive intellectual honesty.
- "The Ratchet might stall" in an "Honest Caveats" section = KEEP (intentional)
- "This could potentially maybe help" in a claim = REMOVE (filler)
- Fix terminology mappings precisely (Tokens→Credits, etc.)
- Maintain document structure and section headers
- Don't break sentences when removing words - restructure gracefully

Output format (use exactly this structure):

---
## Rewrite: [Document Title]

### Diagnosis Summary
[2-3 sentences on source state]

### Key Changes Made
- [Change 1]
- [Change 2]
- [etc.]

### Flags for Review
- [Any uncertainties, decisions needed, or ESCALATE items]

---

[FULL REWRITTEN CONTENT]
---
"""


class ClaudeEditor:
    """Claude-powered editor that follows Grove editorial methodology."""

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

        print(f"Loaded editorial engine ({len(self.engine_content)} chars)")
        print(f"Loaded editorial checkpoint ({len(self.checkpoint_content)} chars)")

    def rewrite(self, source_path: Path) -> WriterOutput:
        """Rewrite a document using Claude."""
        source_content = source_path.read_text(encoding="utf-8")
        source_name = source_path.name

        # Build the user message with all context
        user_message = f"""## Grove Editorial Engine (Methodology)

{self.engine_content}

---

## Grove Editorial Checkpoint (Current State)

{self.checkpoint_content}

---

## Source Document to Rewrite

**Filename:** {source_name}

{source_content}

---

Please rewrite this document following the methodology and checkpoint above.
Remember to preserve intentional honesty in sections about caveats, risks, and uncertainties.
"""

        print(f"Calling Claude to rewrite {source_name}...")
        print(f"  Source: {len(source_content):,} chars")

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            system=WRITER_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        raw_response = response.content[0].text
        print(f"  Response: {len(raw_response):,} chars")

        # Parse the response
        return self._parse_response(source_name, raw_response)

    def _parse_response(self, source_name: str, raw_response: str) -> WriterOutput:
        """Parse Claude's response into structured output."""
        # Extract sections from the response
        diagnosis = ""
        key_changes = []
        flags = []
        content = ""

        lines = raw_response.split("\n")
        current_section = None
        content_started = False
        content_lines = []

        for i, line in enumerate(lines):
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
                # End of content
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

        # If parsing failed, use the whole response as content
        if not content:
            # Find content after the last "---" before "Flags for Review"
            parts = raw_response.split("---")
            if len(parts) >= 3:
                content = "---".join(parts[2:]).strip()
            else:
                content = raw_response

        return WriterOutput(
            original_name=source_name,
            working_name=source_name.lower().replace(" ", "-"),
            diagnosis_summary=diagnosis.strip(),
            key_changes=key_changes,
            flags_for_review=flags,
            content=content,
            raw_response=raw_response,
        )


def main():
    """Test the Claude editor on a single file."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python claude_editor.py <path-to-file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    editor = ClaudeEditor()
    editor.load_context()

    output = editor.rewrite(file_path)

    print("\n" + "=" * 60)
    print("WRITER OUTPUT")
    print("=" * 60)
    print(f"Original: {output.original_name}")
    print(f"Diagnosis: {output.diagnosis_summary}")
    print(f"Changes: {len(output.key_changes)}")
    print(f"Flags: {len(output.flags_for_review)}")
    print(f"Content length: {len(output.content):,} chars")

    # Save output
    output_path = REFINERY_DIR / "drafts" / f"{output.working_name}--DRAFT-claude.md"
    output_path.write_text(output.raw_response, encoding="utf-8")
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
