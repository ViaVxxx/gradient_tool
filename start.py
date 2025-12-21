#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""启动脚本"""
import sys
import os

# 设置TCL/TK环境变量
python_prefix = sys.prefix
tcl_path = os.path.join(python_prefix, 'tcl', 'tcl8.6')
tk_path = os.path.join(python_prefix, 'tcl', 'tk8.6')

if os.path.exists(tcl_path):
    os.environ['TCL_LIBRARY'] = tcl_path
    print(f"TCL_LIBRARY: {tcl_path}")

if os.path.exists(tk_path):
    os.environ['TK_LIBRARY'] = tk_path
    print(f"TK_LIBRARY: {tk_path}")

print("Starting Gradient Tool...")

# 导入并启动
import tkinter as tk
from ui.main_window import MainWindow

root = tk.Tk()
app = MainWindow(root)

# 快捷键
root.bind('<Control-z>', lambda e: app.undo())
root.bind('<Control-y>', lambda e: app.redo())
root.bind('<Control-s>', lambda e: app.export_image('png'))
root.bind('<space>', lambda e: app.random_gradient())

root.mainloop()
