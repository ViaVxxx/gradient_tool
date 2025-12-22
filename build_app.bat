@echo off
echo Building Gradient Tool...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

REM Install PyInstaller if needed
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Clean and build
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo Packaging application...
python -m PyInstaller gradient_tool.spec --clean

if errorlevel 1 (
    echo Build failed
    pause
    exit /b 1
)

echo Build complete: dist\GradientTool.exe
pause
