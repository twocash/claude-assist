# User Stories: skill-builder v1

---

## Story 1: Interactive Skill Creation

**As a** developer testing agent coordination
**I want** an interactive wizard to create new skills
**So that** I can build skills quickly without manual template editing

**Acceptance Criteria:**
- Wizard asks all required questions in sequence
- Each question has clear prompt and validation
- Answers are collected before generation
- Invalid inputs are rejected with helpful messages

---

## Story 2: Skill Generation from Template

**As a** skill creator
**I want** the wizard to generate properly formatted skill.md files
**So that** all skills follow consistent structure

**Acceptance Criteria:**
- Generated skill uses skill-template.md as base
- All placeholders are replaced with user answers
- Trigger phrases formatted as bulleted list
- Instructions broken into clear steps
- Examples properly formatted
- Dependencies listed

---

## Story 3: Category-Based Organization

**As a** skill maintainer
**I want** skills saved to correct category directories
**So that** the skill suite stays organized

**Acceptance Criteria:**
- Wizard asks for category selection
- Valid categories: coordination, testing, utilities, meta
- Directory created automatically: skills/{category}/{skill-name}/
- Skill saved to: skills/{category}/{skill-name}/skill.md

---

## Story 4: Preview Before Save

**As a** skill creator
**I want** to review generated content before saving
**So that** I can catch errors and make adjustments

**Acceptance Criteria:**
- Wizard displays full generated content
- User can approve, reject, or request edits
- Edits can be made iteratively
- File only saved on explicit approval

---

## Story 5: Test Template Generation

**As a** skill tester
**I want** test templates auto-generated with each skill
**So that** I can validate skill behavior

**Acceptance Criteria:**
- Test template created at: skills/.templates/tests/test-{skill-name}.md
- Template includes example scenarios from wizard
- Verification checklists generated
- Template ready for manual testing

---

## Story 6: Clear Next Steps

**As a** skill creator
**I want** guidance on what to do after skill creation
**So that** I know how to test and deploy

**Acceptance Criteria:**
- Success message shows file paths
- Next steps listed clearly
- Includes how to invoke the skill
- Includes how to iterate if needed

---

*All stories target skill-builder v1.0*
