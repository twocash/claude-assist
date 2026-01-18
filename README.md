# Claude Assist - Agent Coordination Testbed

**Purpose:** Sandbox environment for testing and refining multi-agent coordination infrastructure before deploying to production (grove-foundation).

**Status:** Development
**Python:** 3.14.0
**Location:** `C:\github\claude-assist`

---

## Quick Start

### Launch Claude Code (Interactive Model Selection)

**Windows:**
```cmd
launch-claude.bat
```

**Linux/WSL/SSH:**
```bash
./launch-claude.sh
```

This will prompt you to select a model backend:
1. Native (Anthropic Claude Sonnet 4.5)
2. MiniMax M2.1
3. Exit

---

## Direct Launch (No Prompt)

### Native Anthropic (Default)
```cmd
launchers\claude-native.bat
```

### MiniMax M2.1
```cmd
launchers\claude-minimax.bat
```

### Standard (No launcher)
```bash
claude
```

---

## Directory Structure

- `.agent/` - Coordination infrastructure
- `sandbox/` - Testing workspace
- `.claude/` - Local skill/note storage
- `skills/` - Custom skills system
- `launchers/` - Model-specific launchers
- `configs/` - Model configurations

---

## What Gets Tested Here

- Agent role definitions
- Status logging protocols
- Multi-agent coordination patterns
- Notion sync mechanisms
- Dispatch protocols
- **Multiple LLM backends**

**Once proven:** Deploy to `grove-foundation` repo.

---

## Python Environment

Python 3.14.0 available at: `C:\Python314\python.exe`

Required packages: (TBD - create requirements.txt as needed)

---

## ATLAS Persona

The default agent persona (ATLAS - Agent Testing & Laboratory Assistant) loads automatically on session start, regardless of which model backend you choose.

To manually activate:
```
load ATLAS
```

---

## Available Skills ✅ 22/22 COMPLETE

### Meta Tools (2)
- `/skill-builder` - Create new skills interactively
- `/load-persona` - Load ATLAS or custom personas

### Coordination (4)
- `/health-check` - Infrastructure health validator
- `/agent-dispatch` - Launch test agents with activation prompts
- `/status-inspector` - Log entry analyzer
- `/heartbeat-monitor` - Real-time agent tracker

### Testing (4)
- `/mock-sprint` - Fake sprint generator
- `/protocol-validator` - Format compliance checker
- `/workflow-simulator` - Multi-agent scenario tester
- `/log-analyzer` - Report generator

### Utilities (5)
- `/gitfun <url>` - Analyze GitHub repo installation difficulty
- `/python-env` - Python health checker
- `/sandbox-clean` - Cleanup utility
- `/git-snapshot` - Git context viewer
- `/directory-map` - Structure mapper

### Advanced (7)
- `/protocol-adapter` - MCP/A2A/ANP protocol translation
- `/approval-checkpoint` - Bounded autonomy with approval gates
- `/parallel-dispatch` - Multi-agent parallel execution
- `/test-healer` - Auto-heal flaky tests
- `/risk-analyzer` - Predictive test prioritization
- `/mesh-coordinator` - Peer-to-peer coordination
- `/audit-trail` - Decision provenance tracking

**Deploy skills:**
```cmd
deploy-skills.bat  # Windows
./deploy-skills.sh # Linux/WSL
```

**See:** `docs/SKILLS_MASTER_PLAN.md` for details

---

## Model Backends

### Native (Anthropic)
- Model: Claude Sonnet 4.5
- Best for: Production work, highest quality
- Setup: None (default)

### MiniMax M2.1
- Model: MiniMax-M2.1
- Best for: Testing, cost optimization
- Setup: Set `MINIMAX_API_KEY` environment variable
- Get key: https://platform.minimax.io/

See `launchers/README.md` for detailed setup instructions.

---

## Remote Access (iPhone/SSH)

```bash
# SSH into machine
ssh jim@your-machine

# Switch to user (if needed)
su jim

# Navigate to project
cd /mnt/c/github/claude-assist

# Launch with model selection
./launch-claude.sh
```

---

*Breaking changes welcome. This is the laboratory.*
