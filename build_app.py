#!/usr/bin/env python3
"""
Gradient Tool - 跨平台打包脚本
支持 Windows、Linux 和 macOS
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50 + "\n")


def print_step(step, total, text):
    """打印步骤信息"""
    print(f"[{step}/{total}] {text}")


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("[错误] 需要Python 3.11或更高版本")
        print(f"当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"Python版本: {version.major}.{version.minor}.{version.micro} ✓")
    return True


def install_pyinstaller():
    """安装PyInstaller"""
    try:
        import PyInstaller
        print(f"PyInstaller已安装 (版本: {PyInstaller.__version__}) ✓")
        return True
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("PyInstaller安装成功 ✓")
            return True
        except subprocess.CalledProcessError:
            print("[错误] PyInstaller安装失败")
            return False


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ["build", "dist"]
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"删除 {dir_name}/ 目录...")
            shutil.rmtree(dir_path)
    print("清理完成 ✓")


def build_app():
    """构建应用"""
    print("开始打包应用...")
    print("这可能需要几分钟，请耐心等待...\n")

    try:
        # 使用spec文件打包
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "gradient_tool.spec",
            "--clean"
        ])
        return True
    except subprocess.CalledProcessError:
        print("\n[错误] 打包失败")
        return False


def get_executable_name():
    """获取可执行文件名"""
    if sys.platform == "win32":
        return "GradientTool.exe"
    elif sys.platform == "darwin":
        return "Gradient Tool.app"
    else:
        return "GradientTool"


def get_file_size(file_path):
    """获取文件大小（人类可读格式）"""
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def show_success_info():
    """显示成功信息"""
    exe_name = get_executable_name()
    exe_path = Path("dist") / exe_name

    print_header("打包成功！")

    print("📦 可执行文件信息：")
    print(f"   位置: {exe_path}")

    if exe_path.exists():
        if sys.platform == "darwin" and exe_path.is_dir():
            # macOS .app是一个目录
            print(f"   类型: macOS应用包")
        else:
            size = get_file_size(exe_path)
            print(f"   大小: {size}")

    print("\n✨ 使用说明：")
    if sys.platform == "win32":
        print("   • 双击 GradientTool.exe 运行")
        print("   • 可复制到任何位置，无需安装")
    elif sys.platform == "darwin":
        print("   • 双击 Gradient Tool.app 运行")
        print("   • 可拖动到 应用程序 文件夹")
    else:
        print("   • 在终端运行: ./dist/GradientTool")
        print("   • 或赋予执行权限后双击运行")

    print("\n📚 分发说明：")
    print("   • 无需Python环境")
    print("   • 无需安装额外依赖")
    print("   • 可直接在同平台其他电脑运行")

    print("\n" + "=" * 50)


def main():
    """主函数"""
    print_header("Gradient Tool - 应用打包工具")

    # 步骤1：检查Python版本
    print_step(1, 5, "检查Python环境...")
    if not check_python_version():
        return 1
    print()

    # 步骤2：检查并安装PyInstaller
    print_step(2, 5, "检查PyInstaller...")
    if not install_pyinstaller():
        return 1
    print()

    # 步骤3：清理旧的构建文件
    print_step(3, 5, "清理旧的构建文件...")
    clean_build_dirs()
    print()

    # 步骤4：开始打包
    print_step(4, 5, "打包应用...")
    if not build_app():
        return 1
    print()

    # 步骤5：显示成功信息
    print_step(5, 5, "完成！")
    show_success_info()

    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n[取消] 用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n[错误] 发生异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
