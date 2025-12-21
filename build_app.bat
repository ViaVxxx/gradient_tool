@echo off
REM ============================================
REM Gradient Tool - Windows 打包脚本
REM ============================================
REM 使用PyInstaller将应用打包为独立可执行文件
REM ============================================

chcp 65001 >nul
echo ========================================
echo Gradient Tool - 应用打包工具
echo ========================================
echo.

REM 检查Python环境
echo [1/6] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.11+
    pause
    exit /b 1
)
python --version
echo.

REM 运行环境检查脚本
echo [2/6] 检查Tkinter环境...
if exist "check_env.py" (
    python check_env.py
    if errorlevel 1 (
        echo [警告] 环境检查发现问题，但尝试继续...
    )
)
echo.

REM 检查并安装PyInstaller
echo [3/6] 检查PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller未安装，正在安装...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller安装失败
        pause
        exit /b 1
    )
) else (
    echo PyInstaller已安装
)
echo.

REM 清理旧的构建文件
echo [4/6] 清理旧的构建文件...
if exist "build" (
    echo 删除 build 目录...
    rmdir /s /q build
)
if exist "dist" (
    echo 删除 dist 目录...
    rmdir /s /q dist
)
echo 清理完成
echo.

REM 设置 TCL/TK 环境变量
echo 正在配置 TCL/TK 环境变量...
for /f "delims=" %%i in ('python -c "import sys, os; print(os.path.join(sys.base_prefix, 'tcl', 'tcl8.6'))"') do set TCL_LIBRARY=%%i
for /f "delims=" %%i in ('python -c "import sys, os; print(os.path.join(sys.base_prefix, 'tcl', 'tk8.6'))"') do set TK_LIBRARY=%%i
echo TCL_LIBRARY=%TCL_LIBRARY%
echo TK_LIBRARY=%TK_LIBRARY%
echo.

REM 开始打包
echo [5/6] 开始打包应用...
echo 这可能需要几分钟，请耐心等待...
echo.
REM 使用 python -m PyInstaller 确保使用相同的Python环境
python -m PyInstaller gradient_tool.spec --clean

if errorlevel 1 (
    echo.
    echo [错误] 打包失败，请检查错误信息
    pause
    exit /b 1
)
echo.

REM 打包完成
echo [6/6] 打包完成！
echo.
echo ========================================
echo 打包成功！
echo ========================================
echo.
echo 可执行文件位置：
echo   dist\GradientTool.exe
echo.
echo 文件大小：
for %%A in ("dist\GradientTool.exe") do echo   %%~zA 字节 (约 %%~zAKB)
echo.
echo 您可以将 GradientTool.exe 复制到任何位置运行
echo 无需安装Python或其他依赖
echo.
echo ========================================

REM 询问是否测试运行
echo.
set /p test="是否测试运行打包的程序？(Y/N): "
if /i "%test%"=="Y" (
    echo.
    echo 正在启动 GradientTool.exe...
    start "" "dist\GradientTool.exe"
)

echo.
pause
