@echo off
REM Launch Claude Code with Anthropic Sonnet 4.5 (default native model)

echo ============================================
echo Launching Claude Code: SONNET MODE
echo Model: Claude Sonnet 4.5 (Anthropic)
echo ============================================
echo.

REM Clear any MiniMax overrides - use native Anthropic
set MINIMAX_API_KEY=
set ANTHROPIC_BASE_URL=
set ANTHROPIC_AUTH_TOKEN=
set ANTHROPIC_MODEL=
set ANTHROPIC_SMALL_FAST_MODEL=sonnet-4-5-20250514
set ANTHROPIC_DEFAULT_SONNET_MODEL=sonnet-4-5-20250514
set ANTHROPIC_DEFAULT_OPUS_MODEL=sonnet-4-5-20250514
set ANTHROPIC_DEFAULT_HAIKU_MODEL=sonnet-4-5-20250514

echo Configuration:
echo   Model: sonnet-4-5-20250514
echo   Mode: Native Anthropic API
echo.

REM Launch Claude Code
claude %*
