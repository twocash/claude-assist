@echo off
cls
echo ============================================
echo   CLAUDE CODE - MODEL SELECTOR
echo   claude-assist testbed
echo ============================================
echo.
echo Select your model backend:
echo.
echo   1. Native (Anthropic Claude Sonnet 4.5)
echo   2. MiniMax M2.1
echo   3. Exit
echo.
echo ============================================
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto native
if "%choice%"=="2" goto minimax
if "%choice%"=="3" goto exit
echo Invalid choice. Please try again.
pause
goto :eof

:native
echo.
echo Starting Claude Code with Native Anthropic models...
echo.
call launchers\claude-native.bat
goto :eof

:minimax
echo.
echo Starting Claude Code with MiniMax M2.1...
echo.
call launchers\claude-minimax.bat
goto :eof

:exit
echo.
echo Exiting...
exit /b 0
