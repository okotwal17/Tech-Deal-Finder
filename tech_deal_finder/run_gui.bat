@echo off
echo Tech Deal Finder GUI
echo ===================
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
echo Launching Tech Deal Finder GUI...
echo.

REM Run the GUI
python deal_finder_gui.py

exit /b 0
