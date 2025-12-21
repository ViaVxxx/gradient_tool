# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller配置文件 - Gradient Tool
用于打包渐变色图像生成工具为独立可执行文件
"""

import sys
import os

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL._tkinter_finder',  # Pillow的tkinter集成
        'tkinter',
        'tkinter.ttk',
        'tkinter.colorchooser',
        'tkinter.filedialog',
        'tkinter.messagebox',
        '_tkinter',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['pyi_rth_tkinter_fix.py'], # 添加自定义运行时 hook
    excludes=[
        'matplotlib',  # 排除不需要的大型库
        'numpy',
        'pandas',
        'scipy',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GradientTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # 使用UPX压缩（如果可用）
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 临时开启控制台以便查看错误
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有图标：icon='assets/icon.ico'
)

# macOS应用包配置（仅在macOS上生效）
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='Gradient Tool.app',
        icon=None,  # 如果有图标：icon='assets/icon.icns'
        bundle_identifier='com.gradienttool.app',
        info_plist={
            'CFBundleName': 'Gradient Tool',
            'CFBundleDisplayName': 'Gradient Tool',
            'CFBundleVersion': '1.1.0',
            'CFBundleShortVersionString': '1.1',
            'NSHighResolutionCapable': 'True',
        },
    )
