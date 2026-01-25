#!/usr/bin/env python3
"""
Re-run refinery on 36 REVISE documents using Opus.

These documents failed the first pass due to context window limits with Sonnet.
Settings have been updated to use claude-opus-4-20250514 for the writer agent.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from refinery import RefineryOrchestrator

# Base directory
BASE_DIR = Path('C:/GitHub/claude-assist/grove_docs_refinery')

# The 36 REVISE documents - mapped from review file naming back to input files
# Review: lowercase-hyphenated -> Input: Mixed Case with Spaces
REVISE_DOCUMENTS = [
    # Large documents (30KB+) - definitely need Opus
    '251200-V-THESIS-Grove World Changing Play Full.md',          # 213KB
    '251200-V-THESIS-Grove World Changing Play Condensed.md',     # 60KB
    '251200-V-ECON-Asymptotic Convergence Capital Cognition.md',  # 35KB
    '251200-S-ARCH-Technical Architecture Reference.md',          # 35KB
    '251200-V-ENGAGE-Engagement Research Brief.md',               # 34KB
    '251200-S-SPEC-Research Agent Product Vision.md',             # 32KB
    '251200-V-THESIS-Grove World Changing Play V2 Draft.md',      # 32KB
    '260100-S-EXEC-Grove Execution Protocol v1.4.md',             # 31KB

    # Medium documents (15-30KB)
    '251200-V-EDGE-Capability Trajectory 2023-2025.md',           # 26KB
    '260100-V-RESEARCH-Coordination Physics Validates DEX.md',    # 26KB
    '251200-S-METHOD-Sprout System Cultivation.md',               # 24KB
    '251200-V-EDGE-Why Edge Is Structural Answer.md',             # 24KB
    '251200-V-THESIS-White Paper Outline.md',                     # 24KB
    '260100-S-DRAFT-Cognitive Simulator Sprints 4-6.md',          # 21KB
    '251200-V-RATCHET-Deep Dive.md',                              # 21KB
    '251200-V-RESEARCH-FunctionGemma Validates Hybrid Theory.md', # 21KB
    '260100-S-PATTERN-Declarative Wizard Engine.md',              # 21KB
    '260100-S-ARCH-Bedrock Information Architecture.md',          # 20KB
    '260112-S-SPEC-Research Lifecycle 1.0 Roadmap.md',            # 19KB
    '251200-S-METHOD-Foundation Loop Full Skill.md',              # 19KB
    '251200-S-PATTERN-Hub Prefixes and Rules.md',                 # 16KB
    '251200-V-EDGE-P2P Networking for Decentralization.md',       # 15KB
    '251200-V-ENGAGE-Knowledge Commons Deep Dive.md',             # 15KB

    # Smaller documents (10-15KB) - should work but using Opus for consistency
    '251200-V-EDGE-Grove as Infrastructure Provider.md',          # 15KB
    '251200-V-ENGAGE-Journal System Architecture.md',             # 14KB
    '251224-S-PATTERN-Console Extraction vs Rewrite.md',          # 14KB
    '251200-V-THESIS-Grove Infrastructure Overview.md',           # 13KB
    '251230-S-EXEC-Bedrock Sprint Contract v1.0.md',              # 13KB
    '260104-S-EXEC-Bedrock Sprint Contract v1.1.md',              # 17KB
    '251200-V-RATCHET-Capability Propagation Thesis.md',          # 12KB
    '251200-V-RATCHET-Quantitative Analysis.md',                  # 12KB
    '251200-V-RESEARCH-Multi Agent Stacking Architecture.md',     # 11KB
    '251200-V-STRAT-Exploration Architecture Insight.md',         # 11KB
    '251200-V-STRAT-Purdue Partnership Proposal.md',              # 11KB
    '251200-V-THESIS-White Paper Key Concepts.md',                # 10KB
    '251200-S-ARCH-Architecture Documentation Index.md',          # 10KB
    '260100-S-SPEC-DEX Master Code Hygiene Agent.md',             # 10KB
    '260100-S-EXEC-DEX Master Scan Prompt.md',                    # 8KB
    '260105-S-SPEC-Exploration Architecture Self Validation.md',  # 7KB
    '251230-S-ARCH-Trellis Bedrock Addendum.md',                  # 6KB
    '251200-V-ECON-Declining Take Rate Mechanism.md',             # 5KB
    '251200-V-ECON-Reverse Progressive Tax Model.md',             # 5KB
]

MIN_OUTPUT_CHARS = 1000  # Quality threshold


def find_input_file(name: str, input_dir: Path) -> Path | None:
    """Find the input file - handles case sensitivity on Windows."""
    # Direct match first
    exact_path = input_dir / name
    if exact_path.exists():
        return exact_path

    # Case-insensitive search
    name_lower = name.lower()
    for f in input_dir.iterdir():
        if f.name.lower() == name_lower:
            return f

    return None


def check_quality(content: str) -> tuple[bool, str]:
    """Check if output meets quality threshold."""
    if not content:
        return False, "Empty content"

    # Strip frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2].strip()
        else:
            body = content
    else:
        body = content

    if len(body) < MIN_OUTPUT_CHARS:
        return False, f"Content too short ({len(body)} < {MIN_OUTPUT_CHARS})"

    return True, f"OK ({len(body)} chars)"


def main():
    input_dir = BASE_DIR / 'input'
    refined_dir = BASE_DIR / 'refined'

    print("=" * 70)
    print("GROVE DOCS REFINERY - Re-run REVISE Documents with Opus")
    print("=" * 70)
    print(f"Model: claude-opus-4-20250514 (larger context window)")
    print(f"Documents to process: {len(REVISE_DOCUMENTS)}")
    print()

    # Verify input files exist
    missing = []
    for name in REVISE_DOCUMENTS:
        if not find_input_file(name, input_dir):
            missing.append(name)

    if missing:
        print(f"WARNING: {len(missing)} input files not found:")
        for name in missing[:5]:
            print(f"  - {name}")
        if len(missing) > 5:
            print(f"  ... and {len(missing) - 5} more")
        print()

    # Initialize refinery
    print("Initializing refinery with Opus settings...")
    refinery = RefineryOrchestrator(backend='claude')
    refinery.initialize()
    print("Ready.\n")

    results = {
        'success': 0,
        'revise': 0,
        'escalate': 0,
        'error': 0,
        'skipped': 0,
    }

    start_time = datetime.now()

    for i, name in enumerate(REVISE_DOCUMENTS, 1):
        print(f"\n{'='*70}")
        print(f"[{i}/{len(REVISE_DOCUMENTS)}] {name[:60]}...")

        input_path = find_input_file(name, input_dir)
        if not input_path:
            print(f"  SKIPPED: Input file not found")
            results['skipped'] += 1
            continue

        file_size = input_path.stat().st_size
        print(f"  Size: {file_size / 1024:.1f} KB")

        try:
            # Run refinery
            result = refinery.run_single(input_path)

            status = result.get('status', 'UNKNOWN')

            if status == 'PASS' and result.get('final_path'):
                # Check quality
                final_content = Path(result['final_path']).read_text(encoding='utf-8')
                passed, msg = check_quality(final_content)

                if passed:
                    print(f"  PASS: {msg}")
                    results['success'] += 1
                else:
                    print(f"  QUALITY FAIL: {msg}")
                    results['error'] += 1
            elif status == 'REVISE':
                print(f"  REVISE: Still failed - may need manual review")
                notes = result.get('notes', '')[:100]
                if notes:
                    print(f"  Notes: {notes}")
                results['revise'] += 1
            elif status == 'ESCALATE':
                print(f"  ESCALATE: Requires manual intervention")
                results['escalate'] += 1
            else:
                print(f"  STATUS: {status}")
                results['error'] += 1

        except Exception as e:
            print(f"  EXCEPTION: {e}")
            results['error'] += 1

        # Progress update every 10 docs
        if i % 10 == 0:
            elapsed = (datetime.now() - start_time).total_seconds()
            avg_time = elapsed / i
            remaining = (len(REVISE_DOCUMENTS) - i) * avg_time
            print(f"\n  --- Progress: {i}/{len(REVISE_DOCUMENTS)} | "
                  f"~{remaining/60:.1f} min remaining ---\n")

    # Summary
    elapsed = (datetime.now() - start_time).total_seconds()
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Success (PASS):    {results['success']}")
    print(f"Still REVISE:      {results['revise']}")
    print(f"ESCALATE:          {results['escalate']}")
    print(f"Errors:            {results['error']}")
    print(f"Skipped:           {results['skipped']}")
    print(f"Total:             {len(REVISE_DOCUMENTS)}")
    print(f"Time:              {elapsed/60:.1f} minutes")
    print("=" * 70)

    # Return exit code based on success
    success_rate = results['success'] / len(REVISE_DOCUMENTS)
    if success_rate < 0.5:
        print("\nWARNING: Less than 50% success rate")
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
