# Atlas Telegram Bot - Claude Code Instructions

**Project:** Atlas Telegram — Real-time clarification layer  
**Owner:** Jim Calhoun  
**Status:** Sprints 1-3 COMPLETE ✅ | Sprint 4 (Polish) PENDING

---

## Current State

The bot is **feature complete for MVP**. All core functionality works:
- ✅ Telegram message handling with user allowlist
- ✅ URL extraction and content fetching
- ✅ SPARKS-based classification via Claude
- ✅ Inline keyboard clarification flow
- ✅ Notion Inbox 2.0 item creation
- ✅ Comment-based conversation memory
- ✅ Work Queue routing with relations
- ✅ Error handling and graceful failures

**Ready for testing.** See QUICKSTART.md for setup.

---

## Project Context

You're building a Telegram bot that enables Jim to share links/sparks from mobile and get instant classification + clarification before routing to Notion.

**Key documents to read first:**
1. `QUICKSTART.md` — 5-minute setup guide
2. `HANDOFF.md` — Design session context and "why"
3. `ARCHITECTURE.md` — Technical architecture
4. `IMPLEMENTATION.md` — Sprint plan with progress
5. `workspace/SPARKS.md` — Classification framework

---

## Tech Stack

- **Runtime:** Bun (not Node.js)
- **Language:** TypeScript (strict mode)
- **Telegram:** grammy
- **AI:** Anthropic SDK (`@anthropic-ai/sdk`)
- **Notion:** `@notionhq/client`

---

## Commands

```bash
# Install dependencies
bun install

# Run in development (auto-reload)
bun run dev

# Run in production
bun run start

# Test Notion connection
bun run test:notion

# Test Claude connection
bun run test:claude

# Type check
bun run typecheck
```

---

## File Overview

| File | Purpose |
|------|---------|
| `src/index.ts` | Entry point, env validation, startup |
| `src/bot.ts` | Telegram bot setup, middleware, routes |
| `src/handler.ts` | Message orchestration (the main flow) |
| `src/claude.ts` | Claude classification with SPARKS context |
| `src/classifier.ts` | Heuristic fallback + confidence thresholds |
| `src/clarify.ts` | Question generation + inline keyboards |
| `src/notion.ts` | Inbox/Work Queue creation + comments |
| `src/url.ts` | URL extraction and content fetching |
| `src/types.ts` | All TypeScript interfaces |
| `src/logger.ts` | Logging utility |
| `src/audit.ts` | Audit trail to file |

---

## Remaining Work (Sprint 4)

1. **Rate limiting** - Add request throttling for Claude/Notion
2. **Session persistence** - Move from in-memory to SQLite
3. **Service setup** - systemd (Linux) or Windows service
4. **Log rotation** - Auto-cleanup of old logs

These are nice-to-haves. The bot is functional without them.

---

## Database IDs

```typescript
const NOTION_DATABASES = {
  inbox: "04c04ac3-b974-4b7a-9651-e024ee484630",
  workQueue: "6a8d9c43-b084-47b5-bc83-bc363640f2cd"
};
```

---

## Critical Requirements

### Security (Non-negotiable)
1. **User allowlist:** Only `TELEGRAM_ALLOWED_USERS` can interact
2. **Silent rejection:** Non-allowed users get no response
3. **Audit logging:** Every interaction logged

### The 10-Second Rule
Clarification questions must be answerable in <10 seconds:
- Yes/no or A/B/C/D choices
- Inline keyboard buttons (no typing)
- Single tap to confirm

---

## Testing Checklist

Before marking complete, test these flows:

- [ ] Send GitHub URL → should classify as Grove + Build/Catalog
- [ ] Send arxiv URL → should classify as Grove + Research (high confidence)
- [ ] Send ambiguous link → should present A/B/C/D options
- [ ] Tap button → should create Notion item
- [ ] Check Notion → item has all properties + comment
- [ ] Send from different user ID → should be ignored (no response)
- [ ] Run `/status` → shows Notion + Claude connected

---

## Session Notes

*(Add notes about what you worked on, decisions made, blockers hit)*

### Session: 2026-01-29
- Initial scaffolding complete
- All source files created
- Sprint 1-3 features implemented
- Ready for testing
