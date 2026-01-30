# Atlas System Directory (`.atlas/`)

## Purpose

Give Atlas a persistent local brain. This directory holds state, tasks, heartbeats, and memory that survives across sessions — regardless of where Jim accesses Atlas from.

## Directory Structure

```
atlas-telegram/
├── .atlas/
│   ├── README.md              # What this directory is (checked in)
│   ├── state.json             # Current runtime state
│   ├── heartbeat.json         # Health status, last activity
│   ├── tasks.json             # Atlas's own task queue
│   ├── updates.log            # Agent update log (append-only)
│   └── memory/
│       ├── context.json       # Persistent context/facts
│       └── sessions/
│           └── {date}.json    # Session summaries
```

## File Specifications

### `state.json`

Current runtime state. Updated on every significant action.

```json
{
  "version": "1.0",
  "lastActive": "2026-01-29T18:45:00Z",
  "currentMode": "idle",
  "activeTasks": [],
  "pendingClarifications": [],
  "stats": {
    "messagesHandled": 142,
    "sparksCaptures": 28,
    "queriesAnswered": 67,
    "sessionStart": "2026-01-29T14:00:00Z"
  }
}
```

### `heartbeat.json`

Health status for monitoring. Updated every message or on interval.

```json
{
  "status": "healthy",
  "lastHeartbeat": "2026-01-29T18:45:00Z",
  "uptime": "4h 45m",
  "telegramConnected": true,
  "notionConnected": true,
  "claudeConnected": true,
  "lastError": null,
  "pendingWork": 0
}
```

### `tasks.json`

Atlas's internal task queue — things it wants to do or is tracking.

```json
{
  "queue": [
    {
      "id": "task_001",
      "type": "followup",
      "description": "Check if Jim reviewed the DrumWave doc",
      "created": "2026-01-29T16:00:00Z",
      "triggerAt": "2026-01-30T09:00:00Z",
      "status": "pending"
    },
    {
      "id": "task_002", 
      "type": "reminder",
      "description": "Inbox has 5 unrouted items for 24h+",
      "created": "2026-01-29T18:00:00Z",
      "status": "pending"
    }
  ],
  "completed": []
}
```

### `updates.log`

Append-only log of agent observations, changes, and notes.

```
[2026-01-29T14:00:00Z] STARTUP: Atlas initialized, all connections healthy
[2026-01-29T14:05:23Z] OBSERVATION: Jim seems to prefer Grove queries in morning
[2026-01-29T16:30:00Z] TASK_CREATED: Followup on DrumWave doc review
[2026-01-29T18:45:00Z] STATUS: 5 sparks captured today, 3 routed to work queue
```

### `memory/context.json`

Persistent facts and preferences learned over time.

```json
{
  "preferences": {
    "defaultPillar": "The Grove",
    "preferredQueryFormat": "concise",
    "activeHours": "09:00-18:00 EST"
  },
  "facts": {
    "currentProjects": ["Atlas 2.0", "Grove Site", "DrumWave Calculator"],
    "recentFocus": "Atlas Telegram Bot"
  },
  "patterns": {
    "morningQueries": ["status", "inbox"],
    "eveningQueries": ["work queue"]
  }
}
```

### `memory/sessions/{date}.json`

Daily session summary for longer-term memory.

```json
{
  "date": "2026-01-29",
  "summary": "Focused on Atlas development. Captured 5 sparks, 3 Grove-related. Discussed cognitive router architecture.",
  "sparks": 5,
  "queries": 12,
  "topics": ["Atlas", "Cognitive Router", "Multi-agent"],
  "notableItems": [
    "Captured Claude Code Buddy GitHub repo",
    "Discussed token routing hierarchy"
  ]
}
```

## Implementation

### `src/atlas-system.ts`

```typescript
/**
 * Atlas System Directory Management
 * 
 * Manages .atlas/ directory for persistent state, tasks, and memory.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, appendFileSync } from "fs";
import { join } from "path";
import { logger } from "./logger";

const ATLAS_DIR = process.env.ATLAS_SYSTEM_DIR || "./.atlas";

// Ensure directory structure exists
export function initAtlasSystem(): void {
  const dirs = [ATLAS_DIR, join(ATLAS_DIR, "memory"), join(ATLAS_DIR, "memory/sessions")];
  
  for (const dir of dirs) {
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
      logger.info(`Created Atlas system directory: ${dir}`);
    }
  }
  
  // Initialize files if missing
  if (!existsSync(join(ATLAS_DIR, "state.json"))) {
    writeState(getDefaultState());
  }
  if (!existsSync(join(ATLAS_DIR, "heartbeat.json"))) {
    writeHeartbeat({ status: "starting", lastHeartbeat: new Date().toISOString() });
  }
  if (!existsSync(join(ATLAS_DIR, "tasks.json"))) {
    writeTasks({ queue: [], completed: [] });
  }
}

// State management
export interface AtlasState {
  version: string;
  lastActive: string;
  currentMode: "idle" | "processing" | "waiting";
  activeTasks: string[];
  pendingClarifications: string[];
  stats: {
    messagesHandled: number;
    sparksCaptured: number;
    queriesAnswered: number;
    sessionStart: string;
  };
}

export function getState(): AtlasState {
  try {
    return JSON.parse(readFileSync(join(ATLAS_DIR, "state.json"), "utf-8"));
  } catch {
    return getDefaultState();
  }
}

export function writeState(state: AtlasState): void {
  writeFileSync(join(ATLAS_DIR, "state.json"), JSON.stringify(state, null, 2));
}

export function updateState(updates: Partial<AtlasState>): void {
  const state = getState();
  writeState({ ...state, ...updates, lastActive: new Date().toISOString() });
}

function getDefaultState(): AtlasState {
  return {
    version: "1.0",
    lastActive: new Date().toISOString(),
    currentMode: "idle",
    activeTasks: [],
    pendingClarifications: [],
    stats: {
      messagesHandled: 0,
      sparksCaptured: 0,
      queriesAnswered: 0,
      sessionStart: new Date().toISOString(),
    },
  };
}

// Heartbeat
export interface Heartbeat {
  status: "healthy" | "degraded" | "error" | "starting";
  lastHeartbeat: string;
  uptime?: string;
  telegramConnected?: boolean;
  notionConnected?: boolean;
  claudeConnected?: boolean;
  lastError?: string | null;
  pendingWork?: number;
}

export function getHeartbeat(): Heartbeat {
  try {
    return JSON.parse(readFileSync(join(ATLAS_DIR, "heartbeat.json"), "utf-8"));
  } catch {
    return { status: "starting", lastHeartbeat: new Date().toISOString() };
  }
}

export function writeHeartbeat(heartbeat: Heartbeat): void {
  writeFileSync(join(ATLAS_DIR, "heartbeat.json"), JSON.stringify(heartbeat, null, 2));
}

export function updateHeartbeat(updates: Partial<Heartbeat>): void {
  const hb = getHeartbeat();
  writeHeartbeat({ ...hb, ...updates, lastHeartbeat: new Date().toISOString() });
}

// Task queue
export interface AtlasTask {
  id: string;
  type: "followup" | "reminder" | "check" | "report";
  description: string;
  created: string;
  triggerAt?: string;
  status: "pending" | "active" | "completed" | "dismissed";
  metadata?: Record<string, unknown>;
}

export interface TaskQueue {
  queue: AtlasTask[];
  completed: AtlasTask[];
}

export function getTasks(): TaskQueue {
  try {
    return JSON.parse(readFileSync(join(ATLAS_DIR, "tasks.json"), "utf-8"));
  } catch {
    return { queue: [], completed: [] };
  }
}

export function writeTasks(tasks: TaskQueue): void {
  writeFileSync(join(ATLAS_DIR, "tasks.json"), JSON.stringify(tasks, null, 2));
}

export function addTask(task: Omit<AtlasTask, "id" | "created" | "status">): AtlasTask {
  const tasks = getTasks();
  const newTask: AtlasTask = {
    ...task,
    id: `task_${Date.now()}`,
    created: new Date().toISOString(),
    status: "pending",
  };
  tasks.queue.push(newTask);
  writeTasks(tasks);
  return newTask;
}

export function completeTask(taskId: string): void {
  const tasks = getTasks();
  const idx = tasks.queue.findIndex(t => t.id === taskId);
  if (idx >= 0) {
    const task = tasks.queue.splice(idx, 1)[0];
    task.status = "completed";
    tasks.completed.push(task);
    writeTasks(tasks);
  }
}

// Updates log
export function logUpdate(message: string): void {
  const timestamp = new Date().toISOString();
  const entry = `[${timestamp}] ${message}\n`;
  appendFileSync(join(ATLAS_DIR, "updates.log"), entry);
}

// Memory
export function getContext(): Record<string, unknown> {
  try {
    return JSON.parse(readFileSync(join(ATLAS_DIR, "memory/context.json"), "utf-8"));
  } catch {
    return { preferences: {}, facts: {}, patterns: {} };
  }
}

export function updateContext(updates: Record<string, unknown>): void {
  const context = getContext();
  writeFileSync(
    join(ATLAS_DIR, "memory/context.json"),
    JSON.stringify({ ...context, ...updates }, null, 2)
  );
}

export function saveSessionSummary(summary: {
  date: string;
  summary: string;
  sparks: number;
  queries: number;
  topics: string[];
  notableItems: string[];
}): void {
  const filename = join(ATLAS_DIR, `memory/sessions/${summary.date}.json`);
  writeFileSync(filename, JSON.stringify(summary, null, 2));
}
```

## Git Configuration

Add to `.gitignore`:

```gitignore
# Atlas system directory (local state)
.atlas/*
!.atlas/README.md
```

Create `.atlas/README.md` (this file IS committed):

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

## Usage

Atlas manages this directory automatically. You can inspect files to see what Atlas is tracking.

Check `heartbeat.json` to verify Atlas is healthy.
Check `tasks.json` to see what Atlas is planning.
Check `updates.log` for recent activity.
```

## Integration Points

1. **Startup** (`src/index.ts`): Call `initAtlasSystem()` before bot starts
2. **Message handling** (`src/handlers/index.ts`): Increment stats, update heartbeat
3. **Spark capture** (`src/handlers/spark.ts`): Log to updates, increment sparksCaptured
4. **Chat handler** (`src/handlers/chat.ts`): Can read state/tasks for context
5. **Shutdown**: Write final session summary

## Future Extensions

- **Scheduled tasks**: Check `tasks.json` on interval, trigger reminders
- **Health monitoring**: External process reads `heartbeat.json`
- **Sync to Notion**: Periodically sync local state to Notion for backup
- **Cross-device sync**: Could use Notion as sync layer for multi-device state
