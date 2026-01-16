# Skills Directory

**Repository:** claude-assist testbed
**Purpose:** Prototype and test skills before deploying to ~/.claude/skills/

---

## Directory Structure

```
skills/
├── .templates/          # Skill templates and boilerplates
├── coordination/        # Agent coordination skills
├── testing/             # Testing and validation skills
├── utilities/           # General utility skills
└── README.md
```

---

## Skill Categories

### Coordination Skills
Skills for managing multi-agent workflows:
- Status monitoring and health checks
- Agent dispatch and lifecycle management
- Cross-agent communication protocols

### Testing Skills
Skills for validating agent behavior:
- Mock data generation
- Protocol compliance testing
- Simulated workflows

### Utility Skills
General-purpose tools:
- File operations
- Data transformation
- Environment inspection

---

## Creating a New Skill

1. Copy template from `.templates/skill-template.md`
2. Define trigger phrases and purpose
3. Write skill instructions
4. Test in sandbox environment
5. Deploy to ~/.claude/skills/ when proven

---

## Skill Format

Each skill is a markdown file with:
- **Identity** - Name and persona
- **Triggers** - Activation phrases
- **Purpose** - What it does
- **Instructions** - How to execute
- **Examples** - Usage patterns

---

*Skills tested here, deployed to production when proven.*
