# Atlas Interim Fix: Conversational Intelligence

## Problem Statement

Atlas works but feels robotic. Example:

```
Jim: show the work queue
Atlas: Work Queue (3)
       > Atlas Outreach Auto-Sync [Done]
       > Some URL [Queued]
       > Validate Pipeline [Queued]
```

Jim's feedback: "This isn't very conversational. I expect to speak to Claude Code through this interface."

## Root Causes

1. **Handlers return formatted text, not adaptive responses** — data dumps regardless of context
2. **Chat handler has no tools** — conversational queries can't look anything up
3. **No local state** — Atlas has no memory between sessions, can't track what it's working on

## Solution: Three Enhancements

### 1. Atlas System Directory (`.atlas/`)

Local filesystem state that persists across sessions. Atlas can:
- Track pending tasks and status
- Write heartbeats and agent updates
- Maintain session memory
- Queue work for background processing

### 2. Tool-Aware Chat Handler

When intent falls to "chat", give Claude tool access. Conversational queries like "what should I work on?" now trigger actual lookups.

### 3. Tighter Voice

Shorter, sharper responses. No preamble, no hedging.

## Success Criteria

| Before | After |
|--------|-------|
| "what should I work on?" → empty chat | "what should I work on?" → Claude queries queue, recommends |
| "anything urgent?" → "I'm here" | "anything urgent?" → checks P0s, reports |
| No session memory | Atlas tracks what it's doing locally |
| No heartbeat/status | `.atlas/heartbeat.json` shows health |

## Files Changed

- `src/claude.ts` — add `generateResponseWithTools()`
- `src/handlers/chat.ts` — use tool-aware response for data queries
- `src/atlas-system.ts` — new module for `.atlas/` directory management
- `.atlas/` — new directory structure (gitignored except README)

## Scope

This is an **interim fix** — not the full Cognitive Router sprint. Goal is to make Atlas feel less robotic today while the bigger architecture is designed.

Estimated effort: 2-3 hours
