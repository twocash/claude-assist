# Execution Prompt: skill-builder v1

---

## Agent Role Declaration

You are acting as **DEVELOPER** for sprint: **skill-builder-v1**

**Sprint Objective:** Build the skill-builder meta-tool that creates all other skills

**Reference Documents:**
- SPEC: `docs/sprints/skill-builder-v1/SPEC.md`
- User Stories: `docs/sprints/skill-builder-v1/USER_STORIES.md`
- Master Plan: `docs/SKILLS_MASTER_PLAN.md`

---

## Execution Contract

### Mode
**Execute** - Implement the skill per specification

### Deliverables
1. Working skill-builder skill at: `skills/meta/skill-builder/skill.md` ✓ COMPLETE
2. Test the skill by creating a mock skill
3. Generate REVIEW.html with screenshots/evidence
4. Write COMPLETE status entry

### Hard Constraints
- Follow skill template structure exactly
- Use AskUserQuestion for interactive flow
- Validate all inputs before generation
- Create test templates automatically
- DO NOT skip the preview/confirm step

---

## Implementation Steps

### Phase 1: Setup ✓ COMPLETE
- [x] Create skills/meta/skill-builder/ directory
- [x] Write skill.md following template
- [x] Write README.md with quick start guide

### Phase 2: Testing 🔄 CURRENT
- [ ] Test skill-builder by creating a mock skill
- [ ] Verify all questions asked correctly
- [ ] Verify file generation works
- [ ] Verify test template created
- [ ] Document any issues

### Phase 3: Documentation
- [ ] Capture screenshots of interaction
- [ ] Generate REVIEW.html
- [ ] Write status entry with results

### Phase 4: Iteration (if needed)
- [ ] Fix any bugs found in testing
- [ ] Refine question flow if needed
- [ ] Update documentation

---

## Test Plan

Create a **mock skill** to verify skill-builder works:

**Test Skill Details:**
- Name: `test-hello`
- Category: `utilities`
- Description: "Says hello to the user"
- Triggers: "hello", "greet me"
- Mode: Execute
- Purpose: Simple greeting skill for testing skill-builder

**Verification Checklist:**
- [ ] Wizard asks all 10+ questions
- [ ] Answers are validated
- [ ] Preview shown before save
- [ ] File created at: skills/utilities/test-hello/skill.md
- [ ] Test template created at: skills/.templates/tests/test-test-hello.md
- [ ] Success message displays correct paths
- [ ] Generated skill is properly formatted

---

## Success Criteria

Sprint is COMPLETE when:
- [ ] skill-builder skill created and documented
- [ ] Tested with mock skill successfully
- [ ] All acceptance criteria pass (see SPEC.md)
- [ ] REVIEW.html generated with evidence
- [ ] COMPLETE status entry written
- [ ] Ready to use for creating other skills

---

## Status Update Protocol

Write status entries to: `.agent/status/current/`

**Entry Format:** `{NNN}-{timestamp}-developer.md`

**Update heartbeat every 5 minutes during active work**

**Phases to report:**
- STARTED - Beginning implementation
- IN_PROGRESS - Active development
- COMPLETE - Sprint finished

---

## Notes

**This is the foundation skill** - get it right! All 14 other skills will be created using this tool.

**Testing is critical** - don't skip the mock skill test. If skill-builder has bugs, all subsequent skills will inherit them.

**Quality over speed** - take time to make the interactive flow smooth and intuitive.

---

*Execute per Bedrock Sprint Contract - focus, iterate, deliver*
