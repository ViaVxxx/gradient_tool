@echo off
REM Gradient Tool 启动脚本
REM 设置TCL/TK环境变量

echo 正在启动 Gradient Tool...

REM 检查Python版本
python --version

REM 检查Pillow是否安装
python -c "import PIL; print('Pillow version:', PIL.__version__)" 2>nul
if errorlevel 1 (
    echo.
    echo 检测到Pillow未安装，正在安装...
    pip install Pillow
)


REM 启动应用
python main.py

pause
