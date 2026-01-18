#!/usr/bin/env python3
"""
Grove Docs Refinery - Main Orchestrator

Orchestrates the batch content refactoring workflow.
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import get_config
from checkpoint import load_checkpoint, EditorialCheckpoint

# Import both backends - we'll choose based on config
from editor import EditorAgent, Analysis, Draft
from reviewer import ReviewerAgent, Review, Assessment

# Claude-powered agents (drop-in replacements)
from claude_agents import ClaudeEditorAgent, ClaudeReviewerAgent


@dataclass
class RunManifest:
    """Manifest tracking a refinery run."""
    run_id: str
    run_date: str
    files: List[Dict] = field(default_factory=list)
    escalate_items: List[Dict] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "run_id": self.run_id,
            "run_date": self.run_date,
            "files": self.files,
            "escalate_items": self.escalate_items,
            "summary": self.summary,
        }

    def save(self, path: Path):
        path.write_text(json.dumps(self.to_dict(), indent=2))

    @classmethod
    def load(cls, path: Path) -> 'RunManifest':
        data = json.loads(path.read_text())
        manifest = cls(
            run_id=data["run_id"],
            run_date=data["run_date"],
        )
        manifest.files = data.get("files", [])
        manifest.escalate_items = data.get("escalate_items", [])
        manifest.summary = data.get("summary", {})
        return manifest


class RefineryOrchestrator:
    """Main orchestrator for Grove Docs Refinery."""

    def __init__(
        self,
        config_path: Optional[Path] = None,
        backend: Optional[str] = None,
    ):
        self.config = get_config()
        self.config.ensure_directories()

        # Use specified backend or fall back to config
        self.backend = backend or self.config.backend
        print(f"Refinery backend: {self.backend}")

        self.checkpoint: Optional[EditorialCheckpoint] = None

        # Initialize agents based on backend
        if self.backend == "claude":
            self.editor = ClaudeEditorAgent()
            self.reviewer = ClaudeReviewerAgent()
        else:
            self.editor = EditorAgent()
            self.reviewer = ReviewerAgent()

        self.manifest: Optional[RunManifest] = None

    def initialize(self):
        """Initialize the refinery."""
        # Load checkpoint
        self.checkpoint = load_checkpoint(self.config.checkpoint_path)

        # Load context for agents
        self.editor.load_context(
            engine_path=self.config.engine_path,
            checkpoint_path=self.config.checkpoint_path,
        )
        self.reviewer.load_context(
            engine_path=self.config.engine_path,
            checkpoint_path=self.config.checkpoint_path,
        )

    def run_batch(
        self,
        input_dir: Optional[Path] = None,
        output_base: Optional[Path] = None,
        batch_size: Optional[int] = None,
    ) -> RunManifest:
        """Run refinery on all files in input directory."""
        input_dir = input_dir or self.config.input_dir
        output_base = output_base or self.config.drafts_dir.parent

        batch_size = batch_size or self.config.batch_size

        # Create manifest
        run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.manifest = RunManifest(
            run_id=run_id,
            run_date=datetime.now().isoformat(),
        )

        # Scan input directory
        input_files = self._scan_input_dir(input_dir)
        print(f"Found {len(input_files)} files to process")

        # Process files
        for i, file_path in enumerate(input_files):
            print(f"\n[{i+1}/{len(input_files)}] Processing: {file_path.name}")

            try:
                result = self._process_file(file_path, output_base)
                self.manifest.files.append(result)

                if result["status"] == Assessment.ESCALATE.value:
                    self.manifest.escalate_items.append({
                        "file": file_path.name,
                        "issue": "Requires human decision",
                        "options": "See review for details",
                    })

            except Exception as e:
                print(f"ERROR: {e}")
                self.manifest.files.append({
                    "original_name": file_path.name,
                    "status": "ERROR",
                    "error": str(e),
                })

        # Generate summary
        self._generate_summary()

        # Save manifest
        manifest_path = self.config.logs_dir / f"refinery-run-{run_id}.json"
        self.manifest.save(manifest_path)
        print(f"\nManifest saved: {manifest_path}")

        return self.manifest

    def run_single(
        self,
        file_path: Path,
        output_base: Optional[Path] = None,
    ) -> Dict:
        """Run refinery on a single file."""
        output_base = output_base or self.config.drafts_dir.parent
        return self._process_file(file_path, output_base)

    def _scan_input_dir(self, input_dir: Path) -> List[Path]:
        """Scan input directory for processable files."""
        files = []
        for ext in [".md", ".txt", ".markdown"]:
            files.extend(input_dir.glob(f"*{ext}"))
        return sorted(files)

    def _process_file(
        self,
        file_path: Path,
        output_base: Path,
    ) -> Dict:
        """Process a single file through the pipeline."""
        working_name = self._normalize_name(file_path.name)

        # Phase 1: Analysis
        print(f"  Analyzing...")
        analysis = self.editor.analyze(file_path)

        # Phase 2: Editor Pass
        print(f"  Rewriting...")
        draft = self.editor.rewrite(file_path, analysis)

        # Save draft
        draft_path = self.config.drafts_dir / f"{working_name}--DRAFT.md"
        draft_content = self._format_draft(draft)
        draft_path.write_text(draft_content, encoding="utf-8")

        # Phase 3: Reviewer Pass
        print(f"  Reviewing...")
        review = self.reviewer.validate(file_path, draft_path)

        # Save review
        review_path = self.config.reviews_dir / f"{working_name}--REVIEW.md"
        review_content = self.reviewer.generate_review_report(review)
        review_path.write_text(review_content, encoding="utf-8")

        # Determine final status and move to appropriate output
        if review.assessment == Assessment.PASS:
            final_path = self.config.refined_dir / f"{working_name}--FINAL.md"
            final_content = draft.content
            status = "PASS"
        elif review.assessment == Assessment.REVISE:
            # Keep draft for revision
            final_path = None
            status = "REVISE"
        else:  # ESCALATE
            final_path = None
            status = "ESCALATE"

        if final_path:
            final_path.write_text(final_content, encoding="utf-8")

        # Calculate word counts
        original_words = analysis.word_count
        refined_words = len(draft.content.split()) if draft.content else 0

        result = {
            "original_name": file_path.name,
            "working_name": working_name,
            "status": status,
            "original_words": original_words,
            "refined_words": refined_words,
            "draft_path": str(draft_path),
            "review_path": str(review_path) if review_path else None,
            "final_path": str(final_path) if final_path else None,
            "notes": review.specific_feedback[:200] if review.specific_feedback else "",
        }

        print(f"  Status: {status}")

        return result

    def _format_draft(self, draft: Draft) -> str:
        """Format draft as markdown."""
        lines = [
            f"## Rewrite: {draft.working_name}",
            f"### Diagnosis Summary",
            draft.diagnosis_summary,
            "",
            "### Key Changes Made",
        ]
        for change in draft.key_changes:
            lines.append(f"- {change}")
        lines.extend([
            "",
            "### Flags for Review",
        ])
        for flag in draft.flags_for_review:
            lines.append(f"- {flag}")
        lines.extend([
            "",
            "---",
            draft.content,
        ])
        return "\n".join(lines)

    def _normalize_name(self, name: str) -> str:
        """Normalize filename."""
        # Strip spaces, use kebab-case
        return name.strip().replace(" ", "-").lower()

    def _generate_summary(self):
        """Generate run summary."""
        if not self.manifest:
            return

        files = self.manifest.files
        total = len(files)
        passed = sum(1 for f in files if f.get("status") == "PASS")
        revised = sum(1 for f in files if f.get("status") == "REVISE")
        escalated = sum(1 for f in files if f.get("status") == "ESCALATE")
        errors = sum(1 for f in files if f.get("status") == "ERROR")

        total_orig_words = sum(f.get("original_words", 0) for f in files)
        total_refined_words = sum(f.get("refined_words", 0) for f in files)

        self.manifest.summary = {
            "total_files": total,
            "passed": passed,
            "revised": revised,
            "escalated": escalated,
            "errors": errors,
            "total_original_words": total_orig_words,
            "total_refined_words": total_refined_words,
            "word_change_pct": (
                int((total_refined_words / total_orig_words * 100))
                if total_orig_words > 0 else 0
            ),
        }

        # Print summary
        print("\n" + "=" * 50)
        print("REFINERY RUN SUMMARY")
        print("=" * 50)
        print(f"Files processed: {total}")
        print(f"  PASS: {passed}")
        print(f"  REVISE: {revised}")
        print(f"  ESCALATE: {escalated}")
        print(f"  ERROR: {errors}")
        print(f"Words: {total_orig_words} -> {total_refined_words} ({self.manifest.summary['word_change_pct']}%)")

        if self.manifest.escalate_items:
            print("\nESCALATE ITEMS REQUIRING DECISION:")
            for item in self.manifest.escalate_items:
                print(f"  - {item['file']}: {item['issue']}")

    def generate_summary_report(self) -> str:
        """Generate human-readable summary report."""
        if not self.manifest:
            return "No run recorded."

        summary = self.manifest.summary
        lines = [
            "# Refinery Run Summary",
            f"**Run ID:** {self.manifest.run_id}",
            f"**Date:** {self.manifest.run_date}",
            "",
            "## Results",
            f"- Files processed: {summary['total_files']}",
            f"- PASS: {summary['passed']}",
            f"- REVISE: {summary['revised']}",
            f"- ESCALATE: {summary['escalated']}",
            f"- ERROR: {summary['errors']}",
            "",
            "## Word Count",
            f"- Original: {summary['total_original_words']:,}",
            f"- Refined: {summary['total_refined_words']:,}",
            f"- Change: {summary['word_change_pct']}%",
        ]

        if self.manifest.escalate_items:
            lines.extend([
                "",
                "## Escalate Items",
            ])
            for item in self.manifest.escalate_items:
                lines.append(f"### {item['file']}")
                lines.append(f"**Issue:** {item['issue']}")
                lines.append(f"**Options:** {item['options']}")
                lines.append("")

        return "\n".join(lines)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Grove Docs Refinery - Batch content refactoring"
    )
    parser.add_argument(
        "--single",
        type=Path,
        help="Process a single file",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=None,
        help="Input directory (default: config input_dir)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=None,
        help="Files per batch",
    )
    parser.add_argument(
        "--backend",
        choices=["claude", "rules"],
        default=None,
        help="Processing backend: 'claude' (AI-powered) or 'rules' (regex-based)",
    )

    args = parser.parse_args()

    orchestrator = RefineryOrchestrator(backend=args.backend)
    orchestrator.initialize()

    if args.single:
        result = orchestrator.run_single(args.single)
        print(f"\nResult: {result['status']}")
    else:
        manifest = orchestrator.run_batch(
            input_dir=args.input,
            batch_size=args.batch_size,
        )
        print("\n" + orchestrator.generate_summary_report())


if __name__ == "__main__":
    main()
