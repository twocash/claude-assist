@echo off
REM Deploy skills from claude-assist to global ~/.claude/skills/

echo Deploying skills to %USERPROFILE%\.claude\skills
echo ==============================================

REM Create skills directory if it doesn't exist
if not exist "%USERPROFILE%\.claude\skills" mkdir "%USERPROFILE%\.claude\skills"

echo.
echo Meta Skills:
xcopy /E /I /Y "skills\meta\skill-builder" "%USERPROFILE%\.claude\skills\skill-builder"
xcopy /E /I /Y "skills\meta\load-persona" "%USERPROFILE%\.claude\skills\load-persona"

echo.
echo Coordination Skills:
xcopy /E /I /Y "skills\coordination\agent-dispatch" "%USERPROFILE%\.claude\skills\agent-dispatch"

echo.
echo Utility Skills:
xcopy /E /I /Y "skills\utilities\gitfun" "%USERPROFILE%\.claude\skills\gitfun"

echo.
echo ==============================================
echo Deployment complete!
echo.
echo Available skills:
echo   /skill-builder - Create new skills
echo   /load-persona - Load ATLAS or other personas
echo   /agent-dispatch - Launch test agents
echo   /gitfun - Analyze GitHub repo installation difficulty
echo.
echo Test with: /gitfun https://github.com/some/repo
echo.
pause
