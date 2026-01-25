#!/usr/bin/env python3
"""
Research Agent - Research and summarize topics

Usage: python researcher.py <task-id> <topic> <format>

This agent researches topics and delivers summaries:
- Web search and synthesis
- Key findings extraction
- Link collection
- Format: brief, detailed, or report
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def main():
    if len(sys.argv) < 4:
        print("Usage: python researcher.py <task-id> <topic> <format>")
        print("Example: python researcher.py ai-agents 'Latest AI agents' brief")
        sys.exit(1)

    task_id = sys.argv[1]
    topic = sys.argv[2]
    format_type = sys.argv[3].lower()

    # Output directory
    output_dir = Path(__file__).parent.parent / "workspace" / "tasks" / task_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Research Agent starting...")
    print(f"Task: {task_id}")
    print(f"Topic: {topic}")
    print(f"Format: {format_type}")

    # Research would use web search tools here
    # For now, create a template for research results

    template = f"""# Research: {topic}
**Task ID:** {task_id}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Format:** {format_type}

## Executive Summary
*[Brief 2-3 sentence summary of key findings]*

## Key Findings

### Finding 1
*[Description]*
- Point 1
- Point 2

### Finding 2
*[Description]*
- Point 1
- Point 2

## Important Links

1. [Title](url) - Description
2. [Title](url) - Description

## Recommendations
*[Based on research findings]*

## Next Steps
1. Action item 1
2. Action item 2

---
*Research completed by ATLAS Researcher Agent*
"""

    output_file = output_dir / "research.md"
    output_file.write_text(template)

    print(f"\nResearch template created: {output_file}")
    print("\nTo complete research:")
    print("1. Fill in the template with research findings")
    print("2. Add important links and sources")
    print("3. Update recommendations based on findings")

    # Create summary file
    summary = {
        "task_id": task_id,
        "topic": topic,
        "format": format_type,
        "status": "research_needed",
        "output_file": str(output_file)
    }

    (output_dir / "dispatch.json").write_text(json.dumps(summary, indent=2))

    print(f"\nDispatch info saved to: {output_dir}/dispatch.json")

if __name__ == "__main__":
    main()
