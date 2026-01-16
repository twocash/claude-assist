@echo off
REM Launch Claude Code with MiniMax M2.1 model

echo ============================================
echo Launching Claude Code: MINIMAX MODE
echo Model: MiniMax-M2.1
echo Base URL: https://api.minimax.io/anthropic
echo ============================================
echo.

REM Check if API key is set
if "%MINIMAX_API_KEY%"=="" (
    echo ERROR: MINIMAX_API_KEY not set!
    echo.
    echo Please set your MiniMax API key:
    echo   set MINIMAX_API_KEY=your-key-here
    echo.
    echo Or add to your environment variables permanently.
    pause
    exit /b 1
)

REM Configure MiniMax environment
set ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic
set ANTHROPIC_AUTH_TOKEN=%MINIMAX_API_KEY%
set API_TIMEOUT_MS=3000000
set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
set ANTHROPIC_MODEL=MiniMax-M2.1
set ANTHROPIC_SMALL_FAST_MODEL=MiniMax-M2.1
set ANTHROPIC_DEFAULT_SONNET_MODEL=MiniMax-M2.1
set ANTHROPIC_DEFAULT_OPUS_MODEL=MiniMax-M2.1
set ANTHROPIC_DEFAULT_HAIKU_MODEL=MiniMax-M2.1

echo Configuration:
echo   API Key: %MINIMAX_API_KEY:~0,10%...
echo   Model: MiniMax-M2.1
echo.

REM Launch Claude Code
claude
