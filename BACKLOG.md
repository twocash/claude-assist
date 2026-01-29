# Atlas Product Backlog

**Owner:** Jim Calhoun  
**Updated:** 2026-01-29

---

## Prioritization Framework

| Priority | Definition | Timeframe |
|----------|------------|-----------|
| **P0** | Blocking current work, fix now | This session |
| **P1** | High-leverage unlock, do next | This week |
| **P2** | Important improvement | This month |
| **P3** | Nice to have, backlog | When time permits |

**Effort scale:** XS (< 1 hour) | S (1-4 hours) | M (1-2 days) | L (3-5 days) | XL (1+ week)

---

## Workstream 1: Atlas Core (Triage & Execution)

### P1-CORE-001: Extension Dashboard Tab
**Problem:** No visibility into Atlas queue state without running scripts or opening Notion.  
**Hypothesis:** A "Dashboard" tab in the extension showing inbox count, pending items, and blocked work will eliminate 80% of Notion round-trips.  
**Effort:** M  
**Acceptance criteria:**
- [ ] New tab in extension side panel: "Atlas"
- [ ] Shows: Inbox count, Pending triage, Blocked on Jim, Recently completed
- [ ] Clicking an item opens it in Notion
- [ ] Refreshes on panel open + manual refresh button

**Dependencies:** Notion API integration in extension

---

### P1-CORE-002: Quick Capture from Any Page
**Problem:** Capturing to Atlas requires navigating to Notion and creating an inbox item manually.  
**Hypothesis:** A capture button in the extension that grabs page URL + selected text + pillar dropdown will reduce capture friction to < 5 seconds.  
**Effort:** S  
**Acceptance criteria:**
- [ ] Capture button in extension (or keyboard shortcut)
- [ ] Pre-fills: URL, page title, selected text (if any)
- [ ] Pillar dropdown (Personal, Grove, Consulting, Home)
- [ ] Optional note field
- [ ] Creates item in Atlas Inbox via Notion API

**Dependencies:** P1-CORE-001 (Notion API in extension)

---

### P1-CORE-003: Blocked Items Alert
**Problem:** Items waiting on Jim's feedback get buried and stall for days.  
**Hypothesis:** Surfacing "blocked on you" items with age indicator will reduce average blocked time from days to hours.  
**Effort:** S  
**Acceptance criteria:**
- [ ] Dashboard shows "Blocked on You" section
- [ ] Items show age (e.g., "2 days")
- [ ] Visual escalation: yellow > 24h, red > 48h
- [ ] One-click to open and respond

**Dependencies:** P1-CORE-001

---

### P2-CORE-004: Inline Triage Actions
**Problem:** Triage decisions require opening Notion, finding the item, updating properties.  
**Hypothesis:** Quick-action buttons in extension (Approve, Defer, Delegate, Archive) will cut triage time by 70%.  
**Effort:** M  
**Acceptance criteria:**
- [ ] Each inbox item in dashboard has action buttons
- [ ] Actions: ✓ Approve | ⏸ Defer | → Delegate | 📁 Archive
- [ ] Updates Notion properties via API
- [ ] Optimistic UI update, error handling

**Dependencies:** P1-CORE-001, P1-CORE-002

---

### P2-CORE-005: Session Handoff Summary
**Problem:** Starting a new session requires reading Feed entries to understand state.  
**Hypothesis:** Auto-generated "last session summary" on startup reduces context recovery time.  
**Effort:** S  
**Acceptance criteria:**
- [ ] `atlas_startup.py` outputs structured summary
- [ ] Summary: What was done, what's pending, what's blocked
- [ ] Extension dashboard shows "Last Session" card
- [ ] Includes link to full Feed entry

**Dependencies:** P1-CORE-001

---

### P3-CORE-006: Chat Interface in Extension
**Problem:** Current interaction model is async (Notion comments) or CLI.  
**Hypothesis:** Real-time chat in extension side panel creates conversational flow without leaving work context.  
**Effort:** L  
**Acceptance criteria:**
- [ ] Chat tab in extension
- [ ] Messages sent to Atlas (TBD: how - Anthropic API? Local agent?)
- [ ] Context injection: current page, recent items, queue state
- [ ] History persisted to Notion Feed

**Dependencies:** Architecture decision on chat backend

---

## Workstream 2: Life Projects (Home, Personal, Consulting)

### P1-LIFE-001: Project Budget Tracker
**Problem:** Tracking costs for the garage build (and future projects) requires manual spreadsheet work or hunting through receipts.  
**Hypothesis:** A simple budget view per project—with running total, category breakdown, and over/under indicator—makes financial tracking effortless.  
**Effort:** M  
**Acceptance criteria:**
- [ ] Budget property on project pages (target amount)
- [ ] Expense items linked to project with amount + category
- [ ] Dashboard shows: spent / budget, by category
- [ ] Visual indicator: green (under), yellow (close), red (over)
- [ ] Works for any pillar (garage, consulting project, personal goal)

**Dependencies:** P1-CORE-001 (extension dashboard)

---

### P1-LIFE-002: Receipt/Expense Quick Capture
**Problem:** Capturing a receipt means: photo, open Notion, create entry, link to project, enter amount. Too many steps.  
**Hypothesis:** "Log expense" button with amount + category + optional photo reduces capture to < 10 seconds.  
**Effort:** S  
**Acceptance criteria:**
- [ ] "Log Expense" action in extension
- [ ] Fields: Amount, Category (dropdown), Project (dropdown), Note, Photo (optional)
- [ ] Creates expense item in Notion linked to project
- [ ] Running total updates automatically

**Dependencies:** P1-CORE-002 (quick capture infrastructure)

---

### P2-LIFE-003: Project Progress Milestones
**Problem:** No visibility into project progress beyond "done/not done" for complex projects like the garage build.  
**Hypothesis:** Simple milestone tracking (phase + % complete + target date) provides progress visibility without heavyweight PM tooling.  
**Effort:** S  
**Acceptance criteria:**
- [ ] Milestone list on project pages
- [ ] Each milestone: Name, Target date, Status (not started/in progress/complete)
- [ ] Dashboard shows next milestone due per active project
- [ ] Optional: Progress bar visualization

**Dependencies:** P1-CORE-001

---

### P2-LIFE-004: Contractor/Vendor Coordination
**Problem:** Coordinating with contractors (garage), service providers (home), or clients (consulting) requires tracking conversations, commitments, and follow-ups.  
**Hypothesis:** A simple "People" view per project with last contact + next action reduces coordination overhead.  
**Effort:** M  
**Acceptance criteria:**
- [ ] People linked to projects
- [ ] Track: Last contact date, Next action, Notes
- [ ] "Needs follow-up" indicator (no contact > X days)
- [ ] Works across pillars (contractor, client, doctor, etc.)

**Dependencies:** Contacts database extension

---

## Workstream 3: Grove Marketing Suite

### P2-GROVE-001: Engagement Trends Dashboard
**Problem:** No visibility into LinkedIn engagement patterns over time.  
**Hypothesis:** Showing engagement trends (by post, by segment, by week) enables data-driven content decisions.  
**Effort:** M  
**Acceptance criteria:**
- [ ] New tab or section: "Engagement Trends"
- [ ] Chart: Engagements over time (line chart)
- [ ] Breakdown: By post, by sector, by alignment score
- [ ] Top performers list

**Dependencies:** Existing Notion data

---

### P2-GROVE-002: Content Pipeline in Extension
**Problem:** Content generation requires CLI and file management.  
**Hypothesis:** Triggering content generation from extension (with progress visibility) reduces friction.  
**Effort:** M  
**Acceptance criteria:**
- [ ] "Generate Content" action in extension
- [ ] Input: Topic, format (blog/whitepaper/brief), source URLs
- [ ] Progress indicator while generating
- [ ] Output: Link to draft in Notion

**Dependencies:** grove_research_generator API endpoint or local execution

---

### P3-GROVE-003: Contact Enrichment Triggers
**Problem:** Manual process to enrich contacts from LinkedIn profiles.  
**Hypothesis:** "Enrich this contact" button on any LinkedIn profile auto-populates Notion fields.  
**Effort:** S  
**Acceptance criteria:**
- [ ] Button appears on LinkedIn profile pages
- [ ] Scrapes: Name, headline, location, about, experience
- [ ] Updates existing Notion contact or creates new
- [ ] Shows confirmation toast

**Dependencies:** Existing classification logic in extension

---

## Workstream 4: Infrastructure & Skills

### P3-INFRA-001: Project Context File
**Problem:** This Claude project lacks persistent product context.  
**Hypothesis:** Uploading PRODUCT.md and BACKLOG.md to project knowledge enables better PM conversations.  
**Effort:** XS  
**Acceptance criteria:**
- [ ] PRODUCT.md in project knowledge
- [ ] BACKLOG.md in project knowledge
- [ ] Claude references them in product discussions

**Dependencies:** None

---

### P3-INFRA-002: Multi-Machine State Sync
**Problem:** Atlas on laptop vs grove-node-1 can have different views of state.  
**Hypothesis:** Using Notion as single source of truth (already true) + machine tags in Feed (already done) is sufficient.  
**Effort:** XS (validate current approach)  
**Acceptance criteria:**
- [ ] Document current multi-machine approach
- [ ] Confirm no state drift issues
- [ ] Add to PRODUCT.md if working well

**Dependencies:** None

---

### P3-INFRA-003: Skill Library Activation
**Problem:** 22 skills defined but rarely used in practice.  
**Hypothesis:** Skills are underutilized because discovery is poor—need to surface relevant skills contextually.  
**Effort:** M  
**Acceptance criteria:**
- [ ] Audit which skills are actually useful
- [ ] Remove or archive unused skills
- [ ] Integrate useful skills into Atlas startup/workflows

**Dependencies:** None

---

## Parking Lot (Ideas Not Yet Prioritized)

**Life/Home:**
- Photo documentation for projects (before/after, progress shots)
- Permit and inspection tracking with reminders
- Tool/equipment inventory
- Maintenance schedule (car, house, appliances)

**Personal:**
- Health metrics dashboard (weight, exercise, sleep)
- Reading/learning queue with progress
- Family calendar integration

**Work/Grove:**
- Telegram bot for mobile capture
- Voice capture via Whisper transcription
- Calendar integration for deadline surfacing
- Email triage with Atlas logic

**Technical:**
- Notion bi-directional sync (real-time)
- AI-suggested triage (Atlas proposes, Jim confirms)
- Offline mode for extension

---

## Sprint Planning View

### Recommended First Sprint: "Atlas in the Browser"

**Goal:** Prove the extension-as-command-center model across all pillars

**Scope:**
1. P1-CORE-001: Extension Dashboard Tab (M)
2. P1-CORE-002: Quick Capture from Any Page (S)
3. P1-CORE-003: Blocked Items Alert (S)

**Total effort:** ~3-4 days

**Success metric:** Jim uses extension dashboard daily instead of opening Notion to check Atlas state.

---

### Recommended Second Sprint: "Life Projects"

**Goal:** Prove Atlas works for garage build and other non-Grove projects

**Scope:**
1. P1-LIFE-001: Project Budget Tracker (M)
2. P1-LIFE-002: Receipt/Expense Quick Capture (S)
3. P2-LIFE-003: Project Progress Milestones (S)

**Total effort:** ~3-4 days

**Success metric:** Garage build budget tracked in Atlas with < 30 seconds per expense capture.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-01-29 | Initial backlog created from product discovery |

---

*Backlog is a living document. Update as priorities shift.*
