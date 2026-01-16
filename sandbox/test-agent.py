#!/usr/bin/env python3
"""
Test Agent - Status Logging Protocol Simulator

Tests the agent coordination infrastructure by simulating
status entry creation and heartbeat updates.
"""

import os
import time
from datetime import datetime, timezone
from pathlib import Path

# Configuration
REPO_ROOT = Path(__file__).parent.parent
STATUS_DIR = REPO_ROOT / ".agent" / "status" / "current"
TEMPLATE_PATH = REPO_ROOT / ".agent" / "status" / "ENTRY_TEMPLATE.md"

def get_timestamp():
    """Return current timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def get_next_entry_number():
    """Find the next available entry number."""
    if not STATUS_DIR.exists():
        return 1

    entries = list(STATUS_DIR.glob("*.md"))
    if not entries:
        return 1

    numbers = []
    for entry in entries:
        try:
            num = int(entry.name.split("-")[0])
            numbers.append(num)
        except ValueError:
            continue

    return max(numbers) + 1 if numbers else 1

def create_status_entry(sprint_name, agent_name, status, phase, summary, **kwargs):
    """Create a status entry file."""
    STATUS_DIR.mkdir(parents=True, exist_ok=True)

    entry_num = get_next_entry_number()
    timestamp = get_timestamp()
    timestamp_safe = timestamp.replace(":", "-")

    filename = f"{entry_num:03d}-{timestamp_safe}-{agent_name}.md"
    filepath = STATUS_DIR / filename

    # Build frontmatter
    frontmatter = f"""---
timestamp: {timestamp}
sprint: {sprint_name}
status: {status}
agent: {agent_name}
branch: {kwargs.get('branch', 'main')}
heartbeat: {timestamp}
severity: {kwargs.get('severity', 'INFO')}
sprint_id: {kwargs.get('sprint_id', '')}
notion_synced: false
phase: {phase}
commit: {kwargs.get('commit', '')}
---

## {timestamp} | {sprint_name} | {phase}

**Agent:** {agent_name} / {kwargs.get('branch', 'main')}
**Status:** {status}
**Summary:** {summary}
**Files:** {kwargs.get('files', 'N/A')}
**Tests:** {kwargs.get('tests', 'N/A')}
**Commit:** {kwargs.get('commit', 'TBD')}
**Unblocks:** {kwargs.get('unblocks', 'N/A')}
**Next:** {kwargs.get('next', 'Continue work')}
"""

    filepath.write_text(frontmatter, encoding='utf-8')
    print(f"[OK] Created: {filename}")
    return filepath

def update_heartbeat(filepath):
    """Update the heartbeat timestamp in an existing entry."""
    if not filepath.exists():
        print(f"[ERR] Entry not found: {filepath}")
        return False

    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    new_timestamp = get_timestamp()
    updated_lines = []

    for line in lines:
        if line.startswith('heartbeat:'):
            updated_lines.append(f'heartbeat: {new_timestamp}')
        else:
            updated_lines.append(line)

    filepath.write_text('\n'.join(updated_lines), encoding='utf-8')
    print(f"[HB] Heartbeat updated: {new_timestamp}")
    return True

def simulate_happy_path():
    """Simulate a normal agent workflow."""
    print("\n=== Simulating Happy Path ===\n")

    # STARTED
    entry = create_status_entry(
        sprint_name="test-coordination-v1",
        agent_name="test-agent",
        status="STARTED",
        phase="Initialization",
        summary="Beginning test coordination sprint"
    )

    time.sleep(2)

    # IN_PROGRESS
    entry = create_status_entry(
        sprint_name="test-coordination-v1",
        agent_name="test-agent",
        status="IN_PROGRESS",
        phase="Implementation",
        summary="Testing status entry creation and heartbeat updates",
        files="sandbox/test-agent.py",
        tests="N/A"
    )

    # Simulate heartbeat updates
    print("\nSimulating heartbeat updates (3x with 2s intervals)...")
    for i in range(3):
        time.sleep(2)
        update_heartbeat(entry)

    time.sleep(2)

    # COMPLETE
    create_status_entry(
        sprint_name="test-coordination-v1",
        agent_name="test-agent",
        status="COMPLETE",
        phase="Completion",
        summary="Successfully tested coordination protocol with status entries and heartbeats",
        files="sandbox/test-agent.py, .agent/status/current/*.md",
        tests="Manual verification",
        commit="test-run",
        unblocks="Health check validation",
        next="Run chief-of-staff health check"
    )

    print("\n[OK] Happy path simulation complete!")

def main():
    """Main entry point."""
    print("Test Agent - Status Logging Protocol Simulator")
    print("=" * 50)
    print(f"Repository: {REPO_ROOT}")
    print(f"Status Directory: {STATUS_DIR}")
    print(f"Python: {os.sys.version}")

    if not TEMPLATE_PATH.exists():
        print(f"\n[ERR] Template not found: {TEMPLATE_PATH}")
        print("Run infrastructure setup first.")
        return 1

    simulate_happy_path()

    print("\n" + "=" * 50)
    print("Check status entries in: .agent/status/current/")
    print("Run health check with: /chief-of-staff")

    return 0

if __name__ == "__main__":
    exit(main())
