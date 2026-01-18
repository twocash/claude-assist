# python-env

**Category:** Utilities
**Version:** 1.0.0
**Status:** Active

---

## Identity

**Purpose:** Check Python environment health, validate versions, and verify dependencies

**Triggers:**
- `/python-env`
- `/check-python`
- "verify python environment"
- "check python version"

**Depends On:**
- Python 3.14.0 installation
- Access to command line

---

## Instructions

When this skill is invoked, perform comprehensive Python environment validation.

### Step 1: Check Python Installation

Verify Python is installed and accessible:

1. **Check python command:**
   ```bash
   python --version
   python3 --version
   ```

2. **Check python.exe location:**
   ```bash
   where python     # Windows
   which python     # Linux/Mac
   ```

3. **Expected Location:**
   - Windows: `C:\Python314\python.exe`
   - Linux: `/usr/local/bin/python3.14` or similar

### Step 2: Validate Python Version

Ensure correct version is active:

```python
import sys
print(f"Python {sys.version}")
print(f"Version Info: {sys.version_info}")
```

**Expected:** Python 3.14.0 or 3.14.x

**Alert if:**
- Version < 3.14
- Version is 3.13 or older (wrong version active)
- Multiple Python installations detected

### Step 3: Check Core Packages

Verify essential packages are available:

```bash
python -c "import yaml; print('PyYAML:', yaml.__version__)"
python -c "import json; print('JSON: built-in')"
python -c "import datetime; print('datetime: built-in')"
python -c "import pathlib; print('pathlib: built-in')"
```

**Required Packages:**
- PyYAML (for status entry parsing)
- Standard library modules (json, datetime, pathlib, os, sys)

### Step 4: Check Virtual Environment

Determine if venv is active:

```python
import sys
in_venv = sys.prefix != sys.base_prefix
print(f"Virtual Environment: {in_venv}")
if in_venv:
    print(f"Venv Path: {sys.prefix}")
```

**Recommendation:**
- Not required, but useful for isolation
- Suggest creating venv if many packages needed

### Step 5: Test Python Execution

Run sample code to verify functionality:

```python
# Test script: test-python.py
import sys
import json
import datetime
from pathlib import Path

def test_environment():
    """Validate Python environment."""
    checks = {
        "python_version": sys.version_info >= (3, 14),
        "json_module": True,
        "datetime_module": True,
        "pathlib_module": True,
    }

    try:
        import yaml
        checks["pyyaml"] = True
    except ImportError:
        checks["pyyaml"] = False

    return checks

if __name__ == "__main__":
    results = test_environment()
    print(json.dumps(results, indent=2))
```

Execute and verify output.

### Step 6: Generate Environment Report

Present findings in structured format:

```markdown
# Python Environment Report
**Generated:** {timestamp}
**Location:** {working_directory}

---

## Python Installation

✅ **Version:** Python 3.14.0
✅ **Location:** C:\Python314\python.exe
✅ **Accessible:** python, python3 commands work

## Core Modules

✅ **json** - Built-in (OK)
✅ **datetime** - Built-in (OK)
✅ **pathlib** - Built-in (OK)
✅ **sys** - Built-in (OK)
✅ **os** - Built-in (OK)

## Required Packages

✅ **PyYAML** - 6.0.1 (OK)

## Virtual Environment

ℹ️ **Status:** Not activated
ℹ️ **Recommendation:** Optional for this project

## Execution Test

✅ **Sample Script:** Executed successfully
✅ **All Checks:** Passed

---

## Summary

🟢 **Environment Status:** HEALTHY

All requirements satisfied. Python 3.14.0 is correctly installed and functional.

### Recommended Actions
None - environment ready for use.

---

## Troubleshooting Commands

If issues arise:

```bash
# Reinstall PyYAML
python -m pip install --upgrade pyyaml

# Check pip
python -m pip --version

# List installed packages
python -m pip list

# Create virtual environment (optional)
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux
```
```

### Step 7: Suggest Fixes for Issues

If problems detected, provide specific remediation:

**Issue:** Python not found
```
❌ Python command not recognized

Fix:
1. Verify Python 3.14.0 is installed
2. Add to PATH:
   - Windows: Add C:\Python314 to System PATH
   - Linux: Ensure python3.14 is symlinked
3. Restart terminal
```

**Issue:** Wrong Python version
```
⚠️ Python 3.13.0 detected (expected 3.14.0)

Fix:
1. Install Python 3.14.0 from python.org
2. Update PATH to prioritize 3.14
3. Verify with: python --version
```

**Issue:** Missing PyYAML
```
❌ PyYAML not installed

Fix:
python -m pip install pyyaml

Or add to requirements.txt:
pyyaml>=6.0
```

---

## Examples

### Example 1: Healthy Environment
```
User: /python-env

Checking Python environment...

# Python Environment Report
**Generated:** 2026-01-16T21:15:00Z

## Python Installation
✅ Version: Python 3.14.0
✅ Location: C:\Python314\python.exe
✅ Commands: python, python3 both work

## Required Packages
✅ PyYAML: 6.0.1

## Execution Test
✅ All checks passed

## Summary
🟢 Environment Status: HEALTHY

No action needed. Ready for agent testing.
```

### Example 2: Issues Detected
```
User: /check-python

Checking Python environment...

# Python Environment Report
**Generated:** 2026-01-16T21:15:00Z

## Python Installation
⚠️ Version: Python 3.13.5 (expected 3.14.0)
✅ Location: C:\Python313\python.exe
✅ Commands: python works

## Required Packages
❌ PyYAML: NOT FOUND

## Summary
🟡 Environment Status: NEEDS ATTENTION

### Issues Found

1. **Wrong Python Version**
   - Current: 3.13.5
   - Expected: 3.14.0
   - Impact: May lack 3.14 features

   Fix: Install Python 3.14.0

2. **Missing PyYAML**
   - Required for status entry parsing

   Fix: python -m pip install pyyaml

### Recommended Actions

1. Upgrade to Python 3.14.0
2. Install PyYAML package
3. Re-run /python-env to verify
```

---

## Implementation Notes

- Run checks in subprocess to avoid import pollution
- Cache version info for 1 hour (doesn't change frequently)
- Support `--fix` flag to auto-install missing packages
- Integrate with health-check skill for full infrastructure validation
- Log environment reports to `.agent/reports/python-env/`

---

## Success Criteria

- ✅ Accurately detects Python version
- ✅ Verifies required packages
- ✅ Tests actual Python execution
- ✅ Provides actionable fix suggestions
- ✅ Clear pass/fail status indication

---

**Breaking changes welcome. This is the laboratory.**
