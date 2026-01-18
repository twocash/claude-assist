@echo off
REM Launch Claude Code with Anthropic Opus 4 (high-performance native model)

echo ============================================
echo Launching Claude Code: OPUS MODE
echo Model: Claude Opus 4 (Anthropic)
echo ============================================
echo.

REM Clear any MiniMax overrides - use native Anthropic
set MINIMAX_API_KEY=
set ANTHROPIC_BASE_URL=
set ANTHROPIC_AUTH_TOKEN=
set ANTHROPIC_MODEL=
set ANTHROPIC_SMALL_FAST_MODEL=opus-4-2-20250501
set ANTHROPIC_DEFAULT_SONNET_MODEL=opus-4-2-20250501
set ANTHROPIC_DEFAULT_OPUS_MODEL=opus-4-2-20250501
set ANTHROPIC_DEFAULT_HAIKU_MODEL=opus-4-2-20250501

echo Configuration:
echo   Model: opus-4-2-20250501
echo   Mode: Native Anthropic API
echo.

REM Launch Claude Code
claude %*
