# Grove Editorial Engine

A skill for rewriting, updating, and rationalizing Grove content to reflect current strategic positioning, architectural thinking, and voice standards.

## Purpose

This skill enables any Claude instance to produce Grove content that is:
- **Current** — reflects evolved thinking, not legacy positioning
- **Consistent** — unified voice, terminology, and framing
- **Strategic** — serves Grove's actual goals, not generic AI/crypto tropes

## Prerequisites

Before any rewrite task, load the checkpoint:
```
/mnt/skills/user/grove-editorial-engine/grove-editorial-checkpoint.md
```

The checkpoint contains dynamic state (what's current). This skill contains stable methodology (how to apply it).

---

## Voice Standards

### Core Principles

1. **Strategic, not smug** — Confidence without arrogance. Grove has a genuine thesis; state it clearly without overselling.

2. **Concrete over abstract** — Replace "distributed intelligence" with specific mechanisms. What actually happens?

3. **Honest about uncertainty** — Document what we don't know. "This is our hypothesis" beats false certainty.

4. **8th-grade accessibility, graduate-level thinking** — Simple sentences carrying sophisticated ideas.

5. **Active voice, present tense** — "Grove enables" not "will be enabled by Grove"

### Terminology Precision

- **Exploration architecture** (not "AI platform" or "decentralized AI")
- **Agents** (not "bots" or "AI assistants")
- **The Observer** (not "user" in agent-facing contexts)
- **Credits** (not "tokens" — avoid crypto connotation)
- **Trellis Architecture** (the standard), **Grove** (the implementation)
- **Foundation** (the organization), **Terminal** (the interface)

### What to Avoid

- Buzzwords: "revolutionary," "paradigm shift," "Web3," "democratize"
- Hedging: "might," "could potentially," "it's possible that"
- Throat-clearing: "It's important to note that," "In order to"
- Crypto/VC signaling: "tokenomics," "network effects," "moats"
- Generic AI hype: "the future of AI," "unprecedented capabilities"

---

## Rewrite Methodology

### Step 1: Diagnosis

Before rewriting, assess the source content:

| Question | Implications |
|----------|--------------|
| When was this written? | Earlier = more likely to have legacy framing |
| What's the document type? | White paper vs. think piece vs. spec have different standards |
| Who's the audience? | Technical, executive, academic, general? |
| What's working? | Preserve what's good; don't rewrite for rewriting's sake |
| What's broken? | Outdated positioning, wrong terminology, weak arguments? |

### Step 2: Checkpoint Alignment

Compare source content against checkpoint:

- **Terminology:** Flag any legacy terms; map to current equivalents
- **Positioning:** Does it reflect current strategic framing?
- **Architecture:** Does technical description match current implementation?
- **Tensions:** Does it acknowledge known tensions, or paper over them?

### Step 3: Structural Assessment

Evaluate document structure:

- **Lead with "so what"** — Does the opening paragraph state the core insight?
- **Argument flow** — Does each section build toward the conclusion?
- **Evidence quality** — Are claims supported? Are sources current?
- **Length appropriateness** — Is it the right length for its purpose?

### Step 4: Rewrite

Apply changes in this order:

1. **Fix terminology** — Mechanical find/replace using checkpoint mappings
2. **Update positioning** — Align framing with current strategic state
3. **Strengthen arguments** — Add evidence, remove hedging, sharpen claims
4. **Tighten prose** — Cut filler, activate passive constructions, reduce word count
5. **Verify voice** — Read aloud; does it sound like Grove?

### Step 5: Validation

Check the rewrite against:

- [ ] All terminology is current (per checkpoint)
- [ ] Strategic positioning reflects current state
- [ ] Technical descriptions are accurate
- [ ] Voice is consistent throughout
- [ ] No buzzwords or hedging language
- [ ] Appropriate length for document type
- [ ] Sources/references are current

---

## Document Type Protocols

### White Papers / Technical Documents

- **Tone:** Authoritative but accessible
- **Structure:** Problem → Approach → Mechanism → Implications
- **Evidence:** Academic citations, technical specifics, concrete examples
- **Length:** 2,000-5,000 words typical
- **Voice:** Third-person institutional ("Grove implements..." not "We implement...")

### Think Pieces / Strategic Essays

- **Tone:** Provocative but substantiated
- **Structure:** Observation → Insight → Implications → Call to action
- **Evidence:** Market data, analogies, logical arguments
- **Length:** 1,000-2,500 words typical
- **Voice:** Can be first-person for perspective pieces

### Technical Specifications

- **Tone:** Precise, unambiguous
- **Structure:** Overview → Components → Interfaces → Behaviors → Edge Cases
- **Evidence:** Code references, architectural diagrams, concrete examples
- **Length:** As needed for completeness
- **Voice:** Imperative for requirements ("The system SHALL...")

### Pitch Materials / Executive Summaries

- **Tone:** Confident, strategic
- **Structure:** Hook → Problem → Solution → Differentiation → Ask
- **Evidence:** Market validation, traction metrics, strategic positioning
- **Length:** 500-1,500 words (or slide-appropriate)
- **Voice:** Direct, active, benefit-focused

### Outreach / Partnership Materials

- **Tone:** Collaborative, mutual-benefit focused
- **Structure:** Shared context → Opportunity → Proposed collaboration → Next steps
- **Evidence:** Alignment points, complementary capabilities
- **Length:** Brief (under 1,000 words)
- **Voice:** Warm but professional; peer-to-peer

---

## Refinery Workflow Integration

This skill is designed to work in a multi-agent refinery:

### Writer Agent Role
- Loads this skill + checkpoint
- Receives source content
- Produces rewritten draft
- Flags areas of uncertainty for reviewer

### Reviewer Agent Role
- Loads this skill + checkpoint
- Receives rewritten draft
- Validates against methodology and checkpoint
- Produces assessment: PASS / REVISE (with specific feedback) / ESCALATE (needs human decision)

### Human Review Points
- Strategic positioning changes (reviewer escalates)
- Terminology decisions not covered by checkpoint
- Content that fundamentally changes Grove's claims
- Anything touching legal, financial, or partnership commitments

### Output Format

Writer agent outputs:
```markdown
## Rewrite: [Document Title]

### Diagnosis Summary
[Brief assessment of source content]

### Key Changes
- [Change 1]
- [Change 2]
- [etc.]

### Flags for Review
- [Any uncertainties or decisions needed]

---

[REWRITTEN CONTENT]
```

Reviewer agent outputs:
```markdown
## Review: [Document Title]

### Assessment: [PASS / REVISE / ESCALATE]

### Validation Checklist
- [ ] Terminology current
- [ ] Positioning aligned
- [ ] Technical accuracy
- [ ] Voice consistency
- [ ] No prohibited language
- [ ] Appropriate length

### Specific Feedback
[If REVISE: what needs to change]
[If ESCALATE: what decision is needed]
```

---

## Reference Hierarchy

When source content conflicts with reference documents, defer in this order:

1. **grove-editorial-checkpoint.md** — Current state (highest authority)
2. **Trellis_Architecture_Bedrock_Addendum.md** — Architectural canon
3. **Grove_Technical_Architecture_Reference.md** — Technical specifics
4. **Advisory Council consensus points** — Design philosophy
5. **Source content** — May contain legacy thinking (lowest authority)

---

## Updates

This skill should remain stable. When Grove's methodology evolves:
- Update the checkpoint (for state changes)
- Update this skill only for process/methodology changes

Last methodology update: January 2026
