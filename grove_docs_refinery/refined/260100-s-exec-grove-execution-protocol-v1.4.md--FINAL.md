# Grove Execution Protocol v1.4

**Purpose:** Execution contracts for Grove Foundation development implementing DEX/Trellis architecture principles with atomic verification gates.

**Philosophy:** This is not a planning methodology. This is an execution contract format. Planning happens in conversation; execution follows this protocol.

**v1.4 Changes:**
- Added Constraint 10: REVIEW.html Completion Gate
- Added Constraint 7b: UI Slot Check — New Object Audit
- REVIEW.html must be complete with all screenshots before user handoff
- Standardized handoff sequence with user notification
- New objects must pass UI Slot decision tree before creating routes

**v1.3 Changes:**
- Added Constraint 2b: Playwright Visual Verification (replaces unreliable Chrome MCP)
- Playwright commands for deterministic screenshot capture
- E2E test file pattern for User Story smoke tests

**v1.2 Changes:**
- Added Constraint 8: Code-Simplifier Pre-Commit Gate
- Added Constraint 9: Sprint Documentation Commits
- Added DEX Compliance Gates as enforceable checkpoints
- Strengthened Constraint 2: Visual Verification enforcement