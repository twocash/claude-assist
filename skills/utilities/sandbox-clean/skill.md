# sandbox-clean

**Category:** Utilities
**Version:** 1.0.0
**Status:** Active

---

## Identity

**Purpose:** Clean up test files, mock data, and temporary artifacts from sandbox

**Triggers:**
- `/sandbox-clean`
- `/cleanup`
- "clean sandbox"
- "remove test data"

**Depends On:**
- `sandbox/` directory structure
- `.agent/status/` directory
- Safe file deletion capability

---

## Instructions

When this skill is invoked, perform controlled cleanup of test and temporary files.

### Step 1: Identify Cleanable Targets

Scan for files safe to remove:

#### Target 1: Mock Status Entries
**Location:** `.agent/status/`
**Pattern:** Entries with `mock: true` in YAML frontmatter
**Example:** `mock-sprint-*.md`

#### Target 2: Old Sandbox Files
**Location:** `sandbox/test-sprints/`, `sandbox/work/`, `sandbox/temp/`
**Pattern:** Files older than X days (default 7)
**Example:** `test-*.py`, `temp-*.txt`, `scratch-*.md`

#### Target 3: Archived Status Entries
**Location:** `.agent/status/archive/`
**Pattern:** Entries older than 30 days
**Example:** `archive/2025-12/*.md`

#### Target 4: Test Artifacts
**Location:** Various
**Patterns:**
- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `.pytest_cache/`
- `*.log` (older than 7 days)
- `*.tmp`

#### Target 5: Simulation Results
**Location:** `.agent/simulations/`
**Pattern:** Old workflow simulation outputs
**Example:** `workflow-sim-*.json`

### Step 2: Analyze Impact

Before deletion, calculate:

```markdown
# Cleanup Analysis
**Scan Date:** {timestamp}

## Cleanable Targets

### Mock Status Entries
- Count: {count} files
- Total Size: {size} KB
- Age Range: {oldest} to {newest}

### Sandbox Files
- Count: {count} files
- Total Size: {size} KB
- Directories: test-sprints (X), work (Y), temp (Z)

### Archived Entries
- Count: {count} files
- Total Size: {size} KB
- Oldest: {date}

### Test Artifacts
- __pycache__: {count} directories
- *.pyc files: {count} files
- Log files: {count} files

### Simulations
- Count: {count} files
- Total Size: {size} KB

---

## Total Impact
- **Files to Remove:** {count}
- **Space to Reclaim:** {size} MB
- **Directories to Clean:** {count}
```

### Step 3: Offer Cleanup Modes

Present options to user:

**Mode 1: Safe (Default)**
- Remove only files explicitly marked as test/mock
- Keep anything that might be important
- No prompts, just clean obvious targets

**Mode 2: Aggressive**
- Remove all old files (> 7 days) from sandbox
- Clean all test artifacts
- Archive old status entries
- Prompt before deletion

**Mode 3: Nuclear**
- Wipe entire sandbox directory
- Remove all status entries (except template)
- Clean all artifacts
- **Requires explicit confirmation**

**Mode 4: Selective**
- Interactive mode: ask about each category
- User decides what to delete

### Step 4: Perform Cleanup

Execute deletion with safety checks:

1. **Backup First** (optional):
   ```bash
   # Create backup before cleanup
   tar -czf backup-{timestamp}.tar.gz sandbox/ .agent/status/
   ```

2. **Delete Files:**
   - Use safe deletion (not immediate rm -rf)
   - Move to trash/recycle bin if available
   - Log all deletions to `.agent/logs/cleanup-{timestamp}.log`

3. **Verify Results:**
   - Confirm files removed
   - Recalculate disk usage
   - Report space reclaimed

### Step 5: Generate Cleanup Report

```markdown
# Cleanup Report
**Executed:** {timestamp}
**Mode:** {mode}
**Duration:** {seconds}s

---

## Actions Taken

### Mock Status Entries
✅ Removed {count} mock entries
✅ Space reclaimed: {size} KB

Files deleted:
- mock-sprint-20260110-*.md (15 files)
- mock-workflow-*.md (8 files)

### Sandbox Directories

**sandbox/test-sprints/**
✅ Removed {count} old test files
- test-agent-output-*.txt (12 files)
- sprint-simulation-*.json (5 files)

**sandbox/work/**
✅ Removed {count} temporary files
- scratch-*.py (3 files)
- temp-notes-*.md (7 files)

**sandbox/temp/**
✅ Cleaned entire directory
- {count} files removed

### Test Artifacts
✅ Removed {count} __pycache__ directories
✅ Removed {count} .pyc files
✅ Removed {count} old log files

### Archived Entries
✅ Removed {count} old archives (> 30 days)
- .agent/status/archive/2025-11/ (15 files)

---

## Summary

📊 **Results**
- Total Files Removed: {count}
- Directories Cleaned: {count}
- Space Reclaimed: {size} MB
- Errors: {count}

🟢 **Status:** Cleanup successful

## Preserved

Important files kept:
✅ ENTRY_TEMPLATE.md
✅ Current status entries (< 7 days)
✅ Active sandbox scripts
✅ Recent test results (< 24h)

---

## Recommendations

Next cleanup in: {days} days
Or run manually: /sandbox-clean
```

### Step 6: Handle Edge Cases

**Protected Files (Never Delete):**
- `.agent/status/ENTRY_TEMPLATE.md`
- `.agent/roles/*.md`
- `.agent/config/*.yaml`
- Active status entries (< 24h old, not COMPLETE)
- `sandbox/test-agent.py` (core utility)

**Confirmation Required:**
- Deleting > 100 files
- Reclaiming > 100 MB
- Nuclear mode
- Any non-test, non-mock files

**Error Handling:**
- Permission denied → Skip file, report error
- File in use → Skip file, recommend closing
- Invalid path → Skip, log warning

---

## Examples

### Example 1: Safe Cleanup
```
User: /sandbox-clean

Scanning for cleanup targets...

# Cleanup Analysis
**Scan Date:** 2026-01-16T21:30:00Z

## Cleanable Targets
- Mock entries: 23 files (156 KB)
- Sandbox temp files: 12 files (48 KB)
- Test artifacts: 8 __pycache__ dirs (2.3 MB)
- Old logs: 5 files (1.2 MB)

**Total:** 48 items, 3.7 MB

Proceed with safe cleanup? [Y/n]: Y

Cleaning...
✓ Removed 23 mock entries
✓ Removed 12 temp files
✓ Cleaned 8 __pycache__ directories
✓ Removed 5 log files

# Cleanup Report
**Space Reclaimed:** 3.7 MB
**Files Removed:** 48
**Status:** ✅ Success

Sandbox is clean!
```

### Example 2: Aggressive with Confirmation
```
User: /cleanup --aggressive

Scanning for cleanup targets (aggressive mode)...

# Cleanup Analysis
**Mode:** AGGRESSIVE
**Impact:** HIGH

⚠️ This will remove:
- 45 mock status entries
- 87 sandbox files (some > 1 day old)
- 124 test artifacts
- 18 archived entries (> 30 days)

**Total:** 274 files, 15.3 MB

⚠️ Some files are < 7 days old but will be removed in aggressive mode.

Type 'DELETE' to confirm: DELETE

Proceeding with aggressive cleanup...

[====================================] 100%

# Cleanup Report
**Executed:** 2026-01-16T21:35:00Z
**Mode:** AGGRESSIVE
**Duration:** 3.2s

✅ Removed 274 files
✅ Space reclaimed: 15.3 MB
✅ No errors

Sandbox aggressively cleaned!
```

### Example 3: Selective (Interactive)
```
User: /sandbox-clean --selective

Running selective cleanup...

## Target 1: Mock Status Entries (23 files, 156 KB)
Remove mock entries? [Y/n]: Y
✓ Removed 23 mock entries

## Target 2: Sandbox Temp Files (12 files, 48 KB)
Remove temp files? [Y/n]: n
↓ Skipped temp files

## Target 3: Test Artifacts (2.3 MB)
Remove __pycache__ and .pyc files? [Y/n]: Y
✓ Cleaned test artifacts

## Target 4: Old Logs (5 files, 1.2 MB)
Remove logs older than 7 days? [Y/n]: Y
✓ Removed old logs

## Target 5: Archived Entries (18 files)
Remove archives > 30 days old? [Y/n]: n
↓ Skipped archives

# Summary
Removed: 41 items
Skipped: 30 items
Space Reclaimed: 3.7 MB
```

---

## Implementation Notes

- Use `send2trash` library for safe deletion (moves to recycle bin)
- Create `.cleanup_log` with all deletion records
- Support `--dry-run` to preview without deleting
- Implement undo feature (restore from trash within 24h)
- Schedule automatic cleanup (weekly?) via cron/task scheduler

---

## Success Criteria

- ✅ Never deletes important/active files
- ✅ Requires confirmation for large deletions
- ✅ Provides clear before/after reporting
- ✅ Logs all deletions for audit trail
- ✅ Supports multiple cleanup modes

---

**Breaking changes welcome. This is the laboratory.**
