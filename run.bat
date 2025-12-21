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

REM 设置TCL环境变量（根据你的Python安装路径）
set TCL_LIBRARY=F:\Python\Python 311\tcl\tcl8.6
set TK_LIBRARY=F:\Python\Python 311\tcl\tk8.6

REM 如果上面的路径不对，尝试标准路径
if not exist "%TCL_LIBRARY%" (
    echo 自动检测TCL路径...
    for /f "delims=" %%i in ('python -c "import sys; print(sys.prefix)"') do set PYTHON_PREFIX=%%i
    set TCL_LIBRARY=%PYTHON_PREFIX%\tcl\tcl8.6
    set TK_LIBRARY=%PYTHON_PREFIX%\tcl\tk8.6
)

echo.
echo TCL_LIBRARY: %TCL_LIBRARY%
echo TK_LIBRARY: %TK_LIBRARY%
echo.

REM 启动应用
python main.py

pause
