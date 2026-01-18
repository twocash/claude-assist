@echo off
cls
echo ============================================
echo   CLAUDE CODE - ATLAS WORKSPACE
echo   claude-assist
echo ============================================
echo.
echo Select model:
echo.
echo   1. Sonnet 4.5 (default)
echo   2. Opus 4
echo   3. Exit
echo.
set /p choice="Choice (1-3): "

if "%choice%"=="1" goto sonnet
if "%choice%"=="2" goto opus
if "%choice%"=="3" exit /b 0
echo Invalid choice.
pause
goto :eof

:sonnet
call launchers\claude-sonnet.bat
goto :eof

:opus
call launchers\claude-opus.bat
goto :eof
