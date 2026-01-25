---
author: Jim Calhoun
date: '2026-01-19'
domain: spec
last_synced: '2026-01-19T22:08:05.017795'
local_file: 260119-s-spec-grove-hygiene-launcher-web-app-spec.md--FINAL.md
notion_id: 2ed780a7-8eef-81c4-863c-dc51c444458b
notion_url: https://www.notion.so/Grove-Hygiene-Launcher-Web-App-Spec-2ed780a78eef81c4863cdc51c444458b
status: final
title: Grove Hygiene Launcher — Web App Spec
type: software
---

# Grove Hygiene Launcher — Web App Spec

## Purpose

Web interface for Grove's code hygiene system that:
1. Displays Hygiene Queue from Notion
1. Enables review/approval/rejection of maintenance items
1. Executes Claude Code sessions for approved fixes
1. Presents session summaries with verification screenshots
This tool supports Grove's architectural health by automating routine maintenance while preserving human oversight for strategic decisions.

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Data:** Notion API (read/write operations)
- **Execution:** Shell spawn to Claude Code CLI
- **Screenshots:** Claude Code + Chrome integration

## Routes

```plain text
/                       # Dashboard — queue statistics, recent completions
/queue                  # Hygiene Queue (filterable by status, type, risk)
/queue/[id]             # Single fix detail + approval interface
/queue/[id]/execute     # Live execution monitor
/strategic              # Strategic Notes browser
/summaries              # Session summary gallery with screenshots
/summaries/[id]         # Individual summary detail view
/scan                   # Manual DEX Master scan trigger
```

## Key Components

### Dashboard (`/`)

```plain text
┌────────────────────────────────────────────────────────────┐
│  GROVE HYGIENE                               [Run Scan]    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Ready: 12  │  In Progress: 2  │  Complete: 47            │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  READY FOR REVIEW                                    │ │
│  │  ○ Remove unused import · cleanup · 95% · low risk   │ │
│  │  ○ Update axios version · dependency · 90% · low     │ │
│  │  ○ Fix deprecated test API · test · 88% · low        │ │
│  │                                      [View Queue →]  │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │  RECENT COMPLETIONS                                  │ │
│  │  ✓ Remove dead explore/v1 routes · +2 tests · 100%  │ │
│  │  ✓ Clean bedrock legacy import · 0 tests · 100%     │ │
│  │                                   [View Summaries →] │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

### Review Screen (`/queue/[id]`)

```plain text
┌────────────────────────────────────────────────────────────┐
│  ← Back                                                    │
│                                                            │
│  Remove unused bedrock.legacy_handler import               │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                   │
│                                                            │
│  Type: cleanup     Risk: low     Confidence: 95%           │
│  Source: dex-master                                        │
│                                                            │
│  AFFECTED FILES                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ src/grove/core/router.ts                             │ │
│  │ Lines: 12-14, 89-102                      [View →]   │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  RATIONALE                                                 │
│  Import unused since commit abc123. Function was           │
│  scaffolding for deprecated v1 routing. No references.     │
│                                                            │
│  CONTRACT SPEC                                   [Edit]    │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 1. Open src/grove/core/router.ts                     │ │
│  │ 2. Remove import on line 12                          │ │
│  │ 3. Remove dead code lines 89-102                     │ │
│  │ 4. Run: npm test -- router                           │ │
│  │ 5. Verify: /bedrock and /explore routes load         │ │
│  │ 6. Screenshot: Both routes render                    │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  [Reject]              [Save Edits]         [✓ Approve]    │
└─────────────────────
// ... (truncated)
```

### Execution Flow

When "Approve" is clicked:
1. **Update Notion:** Status → `approved`, Approved At → now
1. **Spawn Claude Code:**

```bash

   claude -p "Execute this fix contract: [contract spec].

              When complete, write session summary to Notion

              database 35e8f98c-3ddc-4f2f-ad54-130398ab01cb"

```

1. **Monitor:** Stream output to `/queue/[id]/execute` page
1. **Complete:** Claude Code writes summary to Notion
1. **Update:** Status → `complete`, link Session Summary

## API Routes

```typescript
// app/api/queue/route.ts
GET  /api/queue              // List queue items from Notion
POST /api/queue              // Create new queue item

// app/api/queue/[id]/route.ts
GET    /api/queue/[id]       // Get single item
PATCH  /api/queue/[id]       // Update item (approve, reject, edit)

// app/api/queue/[id]/execute/route.ts
POST   /api/queue/[id]/execute  // Trigger Claude Code execution

// app/api/summaries/route.ts
GET  /api/summaries          // List session summaries

// app/api/scan/route.ts
POST /api/scan               // Trigger DEX Master scan
```

## Notion Integration

```typescript
// lib/notion.ts
import { Client } from '@notionhq/client';

const notion = new Client({ auth: process.env.NOTIONTOKEN });

const FIXQUEUEDB = '4342664c-be13-4a07-9ec5-8488a79ddcb1';
const STRATEGICNOTESDB = '394db86c-01fa-44e4-842d-3de6dc09e08c';
const SESSIONSUMMARIESDB = '35e8f98c-3ddc-4f2f-ad54-130398ab01cb';

export async function getQueueItems(status?: string) {
  const response = await notion.databases.query({
    databaseid: FIXQUEUEDB,
    filter: status ? {
      property: 'Status',
      select: { equals: status }
    } : undefined,
    sorts: [{ property: 'Confidence', direction: 'descending' }]
  });
  return response.results;
}

export async function updateQueueItem(pageId: string, properties: any) {
  return notion.pages.update({ pageid: pageId, properties });
}

export async function createSessionSummary(data: SessionSummary) {
  return notion.pages.create({
    parent: { databaseid: SESSIONSUMMARIESDB },
    properties: {
      Title: { title: [{ text: { content: data.title } }] },
      // ... other properties
    }
  });
}
```

## Claude Code Execution

```typescript
// lib/claude-code.ts
import { spawn } from 'childprocess';

export function executeContract(contractSpec: string, queueItemId: string) {
  const prompt = `
You are executing a fix contract from the Grove Hygiene system.

CONTRACT:
${contractSpec}

REQUIREMENTS:
1. Execute each step exactly as specified
2. Capture before/after test counts
3. Take screenshots as specified
4. Write session summary to Notion database ${SESSIONSUMMARIES_DB}
5. Include verification status

Begin execution.
`;

  const claude = spawn('claude', ['-p', prompt], {
    cwd: 'C:\\Github\\the-grove-foundation',
    shell: true
  });

  return claude;
}
```

## Environment Variables

```plain text
NOTIONTOKEN=secret...
GROVEREPOPATH=C:\Github\the-grove-foundation
CLAUDECODEPATH=claude  # or full path if not in PATH
```

## Build Sequence

| Step | Task | Time |
|---|---|---|
| 1 | `npx create-next-app grove-hygiene` | 5 min |
| 2 | Notion API integration | 30 min |
| 3 | Dashboard + Queue list | 1 hr |
| 4 | Review screen | 1 hr |
| 5 | Execution integration | 2 hr |
| 6 | Summary display | 1 hr |
| 7 | Scan trigger | 30 min |

**Total:** ~6 hours for MVP

## Future Enhancements

- [ ] WebSocket for real-time execution updates
- [ ] Batch approve low-risk items
- [ ] Git integration (auto-create branches)
- [ ] PR creation after fix completion
- [ ] Slack notifications on completion
- [ ] Metrics dashboard (fixes/week, test delta trends)
