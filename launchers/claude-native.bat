@echo off
REM Launch Claude Code with native Anthropic models (default)

echo ============================================
echo Launching Claude Code: NATIVE MODE
echo Model: Claude Sonnet 4.5 (Anthropic)
echo ============================================
echo.

REM Clear any MiniMax or other overrides
set ANTHROPIC_BASE_URL=
set ANTHROPIC_MODEL=
set ANTHROPIC_SMALL_FAST_MODEL=
set ANTHROPIC_DEFAULT_SONNET_MODEL=
set ANTHROPIC_DEFAULT_OPUS_MODEL=
set ANTHROPIC_DEFAULT_HAIKU_MODEL=

REM Launch Claude Code
claude
