# Claude Code Handoff: Atlas Interim Fix

## Context

Atlas is a Telegram bot that serves as Jim's AI Chief of Staff. It captures "sparks" (links, ideas), routes them to Notion, and provides query/status capabilities.

**Problem:** The bot works but feels robotic. Responses are formatted dumps, not conversational. When intent falls to "chat", Claude has no tools to look anything up.

**Goal:** Make Atlas feel more like talking to Claude Code — conversational, able to reason about what to fetch, while keeping latency acceptable for mobile.

---

## Your Task

Implement two enhancements:

### 1. Atlas System Directory (`.atlas/`)

Create a local filesystem directory for Atlas to maintain state across sessions:

```
.atlas/
├── README.md              # Checked into git
├── state.json             # Runtime state, stats
├── heartbeat.json         # Health status
├── tasks.json             # Atlas's task queue
├── updates.log            # Agent activity log
└── memory/
    ├── context.json       # Persistent preferences/facts
    └── sessions/          # Daily session summaries
```

**Implementation:**
- Create `src/atlas-system.ts` with state management functions
- Wire into startup (`initAtlasSystem()`)
- Update handlers to track stats and write heartbeats

### 2. Tool-Aware Chat Handler

When the chat handler gets a message that looks like it needs data:
- Give Claude access to query tools (inbox, work queue, status, atlas state)
- Let Claude reason about what to fetch before responding

**Implementation:**
- Add `generateResponseWithTools()` to `src/claude.ts`
- Update `src/handlers/chat.ts` to detect data queries and route to tool-aware response
- Keep fast path for simple greetings/acknowledgments

---

## Files to Read First

```
docs/feedback/01-interim-fix-overview.md    # Executive summary
docs/feedback/02-atlas-system-directory.md  # Full .atlas/ spec with code
docs/feedback/03-chat-tools-implementation.md # Tool-aware chat code
docs/feedback/04-implementation-checklist.md # Step-by-step checklist
```

## Files to Modify

```
src/atlas-system.ts     # NEW - create this
src/claude.ts           # ADD generateResponseWithTools()
src/handlers/chat.ts    # UPDATE to use tool-aware response
src/handlers/index.ts   # ADD stats tracking
src/handlers/spark.ts   # ADD capture logging
src/handlers/query.ts   # ADD query tracking
src/index.ts            # ADD initAtlasSystem() call
.gitignore              # ADD .atlas/* exclusion
.atlas/README.md        # NEW - create this (checked in)
```

## Existing Code Reference

```
src/notion.ts           # Has queryInbox(), queryWorkQueue(), getStatusSummary()
src/claude.ts           # Has generateResponse(), classifyWithClaude()
workspace/CLAUDE.md     # Atlas identity/voice
```

---

## Key Constraints

1. **Don't break existing functionality** — intent router and handlers work, just need enhancement
2. **Keep latency reasonable** — tool-aware response only when needed, fast path for simple messages
3. **Local state is gitignored** — only `.atlas/README.md` is committed
4. **Voice matters** — responses should be direct, concise, zero-bullshit

---

## Testing After Implementation

```bash
# Start the bot
npm run dev

# Check Atlas initialized
cat .atlas/heartbeat.json  # Should show "healthy"

# Test in Telegram:
# 1. "hey" → quick response (no tools)
# 2. "what's in my inbox?" → tool-aware, real data
# 3. "anything urgent?" → checks P0s
# 4. "how's Atlas doing?" → reports state

# Verify stats tracked
cat .atlas/state.json  # Should show message counts
cat .atlas/updates.log # Should show activity
```

---

## Success Criteria

- [ ] `.atlas/` directory created on startup
- [ ] `heartbeat.json` shows healthy status
- [ ] `state.json` tracks message stats
- [ ] `updates.log` records activity
- [ ] "what's in my inbox?" uses tools, returns real data
- [ ] "anything urgent?" checks for P0s
- [ ] "hey" still uses fast path (no tools)
- [ ] Existing handlers still work unchanged
