#!/usr/bin/env python3
"""
Gradient Tool - Web 版本启动脚本
自动检查依赖并启动应用
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

    web_dir = Path('web')
    node_modules = web_dir / 'node_modules'

    if not node_modules.exists():
        print("正在安装前端依赖...")
        print("这可能需要几分钟，请耐心等待...\n")

        try:
            subprocess.run(['npm', 'install'],
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
    print("\n启动开发模式...")
    print("\n终端 1: 启动前端开发服务器")
    print("终端 2: 启动 Python 后端\n")

    # 启动前端开发服务器（新窗口）
    if sys.platform == 'win32':
        subprocess.Popen(['start', 'cmd', '/k', 'cd web && npm run dev'],
                        shell=True)
    else:
        # macOS/Linux
        subprocess.Popen(['npm', 'run', 'dev'],
                        cwd='web',
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    # 等待开发服务器启动
    print("等待前端开发服务器启动...")
    time.sleep(5)

    # 启动 Python 后端
    print("\n启动 Python 后端...")
    subprocess.run([sys.executable, 'main_web.py'])


def start_prod_mode():
    """启动生产模式"""
    print("\n启动生产模式...")

    # 构建前端
    print("\n正在构建前端...")
    try:
        subprocess.run(['npm', 'run', 'build'],
                      cwd='web',
                      check=True)
        print("✓ 前端构建完成")
    except subprocess.CalledProcessError:
        print("✗ 前端构建失败")
        return False

    # 启动应用
    print("\n启动应用...")
    subprocess.run([sys.executable, 'main_web.py'])


def main():
    """主函数"""
    print_header("Gradient Tool - Web 版本启动器")

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

    # 选择启动模式
    print("\n[4/4] 选择启动模式")
    print_header("启动模式")
    print("1 - 开发模式 (热重载，推荐开发时使用)")
    print("2 - 生产模式 (构建后运行，推荐测试/使用)")
    print("=" * 50)

    choice = input("\n请选择 (1/2，默认 1): ").strip() or "1"

    if choice == "1":
        start_dev_mode()
    elif choice == "2":
        start_prod_mode()
    else:
        print("无效的选择")
        return 1

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
