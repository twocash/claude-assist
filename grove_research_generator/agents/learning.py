#!/usr/bin/env python3
"""
Learning Agent

Analyzes differences between AI-generated drafts and human-edited versions
to extract editorial preferences and update the editorial memory.
"""

import re
import difflib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from ..config import ResearchConfig


@dataclass
class EditPattern:
    """A learned editorial pattern."""
    category: str  # terminology, voice, concepts, structure, phrasing
    pattern: str  # What was changed
    original: str  # AI version
    edited: str  # Human version
    explanation: str  # Why this matters
    source_doc: str  # Which document this came from
    date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


@dataclass
class DiffAnalysis:
    """Results of analyzing differences between draft and edited version."""
    total_changes: int = 0
    terminology_changes: List[EditPattern] = field(default_factory=list)
    voice_changes: List[EditPattern] = field(default_factory=list)
    added_concepts: List[EditPattern] = field(default_factory=list)
    structural_changes: List[EditPattern] = field(default_factory=list)
    phrasing_changes: List[EditPattern] = field(default_factory=list)
    minor_edits: int = 0  # Typos, grammar - not stored

    def has_learnings(self) -> bool:
        """Check if there are meaningful learnings to store."""
        return bool(
            self.terminology_changes or
            self.voice_changes or
            self.added_concepts or
            self.structural_changes or
            self.phrasing_changes
        )


class LearningAgent:
    """Extracts editorial learnings from draft-to-final diffs."""

    # Known terminology patterns to watch for
    TERMINOLOGY_PATTERNS = [
        (r'\bGrove\b(?! )', r'The Grove'),  # Grove without "The"
        (r'\bTrellis\b(?! Architecture)', r'Trellis Architecture'),
        (r'\bagent\b', r'Agent'),  # Capitalization
        (r'\bobserver\b', r'Observer'),
    ]

    # Phrases that indicate voice/framing changes
    VOICE_INDICATORS = [
        'might', 'could potentially', 'perhaps',  # Hedging removed
        'revolutionary', 'paradigm shift',  # Buzzwords removed
        'it is important to note',  # Filler removed
    ]

    def __init__(self, config: 'ResearchConfig' = None):
        self.config = config
        self.memory_path = Path(__file__).parent.parent / "editorial_memory.md"

    def analyze_diff(
        self,
        original: str,
        edited: str,
        source_doc: str = "Unknown",
    ) -> DiffAnalysis:
        """
        Analyze differences between original draft and edited version.

        Returns DiffAnalysis with categorized learnings.
        """
        analysis = DiffAnalysis()

        # Get line-by-line diff
        original_lines = original.splitlines()
        edited_lines = edited.splitlines()

        differ = difflib.unified_diff(
            original_lines,
            edited_lines,
            lineterm='',
        )
        diff_lines = list(differ)

        # Also get word-level changes for finer analysis
        word_changes = self._get_word_changes(original, edited)

        # Analyze terminology changes (pass full text for pattern matching)
        analysis.terminology_changes = self._find_terminology_patterns(
            word_changes, source_doc,
            original_text=original,
            edited_text=edited,
        )

        # Analyze added content (concepts AI missed)
        analysis.added_concepts = self._find_added_concepts(
            original, edited, source_doc
        )

        # Analyze voice/framing changes
        analysis.voice_changes = self._find_voice_changes(
            word_changes, source_doc
        )

        # Analyze structural changes
        analysis.structural_changes = self._find_structural_changes(
            original_lines, edited_lines, source_doc
        )

        # Analyze phrasing patterns
        analysis.phrasing_changes = self._find_phrasing_patterns(
            word_changes, source_doc
        )

        # Count total meaningful changes
        analysis.total_changes = (
            len(analysis.terminology_changes) +
            len(analysis.voice_changes) +
            len(analysis.added_concepts) +
            len(analysis.structural_changes) +
            len(analysis.phrasing_changes)
        )

        return analysis

    def _get_word_changes(
        self,
        original: str,
        edited: str,
    ) -> List[Tuple[str, str, str]]:
        """Get word-level changes as (context, original, edited) tuples."""
        changes = []

        # Split into sentences for context
        orig_sentences = re.split(r'(?<=[.!?])\s+', original)
        edit_sentences = re.split(r'(?<=[.!?])\s+', edited)

        # Use SequenceMatcher to align sentences
        matcher = difflib.SequenceMatcher(None, orig_sentences, edit_sentences)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                for orig_sent, edit_sent in zip(
                    orig_sentences[i1:i2],
                    edit_sentences[j1:j2]
                ):
                    # Find word-level differences within sentences
                    orig_words = orig_sent.split()
                    edit_words = edit_sent.split()
                    word_matcher = difflib.SequenceMatcher(
                        None, orig_words, edit_words
                    )
                    for wtag, wi1, wi2, wj1, wj2 in word_matcher.get_opcodes():
                        if wtag == 'replace':
                            orig_phrase = ' '.join(orig_words[wi1:wi2])
                            edit_phrase = ' '.join(edit_words[wj1:wj2])
                            context = orig_sent[:50] + "..."
                            changes.append((context, orig_phrase, edit_phrase))

        return changes

    def _find_terminology_patterns(
        self,
        word_changes: List[Tuple[str, str, str]],
        source_doc: str,
        original_text: str = "",
        edited_text: str = "",
    ) -> List[EditPattern]:
        """Find terminology corrections."""
        patterns = []
        seen = set()

        # First: Direct pattern matching on full text (more reliable)
        # Look for cases where "Grove" alone was changed to "The Grove"
        if original_text and edited_text:
            # Count occurrences of "Grove" without "The" before it
            grove_alone_orig = len(re.findall(r'(?<![Tt]he\s)\bGrove\b', original_text))
            grove_alone_edit = len(re.findall(r'(?<![Tt]he\s)\bGrove\b', edited_text))
            the_grove_orig = len(re.findall(r'\bThe Grove\b', original_text))
            the_grove_edit = len(re.findall(r'\bThe Grove\b', edited_text))

            # If "Grove" alone decreased and "The Grove" increased, pattern detected
            if grove_alone_orig > grove_alone_edit and the_grove_edit > the_grove_orig:
                key = ('Grove', 'The Grove')
                if key not in seen:
                    seen.add(key)
                    patterns.append(EditPattern(
                        category="terminology",
                        pattern="The Grove (not \"Grove\")",
                        original="Grove",
                        edited="The Grove",
                        explanation="Always use 'The Grove' with the article, never just 'Grove' alone",
                        source_doc=source_doc,
                    ))

        # Then: Check word-level changes for other patterns
        for context, original, edited in word_changes:
            # Check for known terminology patterns
            for pattern, correct in self.TERMINOLOGY_PATTERNS:
                if re.search(pattern, original, re.IGNORECASE):
                    key = (pattern, correct)
                    if key not in seen:
                        seen.add(key)
                        patterns.append(EditPattern(
                            category="terminology",
                            pattern=f"{original} → {edited}",
                            original=original,
                            edited=edited,
                            explanation=f"Prefer '{edited}' over '{original}'",
                            source_doc=source_doc,
                        ))

            # Check for capitalization changes on key terms
            if original.lower() == edited.lower() and original != edited:
                if any(term in edited for term in ['Grove', 'Trellis', 'Observer', 'Agent']):
                    key = (original.lower(), edited)
                    if key not in seen:
                        seen.add(key)
                        patterns.append(EditPattern(
                            category="terminology",
                            pattern=f"Capitalize: {original} → {edited}",
                            original=original,
                            edited=edited,
                            explanation=f"'{edited}' should be capitalized",
                            source_doc=source_doc,
                        ))

        return patterns

    def _find_added_concepts(
        self,
        original: str,
        edited: str,
        source_doc: str,
    ) -> List[EditPattern]:
        """Find concepts that were added (AI missed them)."""
        patterns = []

        # Look for significant additions (new sentences or phrases)
        orig_sentences = set(re.split(r'(?<=[.!?])\s+', original))
        edit_sentences = set(re.split(r'(?<=[.!?])\s+', edited))

        added_sentences = edit_sentences - orig_sentences

        for sentence in added_sentences:
            # Skip very short additions (likely minor edits)
            if len(sentence.split()) < 10:
                continue

            # Look for concept-heavy additions
            concept_indicators = [
                'hybrid cognition', 'federated knowledge', 'edge AI',
                'distributed', 'sovereignty', 'form factor',
            ]
            for indicator in concept_indicators:
                if indicator.lower() in sentence.lower():
                    patterns.append(EditPattern(
                        category="concepts",
                        pattern=f"Added concept: {indicator}",
                        original="[not present]",
                        edited=sentence[:100] + "...",
                        explanation=f"AI missed mentioning '{indicator}' - add to future generations",
                        source_doc=source_doc,
                    ))
                    break

        return patterns

    def _find_voice_changes(
        self,
        word_changes: List[Tuple[str, str, str]],
        source_doc: str,
    ) -> List[EditPattern]:
        """Find voice/framing corrections."""
        patterns = []
        seen = set()

        for context, original, edited in word_changes:
            # Check for hedging language removed
            for hedge in self.VOICE_INDICATORS:
                if hedge.lower() in original.lower() and hedge.lower() not in edited.lower():
                    if hedge not in seen:
                        seen.add(hedge)
                        patterns.append(EditPattern(
                            category="voice",
                            pattern=f"Remove hedging: '{hedge}'",
                            original=original,
                            edited=edited,
                            explanation=f"Avoid '{hedge}' - be more direct",
                            source_doc=source_doc,
                        ))

        return patterns

    def _find_structural_changes(
        self,
        original_lines: List[str],
        edited_lines: List[str],
        source_doc: str,
    ) -> List[EditPattern]:
        """Find structural/organizational changes."""
        patterns = []

        # Look for heading changes
        orig_headings = [l for l in original_lines if l.startswith('#')]
        edit_headings = [l for l in edited_lines if l.startswith('#')]

        if orig_headings != edit_headings:
            # Find specific heading changes
            for orig_h, edit_h in zip(orig_headings, edit_headings):
                if orig_h != edit_h:
                    patterns.append(EditPattern(
                        category="structure",
                        pattern=f"Heading: {orig_h} → {edit_h}",
                        original=orig_h,
                        edited=edit_h,
                        explanation="Prefer this heading style",
                        source_doc=source_doc,
                    ))

        return patterns

    def _find_phrasing_patterns(
        self,
        word_changes: List[Tuple[str, str, str]],
        source_doc: str,
    ) -> List[EditPattern]:
        """Find general phrasing preferences."""
        patterns = []

        for context, original, edited in word_changes:
            # Look for consistent phrase replacements
            # Skip single word changes (likely typos)
            if ' ' in original and ' ' in edited:
                # This is a multi-word phrase change
                if len(original.split()) >= 3 and len(edited.split()) >= 3:
                    patterns.append(EditPattern(
                        category="phrasing",
                        pattern=f"'{original}' → '{edited}'",
                        original=original,
                        edited=edited,
                        explanation="Preferred phrasing",
                        source_doc=source_doc,
                    ))

        return patterns[:5]  # Limit to avoid noise

    def update_memory(self, analysis: DiffAnalysis) -> bool:
        """Update editorial_memory.md with new learnings."""
        if not analysis.has_learnings():
            return False

        # Read current memory
        if self.memory_path.exists():
            content = self.memory_path.read_text(encoding='utf-8')
        else:
            content = self._create_empty_memory()

        # Update each section
        today = datetime.now().strftime("%Y-%m-%d")

        # Update terminology
        for pattern in analysis.terminology_changes:
            content = self._add_to_section(
                content,
                "## Terminology Preferences",
                self._format_pattern(pattern),
            )

        # Update voice
        for pattern in analysis.voice_changes:
            content = self._add_to_section(
                content,
                "## Voice & Framing",
                self._format_pattern(pattern),
            )

        # Update concepts
        for pattern in analysis.added_concepts:
            content = self._add_to_section(
                content,
                "## Concepts AI Tends to Miss",
                self._format_pattern(pattern),
            )

        # Update structure
        for pattern in analysis.structural_changes:
            content = self._add_to_section(
                content,
                "## Structural Preferences",
                self._format_pattern(pattern),
            )

        # Update phrasing
        for pattern in analysis.phrasing_changes:
            content = self._add_to_section(
                content,
                "## Phrasing Patterns",
                self._format_pattern(pattern),
            )

        # Update changelog
        for pattern in (
            analysis.terminology_changes +
            analysis.voice_changes +
            analysis.added_concepts
        )[:3]:  # Top 3 learnings
            changelog_entry = f"| {today} | {pattern.source_doc} | {pattern.pattern[:50]} |"
            content = self._add_to_changelog(content, changelog_entry)

        # Update header
        content = self._update_header(content, analysis.total_changes)

        # Write back
        self.memory_path.write_text(content, encoding='utf-8')
        return True

    def _format_pattern(self, pattern: EditPattern) -> str:
        """Format a pattern for the memory file."""
        return f"""
### {pattern.pattern}
- **Category:** {pattern.category}
- **Original:** {pattern.original}
- **Edited:** {pattern.edited}
- **Why:** {pattern.explanation}
- **Source:** {pattern.source_doc} ({pattern.date})
"""

    def _add_to_section(self, content: str, section: str, entry: str) -> str:
        """Add an entry to a section in the memory file."""
        # Find the section
        section_pattern = re.escape(section)
        next_section = r'\n---\n\n## '

        match = re.search(
            f'{section_pattern}(.*?)({next_section}|## Changelog)',
            content,
            re.DOTALL
        )

        if match:
            section_content = match.group(1)
            # Remove placeholder if present
            section_content = re.sub(
                r'\*No learnings yet.*?\*\n*',
                '',
                section_content
            )
            # Add new entry
            new_section_content = section_content.rstrip() + "\n" + entry
            content = content[:match.start(1)] + new_section_content + content[match.end(1):]

        return content

    def _add_to_changelog(self, content: str, entry: str) -> str:
        """Add entry to changelog table."""
        # Find the changelog table
        changelog_match = re.search(
            r'(\| Date \| Document \| Learning \|\n\|[-|]+\|)\n',
            content
        )
        if changelog_match:
            insert_pos = changelog_match.end()
            content = content[:insert_pos] + entry + "\n" + content[insert_pos:]
        return content

    def _update_header(self, content: str, new_learnings: int) -> str:
        """Update the header with new counts."""
        today = datetime.now().strftime("%Y-%m-%d")

        # Update date
        content = re.sub(
            r'\*\*Last updated:\*\* \d{4}-\d{2}-\d{2}',
            f'**Last updated:** {today}',
            content
        )

        # Update count
        count_match = re.search(r'\*\*Total learnings:\*\* (\d+)', content)
        if count_match:
            current = int(count_match.group(1))
            content = re.sub(
                r'\*\*Total learnings:\*\* \d+',
                f'**Total learnings:** {current + new_learnings}',
                content
            )

        return content

    def _create_empty_memory(self) -> str:
        """Create empty memory file content."""
        return """# Editorial Memory

This file captures learned preferences from editorial feedback.

**Last updated:** {date}
**Total learnings:** 0

---

## Terminology Preferences

*No learnings yet*

---

## Voice & Framing

*No learnings yet*

---

## Concepts AI Tends to Miss

*No learnings yet*

---

## Structural Preferences

*No learnings yet*

---

## Phrasing Patterns

*No learnings yet*

---

## Changelog

| Date | Document | Learning |
|------|----------|----------|

""".format(date=datetime.now().strftime("%Y-%m-%d"))

    def load_memory(self) -> str:
        """Load editorial memory for use in prompts."""
        if self.memory_path.exists():
            return self.memory_path.read_text(encoding='utf-8')
        return ""

    def get_memory_summary(self) -> str:
        """Get a condensed summary for system prompts."""
        if not self.memory_path.exists():
            return "No editorial memory yet."

        content = self.memory_path.read_text(encoding='utf-8')

        # Extract key learnings for prompt injection
        summary_parts = []

        # Get terminology rules
        term_match = re.search(
            r'## Terminology Preferences\n(.*?)(?=\n---|\n## )',
            content,
            re.DOTALL
        )
        if term_match and 'No learnings' not in term_match.group(1):
            summary_parts.append("**Terminology:**")
            # Extract pattern names
            patterns = re.findall(r'### ([^\n]+)', term_match.group(1))
            for p in patterns[:5]:
                summary_parts.append(f"- {p}")

        # Get voice rules
        voice_match = re.search(
            r'## Voice & Framing\n(.*?)(?=\n---|\n## )',
            content,
            re.DOTALL
        )
        if voice_match and 'No learnings' not in voice_match.group(1):
            summary_parts.append("\n**Voice:**")
            patterns = re.findall(r'### ([^\n]+)', voice_match.group(1))
            for p in patterns[:5]:
                summary_parts.append(f"- {p}")

        # Get concepts to include
        concepts_match = re.search(
            r'## Concepts AI Tends to Miss\n(.*?)(?=\n---|\n## )',
            content,
            re.DOTALL
        )
        if concepts_match and 'No learnings' not in concepts_match.group(1):
            summary_parts.append("\n**Concepts to include:**")
            patterns = re.findall(r'### ([^\n]+)', concepts_match.group(1))
            for p in patterns[:5]:
                summary_parts.append(f"- {p}")

        if summary_parts:
            return "\n".join(summary_parts)
        return "No editorial memory yet."
