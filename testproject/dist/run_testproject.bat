@echo off
echo JVAV Brainwave Application: testproject
echo ========================================
echo Starting brainwave interface...
echo.
echo Running testproject.jvav...
echo.
python "%~dp0JvavDK25.exe" -f "%~dp0testproject.jvavpkg"
echo.
echo Application finished.
pause
