@echo off
cd /d %~dp0
echo ============================================================
echo   RuoYi Interface Automation Test Runner
echo   Make sure the backend is running at http://localhost:8080
echo ============================================================
.venv\Scripts\python.exe -m pytest
echo.
echo Finished.
echo HTML report: %~dp0report\report.html  (open in browser)
pause
