# git-snapshot

**Category:** Utilities
**Version:** 1.0.0
**Status:** Active

---

## Identity

**Purpose:** Quick git context display - branch, status, commits, and repository health

**Triggers:**
- `/git-snapshot`
- `/git-status`
- "show git context"
- "git summary"

**Depends On:**
- Git repository (initialized)
- Git command-line access

---

## Instructions

When this skill is invoked, provide comprehensive git repository snapshot.

### Step 1: Repository Detection

Check if in a git repository:

```bash
git rev-parse --git-dir
```

If not a git repo, provide guidance on initializing.

### Step 2: Collect Git Information

Gather key repository data:

#### Branch Information
```bash
# Current branch
git branch --show-current

# All branches
git branch -a

# Remote branches
git branch -r
```

#### Repository Status
```bash
# Working tree status
git status --short --branch

# Untracked files
git ls-files --others --exclude-standard

# Modified files
git diff --name-only

# Staged files
git diff --cached --name-only
```

#### Recent Commit History
```bash
# Last 5 commits
git log -5 --oneline --decorate

# Recent commits with stats
git log -5 --stat --oneline

# Commits today
git log --since="midnight" --oneline
```

#### Remote Information
```bash
# Remote URLs
git remote -v

# Tracking branches
git branch -vv
```

#### Repository Statistics
```bash
# Total commits
git rev-list --count HEAD

# Contributors
git shortlog -sn --all

# File change frequency
git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -10
```

### Step 3: Analyze Repository Health

Check for common issues:

**Uncommitted Changes:**
- Modified files not staged
- Staged files not committed
- Untracked files

**Branch Status:**
- Ahead of remote (unpushed commits)
- Behind remote (need to pull)
- Diverged (conflicts possible)
- Detached HEAD state

**Merge Conflicts:**
- Files with conflicts
- Merge in progress

**Repository Size:**
- Large files (> 10 MB)
- .git directory size
- Total tracked files

### Step 4: Generate Snapshot Report

```markdown
# Git Repository Snapshot
**Generated:** {timestamp}
**Repository:** {repo_name}
**Location:** {repo_path}

---

## Current Branch

🌿 **Branch:** {branch_name}
📍 **Commit:** {short_hash} - {commit_message}
🔗 **Remote:** origin/{branch_name} ({status})

---

## Working Tree Status

### Modified Files ({count})
```
M  src/agent.py
M  docs/README.md
```

### Staged Files ({count})
```
A  skills/utilities/git-snapshot/skill.md
M  .gitignore
```

### Untracked Files ({count})
```
?? sandbox/temp/test-output.txt
?? .agent/status/mock-sprint-*.md
```

### Summary
- ✅ Clean working directory
  OR
- ⚠️ {count} uncommitted changes
- 📦 {count} files staged for commit
- 📄 {count} untracked files

---

## Recent Commits

```
abc1234 (HEAD -> main, origin/main) Add interactive model selector
def5678 Create coordination skills
9012345 Initial testbed setup
3456789 Add ATLAS persona
7890abc Configure SessionStart hook
```

**Today's Activity:** {count} commits

---

## Branch Tracking

| Branch  | Status        | Commits Behind | Commits Ahead | Last Commit     |
|---------|---------------|----------------|---------------|-----------------|
| main    | Up to date    | 0              | 0             | 2 hours ago     |
| feature | Ahead         | 0              | 3             | 30 minutes ago  |
| develop | Behind        | 5              | 0             | 1 day ago       |

---

## Remote Configuration

**Origin:**
- Fetch: https://github.com/user/claude-assist.git
- Push: https://github.com/user/claude-assist.git

**Upstream:** (not configured)

---

## Repository Statistics

📊 **Metrics**
- Total Commits: {count}
- Total Contributors: {count}
- Total Files Tracked: {count}
- Repository Size: {size} MB
- .git Directory: {size} MB

🏆 **Top Contributors**
1. {user} ({count} commits)
2. {user} ({count} commits)
3. {user} ({count} commits)

📝 **Most Modified Files**
1. README.md ({count} changes)
2. src/main.py ({count} changes)
3. docs/SKILLS_MASTER_PLAN.md ({count} changes)

---

## Health Check

### ✅ Healthy Indicators
- Clean working directory (or appropriate status)
- Branch tracking configured
- Remote configured correctly
- No merge conflicts
- No detached HEAD

### ⚠️ Warnings
{If any issues found, list them here}

### Recommendations
{Actionable suggestions based on status}

---

## Quick Actions

```bash
# Commit current changes
git add . && git commit -m "Your message"

# Push to remote
git push origin {branch}

# Pull from remote
git pull origin {branch}

# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout {branch_name}

# View diff
git diff

# View staged diff
git diff --cached
```
```

### Step 5: Provide Context-Aware Suggestions

Based on repository state, offer relevant actions:

**If uncommitted changes:**
```
💡 Suggestion: You have uncommitted changes. Consider:
   1. Review changes: git diff
   2. Stage changes: git add <file>
   3. Commit: git commit -m "message"
```

**If ahead of remote:**
```
💡 Suggestion: You have {count} unpushed commits:
   git push origin {branch}
```

**If behind remote:**
```
💡 Suggestion: Your branch is {count} commits behind:
   git pull origin {branch}
```

**If untracked files:**
```
💡 Suggestion: You have {count} untracked files. Consider:
   1. Add to .gitignore if temporary
   2. Stage and commit if needed: git add <file>
```

**If large files detected:**
```
⚠️ Warning: Large files detected (> 10 MB):
   - {file} ({size} MB)

   Consider using Git LFS for large files:
   git lfs track "{pattern}"
```

---

## Examples

### Example 1: Clean Repository
```
User: /git-snapshot

# Git Repository Snapshot
**Repository:** claude-assist
**Branch:** 🌿 main
**Status:** ✅ Clean

## Current State
- No uncommitted changes
- 0 commits ahead of origin/main
- 0 commits behind origin/main
- Last commit: 2 hours ago

## Recent Commits
abc1234 Add interactive model selector (2h ago)
def5678 Create coordination skills (5h ago)
9012345 Complete testing skills (1d ago)

## Quick Stats
- Total Commits: 127
- Repository Size: 15.3 MB
- Tracked Files: 89

✅ Repository is healthy and up to date.

No action needed.
```

### Example 2: Uncommitted Work
```
User: /git-status

# Git Repository Snapshot
**Repository:** claude-assist
**Branch:** 🌿 feature/utility-skills
**Status:** ⚠️ Uncommitted changes

## Working Tree Status

### Modified Files (3)
M  skills/utilities/git-snapshot/skill.md
M  skills/utilities/sandbox-clean/skill.md
M  docs/SKILLS_MASTER_PLAN.md

### Staged Files (2)
A  skills/utilities/python-env/skill.md
M  README.md

### Untracked Files (4)
?? sandbox/test-git.py
?? .agent/status/mock-*.md

## Branch Tracking
- 3 commits ahead of origin/feature/utility-skills
- 0 commits behind

## Recommendations

💡 **Suggested Actions:**

1. Review your changes:
   git diff

2. Stage remaining files:
   git add skills/utilities/git-snapshot/skill.md

3. Commit your work:
   git commit -m "Complete utility skills"

4. Push to remote:
   git push origin feature/utility-skills

5. Clean up untracked files:
   - mock-*.md can be removed (use /sandbox-clean)
   - test-git.py: add to .gitignore if temporary
```

### Example 3: Behind Remote
```
User: /git-snapshot

# Git Repository Snapshot
**Repository:** claude-assist
**Branch:** 🌿 main
**Status:** ⚠️ Out of sync

## Branch Tracking
- 0 commits ahead of origin/main
- 5 commits behind origin/main

## Missing Commits (from remote)
xyz9876 Add advanced skills (remote) - 1h ago
uvw5432 Update documentation (remote) - 3h ago
rst1098 Fix protocol validator (remote) - 5h ago
... (2 more)

## Recommendation

⚠️ **Your branch is behind remote.**

To sync with remote:
```bash
# Fetch and merge
git pull origin main

# Or fetch and rebase
git pull --rebase origin main
```

After pulling, run /git-snapshot again to verify.
```

---

## Implementation Notes

- Cache git output for 60 seconds to avoid repeated calls
- Support `--refresh` flag to bypass cache
- Colorize output (green = good, yellow = warning, red = error)
- Integrate with status logging (update git context in entries)
- Consider creating `.agent/git-context.json` for machine-readable format

---

## Success Criteria

- ✅ Comprehensive git status in one view
- ✅ Context-aware recommendations
- ✅ Quick access to common git operations
- ✅ Health indicators for repository state
- ✅ Performance optimized (fast execution)

---

**Breaking changes welcome. This is the laboratory.**
