# Implementation Checklist

## Phase 1: Atlas System Directory

### 1.1 Create directory structure

```bash
mkdir .atlas
mkdir .atlas/memory
mkdir .atlas/memory/sessions
```

### 1.2 Create `.atlas/README.md`

```markdown
# Atlas System Directory

This directory contains Atlas's local state, tasks, and memory.

**Contents are gitignored** — each machine maintains its own state.

## Files

- `state.json` — Current runtime state
- `heartbeat.json` — Health status
- `tasks.json` — Atlas task queue
- `updates.log` — Agent update log
- `memory/` — Persistent context and session history

Check `heartbeat.json` to verify Atlas is healthy.
Check `tasks.json` to see what Atlas is planning.
```

### 1.3 Update `.gitignore`

Add:
```gitignore
# Atlas system directory (local state)
.atlas/*
!.atlas/README.md
```

### 1.4 Create `src/atlas-system.ts`

See `02-atlas-system-directory.md` for full implementation.

Functions to implement:
- [ ] `initAtlasSystem()` — Create dirs, init files
- [ ] `getState()` / `writeState()` / `updateState()`
- [ ] `getHeartbeat()` / `writeHeartbeat()` / `updateHeartbeat()`
- [ ] `getTasks()` / `writeTasks()` / `addTask()` / `completeTask()`
- [ ] `logUpdate()`
- [ ] `getContext()` / `updateContext()`
- [ ] `saveSessionSummary()`

### 1.5 Wire into startup

In `src/index.ts`:
```typescript
import { initAtlasSystem, updateHeartbeat, logUpdate } from "./atlas-system";

// At startup, before bot.start()
initAtlasSystem();
updateHeartbeat({ status: "healthy", telegramConnected: true });
logUpdate("STARTUP: Atlas initialized");
```

---

## Phase 2: Tool-Aware Chat

### 2.1 Add `generateResponseWithTools()` to `src/claude.ts`

See `03-chat-tools-implementation.md` for full implementation.

- [ ] Define tools array (query_inbox, query_work_queue, get_status, get_atlas_state)
- [ ] Implement `generateResponseWithTools()`
- [ ] Implement `executeToolCall()`
- [ ] Add imports for atlas-system

### 2.2 Update `src/handlers/chat.ts`

- [ ] Add import for `generateResponseWithTools`
- [ ] Add `mightNeedTools` regex check
- [ ] Route to tool-aware response when needed

### 2.3 Export new function

In `src/claude.ts` exports:
```typescript
export { generateResponseWithTools };
```

---

## Phase 3: Integration & Stats

### 3.1 Update message handler to track stats

In `src/handlers/index.ts`:
```typescript
import { updateState, getState, updateHeartbeat, logUpdate } from "../atlas-system";

// After handling any message:
const state = getState();
updateState({
  stats: {
    ...state.stats,
    messagesHandled: state.stats.messagesHandled + 1,
  }
});
updateHeartbeat({ status: "healthy", pendingWork: 0 });
```

### 3.2 Track spark captures

In `src/handlers/spark.ts`:
```typescript
import { updateState, getState, logUpdate } from "../atlas-system";

// After successful capture:
const state = getState();
updateState({
  stats: {
    ...state.stats,
    sparksCaptured: state.stats.sparksCaptured + 1,
  }
});
logUpdate(`SPARK: Captured "${title}" to ${pillar}`);
```

### 3.3 Track queries

In `src/handlers/query.ts`:
```typescript
import { updateState, getState } from "../atlas-system";

// After successful query:
const state = getState();
updateState({
  stats: {
    ...state.stats,
    queriesAnswered: state.stats.queriesAnswered + 1,
  }
});
```

---

## Phase 4: Testing

### 4.1 Unit tests for atlas-system

- [ ] `initAtlasSystem()` creates directory structure
- [ ] State read/write roundtrips correctly
- [ ] Heartbeat updates work
- [ ] Task queue add/complete works
- [ ] Log append works

### 4.2 Integration tests for chat with tools

- [ ] "what's in my inbox?" triggers tool use
- [ ] "anything urgent?" checks for P0s
- [ ] "hey" uses fast path (no tools)
- [ ] Tool errors handled gracefully

### 4.3 Manual testing

```
1. Start bot
2. Check .atlas/heartbeat.json shows "healthy"
3. Send "hey" → quick response
4. Send "what's in my inbox?" → tool-aware response with real data
5. Send "anything urgent?" → checks P0s
6. Send "how's Atlas doing?" → reports state
7. Check .atlas/state.json shows updated stats
8. Check .atlas/updates.log shows activity
```

---

## Verification

After implementation, verify:

| File | Exists | Works |
|------|--------|-------|
| `.atlas/README.md` | [ ] | N/A |
| `.atlas/state.json` | [ ] | [ ] |
| `.atlas/heartbeat.json` | [ ] | [ ] |
| `.atlas/tasks.json` | [ ] | [ ] |
| `.atlas/updates.log` | [ ] | [ ] |
| `src/atlas-system.ts` | [ ] | [ ] |
| `generateResponseWithTools()` | [ ] | [ ] |
| Chat handler routing | [ ] | [ ] |

---

## Rollback Plan

If issues arise:
1. Revert `src/handlers/chat.ts` to always use `generateResponse()`
2. Remove `atlas-system.ts` imports from handlers
3. Bot continues working without new features
