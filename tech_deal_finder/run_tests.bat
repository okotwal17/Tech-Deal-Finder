@echo off
echo Tech Deal Finder - Test Script
echo ============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3.6+ from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Error installing dependencies. Please run 'pip install -r requirements.txt' manually.
        pause
        exit /b 1
    )
)

echo.
echo Running tests...
echo.

REM Run the test script
python test_scraper.py

echo.
if %errorlevel% equ 0 (
    echo All tests passed!
) else (
    echo Some tests failed. Please check the output above for details.
)

pause
exit /b %errorlevel%
