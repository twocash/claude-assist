#!/usr/bin/env python3
"""
File Organizer Agent - Organize files and directories

Usage: python file-organizer.py <task-id> <source> <destination> <pattern>

This agent organizes files:
- Move files between directories
- Rename files with patterns
- Organize by type/date
- Clean up clutter
"""

import sys
import shutil
from pathlib import Path
from datetime import datetime

def main():
    if len(sys.argv) < 5:
        print("Usage: python file-organizer.py <task-id> <source> <destination> <pattern>")
        print("Example: python file-organizer.py organize-downloads ~/Downloads ~/Documents/documents *.pdf")
        sys.exit(1)

    task_id = sys.argv[1]
    source = Path(sys.argv[2]).expanduser()
    destination = Path(sys.argv[3]).expanduser()
    pattern = sys.argv[4]

    # Output directory
    output_dir = Path(__file__).parent.parent / "workspace" / "tasks" / task_id
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"File Organizer starting...")
    print(f"Task: {task_id}")
    print(f"Source: {source}")
    print(f"Destination: {destination}")
    print(f"Pattern: {pattern}")

    if not source.exists():
        result = f"ERROR: Source directory not found: {source}"
        print(result)
        (output_dir / "result.txt").write_text(result)
        sys.exit(1)

    # Find matching files
    if pattern == "*":
        files = list(source.iterdir())
    else:
        files = list(source.glob(pattern))

    print(f"\nFound {len(files)} matching files")

    # Create organization plan
    plan = f"""# File Organization Plan
**Task ID:** {task_id}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Source
{source}

## Destination
{destination}

## Pattern
{pattern}

## Files to Organize ({len(files)})

"""

    for i, f in enumerate(files, 1):
        plan += f"{i}. {f.name}\n"

    plan += f"""
## Organization Plan

### Step 1: Create destination directory if needed
```
mkdir -p "{destination}"
```

### Step 2: Move files
"""

    for f in files:
        dest_file = destination / f.name
        plan += f```
mv "{f}" "{dest_file}"
```

    plan += """
## Verification
- [ ] All files moved
- [ ] No duplicates created
- [ ] Original files removed

---
*Organization plan by ATLAS File Organizer Agent*
"""

    output_file = output_dir / "organization-plan.md"
    output_file.write_text(plan)

    print(f"\nOrganization plan: {output_file}")
    print(f"\n{len(files)} files found matching '{pattern}'")

    # Create dispatch info
    summary = {
        "task_id": task_id,
        "source": str(source),
        "destination": str(destination),
        "pattern": pattern,
        "files_count": len(files),
        "status": "plan_created",
        "plan_file": str(output_file)
    }

    (output_dir / "dispatch.json").write_text(str(summary))

    print("\nTo execute organization:")
    print("1. Review the organization plan")
    print("2. Execute the mv commands, or")
    print("3. Run this agent again with --execute flag")

if __name__ == "__main__":
    main()
