#!/bin/bash
# Interactive Claude Code launcher with model selection
# For SSH/WSL access

clear
echo "============================================"
echo "  CLAUDE CODE - MODEL SELECTOR"
echo "  claude-assist testbed"
echo "============================================"
echo ""
echo "Select your model backend:"
echo ""
echo "  1. Native (Anthropic Claude Sonnet 4.5)"
echo "  2. MiniMax M2.1"
echo "  3. Exit"
echo ""
echo "============================================"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting Claude Code with Native Anthropic models..."
        echo ""
        # Clear any model overrides
        unset ANTHROPIC_BASE_URL
        unset ANTHROPIC_MODEL
        unset ANTHROPIC_SMALL_FAST_MODEL
        unset ANTHROPIC_DEFAULT_SONNET_MODEL
        unset ANTHROPIC_DEFAULT_OPUS_MODEL
        unset ANTHROPIC_DEFAULT_HAIKU_MODEL
        claude
        ;;
    2)
        echo ""
        echo "Starting Claude Code with MiniMax M2.1..."
        echo ""

        # Check if API key is set
        if [ -z "$MINIMAX_API_KEY" ]; then
            echo "ERROR: MINIMAX_API_KEY not set!"
            echo ""
            echo "Please set your MiniMax API key:"
            echo "  export MINIMAX_API_KEY=your-key-here"
            echo ""
            echo "Or add to ~/.bashrc for permanence."
            exit 1
        fi

        # Configure MiniMax environment
        export ANTHROPIC_BASE_URL="https://api.minimax.io/anthropic"
        export ANTHROPIC_AUTH_TOKEN="$MINIMAX_API_KEY"
        export API_TIMEOUT_MS="3000000"
        export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"
        export ANTHROPIC_MODEL="MiniMax-M2.1"
        export ANTHROPIC_SMALL_FAST_MODEL="MiniMax-M2.1"
        export ANTHROPIC_DEFAULT_SONNET_MODEL="MiniMax-M2.1"
        export ANTHROPIC_DEFAULT_OPUS_MODEL="MiniMax-M2.1"
        export ANTHROPIC_DEFAULT_HAIKU_MODEL="MiniMax-M2.1"

        echo "Configuration:"
        echo "  API Key: ${MINIMAX_API_KEY:0:10}..."
        echo "  Model: MiniMax-M2.1"
        echo ""

        claude
        ;;
    3)
        echo ""
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please try again."
        exit 1
        ;;
esac
