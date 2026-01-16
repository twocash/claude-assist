# Claude Code Launchers

Multiple ways to launch Claude Code with different model backends.

---

## Available Launchers

### 1. Native (Default Anthropic)
```cmd
launchers\claude-native.bat
```
**Model:** Claude Sonnet 4.5 (Anthropic)
**Use for:** Production work, official Claude models

### 2. MiniMax M2.1
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

**Native Claude:**
- Target: `C:\github\claude-assist\launchers\claude-native.bat`
- Start in: `C:\github\claude-assist`
- Name: "Claude Code (Native)"

**MiniMax:**
- Target: `C:\github\claude-assist\launchers\claude-minimax.bat`
- Start in: `C:\github\claude-assist`
- Name: "Claude Code (MiniMax)"

---

## Model Comparison

| Feature | Native (Anthropic) | MiniMax M2.1 |
|---------|-------------------|--------------|
| Model Quality | Highest | Good |
| Speed | Fast | Fast |
| Cost | Standard | Lower |
| API Compatibility | 100% | Claude-compatible |
| Best For | Production | Testing, cost-saving |

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

*Updated: 2026-01-16*
