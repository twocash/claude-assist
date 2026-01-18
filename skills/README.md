# Skills Directory

**Repository:** ATLAS Personal Chief of Staff
**Purpose:** Skills for task delegation and personal productivity

---

## Directory Structure

```
skills/
├── .templates/          # Skill templates
├── coordination/        # Task coordination skills
├── meta/                # Skills about skills
└── utilities/           # General utility skills
```

---

## Skill Categories

### Meta Skills
Skills for creating and managing other skills:
- **skill-builder** - Interactive wizard for creating new skills
- **load-persona** - Activate custom agent personas

### Coordination Skills
Skills for delegating tasks and monitoring progress:
- **agent-dispatch** - Delegate tasks to specialized agents
- **health-check** - Validate ATLAS workspace health
- **heartbeat-monitor** - Monitor active task progress
- **status-inspector** - Analyze task details and history

### Utility Skills
General-purpose tools:
- **gitfun** - Analyze GitHub repo installation difficulty
- **directory-map** - Directory structure visualization
- **git-snapshot** - Create git commit snapshots
- **python-env** - Python environment information
- **sandbox-clean** - Clean workspace/temp files

---

## Creating a New Skill

1. Copy template from `.templates/skill-template.md`
2. Define trigger phrases and purpose
3. Write skill instructions
4. Place in appropriate category directory

---

## Skill Format

Each skill is a markdown file with:
- **Identity** - Name and persona
- **Triggers** - Activation phrases
- **Purpose** - What it does
- **Instructions** - How to execute
- **Examples** - Usage patterns

---

*ATLAS Skills - Delegate smart, execute well*
