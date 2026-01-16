# MCP Server Configuration Guide

**Active Servers:** Supabase, Serena, Notion, Figma

---

## Quick Configuration

### In Claude Code Settings

Add to `.claude/settings.local.json`:

```json
{
  "pluginConfigs": {
    "supabase@anthropic-tools": {
      "mcpServers": {
        "supabase": {
          "SUPABASE_ACCESS_TOKEN": "your-supabase-token-here"
        }
      }
    },
    "notion@anthropic-tools": {
      "mcpServers": {
        "notion": {
          "NOTION_API_KEY": "your-notion-api-key-here"
        }
      }
    },
    "figma@anthropic-tools": {
      "mcpServers": {
        "figma": {
          "FIGMA_ACCESS_TOKEN": "your-figma-token-here"
        }
      }
    }
  }
}
```

---

## Getting API Keys

### Supabase
1. Go to https://supabase.com/dashboard
2. Select your project
3. Settings → API → Project API keys
4. Copy "service_role" key (for full access) or "anon" key (for limited access)

### Notion
1. Go to https://www.notion.so/my-integrations
2. Create new integration
3. Copy "Internal Integration Token"
4. Share pages/databases with your integration

### Figma
1. Go to https://www.figma.com/settings
2. Personal Access Tokens section
3. Generate new token
4. Copy token (only shown once!)

---

## Testing Configuration

```bash
# Check MCP server health
claude mcp list

# Should show all ✓ Connected
```

---

## Serena (No Auth Needed)

Serena is a code analysis tool - no API key required!
It works out of the box for code navigation and symbol search.

---

## Current Status

Check your active instance - run:
```
claude mcp list
```

You should see:
- ✓ Supabase (if token configured)
- ✓ Serena (always works)
- ✓ Notion (if token configured)
- ✓ Figma (if token configured)

---

*Configure once, use everywhere*
