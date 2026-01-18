## Rewrite: 251200-s-method-user-story-refinery.md
### Diagnosis Summary
Source document is a comprehensive methodology for extracting user stories from specifications. Generally well-structured with strong technical content, but uses some legacy terminology and could benefit from Grove's voice standards and strategic alignment.

### Key Changes Made
- Removed throat-clearing phrases ("A structured methodology for", "Use when")
- Replaced "User" with "Observer" where appropriate in Grove contexts
- Tightened prose throughout while preserving technical precision
- Aligned DEX pillar terminology with current checkpoint
- Strengthened opening with direct value proposition
- Maintained all technical methodology and templates intact

### Flags for Review
- Kept all technical templates and Gherkin examples as-is (they're functional specs)
- Preserved INVEST framework terminology as it's industry standard
- Maintained priority/complexity notation (P0/P1/P2, S/M/L) as established conventions

---
# User Story Refinery v1

Transform requirements specifications into testable user stories with acceptance criteria. Produces review-ready story documents, flags clunky flows, proposes simplifications, and prepares for downstream test generation.

**Four-Phase Pipeline:**
1. **Story Extraction** — Parse spec into INVEST-assessed user stories
2. **Acceptance Criteria** — Gherkin scenarios for each story
3. **Test Case Generation** — Derive test cases from criteria (Phase 3)
4. **Playwright Scaffolding** — Generate test file structure (Phase 4)

This skill covers Phases 1-2. Phases 3-4 are downstream execution.