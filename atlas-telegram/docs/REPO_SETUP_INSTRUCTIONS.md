# Atlas 2.0 Repository Setup Instructions

**For:** Claude Code Developer  
**From:** Atlas Planning Session (2026-01-30)  
**Goal:** Create clean `atlas/` repo, move Atlas apps, leave Grove content pipelines untouched

---

## Context

Atlas is Jim's personal cognitive co-pilot across all life domains (Personal, Grove, Consulting, Home). It consists of:

- **Telegram bot** — Mobile-first clarification layer
- **Chrome extension** — Desktop co-pilot for web work
- **Skills system** — Agent coordination capabilities
- **Brain docs** — Institutional knowledge

**Important Firewall:**
- `the-grove-foundation/` = Grove software codebase (separate repo, don't touch)
- `grove_docs_refinery/` and `grove_research_generator/` = Content pipelines that STAY in `claude-assist/`

Atlas can *dispatch* tasks to Grove content pipelines. Atlas does NOT own them.

---

## Step 1: Create New Repo Structure

```bash
# Create atlas repo
cd C:\github
mkdir atlas
cd atlas
git init

# Create directory structure
mkdir -p apps/telegram
mkdir -p apps/chrome-ext
mkdir -p packages/skills
mkdir -p docs
mkdir -p workspace
```

---

## Step 2: Initialize Bun Monorepo

Create `package.json` in root:

```json
{
  "name": "atlas",
  "version": "2.0.0",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "dev:telegram": "cd apps/telegram && bun run dev",
    "dev:chrome": "cd apps/chrome-ext && bun run dev",
    "typecheck": "bun run --filter '*' typecheck"
  }
}
```

---

## Step 3: Copy Telegram Bot

```bash
# Copy all telegram bot files
xcopy /E /I "C:\github\claude-assist\atlas-telegram\*" "C:\github\atlas\apps\telegram\"

# Remove nested docs (we'll put these at root level)
rmdir /S /Q "C:\github\atlas\apps\telegram\docs"
```

Update `apps/telegram/package.json` name to `@atlas/telegram`.

---

## Step 4: Copy Chrome Extension

```bash
# Copy chrome extension
xcopy /E /I "C:\github\claude-assist\atlas-chrome-ext\*" "C:\github\atlas\apps\chrome-ext\"
```

Update `apps/chrome-ext/package.json` name to `@atlas/chrome-ext` (if it has one).

---

## Step 5: Copy Skills (Coordination Only)

```bash
# Copy skills directory
xcopy /E /I "C:\github\claude-assist\skills\*" "C:\github\atlas\packages\skills\"
```

We want these coordination skills:
- `agent-dispatch/`
- `health-check/`
- `heartbeat-monitor/`
- `status-inspector/`
- `skill-builder/`

Can delete utility skills (directory-map, git-snapshot, python-env) or keep for reference.

---

## Step 6: Copy Brain Docs

```bash
# Copy prepared docs
copy "C:\github\claude-assist\atlas-telegram\docs\PRODUCT.md" "C:\github\atlas\docs\"
copy "C:\github\claude-assist\atlas-telegram\docs\DECISIONS.md" "C:\github\atlas\docs\"
copy "C:\github\claude-assist\atlas-telegram\docs\MIGRATION_STRATEGY.md" "C:\github\atlas\docs\"

# Copy SPARKS to docs
copy "C:\github\claude-assist\atlas-telegram\workspace\SPARKS.md" "C:\github\atlas\docs\"

# Copy and update CLAUDE.md
copy "C:\github\claude-assist\atlas-telegram\CLAUDE.md" "C:\github\atlas\CLAUDE.md"
```

---

## Step 7: Create Root README

Create `README.md`:

```markdown
# Atlas

Personal cognitive co-pilot for Jim Calhoun.

## Apps

- **telegram/** — Mobile-first clarification layer
- **chrome-ext/** — Desktop co-pilot for web work

## Quick Start

```bash
# Install dependencies
bun install

# Run telegram bot
bun run dev:telegram

# Build chrome extension
cd apps/chrome-ext && bun run build
```

## Documentation

See `docs/` for:
- PRODUCT.md — Product vision
- DECISIONS.md — Architecture decisions
- SPARKS.md — Classification framework

## Related (Not in This Repo)

- **Grove Content Pipelines** — `claude-assist/grove_docs_refinery/`, `claude-assist/grove_research_generator/`
- **Grove Foundation** — `the-grove-foundation/` (software codebase)
```

---

## Step 8: Update CLAUDE.md Paths

Edit `C:\github\atlas\CLAUDE.md` to reflect new structure:

- Update file paths to `apps/telegram/`, `apps/chrome-ext/`
- Add note about Grove content pipelines location:

```markdown
## Grove Content Pipelines (External)

Atlas dispatches to these but does NOT own them:

| Pipeline | Location | Purpose |
|----------|----------|---------|
| Docs Refinery | `C:\github\claude-assist\grove_docs_refinery\` | Document polishing |
| Research Generator | `C:\github\claude-assist\grove_research_generator\` | Blog/whitepaper generation |

Invoke via subprocess. Editorial memory lives with the pipelines.
```

---

## Step 9: Initial Commit

```bash
cd C:\github\atlas
git add .
git commit -m "feat: Atlas 2.0 - unified cognitive co-pilot

- Telegram bot (mobile clarification layer)
- Chrome extension (desktop web co-pilot)
- Skills system (agent coordination)
- Brain docs (PRODUCT, DECISIONS, SPARKS)

Grove content pipelines remain in claude-assist/ (hardened, separate concern)."
```

---

## Step 10: Create GitHub Repo & Push

1. Create new repo on GitHub: `atlas` (private)
2. Push:

```bash
git remote add origin https://github.com/[org]/atlas.git
git branch -M main
git push -u origin main
```

---

## Step 11: Archive claude-assist

Add to `C:\github\claude-assist\README.md`:

```markdown
# claude-assist (Archived)

**Atlas 2.0 has moved to:** https://github.com/[org]/atlas

## What Remains Here

### Active (Grove Content Pipelines)
- `grove_docs_refinery/` — Document polishing pipeline
- `grove_research_generator/` — Blog/whitepaper generation
- `editorial_memory.md` — Learned editorial preferences
- `notion_pipeline/` — Python Notion utilities

### Archived (Reference Only)
- `atlas-telegram/` — Moved to atlas repo
- `atlas-chrome-ext/` — Moved to atlas repo
- `skills/` — Moved to atlas repo
- `agents/` — Superseded by Agent SDK
- `launchers/`, `sandbox/`, `configs/` — Legacy utilities
```

---

## Verification Checklist

After setup, verify:

- [ ] `bun install` works in atlas root
- [ ] `bun run dev:telegram` starts the bot
- [ ] Chrome extension builds/loads
- [ ] All docs present in `docs/`
- [ ] CLAUDE.md paths are correct
- [ ] Grove content pipelines still work from claude-assist (unchanged)

---

## What NOT to Move

| Directory | Reason |
|-----------|--------|
| `grove_docs_refinery/` | Hardened Grove content pipeline |
| `grove_research_generator/` | Hardened Grove content pipeline |
| `editorial_memory.md` | Belongs with pipelines |
| `notion_pipeline/` | Used by Grove pipelines |
| `the-grove-foundation/` | Separate codebase, own agent system |

---

*Atlas 2.0: Triage, organize, execute — without fighting the brain you have.*
