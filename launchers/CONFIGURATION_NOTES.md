# Atlas/CLAUDE.md Configuration Notes
**Date:** 2026-01-17

---

## User Goal

Jim wants to run a separate "personal assistant" Claude Code setup using the ATLAS persona, Notion integration, and custom skills - completely separate from the Grove Foundation work.

**Key Requirements:**
- Personal agentic system: ATLAS chief-of-staff mode
- Notion integration (personal workspace, not Grove)
- Custom skills and workflows
- Run alongside Grove (different directory/session)
- Use Claude Opus model (not MiniMax)

---

## Current Problem

**Configuration Conflict:** Claude Code keeps defaulting to MiniMax M2.1 model instead of Claude Opus.

**Root Cause:**
- `MINIMAX_API_KEY` was set permanently at the Windows user level via `setx`
- Batch launcher scripts (`claude-opus.bat`) set `set MINIMAX_API_KEY=` but this only clears for the subprocess
- The permanent env var persists across all terminal sessions
- Result: Claude Code always routes through MiniMax API

---

## Solution Applied

**Step 1: Remove permanent MiniMax environment variable**

Run as Administrator (PowerShell):
```powershell
[System.Environment]::SetEnvironmentVariable('MINIMAX_API_KEY', '', 'User')
```

Or via System Properties:
1. `Win + R` → `sysdm.cpl`
2. Advanced → Environment Variables
3. Delete `MINIMAX_API_KEY` from User variables

**Step 2: Use launcher scripts**

After removing the permanent var, use:
- `C:\GitHub\claude-assist\launchers\claude-opus.bat` → Claude Opus 4
- `C:\GitHub\claude-assist\launchers\claude-sonnet.bat` → Claude Sonnet 4.5
- `C:\GitHub\claude-assist\launchers\claude-minimax.bat` → MiniMax M2.1 (requires `MINIMAX_API_KEY`)

---

## Directory Structure

```
claude-assist/
├── .claude/
│   ├── settings.local.json      # Permissions + hooks for ATLAS
│   └── custom-instructions.md   # ATLAS persona instructions
├── CLAUDE.md                    # Project-level instructions
├── launchers/
│   ├── claude-opus.bat          # Opus launcher (FIXED: clears MINIMAX_API_KEY)
│   ├── claude-sonnet.bat        # Sonnet launcher (FIXED: clears MINIMAX_API_KEY)
│   ├── claude-minimax.bat       # MiniMax launcher (requires MINIMAX_API_KEY)
│   └── README.md                # Launcher documentation
├── atlas_startup.py             # Session startup: checks @Atlas mentions
└── skills/                      # Personal skills library
```

---

## Configuration Files

### `.claude/settings.local.json`
- Permissions for Notion, MCP servers, bash commands
- **SessionStart hook** runs `atlas_startup.py` on every session
- **SessionStart hook** loads ATLAS persona prompt

### `.claude/custom-instructions.md`
- Full ATLAS persona definition
- Operating principles (plan first, delegate)
- Toolkit: skills, MCP servers, Notion workflow
- Communication style guidelines

### `CLAUDE.md` (root)
- Lightweight version of custom-instructions.md
- Loaded for all projects in this directory tree

---

## Current Tasks

### In Progress
- [ ] Remove permanent `MINIMAX_API_KEY` from Windows environment variables
- [ ] Test `claude-opus.bat` launches Claude Opus (not MiniMax)

### Up Next
- [ ] Verify ATLAS persona loads correctly in new session
- [ ] Verify Notion integration works (personal workspace)
- [ ] Test skill system (`/skill-builder`, `/agent-dispatch`)
- [ ] Run `atlas_startup.py` - confirm @Atlas mentions are checked

---

## Next Steps for Jim

1. **Remove the permanent env var** (see Solution Applied above)
2. **Close all terminals completely**
3. **Reopen terminal and run:**
   ```
   C:\GitHub\claude-assist\launchers\claude-opus.bat
   ```
4. **Verify:**
   - Model shows "Opus" or "MiniMax-M2.1" in the banner
   - `/env` shows no `MINIMAX_API_KEY` set
   - `/atlas-status` or similar shows ATLAS persona active

---

## Notes

- Batch files must be run from a **fresh terminal** to work correctly
- The `set VAR=` syntax in batch files only affects the subprocess environment
- Permanent env vars set via `setx` persist across all sessions and override batch file clears
- ATLAS setup is designed to load from `.claude/` directory when working in `claude-assist/`
