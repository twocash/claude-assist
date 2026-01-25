#!/usr/bin/env python3
"""
Drafter Agent - Write first drafts and content

Usage: python drafter.py <task-id> <topic> <target-length>

This agent creates first drafts:
- Documentation
- Emails
- Reports
- Proposals
"""

import sys
import json
from pathlib import Path
from datetime import datetime

def main():
    if len(sys.argv) < 4:
        print("Usage: python drafter.py <task-id> <topic> <target-length>")
        print("Example: python drafter.py intro-email 'Welcome email for new users' 200")
        sys.exit(1)

    task_id = sys.argv[1]
    topic = sys.argv[2]
    target_length = sys.argv[3]

    # Output directory
    output_dir = Path(__file__).parent.parent / "workspace" / "tasks" / task_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Drafter Agent starting...")
    print(f"Task: {task_id}")
    print(f"Topic: {topic}")
    print(f"Target Length: {target_length} words")

    # Create draft template
    template = f"""# Draft: {topic}
**Task ID:** {task_id}
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Target Length:** {target_length} words

## Draft Content

*[Write your first draft here]*

---

## Notes
- This is a first draft - iterate as needed
- Key points to cover: [list]
- Tone: [formal/casual/informative]
- Audience: [who is this for]

## Revision History
- v1.0: Initial draft ({datetime.now().strftime('%Y-%m-%d')})

---
*Draft created by ATLAS Drafter Agent*
"""

    output_file = output_dir / "draft.md"
    output_file.write_text(template)

    print(f"\nDraft template created: {output_file}")
    print("\nTo complete draft:")
    print("1. Fill in the draft content")
    print("2. Add any supporting details")
    print("3. Review for clarity and completeness")

    # Create dispatch info
    summary = {
        "task_id": task_id,
        "topic": topic,
        "target_length": target_length,
        "status": "draft_needed",
        "output_file": str(output_file)
    }

    (output_dir / "dispatch.json").write_text(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
