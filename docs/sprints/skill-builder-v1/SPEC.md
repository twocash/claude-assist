# SPEC: skill-builder v1

**Status:** ready
**Sprint ID:** skill-builder-v1
**Created:** 2026-01-16

---

## Problem Statement

Creating new skills manually is time-consuming and error-prone. Each skill requires:
- Proper markdown formatting
- Consistent structure
- Category placement
- Template adherence
- Documentation

We need an **interactive wizard** that guides skill creation and enforces consistency.

---

## Acceptance Criteria

### AC1: Interactive Question Flow
**Given** the user invokes `/skill-builder`
**When** the wizard starts
**Then** it should ask structured questions about:
- Skill name
- One-line description
- Category (coordination/testing/utilities/meta)
- Trigger phrases (at least 2)
- Purpose (2-3 sentences)
- Mode (Plan/Execute/Review/Explore)
- Optional persona
- Step-by-step instructions
- Output format
- Example scenarios
- Dependencies

### AC2: Skill Generation
**Given** user has answered all questions
**When** wizard completes
**Then** it should:
- Generate skill.md from template
- Save to correct category directory (skills/{category}/{skill-name}/)
- Create folder structure if needed
- Display success message with file path

### AC3: Validation
**Given** user provides skill details
**When** generating the skill
**Then** it should validate:
- Skill name is valid (lowercase-with-dashes)
- At least 2 trigger phrases provided
- Purpose is not empty
- At least one instruction step
- Category is valid

### AC4: Review Before Save
**Given** wizard has generated skill content
**When** before saving to file
**Then** it should:
- Display generated content
- Ask user to confirm or edit
- Allow iteration if needed
- Save only on explicit confirmation

### AC5: Test Scenario Generation
**Given** skill has been created
**When** wizard completes
**Then** it should:
- Generate sample test scenarios
- Create test-{skill-name}.md in .templates/tests/
- Include example invocations
- Include expected outputs

---

## Technical Approach

### Implementation

**Mode:** Interactive (uses AskUserQuestion tool)

**Flow:**
1. Welcome + explain process
2. Ask questions in sequence
3. Build skill content progressively
4. Display preview
5. Confirm with user
6. Save to file
7. Generate test template
8. Display next steps

### File Structure

```
skills/{category}/{skill-name}/
├── skill.md           # Main skill definition
└── README.md          # Optional notes
```

### Questions to Ask

1. **Skill name?** (lowercase-with-dashes)
2. **One-line description?**
3. **Category?** (coordination/testing/utilities/meta)
4. **Trigger phrases?** (comma-separated, min 2)
5. **Purpose?** (2-3 sentences)
6. **Mode?** (Plan/Execute/Review/Explore)
7. **Persona?** (optional)
8. **Instruction steps?** (Step 1, Step 2, etc.)
9. **Output format?** (What does it deliver?)
10. **Example scenarios?** (At least 1)
11. **Dependencies?** (Tools/files needed)

---

## Out of Scope (v1)

- Skill editing (use manual file editing)
- Skill deletion (use manual file deletion)
- Skill versioning (future)
- Automated testing (future - see skill-test)

---

## Example Usage

```
User: /skill-builder

Skill Builder: Let's create a new skill! I'll ask you some questions.

[Interactive Q&A flow]

Skill Builder: Generated skill preview:

---
[Shows generated skill.md content]
---

Does this look correct? (yes/no/edit)

User: yes

Skill Builder: ✓ Created: skills/utilities/my-cool-skill/skill.md
               ✓ Created: skills/.templates/tests/test-my-cool-skill.md

Next steps:
1. Review the generated skill
2. Test with: /my-cool-skill
3. Iterate if needed
4. Deploy with /skill-deploy when ready
```

---

## Dependencies

- skills/.templates/skill-template.md
- AskUserQuestion tool for interactive flow
- File write capabilities
- Directory creation

---

## Success Metrics

- Time to create new skill < 5 minutes
- Skills follow consistent format
- All required fields populated
- Test templates generated automatically

---

*Ready for implementation*
