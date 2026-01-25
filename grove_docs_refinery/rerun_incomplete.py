#!/usr/bin/env python3
"""
Re-run refinery on incomplete documents.

These 13 files were identified as stubs (< 30 lines) in the refined/ folder.
This script re-processes them from their original input sources.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from refinery import RefineryOrchestrator

# Mapping of incomplete refined files to their input sources
INCOMPLETE_TO_INPUT = {
    '260119-s-software-bedrock-information-architecture.md--FINAL.md':
        '260100-S-ARCH-Bedrock Information Architecture.md',
    '260119-s-software-field-architecture.md--FINAL.md':
        '251200-S-ARCH-Field Architecture Namespacing.md',
    '260119-s-software-grove-white-paper-prompt-kit.md--FINAL.md':
        '251200-S-METHOD-White Paper Prompt Kit.md',
    '260119-s-software-the-copilot-configurator-local-inference.md--FINAL.md':
        '251200-S-PATTERN-Copilot Configurator.md',
    '260119-s-software-the-trellis-architecture-first-order-directives.md--FINAL.md':
        '251200-S-ARCH-Trellis First Order Directives Alt.md',
    '260119-s-software-user-story-refinery-v1.md--FINAL.md':
        '251200-S-METHOD-User Story Refinery.md',
    '260119-v-vision-chinese-open-source-ai-ratchet-acceleration-thesis.md--FINAL.md':
        '251200-V-RESEARCH-Chinese Open Source Ratchet Evidence.md',
    '260119-v-vision-grove-economics-deep-dive.md--FINAL.md':
        '251200-V-ECON-Economics Deep Dive.md',
    '260119-v-vision-grove-simulation-deep-dive.md--FINAL.md':
        '251200-V-ENGAGE-Simulation Ethics Deep Dive.md',
    '260119-v-vision-how-translation-emerged-in-llms-and-why-it-matters.md--FINAL.md':
        '251200-V-RESEARCH-Translation Emergence in LLMs.md',
    '260119-v-vision-the-grove-terminal-a-deep-dive.md--FINAL.md':
        '251200-V-ENGAGE-Terminal Deep Dive.md',
    '260119-v-vision-why-distributed-ai-infrastructure-matters.md--FINAL.md':
        '251200-V-EDGE-Distributed Infrastructure Implications.md',
    '260119-v-vision-world-models-and-memory-architectures.md--FINAL.md':
        '251200-V-RESEARCH-World Models Memory Architectures.md',
}

MIN_OUTPUT_CHARS = 1000  # Quality threshold


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
    # Use absolute paths
    base_dir = Path('C:/GitHub/claude-assist/grove_docs_refinery')
    input_dir = base_dir / 'input'
    refined_dir = base_dir / 'refined'

    print("=" * 60)
    print("GROVE DOCS REFINERY - Re-run Incomplete Files")
    print("=" * 60)
    print(f"Processing {len(INCOMPLETE_TO_INPUT)} files")
    print()

    # Initialize refinery
    refinery = RefineryOrchestrator(backend='claude')
    refinery.initialize()

    results = {
        'success': 0,
        'failed_quality': 0,
        'error': 0,
    }

    for refined_name, input_name in INCOMPLETE_TO_INPUT.items():
        print(f"\n{'='*60}")
        print(f"Processing: {input_name[:50]}...")

        input_path = input_dir / input_name
        refined_path = refined_dir / refined_name

        if not input_path.exists():
            print(f"  ERROR: Input file not found")
            results['error'] += 1
            continue

        # Backup existing stub
        if refined_path.exists():
            backup_path = refined_path.with_suffix('.md.bak')
            refined_path.rename(backup_path)
            print(f"  Backed up stub to: {backup_path.name}")

        try:
            # Run refinery
            result = refinery.run_single(input_path)

            if result['status'] == 'PASS' and result.get('final_path'):
                # Check quality
                final_content = Path(result['final_path']).read_text(encoding='utf-8')
                passed, msg = check_quality(final_content)

                if passed:
                    print(f"  SUCCESS: {msg}")
                    results['success'] += 1
                else:
                    print(f"  QUALITY FAIL: {msg}")
                    results['failed_quality'] += 1
                    # Restore backup
                    if backup_path.exists():
                        backup_path.rename(refined_path)
            else:
                print(f"  REFINERY STATUS: {result['status']}")
                print(f"  Notes: {result.get('notes', 'N/A')[:100]}")
                results['error'] += 1
                # Restore backup
                if backup_path.exists():
                    backup_path.rename(refined_path)

        except Exception as e:
            print(f"  EXCEPTION: {e}")
            results['error'] += 1
            # Restore backup
            if backup_path.exists():
                backup_path.rename(refined_path)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Success:        {results['success']}")
    print(f"Quality Failed: {results['failed_quality']}")
    print(f"Errors:         {results['error']}")
    print(f"Total:          {len(INCOMPLETE_TO_INPUT)}")


if __name__ == '__main__':
    main()
