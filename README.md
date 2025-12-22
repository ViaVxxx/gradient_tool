# Gradient Tool - 渐变色图像生成器

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**功能强大的渐变色图像生成工具，提供两个独立版本**

*支持多种渐变类型、专业效果处理，可选择 Web 版或桌面版*

---

## 📦 版本选择

本项目提供两个独立的版本，请根据需求选择：

### 🌐 [Web 版本](./web-version/) - 推荐

**现代化 Web 界面，支持玻璃态设计和复杂效果**

- ✨ **现代化 UI**: 玻璃态设计、复杂阴影、圆角效果
- 🎨 **Vue 3 + TailwindCSS**: 响应式、流畅的用户体验
- 🔥 **热重载**: 开发模式支持代码热更新
- 📦 **小体积**: 比 Electron 打包体积更小
- 🚀 **跨平台**: Windows、macOS、Linux 全平台支持

**快速启动**:
```bash
cd web-version
python start_web.py
```

### 🖥️ [Tkinter 桌面版](./tkinter-version/)

**经典桌面应用，稳定可靠**

- 🎨 **原生界面**: 系统原生 UI，轻量级
- 🔧 **简单依赖**: 仅需 Python + Pillow
- ⚡ **快速启动**: 无需 Node.js 环境
- 🌙 **深色主题**: 现代化界面设计
- ⌨️ **快捷键**: 完整的键盘快捷键支持

**快速启动**:
```bash
cd tkinter-version
pip install -r requirements.txt
python main.py
```

---

## ✨ 共同特性

两个版本都支持以下核心功能：

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

---

## 🚀 快速对比

| 特性 | Web 版本 | Tkinter 版本 |
|------|----------|--------------|
| **界面设计** | 现代玻璃态 | 经典原生 |
| **技术栈** | Vue 3 + Python | Pure Python |
| **依赖** | Node.js + Python | 仅 Python |
| **启动速度** | 中等 | 快速 |
| **包体积** | ~30-35MB | ~10-15MB |
| **热重载** | ✅ | ❌ |
| **响应式** | ✅ | ❌ |
| **快捷键** | 部分支持 | 完整支持 |

---

## 🏗️ 项目结构

```
gradient_tool/
├── 📁 web-version/           # Web 版本
│   ├── main_web.py           # Python 后端
│   ├── start_web.py          # 启动脚本
│   ├── web/                  # Vue 前端
│   └── README.md             # Web 版说明
├── 📁 tkinter-version/       # Tkinter 版本
│   ├── main.py               # 应用入口
│   ├── ui/                   # UI 组件
│   └── README.md             # 桌面版说明
├── 📁 core/                  # 共享核心模块
├── 📁 utils/                 # 共享工具函数
└── 📁 favorites/             # 共享收藏数据
```

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源协议。

---

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

Made with ❤️ by developers, for designers