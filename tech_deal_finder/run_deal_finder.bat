@echo off
echo Tech Deal Finder
echo ===============
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
echo Ready to search for tech deals!
echo.

REM Get user input if no arguments provided
if "%~1"=="" (
    set /p product_query="What technology product are you looking for? "
    python deal_finder.py "%product_query%"
) else (
    python deal_finder.py %*
)

echo.
echo Search complete!
pause
