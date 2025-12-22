# Gradient Tool - 渐变色图像生成工具

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

**一个功能强大、用户友好的渐变色图像生成桌面应用**

*支持多种渐变类型和专业 Perlin 噪声纹理效果*

[快速开始](#-快速开始) • [功能特性](#-核心特性) • [纹理效果](#-纹理效果快速体验)

</div>

## ✨ 核心特性

### 基础功能
- ✅ 线性和径向渐变
- ✅ 可视化色标编辑器
- ✅ RGB/HEX颜色选择器
- ✅ 20+精选预设（12个色彩理论分类）
- ✅ PNG/JPG导出
- ✅ 撤销/重做功能（50步历史）
- ✅ 随机生成器

### 🎨 专业纹理效果
- ⭐ **Perlin噪点** - 自然流畅的纹理（最推荐）
- ⭐ **磨砂玻璃** - 优雅柔和的质感
- ⭐ **胶片颗粒** - 复古艺术的韵味
- 🌊 **沙砾质感** - 粗糙颗粒的触感
- 🎯 **多层噪点** - 丰富层次的深度
- ✨ **超强组合** - 终极质感体验

## 🚀 快速开始

### 环境要求
- Python 3.11-3.13（推荐3.11）
- 不支持 Python 3.15 alpha（Pillow库不兼容）

### 安装步骤

1. **克隆项目**：
```bash
git clone <repository-url>
cd gradient_tool
```

2. **创建虚拟环境**：
```bash
python3.11 -m venv .venv
```

3. **激活虚拟环境**：
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

4. **安装依赖**：
```bash
pip install -r requirements.txt
```

### 启动应用

```bash
python main.py
```

## 🎯 纹理效果快速体验

### 步骤1：查看演示效果
```bash
python demo_texture_effects.py
```
将在 `texture_demos/` 目录生成10张对比图像。

### 步骤2：应用纹理到你的图像

**交互式模式**：
```bash
python apply_texture.py
```

**命令行模式**：
```bash
# 使用默认Perlin效果
python apply_texture.py your_image.png

# 指定效果类型
python apply_texture.py your_image.png frosted

# 指定效果和强度
python apply_texture.py your_image.png film 0.25
```

支持的效果：`perlin`, `frosted`, `film`, `granular`, `layered`, `ultra`

### 步骤3：代码集成
```python
from PIL import Image
from core.effects import Effects

# 加载图像
image = Image.open("gradient.png")

# 应用Perlin噪点（推荐）
result = Effects.apply_perlin_noise(image, intensity=0.2, scale=50)
result.save("textured_gradient.png")
```

## 📖 效果选择指南

| 使用场景 | 推荐效果 | 参数建议 |
|---------|---------|---------|
| **日常设计** | Perlin噪点 | intensity=0.2 |
| **UI/UX背景** | 磨砂玻璃 + 晕影 | intensity=0.2, vignette=0.35 |
| **社交媒体** | 胶片颗粒 | intensity=0.25 |
| **艺术海报** | 超强组合 | 预设参数 |
| **商务演示** | Perlin噪点 + 晕影 | intensity=0.15, vignette=0.25 |

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl+Z` | 撤销 |
| `Ctrl+Y` | 重做 |
| `Ctrl+S` | 导出PNG |
| `Space` / `R` | 随机生成渐变 |

## 📁 项目结构

```
gradient_tool/
├── main.py                     # 主入口
├── demo_texture_effects.py     # 纹理效果演示生成器
├── apply_texture.py            # 纹理应用工具
├── core/                       # 核心功能模块
│   ├── gradient_engine.py      # 渐变渲染引擎
│   ├── color_utils.py          # 颜色工具
│   ├── effects.py              # 效果系统（含Perlin噪声）
│   └── presets.py              # 预设库
├── ui/                         # UI组件
│   └── main_window.py          # 主窗口
└── utils/                      # 工具函数
    ├── export.py               # 导出功能
    └── history.py              # 历史记录
```

## 🔧 技术栈

- **GUI框架**: Tkinter (Python内置)
- **图像处理**: Pillow (PIL)
- **渲染**: Canvas 2D + Perlin噪声算法
- **架构**: SOLID原则，KISS & DRY设计

## ⚡ 性能说明

处理一张800x600的图像：

| 效果类型 | 处理时间 | 文件大小 | 推荐指数 |
|---------|---------|---------|---------|
| Perlin噪点 | 3-4秒 | 200-300KB | ⭐⭐⭐ |
| 磨砂玻璃 | 4-5秒 | 1-1.2MB | ⭐⭐⭐ |
| 沙砾质感 | 2-3秒 | 1-1.5MB | ⭐⭐ |
| 胶片颗粒 | 4-5秒 | 800KB-1MB | ⭐⭐⭐ |
| 多层噪点 | 8-10秒 | 250-350KB | ⭐⭐ |
| 超强组合 | 10-12秒 | 1-1.3MB | ⭐⭐⭐ |

## ❓ 常见问题

### 1. 为什么无法安装Pillow？
Python 3.15是alpha版本，Pillow库暂时无法安装。请使用Python 3.11-3.13的稳定版本。

### 2. 如何导出图像？
点击"导出PNG"或"导出JPG"按钮，或使用 `Ctrl+S` 快捷键。

### 3. 效果太强或太弱怎么办？
调整intensity参数：
- 太强：降低到0.12-0.18
- 太弱：提高到0.25-0.35
- 最佳：0.18-0.22

### 4. 可以组合多个效果吗？
可以！按顺序调用效果函数，每个效果降低强度以避免过度。

## 🛣️ 开发路线图

### V1.1 (当前版本)
- [x] MVP基础功能
- [x] 7种专业纹理效果
- [x] Perlin噪声算法
- [x] 命令行纹理应用工具

### V1.5 (计划中)
- [ ] UI集成纹理效果选择器
- [ ] 锥形和网格渐变
- [ ] 完整预设库（300+）
- [ ] SVG/CSS代码导出
- [ ] 自定义预设保存

### V2.0 (未来)
- [ ] 多层渐变叠加
- [ ] 高级效果（扭曲、色差）
- [ ] GPU加速渲染
- [ ] 批量处理工具

## 📄 License

MIT

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**版本**: v1.1 with Texture Effects

享受创作！🎨✨
