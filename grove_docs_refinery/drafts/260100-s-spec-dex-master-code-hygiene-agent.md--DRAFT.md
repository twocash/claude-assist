## Rewrite: 260100-s-spec-dex-master-code-hygiene-agent.md
### Diagnosis Summary
Source document is well-structured technical specification with clear scope and methodology. Some terminology needs updating (Grove Foundation → Foundation, architectural framing), and voice could be more active/direct in places.

### Key Changes Made
- Updated "grove-foundation" references to "Foundation codebase" for clarity
- Replaced "vision lens" metaphor with direct "architectural analysis" language
- Strengthened active voice throughout ("identifies" vs "that identifies")
- Clarified Grove-specific terminology (DEX → Declarative Exploration)
- Made risk classifications more concrete and actionable
- Preserved all technical specifications and workflow details

### Flags for Review
- Database IDs and Notion integration details assumed to be current
- Contract spec requirements align with existing contract skill patterns
- Protected zone file paths should be verified against current codebase structure

---
# DEX Master — Code Hygiene Analysis Agent

A code review agent that scans the Foundation codebase through architectural analysis to identify:
1. **Quick Fixes** — Atomic, high-confidence changes → Fix Queue DB
2. **Strategic Notes** — Architecture observations, future sprint fodder → Strategic Notes DB

## Trigger Modes

### Post-Commit (Automated)
Runs after each commit to main/dev branches when changes touch active review zones.

### Manual Scan (On-Demand)
Full codebase analysis for initial queue population or periodic deep review.