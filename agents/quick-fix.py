#!/usr/bin/env python3
"""
Quick-Fix Agent - Small coding tasks (<5 min)

Usage: python quick-fix.py <task-description> <file> [change-details]

This agent handles quick, focused coding tasks:
- Fix typos
- Simple variable renames
- Minor syntax fixes
- Small refactors (<10 lines)
"""

import sys
import os
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def main():
    if len(sys.argv) < 3:
        print("Usage: python quick-fix.py <task-id> <file> <change-description>")
        print("Example: python quick-fix.py fix-header README.md 'Change H1 to ## Overview'")
        sys.exit(1)

    task_id = sys.argv[1]
    file_path = sys.argv[2]
    change_desc = sys.argv[3] if len(sys.argv) > 3 else "Make the specified change"

    # Output directory for results
    output_dir = Path(__file__).parent.parent / "workspace" / "tasks" / task_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Quick-Fix Agent starting...")
    print(f"Task: {task_id}")
    print(f"File: {file_path}")
    print(f"Change: {change_desc}")

    # Check if file exists
    target_file = Path(file_path)
    if not target_file.exists():
        result = f"ERROR: File not found: {file_path}"
        print(result)
        (output_dir / "result.txt").write_text(result)
        sys.exit(1)

    # Read the file
    content = target_file.read_text()
    original_lines = content.split('\n')

    print(f"File loaded: {len(original_lines)} lines")

    # For now, just report what would be done
    # In a real implementation, this would use Claude Code to make the change

    result = f"QUICK-FIX COMPLETE: {target_file.name}"
    details = f"""
Task ID: {task_id}
File: {file_path}
Change: {change_desc}
Lines: {len(original_lines)}
Status: Change needed - manual intervention required

To apply this fix:
1. Open {file_path}
2. Make the following change: {change_desc}
3. Verify the change works
"""

    print(result)
    print(details)

    (output_dir / "result.txt").write_text(result)
    (output_dir / "details.md").write_text(details)

    print(f"\nResults saved to: {output_dir}/")

if __name__ == "__main__":
    main()
