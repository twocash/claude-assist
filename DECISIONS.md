# Atlas Product Decisions

**Purpose:** Log key architectural and product decisions with rationale.  
**Updated:** 2026-01-29

---

## Decision Format

Each decision follows this structure:
- **Context:** What situation prompted this decision
- **Options considered:** Alternatives evaluated
- **Decision:** What we chose
- **Rationale:** Why this option
- **Consequences:** What this enables/limits
- **Status:** Proposed | Accepted | Superseded

---

## DEC-001: Browser Extension as Primary Interface

**Date:** 2026-01-29  
**Status:** Accepted

**Context:**  
Atlas interaction is currently fragmented: Notion for capture/triage, CLI for scripts, Notion comments for dispositions. This creates async round-trips that break flow.

**Options considered:**
1. **Improve Notion UX** - Custom views, better templates
2. **Build standalone app** - Electron/web app dedicated to Atlas
3. **Telegram bot** - Mobile-first conversational interface
4. **Browser extension** - Side panel in existing work context

**Decision:** Browser extension as primary real-time interface

**Rationale:**
- Extension already exists and works (LinkedIn automation proves the model)
- Zero context-switch—Atlas is present while working in browser
- Can evolve incrementally from current state
- Notion remains source of truth (no migration risk)
- Side panel UX is proven (many tools use this pattern)

**Consequences:**
- Investment in extension UI/UX pays compound returns
- Mobile use case requires separate solution (Telegram later)
- Extension must be reliable—daily driver expectations
- Notion API rate limits may become a factor

---

## DEC-002: Notion Remains Source of Truth

**Date:** 2026-01-29  
**Status:** Accepted

**Context:**  
Could build lighter-weight state management (local files, SQLite, Supabase) instead of relying on Notion API.

**Options considered:**
1. **Notion only** - All state in Notion databases
2. **Local-first** - SQLite/JSON with Notion sync
3. **Supabase** - Postgres backend, faster queries
4. **Hybrid** - Hot state local, cold state Notion

**Decision:** Notion remains sole source of truth; extension reads/writes via API

**Rationale:**
- Notion provides free manual override UI (edit items directly)
- Already invested in Notion structure (Inbox, Feed, Memory, Pillars)
- Avoids sync complexity and conflict resolution
- Notion API is fast enough for dashboard use case
- Jim already lives in Notion for other work

**Consequences:**
- Dependent on Notion API availability/performance
- Complex queries may need server-side aggregation
- No offline support in extension (acceptable tradeoff)
- Rate limiting requires thoughtful API usage

---

## DEC-003: Four Pillars as Top-Level Taxonomy

**Date:** 2026-01-29 (documenting existing)  
**Status:** Accepted

**Context:**  
Need a stable taxonomy for routing all captured content.

**Options considered:**
1. **Project-based** - Route to specific projects
2. **GTD contexts** - @home, @work, @errands, etc.
3. **Life domains** - Personal, Work, Home, etc.
4. **Flat tags** - No hierarchy, tag-based

**Decision:** Four pillars: Personal, The Grove, Consulting, Home/Garage

**Rationale:**
- Maps to how Jim's life is actually structured
- Stable over time (unlike projects which come and go)
- Clear routing rules (permits → Home, clients → Consulting)
- Small enough set to not require sub-categorization

**Consequences:**
- Every item must fit one pillar (no cross-pillar items)
- Pillar rules need documentation (see Atlas Memory)
- New life domains would require adding a pillar

---

## DEC-004: Async Triage with Sync Visibility

**Date:** 2026-01-29  
**Status:** Accepted

**Context:**  
Triage processing can be async (Python scripts), but visibility into state should be real-time.

**Options considered:**
1. **Fully async** - Scripts run on schedule, check Notion for results
2. **Fully sync** - Every action processes immediately
3. **Async processing, sync visibility** - Background triage, real-time dashboard

**Decision:** Async processing with synchronous visibility layer (extension dashboard)

**Rationale:**
- Heavy processing (classification, API calls) shouldn't block UI
- Visibility doesn't require processing—just reading state
- Extension can poll/refresh without waiting for triage completion
- Matches mental model: "things are being handled" vs "I see the queue"

**Consequences:**
- Dashboard shows current state, not real-time processing
- Need visual indicator when processing is in-flight
- Edge case: item captured but not yet triaged (show as "Processing")

---

## DEC-005: Editorial Learning Stays File-Based

**Date:** 2026-01-29 (documenting existing)  
**Status:** Accepted

**Context:**  
Grove docs refinery learns from Jim's edits. Where should learnings be stored?

**Options considered:**
1. **Notion database** - Learnings as database entries
2. **Local markdown** - `editorial_memory.md` in repo
3. **Embedded in prompts** - Hardcode learnings into system prompts

**Decision:** Local markdown file (`editorial_memory.md`)

**Rationale:**
- Easy to read and edit manually
- Version controlled with git
- Injected into prompts at generation time
- No API overhead for every generation

**Consequences:**
- Multi-machine use requires syncing file (git pull)
- Not queryable like a database
- Works well for current scale (< 100 learnings)

---

## Pending Decisions

### PENDING: Chat Backend Architecture

**Context:** P3-CORE-006 proposes chat interface in extension. How should messages reach Atlas?

**Options to evaluate:**
1. **Anthropic API direct** - Extension calls Claude API with Atlas context
2. **Local Claude Code** - Extension triggers local Claude Code session
3. **Server relay** - Messages go to server, server calls Claude
4. **Notion-mediated** - Messages post to Feed, processed async

**Considerations:**
- API costs for direct calls
- Context injection complexity
- Real-time vs async expectations
- Mobile/Telegram parity

**Status:** Needs discussion before P3-CORE-006

---

### PENDING: Mobile Strategy

**Context:** Extension only works on desktop. How to handle mobile capture/visibility?

**Options to evaluate:**
1. **Telegram bot** - Conversational interface
2. **PWA** - Mobile web app
3. **Notion mobile** - Accept Notion app as mobile interface
4. **iOS Shortcuts** - Quick capture via Shortcuts app

**Status:** Parking lot until desktop experience is solid

---

## Changelog

| Date | Decision | Status |
|------|----------|--------|
| 2026-01-29 | DEC-001 through DEC-005 documented | Accepted |

---

*Decisions are permanent unless explicitly superseded.*
