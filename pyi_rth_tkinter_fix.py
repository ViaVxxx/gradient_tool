"""
PyInstaller Runtime Hook for Tkinter
在程序启动时设置 TCL/TK 环境变量，解决 Tcl data directory not found 问题
"""
import os
import sys

def setup_tcl_tk():
    """设置 TCL/TK 环境变量"""
    # 获取程序运行时的基础路径
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的路径
        base_path = sys._MEIPASS
        
        # PyInstaller 默认将 tcl/tk 数据放在 _tcl_data 和 _tk_data
        # 或者根据 spec 文件中的 datas 配置
        
        # 尝试查找可能的路径
        possible_tcl_paths = [
            os.path.join(base_path, '_tcl_data'),
            os.path.join(base_path, 'tcl'),
            os.path.join(base_path, 'lib', 'tcl8.6'),
        ]
        
        possible_tk_paths = [
            os.path.join(base_path, '_tk_data'),
            os.path.join(base_path, 'tk'),
            os.path.join(base_path, 'lib', 'tk8.6'),
        ]
        
        tcl_path = None
        for p in possible_tcl_paths:
            if os.path.exists(p):
                tcl_path = p
                break
                
        tk_path = None
        for p in possible_tk_paths:
            if os.path.exists(p):
                tk_path = p
                break
                
        if tcl_path:
            os.environ['TCL_LIBRARY'] = tcl_path
            # print(f"Set TCL_LIBRARY to {tcl_path}")
            
        if tk_path:
            os.environ['TK_LIBRARY'] = tk_path
            # print(f"Set TK_LIBRARY to {tk_path}")

# 执行设置
setup_tcl_tk()
