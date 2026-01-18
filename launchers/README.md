# Claude Code Launchers

Multiple ways to launch Claude Code with different model backends.

---

## Available Launchers

### 1. Sonnet (Default)
```cmd
launchers\claude-sonnet.bat
```
**Model:** Claude Sonnet 4.5 (Anthropic)
**Use for:** Daily development work, balanced performance/cost

### 2. Opus (High Performance)
```cmd
launchers\claude-opus.bat
```
**Model:** Claude Opus 4 (Anthropic)
**Use for:** Complex reasoning, writing, high-quality output

### 3. MiniMax M2.1
```cmd
launchers\claude-minimax.bat
```
**Model:** MiniMax-M2.1
**Use for:** Testing alternative models, cost optimization

---

## Setup: MiniMax

### Step 1: Get API Key
1. Go to https://platform.minimax.io/
2. Sign up / log in
3. Navigate to API Keys section
4. Generate new API key
5. Copy the key

### Step 2: Set Environment Variable

**Temporary (current session only):**
```cmd
set MINIMAX_API_KEY=your-key-here
launchers\claude-minimax.bat
```

**Permanent (recommended):**
```cmd
setx MINIMAX_API_KEY "your-key-here"
```
Then close and reopen terminal, run:
```cmd
launchers\claude-minimax.bat
```

### Step 3: Launch
```cmd
cd C:\github\claude-assist
launchers\claude-minimax.bat
```

---

## Quick Launch Shortcuts

Create shortcuts on your desktop:

**Claude Sonnet (Default):**
- Target: `C:\github\claude-assist\launchers\claude-sonnet.bat`
- Start in: `C:\github\claude-assist`
- Name: "Claude Code (Sonnet)"

**Claude Opus (High Performance):**
- Target: `C:\github\claude-assist\launchers\claude-opus.bat`
- Start in: `C:\github\claude-assist`
- Name: "Claude Code (Opus)"

**MiniMax:**
- Target: `C:\github\claude-assist\launchers\claude-minimax.bat`
- Start in: `C:\github\claude-assist`
- Name: "Claude Code (MiniMax)"

---

## Model Comparison

| Feature | Claude Sonnet | Claude Opus | MiniMax M2.1 |
|---------|---------------|-------------|--------------|
| Model Quality | High | Highest | Good |
| Speed | Fast | Medium | Fast |
| Cost | Standard | Premium | Lower |
| Best For | Daily dev | Complex tasks | Testing, cost-saving |

---

## Troubleshooting

### "MINIMAX_API_KEY not set"
Solution: Set environment variable (see Step 2 above)

### "Connection failed"
- Check API key is valid
- Verify base URL (international vs China)
- Check internet connection
- Try increasing timeout in .bat file

### "Model not found"
- Ensure model name is exactly: `MiniMax-M2.1`
- Check MiniMax platform status

### ATLAS doesn't load with MiniMax
ATLAS persona should load regardless of model backend.
If not, manually activate:
```
load ATLAS
```

---

## Adding More Models

To add another model backend:

1. Create `launchers\claude-{model-name}.bat`
2. Set appropriate environment variables
3. Configure base URL and model identifier
4. Test launch
5. Document here

---

---

## Troubleshooting

### "Claude Code keeps using MiniMax even when running claude-opus.bat"

**Cause:** `MINIMAX_API_KEY` is set permanently in Windows environment variables.

**Fix:**
```powershell
# Run PowerShell as Administrator
[System.Environment]::SetEnvironmentVariable('MINIMAX_API_KEY', '', 'User')
```

Then close all terminals and reopen.

**Alternative:**
1. `Win + R` → `sysdm.cpl`
2. Advanced → Environment Variables
3. Delete `MINIMAX_API_KEY` from User variables

---

*Updated: 2026-01-17*
