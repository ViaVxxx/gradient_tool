# 应用打包指南

本指南说明如何将 Gradient Tool 打包为独立的可执行应用程序，无需Python环境即可运行。

## 📋 目录

- [快速开始](#快速开始)
- [详细步骤](#详细步骤)
- [打包选项](#打包选项)
- [常见问题](#常见问题)
- [分发说明](#分发说明)

## 🚀 快速开始

### Windows 用户

```bash
# 方式1：使用批处理脚本（推荐）
build_app.bat

# 方式2：使用Python脚本
python build_app.py
```

### Linux/macOS 用户

```bash
# 赋予执行权限
chmod +x build_app.py

# 运行打包脚本
./build_app.py
# 或
python build_app.py
```

打包完成后，可执行文件位于 `dist/` 目录。

## 📝 详细步骤

### 1. 准备环境

**必需条件：**
- Python 3.11-3.13
- pip 包管理器
- 已安装项目依赖（Pillow）

**验证环境：**
```bash
python --version  # 应显示 Python 3.11.x 或更高
pip list | grep -i pillow  # 应显示 Pillow 版本
```

### 2. 安装打包工具

打包脚本会自动安装 PyInstaller，也可以手动安装：

```bash
pip install pyinstaller
```

### 3. 运行打包脚本

#### Windows

```bash
build_app.bat
```

脚本会执行以下步骤：
1. ✓ 检查Python环境
2. ✓ 检查/安装 PyInstaller
3. ✓ 清理旧的构建文件
4. ✓ 使用 PyInstaller 打包应用
5. ✓ 显示打包结果

#### Linux/macOS

```bash
python build_app.py
```

### 4. 查看结果

打包完成后，文件结构：

```
gradient_tool/
├── dist/
│   └── GradientTool.exe        # Windows可执行文件
│       GradientTool            # Linux可执行文件
│       Gradient Tool.app/      # macOS应用包
├── build/                      # 临时构建文件（可删除）
└── gradient_tool.spec          # PyInstaller配置
```

## ⚙️ 打包选项

### 修改应用图标

1. 准备图标文件：
   - Windows: `.ico` 格式（推荐 256x256）
   - macOS: `.icns` 格式
   - Linux: `.png` 格式（推荐 512x512）

2. 将图标放入项目目录（如 `assets/icon.ico`）

3. 编辑 `gradient_tool.spec`：
   ```python
   exe = EXE(
       ...
       icon='assets/icon.ico',  # 取消注释并设置路径
   )
   ```

4. 重新打包

### 调整打包大小

**减小体积：**

1. 在 `gradient_tool.spec` 中排除不需要的模块：
   ```python
   excludes=[
       'matplotlib',
       'numpy',
       'pandas',
       'scipy',
       'pytest',
       'unittest',  # 添加更多要排除的模块
   ]
   ```

2. 启用 UPX 压缩（默认已启用）：
   ```python
   upx=True,
   ```

**包含额外资源：**

如果需要打包额外文件（配置、图片等）：
```python
datas=[
    ('config.json', '.'),           # 配置文件
    ('assets/', 'assets'),          # 资源目录
],
```

### 显示/隐藏控制台

编辑 `gradient_tool.spec`：

```python
exe = EXE(
    ...
    console=False,  # False=不显示控制台（GUI应用）
                    # True=显示控制台（调试用）
)
```

## ❓ 常见问题

### 1. 打包后程序无法启动

**症状：** 双击可执行文件无反应或闪退

**解决方法：**
```bash
# 方法1：在终端运行查看错误信息
./dist/GradientTool.exe  # Windows
./dist/GradientTool      # Linux

# 方法2：启用控制台模式
# 在 gradient_tool.spec 中设置 console=True
```

### 2. 找不到 Tkinter/TCL

**症状：** 错误信息显示 "No module named '_tkinter'" 或 "Can't find tcl"

**解决方法：**
```bash
# 确保Python安装包含Tkinter
# Windows: 重新安装Python，勾选 "tcl/tk and IDLE"
# Linux: sudo apt-get install python3-tk
# macOS: Tkinter 默认包含
```

### 2a. 多 Python 版本导致的 Tkinter 冲突 ⭐

**症状：**
- 打包时警告 "tkinter installation is broken"
- 运行时错误 "Tcl data directory not found"
- 错误信息包含 `_MEI.../_tcl_data` 或 `_tk_data`

**根本原因：**
系统安装了多个 Python 版本，环境变量 `TCL_LIBRARY` 和 `TK_LIBRARY` 指向错误的版本。

**解决方法（推荐）：**

1. **清理系统环境变量：**
   ```
   - 打开"编辑系统环境变量"（Windows搜索）
   - 在"系统变量"中查找并删除：
     • TCL_LIBRARY
     • TK_LIBRARY
   - 重启命令行/PowerShell
   ```

2. **使用 onedir 模式打包（更稳定）：**
   ```bash
   pyinstaller gradient_tool_onedir.spec --clean
   ```

   onedir 模式对 Tkinter 支持更好，避免单文件模式的路径问题。

3. **验证修复：**
   ```bash
   # 测试 Tkinter 是否正常
   python -c "import tkinter; print('Tkinter OK')"

   # 重新打包
   python build_app.py
   ```

**说明：** 现代 Python 能自动找到正确的 TCL/TK 路径，手动设置环境变量在多版本环境下反而会造成冲突。

### 3. Pillow相关错误

**症状：** 错误信息显示 PIL 或图像处理相关问题

**解决方法：**
```bash
# 重新安装 Pillow
pip uninstall Pillow
pip install Pillow

# 然后重新打包
```

### 4. 打包文件太大

**症状：** 生成的 .exe 文件超过 50MB

**解决方法：**
- 检查是否意外包含了大型库（numpy, pandas等）
- 在 `gradient_tool.spec` 的 `excludes` 列表中添加不需要的模块
- 确保 UPX 压缩已启用
- 使用 `--onefile` 可能增大体积，考虑使用 `--onedir`

### 5. Windows Defender 报警

**症状：** Windows 将打包的程序标记为可疑

**原因：** PyInstaller 打包的程序因为不常见可能被误报

**解决方法：**
- 添加为 Windows Defender 排除项
- 对可执行文件进行代码签名（需要证书）
- 提交样本到 Microsoft 进行白名单审核

### 6. macOS "无法打开，因为无法验证开发者"

**症状：** macOS 阻止运行未签名的应用

**解决方法：**
```bash
# 方法1：右键点击应用，选择"打开"
# 方法2：在终端运行
xattr -cr "dist/Gradient Tool.app"

# 方法3：对应用进行签名（需要 Apple Developer ID）
codesign --force --deep --sign - "dist/Gradient Tool.app"
```

### 7. 运行时报错 "Tk data directory not found"

**症状：**
```
Failed to execute script 'pyi_rth_tkinter' due to unhandled exception: Tk data directory "...\AppData\Local\Temp\_MEI...\_tk_data" not found.
```

**原因：**
PyInstaller 在打包时未能正确包含 Tkinter 的数据文件，或者打包配置中的路径映射不正确。

**解决方法：**
修改 `gradient_tool.spec` 文件，确保 `datas` 列表正确映射了 TCL 和 TK 的库路径。

```python
# 确保 datas 包含以下映射
datas=[
    (tcl_lib, '_tcl_data'),
    (tk_lib, '_tk_data'),
],
```
注意：旧版本的 PyInstaller 可能使用 `tcl` 和 `tk` 作为目标目录名，但较新版本的 hook 期望 `_tcl_data` 和 `_tk_data`。

## 📦 分发说明

### Windows

**单文件分发：**
- 直接分发 `dist/GradientTool.exe`
- 用户双击即可运行
- 大小：约 20-30MB

**安装程序（可选）：**
使用 Inno Setup 或 NSIS 创建安装程序：
```bash
# 使用 Inno Setup
pip install pyinstaller[encryption]
# 参考 Inno Setup 文档创建安装脚本
```

### Linux

**AppImage 格式（推荐）：**
```bash
# 转换为 AppImage（跨发行版兼容）
pip install appimage-builder
# 参考 AppImage 文档
```

**直接分发：**
```bash
# 打包为 tar.gz
tar -czf GradientTool-linux-x64.tar.gz -C dist/ GradientTool
```

### macOS

**DMG 镜像（推荐）：**
```bash
# 创建 DMG 安装镜像
hdiutil create -volname "Gradient Tool" -srcfolder "dist/Gradient Tool.app" -ov -format UDZO GradientTool.dmg
```

**签名和公证（发布到 App Store 或官方分发）：**
```bash
# 需要 Apple Developer 账号
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" "dist/Gradient Tool.app"
```

## 📊 打包结果对比

| 平台 | 方法 | 文件大小 | 启动速度 | 兼容性 |
|------|------|----------|----------|--------|
| Windows | --onefile | ~25MB | 快 | Win 7+ |
| Windows | --onedir | ~80MB | 很快 | Win 7+ |
| Linux | --onefile | ~30MB | 快 | 大多数发行版 |
| macOS | .app | ~35MB | 快 | macOS 10.13+ |

## 🔧 高级配置

### 多平台交叉打包

**注意：** PyInstaller 不支持真正的交叉编译，必须在目标平台上打包。

**建议方案：**
- 使用 GitHub Actions 或 CI/CD 自动化打包
- 在虚拟机中打包其他平台版本
- 使用云构建服务（如 Travis CI, AppVeyor）

### 自动化打包工作流

创建 `.github/workflows/build.yml`：
```yaml
name: Build Executables

on: [push, pull_request]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements-stable.txt
      - run: pip install pyinstaller
      - run: python build_app.py
      - uses: actions/upload-artifact@v2
        with:
          name: windows-executable
          path: dist/GradientTool.exe

  build-linux:
    runs-on: ubuntu-latest
    # ... 类似配置

  build-macos:
    runs-on: macos-latest
    # ... 类似配置
```

## 📄 相关文件

- `gradient_tool.spec` - PyInstaller 配置文件
- `build_app.bat` - Windows 打包脚本
- `build_app.py` - 跨平台打包脚本
- `requirements-stable.txt` - Python 依赖列表

## 🆘 获取帮助

如果遇到问题：

1. **查看详细日志：**
   ```bash
   pyinstaller gradient_tool.spec --clean --log-level DEBUG
   ```

2. **查阅官方文档：**
   - [PyInstaller 文档](https://pyinstaller.org/)
   - [常见问题解答](https://github.com/pyinstaller/pyinstaller/wiki)

3. **社区支持：**
   - GitHub Issues
   - Stack Overflow (标签: pyinstaller)

---

**打包完成后，记得测试应用的所有功能！** 🚀✨
