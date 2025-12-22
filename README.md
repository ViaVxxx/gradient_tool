# Gradient Tool - 渐变色图像生成器

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**一个功能强大、界面优雅的渐变色图像生成桌面应用**

*支持多种渐变类型、专业效果处理和现代化深色主题*

</div>

## ✨ 核心特性

### 🎨 渐变设计
- **多种渐变类型**: 线性渐变、径向渐变
- **精确角度控制**: 0-360° 自由调节
- **多色标编辑**: 支持最多 20 个色标点
- **颜色选择器**: RGB/HEX 双模式颜色输入
- **预设库**: 内置多个精美渐变预设

### ✨ 专业效果
- **噪点效果**: 添加自然纹理质感
- **晕影效果**: 营造聚焦视觉效果
- **实时预览**: 所见即所得的编辑体验

### 🎯 智能功能
- **收藏系统**: 保存和管理喜爱的渐变
- **历史记录**: 50 步撤销/重做操作
- **随机生成**: 一键生成创意渐变
- **批量导出**: 支持多选收藏批量导出

### 🌙 现代界面
- **深色主题**: 护眼的现代化界面设计
- **响应式布局**: 三栏式专业布局
- **快捷键支持**: 提升操作效率

## 🚀 快速开始

### 环境要求
```
Python 3.7+
tkinter (Python 内置)
Pillow >= 8.0.0
```

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/gradient-tool.git
cd gradient-tool
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动应用**
```bash
python main.py
```

## 📖 使用指南

### 基础操作
1. **选择渐变类型**: 线性或径向渐变
2. **调整角度**: 仅线性渐变可用，拖动滑块调节
3. **编辑色标**: 点击色标选择颜色，使用 +/- 按钮添加/删除
4. **应用效果**: 调节噪点和晕影强度
5. **设置分辨率**: 选择预设或自定义尺寸
6. **导出图像**: 支持 PNG/JPG 格式

### 高级功能
- **收藏管理**: 点击 ⭐ 收藏当前渐变，支持多选批量操作
- **预设使用**: 从分类预设中快速选择专业渐变
- **历史记录**: 使用撤销/重做功能回到之前的状态

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+S` | 导出 PNG 格式 |
| `Space` / `R` | 随机生成渐变 |
| `Ctrl+Z` | 撤销操作 |
| `Ctrl+Y` | 重做操作 |

## 🏗️ 项目架构

```
gradient-tool/
├── 📄 main.py                  # 应用程序入口
├── 📄 requirements.txt         # 项目依赖
├── 📁 core/                    # 核心功能模块
│   ├── gradient_engine.py      # 渐变渲染引擎
│   ├── color_utils.py          # 颜色处理工具
│   ├── effects.py              # 效果处理系统
│   └── presets.py              # 预设管理器
├── 📁 ui/                      # 用户界面层
│   ├── main_window.py          # 主窗口界面
│   └── themes.py               # 主题系统
└── 📁 utils/                   # 工具函数库
    ├── export.py               # 图像导出功能
    ├── favorites.py            # 收藏管理系统
    └── history.py              # 历史记录管理
```

## 🛠️ 技术栈

- **GUI 框架**: Tkinter (跨平台原生支持)
- **图像处理**: Pillow (PIL Fork)
- **渲染引擎**: 自研 Canvas 2D 渲染
- **架构模式**: MVC 分层架构
- **设计原则**: SOLID 原则，模块化设计

## 📸 功能预览

### 主界面
- 🎨 左侧：渐变设计面板
- 🖼️ 中间：实时预览区域  
- ⚙️ 右侧：输出设置面板

### 核心功能
- ✅ 多色标渐变编辑
- ✅ 实时效果预览
- ✅ 收藏夹管理
- ✅ 批量导出功能
- ✅ 深色主题界面

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

Made with ❤️ by developers, for designers

</div>