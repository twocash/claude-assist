#!/bin/bash
# Deploy skills from claude-assist to global ~/.claude/skills/

SKILLS_DIR="$HOME/.claude/skills"
SOURCE_DIR="$(dirname "$0")/skills"

echo "Deploying skills from claude-assist to $SKILLS_DIR"
echo "=============================================="

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Function to deploy a skill
deploy_skill() {
    category=$1
    skill_name=$2

    if [ -d "$SOURCE_DIR/$category/$skill_name" ]; then
        echo "✓ Deploying $skill_name ($category)"
        cp -r "$SOURCE_DIR/$category/$skill_name" "$SKILLS_DIR/"
    else
        echo "✗ Skill not found: $category/$skill_name"
    fi
}

# Deploy meta skills
echo ""
echo "Meta Skills:"
deploy_skill "meta" "skill-builder"
deploy_skill "meta" "load-persona"

# Deploy coordination skills
echo ""
echo "Coordination Skills:"
deploy_skill "coordination" "agent-dispatch"

# Deploy utility skills
echo ""
echo "Utility Skills:"
deploy_skill "utilities" "gitfun"

# Add more as we build them
# deploy_skill "coordination" "health-check"
# deploy_skill "coordination" "status-inspector"
# etc.

echo ""
echo "=============================================="
echo "Deployment complete!"
echo ""
echo "Available skills:"
echo "  /skill-builder - Create new skills"
echo "  /load-persona - Load ATLAS or other personas"
echo "  /agent-dispatch - Launch test agents"
echo "  /gitfun - Analyze GitHub repo installation difficulty"
echo ""
echo "Test with: /gitfun https://github.com/some/repo"
