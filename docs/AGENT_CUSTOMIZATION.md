# Agent Customization Guide

**Repository:** claude-assist
**Purpose:** How to customize the default agent personality and behavior

---

## Option 1: Custom Instructions File (Recommended)

### Setup

1. **Create instructions file:** `.claude/custom-instructions.md`
2. **Reference in settings:** `.claude/settings.local.json`

```json
{
  "customInstructions": {
    "path": ".claude/custom-instructions.md"
  }
}
```

3. **Write your agent persona** in the markdown file

### What to Include

- **Identity** - Name, role, personality
- **Responsibilities** - What this agent does by default
- **Communication style** - Tone, catchphrases, approach
- **Default behaviors** - Startup routines, problem-solving approach
- **Project context** - What repo is this, what are we building
- **Boundaries** - What to do/not do

### Example: ATLAS Agent

See `.claude/custom-instructions.md` for the ATLAS (Agent Testing & Laboratory Assistant) persona we created for claude-assist.

**Key features:**
- Methodical, experimental tone
- Proactive health checks
- Git hygiene reminders
- Skills awareness
- Testbed safety (keeps prod separate)

---

## Option 2: Per-Session Instructions

Start your session with an activation prompt:

```
You are ATLAS, the Agent Testing & Laboratory Assistant for claude-assist.

Your role: Test agent coordination patterns in this sandbox before deploying to production.

[Paste custom instructions...]
```

**Pros:** Flexible, easy to iterate
**Cons:** Must paste every session

---

## Option 3: Startup Hook (Advanced)

Create a hook in `.claude/hooks/` that runs on session start:

```bash
# .claude/hooks/on-session-start.sh
cat .claude/custom-instructions.md
```

This displays instructions at startup (but doesn't enforce them).

---

## Creating Different Agent Personas

### Example: Security-Focused Agent

```markdown
You are SENTINEL - Security Testing Agent

- Paranoid about vulnerabilities
- Questions all external dependencies
- Validates inputs obsessively
- Documents threat models
- Never trusts, always verifies
```

### Example: Speed-Focused Agent

```markdown
You are VELOCITY - Rapid Prototyping Agent

- Ship fast, iterate faster
- Embrace technical debt (for prototypes)
- Bias toward action over planning
- Document later, build now
- "Make it work, make it right, make it fast" (in that order)
```

### Example: Documentation Agent

```markdown
You are SCRIBE - Documentation Specialist

- Every change gets documented
- README-first development
- Diagrams for complex systems
- Examples for everything
- Future-you shouldn't have to guess
```

---

## Mixing Personas

You can switch agents mid-session:

```
Now act as SENTINEL (security agent) and audit this code for vulnerabilities.

[After security review...]

Switch back to ATLAS (default testbed agent).
```

---

## Best Practices

### 1. Make It Memorable
Give your agent a name and personality - it helps you remember what mode you're in.

### 2. Define Clear Boundaries
What should this agent do vs not do? Explicit boundaries prevent confusion.

### 3. Include Project Context
Remind the agent where it is, what's being built, what stage the project is in.

### 4. Set Communication Expectations
How verbose? How formal? What tone? Define it upfront.

### 5. Specify Default Behaviors
What should happen on startup? During work? When encountering errors?

### 6. List Available Skills
If you have custom skills, mention them so the agent knows to use them.

---

## Testing Your Custom Instructions

### Quick Test

1. Edit `.claude/custom-instructions.md`
2. Start new Claude Code session
3. Give a simple task
4. Check if agent follows the persona

### Validation Checklist

- [ ] Agent uses the defined name/identity
- [ ] Tone matches what you specified
- [ ] Default behaviors execute (e.g., startup checks)
- [ ] Boundaries are respected
- [ ] Project context is referenced

---

## Iteration Tips

**Start simple** - Define just identity and tone first
**Add gradually** - Layer in responsibilities and behaviors
**Test frequently** - Try new instructions with real tasks
**Refine based on use** - Adjust when agent misunderstands
**Document what works** - Keep successful patterns

---

## Example Workflow

### Day 1: Basic Identity
```markdown
You are ATLAS, testbed coordinator.
Be methodical and experimental.
```

### Day 2: Add Responsibilities
```markdown
You are ATLAS, testbed coordinator.
Be methodical and experimental.

Responsibilities:
- Monitor agent health
- Test new skills
- Document patterns
```

### Day 3: Add Behaviors
```markdown
[Previous content...]

Default Behavior:
- Check .agent/status/ on startup
- Commit after each skill created
- Update SESSION_SUMMARY.md at milestones
```

### Day 4: Refine Tone
```markdown
[Previous content...]

Communication:
- Explain failures as learning opportunities
- Use analogies for complex concepts
- Show code examples, don't just describe
```

---

## Advanced: Multiple Configurations

Create different settings files for different modes:

```
.claude/
├── settings.local.json          # Default (ATLAS)
├── settings.security.json       # Security mode (SENTINEL)
├── settings.speed.json          # Rapid prototyping (VELOCITY)
└── settings.docs.json           # Documentation (SCRIBE)
```

Switch by symlinking or copying the desired config.

---

## Resources

- **Current ATLAS config:** `.claude/custom-instructions.md`
- **Settings file:** `.claude/settings.local.json`
- **Master plan:** `docs/SKILLS_MASTER_PLAN.md`
- **Research:** `docs/RESEARCH_INSIGHTS.md`

---

*Customize your agent, customize your workflow*
