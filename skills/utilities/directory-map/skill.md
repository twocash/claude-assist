# directory-map

**Category:** Utilities
**Version:** 1.0.0
**Status:** Active

---

## Identity

**Purpose:** Generate annotated repository structure map with descriptions and purpose

**Triggers:**
- `/directory-map`
- `/show-structure`
- "map repository"
- "show directory tree"

**Depends On:**
- File system access
- `.gitignore` awareness (skip ignored files)

---

## Instructions

When this skill is invoked, create an annotated visual map of the repository structure.

### Step 1: Scan Directory Structure

Recursively traverse the repository:

```bash
# Simple tree (if available)
tree -L 3 -I 'node_modules|__pycache__|.git'

# Or use Python
import os
from pathlib import Path

def scan_directory(path, max_depth=3, current_depth=0):
    """Recursively scan directory structure."""
    # Implementation here
```

**Exclude:**
- `.git/`
- `__pycache__/`
- `node_modules/`
- `.venv/`, `venv/`
- `*.pyc`, `*.pyo`
- Files in `.gitignore`

### Step 2: Categorize Files and Directories

Identify special directories and their purposes:

**Infrastructure Directories:**
- `.agent/` - Agent coordination system
- `.claude/` - Claude Code configuration
- `skills/` - Custom skills
- `sandbox/` - Testing workspace

**Code Directories:**
- `src/` - Source code
- `lib/` - Libraries
- `scripts/` - Utility scripts
- `launchers/` - Startup scripts

**Documentation:**
- `docs/` - Documentation files
- `README.md` - Project overview
- `*.md` files - Various docs

**Configuration:**
- `.gitignore` - Git ignore rules
- `settings.json` - App settings
- `*.yaml`, `*.json` - Config files

### Step 3: Annotate with Descriptions

Add meaningful descriptions for each directory:

```python
annotations = {
    ".agent/": "🤖 Agent coordination infrastructure",
    ".agent/roles/": "📋 Agent role definitions",
    ".agent/config/": "⚙️ System configuration",
    ".agent/status/": "📊 Status logging entries",
    "skills/": "🛠️ Custom skill definitions",
    "skills/coordination/": "🔗 Multi-agent coordination skills",
    "skills/testing/": "🧪 Testing and validation skills",
    "skills/utilities/": "🔧 Utility and helper skills",
    "sandbox/": "🏖️ Isolated testing environment",
    "docs/": "📚 Documentation and guides",
    ".claude/": "💬 Claude Code personalization",
}
```

### Step 4: Generate Visual Tree

Create tree representation with annotations:

```markdown
# Repository Structure Map
**Repository:** claude-assist
**Scanned:** {timestamp}
**Root:** C:\github\claude-assist

---

## Directory Tree

```
claude-assist/
│
├── 📁 .agent/                     🤖 Agent coordination infrastructure
│   ├── 📁 roles/                  📋 Agent role definitions
│   ├── 📁 config/                 ⚙️ Coordination configuration
│   ├── 📁 status/                 📊 Status logging entries
│   │   ├── ENTRY_TEMPLATE.md      📄 Status entry template (ground truth)
│   │   ├── archive/               📦 Old status entries
│   │   └── {timestamp}_*.md       📝 Active status logs
│   └── 📁 logs/                   📜 System logs
│
├── 📁 .claude/                    💬 Claude Code customization
│   ├── custom-instructions.md     👤 ATLAS persona definition
│   ├── settings.local.json        ⚙️ Local settings & hooks
│   └── skills/                    🔌 Deployed skills (symlinks)
│
├── 📁 skills/                     🛠️ Skill development directory
│   ├── 📁 coordination/           🔗 Multi-agent coordination
│   │   ├── health-check/          ✅ Infrastructure health validator
│   │   ├── status-inspector/      🔍 Log entry analyzer
│   │   ├── heartbeat-monitor/     💓 Real-time agent tracker
│   │   └── agent-dispatch/        🚀 Agent launcher
│   │
│   ├── 📁 testing/                🧪 Testing & simulation
│   │   ├── mock-sprint/           🎭 Fake sprint generator
│   │   ├── protocol-validator/    ✔️ Format compliance checker
│   │   ├── workflow-simulator/    🔄 Multi-agent scenarios
│   │   └── log-analyzer/          📊 Report generator
│   │
│   ├── 📁 utilities/              🔧 Helper utilities
│   │   ├── gitfun/                😄 GitHub repo analyzer
│   │   ├── python-env/            🐍 Python health checker
│   │   ├── sandbox-clean/         🧹 Cleanup utility
│   │   ├── git-snapshot/          📸 Git context viewer
│   │   └── directory-map/         🗺️ Structure mapper (this!)
│   │
│   ├── 📁 meta/                   🎯 Meta-tools
│   │   ├── skill-builder/         🏗️ Skill creation wizard
│   │   └── load-persona/          👤 Persona loader
│   │
│   └── 📁 .templates/             📋 Skill templates
│       └── skill-template.md      📄 Standard skill format
│
├── 📁 sandbox/                    🏖️ Isolated testing workspace
│   ├── 📁 test-sprints/           🧪 Sprint test outputs
│   ├── 📁 work/                   💼 Active work files
│   ├── 📁 temp/                   🗑️ Temporary scratch space
│   └── test-agent.py              🤖 Test agent utility
│
├── 📁 docs/                       📚 Documentation
│   ├── SKILLS_MASTER_PLAN.md      📋 Skill roadmap
│   ├── RESEARCH_INSIGHTS.md       🔬 Industry patterns
│   ├── AGENT_CUSTOMIZATION.md     👤 Persona guide
│   └── MCP_SETUP.md               🔌 MCP server config
│
├── 📁 launchers/                  🚀 Model-specific launchers
│   ├── claude-native.bat          🏠 Native Anthropic
│   ├── claude-minimax.bat         🌐 MiniMax M2.1
│   └── README.md                  📖 Launcher guide
│
├── 📁 configs/                    ⚙️ Configuration examples
│   └── minimax.env.example        🌐 MiniMax environment
│
├── 📄 README.md                   📖 Project overview
├── 📄 launch-claude.bat           🎯 Interactive launcher (Windows)
├── 📄 launch-claude.sh            🎯 Interactive launcher (Linux)
├── 📄 deploy-skills.bat           📦 Skill deployment (Windows)
├── 📄 deploy-skills.sh            📦 Skill deployment (Linux)
├── 📄 .gitignore                  🚫 Git ignore rules
└── 📄 requirements.txt            📦 Python dependencies (TBD)
```

---

## Summary Statistics

📊 **Repository Metrics**

- **Total Directories:** {count}
- **Total Files:** {count}
- **Skills Developed:** {count}/22
- **Documentation Files:** {count}
- **Configuration Files:** {count}
- **Scripts:** {count}

### By Category

| Category      | Files | Description                          |
|---------------|-------|--------------------------------------|
| Skills        | {n}   | Skill definition files               |
| Infrastructure| {n}   | Agent coordination system            |
| Documentation | {n}   | Guides and plans                     |
| Configuration | {n}   | Settings and environment             |
| Launchers     | {n}   | Startup scripts                      |
| Sandbox       | {n}   | Test files and utilities             |

---

## Key Files & Their Purpose

### Configuration & Setup
- **README.md** - Project overview and quick start guide
- **launch-claude.{bat,sh}** - Interactive model selector
- **.claude/settings.local.json** - Local settings, SessionStart hooks
- **.claude/custom-instructions.md** - ATLAS persona definition

### Agent Infrastructure
- **.agent/status/ENTRY_TEMPLATE.md** - Ground truth for status format
- **sandbox/test-agent.py** - Python test agent for validation
- **.agent/config/** - Coordination system configuration

### Skills System
- **skills/.templates/skill-template.md** - Template for new skills
- **skills/meta/skill-builder/** - Interactive skill creation wizard
- **deploy-skills.{bat,sh}** - Deploy skills to ~/.claude/skills/

### Documentation
- **docs/SKILLS_MASTER_PLAN.md** - Roadmap of 22 planned skills
- **docs/RESEARCH_INSIGHTS.md** - Industry coordination patterns
- **docs/AGENT_CUSTOMIZATION.md** - How to create custom personas

---

## Notable Patterns

✨ **Good Practices Observed**

1. **Clear Separation of Concerns**
   - Infrastructure (.agent/)
   - Skills (skills/)
   - Testing (sandbox/)
   - Documentation (docs/)

2. **Cross-Platform Support**
   - Both .bat and .sh scripts provided
   - Path handling works on Windows/Linux

3. **Template-Driven Development**
   - ENTRY_TEMPLATE.md for status entries
   - skill-template.md for skills
   - Consistent structure

4. **Meta-First Approach**
   - skill-builder created before other skills
   - Accelerates development

5. **Comprehensive Documentation**
   - Each skill self-documented
   - Master plan tracks progress
   - Research insights inform design

---

## Recommendations

### Organization
✅ Well-organized structure
✅ Clear naming conventions
✅ Appropriate use of directories

### Documentation
✅ Comprehensive README
✅ Skill-level documentation
✅ Master plan for tracking

### Areas for Enhancement
💡 Add requirements.txt for Python deps
💡 Consider adding tests/ directory for unit tests
💡 Add .editorconfig for consistent code style
💡 Consider adding CHANGELOG.md to track changes

---

## Quick Navigation

```bash
# View specific directory
ls .agent/status/               # Status entries
ls skills/coordination/         # Coordination skills
ls sandbox/                     # Test environment

# Find files by type
find . -name "*.md" -type f     # All markdown files
find skills/ -name "skill.md"   # All skill definitions
find docs/ -type f              # All documentation

# Search content
grep -r "ATLAS" .               # Find ATLAS references
grep -r "/skill-builder"        # Find skill-builder usage
```

---

**Generated in:** {ms}ms
```

---

## Examples

### Example 1: Full Repository Map
```
User: /directory-map

Scanning repository structure...

[Full tree output as shown in Step 4 above]

📊 Repository Metrics
- Total Directories: 18
- Total Files: 47
- Skills Developed: 14/22 (64%)
- Documentation Files: 8
- Configuration Files: 5

Structure map saved to: .agent/reports/directory-map-{timestamp}.md
```

### Example 2: Focused View
```
User: /show-structure --focus skills

Mapping skills/ directory...

# Skills Directory Structure

skills/
├── 📁 coordination/ (4 skills)
│   ├── ✅ health-check/
│   ├── ✅ status-inspector/
│   ├── ✅ heartbeat-monitor/
│   └── ✅ agent-dispatch/
│
├── 📁 testing/ (4 skills)
│   ├── ✅ mock-sprint/
│   ├── ✅ protocol-validator/
│   ├── ✅ workflow-simulator/
│   └── ✅ log-analyzer/
│
├── 📁 utilities/ (5 skills)
│   ├── ✅ gitfun/
│   ├── ✅ python-env/
│   ├── ✅ sandbox-clean/
│   ├── ✅ git-snapshot/
│   └── ✅ directory-map/
│
└── 📁 meta/ (2 skills)
    ├── ✅ skill-builder/
    └── ✅ load-persona/

**Progress:** 15/22 skills complete (68%)
**Remaining:** 7 advanced skills
```

### Example 3: With File Counts
```
User: /directory-map --stats

# Repository Structure (with statistics)

📊 **Overall Stats**
- Total size: 23.4 MB
- Total files: 89
- Largest directory: .agent/status/ (156 entries, 2.1 MB)
- Deepest nesting: 4 levels

📁 **By Directory**

.agent/ (15.2 MB, 178 files)
├── status/ (2.1 MB, 156 files) - Most active
├── logs/ (12.8 MB, 15 files) - Largest files
├── roles/ (45 KB, 4 files)
└── config/ (28 KB, 3 files)

skills/ (892 KB, 45 files)
├── coordination/ (215 KB, 12 files)
├── testing/ (380 KB, 16 files)
├── utilities/ (247 KB, 14 files)
└── meta/ (50 KB, 3 files)

sandbox/ (4.8 MB, 67 files)
├── test-sprints/ (3.2 MB, 45 files)
├── work/ (1.5 MB, 18 files)
└── temp/ (100 KB, 4 files)

docs/ (156 KB, 8 files)

📈 **Growth Areas**
- .agent/status/ growing (156 entries)
- sandbox/test-sprints/ accumulating test data
- Recommend: Run /sandbox-clean weekly
```

---

## Implementation Notes

- Use `os.walk()` or `pathlib.Path.rglob()` for traversal
- Respect `.gitignore` patterns
- Cache structure for 5 minutes (use `--refresh` to bypass)
- Support `--depth` parameter to limit recursion
- Export to JSON, Markdown, or ASCII tree format
- Consider generating Mermaid graph for visual representation

---

## Success Criteria

- ✅ Complete directory tree with annotations
- ✅ Meaningful descriptions for each component
- ✅ Quick statistics and metrics
- ✅ Respects .gitignore patterns
- ✅ Helpful navigation suggestions

---

**Breaking changes welcome. This is the laboratory.**
