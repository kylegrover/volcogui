@echo off
REM VolcoGUI First Launch Script for Windows
REM This script will set up and run VolcoGUI for the first time

echo ==================================
echo   VolcoGUI - First Launch Setup
echo ==================================
echo.

REM Check if uv is installed
where uv >nul 2>nul
if %errorlevel% neq 0 (
    echo X Error: 'uv' is not installed
    echo.
    echo Please install uv first:
    echo   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo.
    pause
    exit /b 1
)

echo [OK] uv is installed
echo.

REM Sync dependencies
echo [*] Installing dependencies...
echo    This may take 2-3 minutes on first run...
echo.
uv sync

if %errorlevel% neq 0 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies installed successfully
echo.

REM Check if Volco is available
echo [*] Checking for Volco installation...
uv pip show volco >nul 2>nul
if %errorlevel% equ 0 (
    echo [OK] Volco is installed
    set VOLCO_INSTALLED=true
) else (
    echo [!] Volco is not installed
    echo    App will run in TEST MODE ^(creates test cube^)
    echo.
    echo    To install Volco:
    echo    uv pip install -e /path/to/volco
    echo.
    set VOLCO_INSTALLED=false
)

echo.
echo ==================================
echo   Launching VolcoGUI...
echo ==================================
echo.

REM Launch the application
uv run python -m volcogui.main

echo.
echo Application closed.
echo.

if "%VOLCO_INSTALLED%"=="false" (
    echo [i] Tip: Install Volco for full functionality:
    echo    uv pip install -e /path/to/volco
    echo.
)

pause
