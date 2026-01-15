#!/usr/bin/env python3
"""
Gradient Tool - Web 版本自动启动脚本（开发模式）
自动检查依赖并启动开发模式，无需用户交互
"""
import os
import sys
import subprocess
import time
from pathlib import Path


def print_header(text):
    """打印标题"""
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50 + "\n")


def check_nodejs():
    """检查 Node.js 是否安装"""
    print("[1/4] 检查 Node.js...")
    try:
        result = subprocess.run(['node', '--version'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass

    print("✗ 未找到 Node.js")
    print("\n请先安装 Node.js:")
    print("  https://nodejs.org/")
    return False


def check_frontend_deps():
    """检查并安装前端依赖"""
    print("\n[2/4] 检查前端依赖...")

    # 获取当前脚本所在目录
    script_dir = Path(__file__).parent
    web_dir = script_dir / 'web'
    node_modules = web_dir / 'node_modules'

    if not node_modules.exists():
        print("正在安装前端依赖...")
        print("这可能需要几分钟，请耐心等待...\n")

        try:
            # Windows 上使用 npm.cmd
            npm_cmd = 'npm.cmd' if os.name == 'nt' else 'npm'
            subprocess.run([npm_cmd, 'install'],
                         cwd=str(web_dir),
                         check=True)
            print("\n✓ 前端依赖安装完成")
            return True
        except subprocess.CalledProcessError:
            print("\n✗ 前端依赖安装失败")
            return False
    else:
        print("✓ 前端依赖已就绪")
        return True


def check_python_deps():
    """检查并安装 Python 依赖"""
    print("\n[3/4] 检查 Python 依赖...")

    try:
        import webview
        print(f"✓ PyWebView 已安装")
        return True
    except ImportError:
        print("正在安装 PyWebView...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pywebview'],
                         check=True)
            print("✓ PyWebView 安装完成")
            return True
        except subprocess.CalledProcessError:
            print("✗ PyWebView 安装失败")
            return False


def start_dev_mode():
    """启动开发模式"""
    print("\n[4/4] 启动开发模式...")
    print("\n正在启动前端开发服务器和后端...")

    # 获取当前脚本所在目录
    script_dir = Path(__file__).parent
    web_dir = script_dir / 'web'

    # 启动前端开发服务器（新窗口）
    if sys.platform == 'win32':
        print("✓ 前端开发服务器将在新窗口中启动")
        subprocess.Popen(['start', 'cmd', '/k', f'cd /d {web_dir} && npm.cmd run dev'],
                        shell=True)
    else:
        # macOS/Linux
        print("✓ 启动前端开发服务器...")
        subprocess.Popen(['npm', 'run', 'dev'],
                        cwd=str(web_dir),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    # 等待开发服务器启动
    print("⏳ 等待前端开发服务器启动...")
    time.sleep(5)

    # 启动 Python 后端
    print("✓ 启动 Python 后端...")
    subprocess.run([sys.executable, 'main_web.py'])


def main():
    """主函数"""
    print_header("Gradient Tool - 自动启动开发模式")

    # 检查 Node.js
    if not check_nodejs():
        input("\n按任意键退出...")
        return 1

    # 检查前端依赖
    if not check_frontend_deps():
        input("\n按任意键退出...")
        return 1

    # 检查 Python 依赖
    if not check_python_deps():
        input("\n按任意键退出...")
        return 1

    # 启动开发模式
    start_dev_mode()

    return 0


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        input("\n按任意键退出...")
        sys.exit(1)