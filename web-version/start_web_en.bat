@echo off
REM ============================================
REM Gradient Tool - Web Version Launcher
REM ============================================

echo ========================================
echo Gradient Tool - Web Version
echo ========================================
echo.

REM Check Node.js
echo [1/4] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found!
    echo Please install Node.js: https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo Node.js OK
echo.

REM Check frontend dependencies
echo [2/4] Checking frontend dependencies...
if not exist "web\node_modules" (
    echo Installing frontend dependencies...
    cd web
    call npm install
    cd ..
)
echo Frontend dependencies OK
echo.

REM Check Python dependencies
echo [3/4] Checking Python dependencies...
python -c "import webview" >nul 2>&1
if errorlevel 1 (
    echo Installing PyWebView...
    pip install pywebview
)
echo Python dependencies OK
echo.

REM Launch application
echo [4/4] Launching application...
echo.
echo ========================================
echo Launch Mode:
echo 1 - Development (Hot Reload)
echo 2 - Production
echo ========================================
echo.
set /p mode="Select (1/2): "

if "%mode%"=="1" (
    echo.
    echo Starting Development Mode...
    echo.
    echo Terminal 1: Frontend Dev Server...
    start "Frontend Dev Server" cmd /k "cd web && npm run dev"

    timeout /t 5 >nul

    echo Terminal 2: Python Backend...
    python main_web.py
) else (
    echo.
    echo Building frontend...
    cd web
    call npm run build
    cd ..

    echo.
    echo Starting Production Mode...
    python main_web.py
)

pause
