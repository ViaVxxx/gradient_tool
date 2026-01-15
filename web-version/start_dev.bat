@echo off
chcp 65001 >nul
title Gradient Tool - 开发模式启动器

echo.
echo ========================================
echo    Gradient Tool - 开发模式启动器
echo ========================================
echo.

cd /d "%~dp0"
python start_dev_auto.py

pause