# Gradient Tool - 渐变色图像生成器

一个基于 Python 和 Tkinter 的渐变色图像生成工具，支持线性和径向渐变，具有深色主题界面。

## 功能特性

- 🎨 **渐变类型**: 支持线性渐变和径向渐变
- 🎯 **角度控制**: 线性渐变角度可调
- 🌈 **色标编辑**: 支持多个色标点，自定义颜色
- ✨ **效果处理**: 噪点和晕影效果
- 📐 **分辨率设置**: 预设分辨率和自定义尺寸
- ⭐ **收藏功能**: 保存和管理喜欢的渐变
- 🌙 **深色主题**: 现代化的深色界面
- 📤 **导出格式**: 支持 PNG 和 JPG 格式

## 环境要求

- Python 3.7+
- tkinter (通常随 Python 安装)
- Pillow (PIL)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行程序

```bash
python main.py
```

## 项目结构

```
├── main.py              # 主程序入口
├── requirements.txt     # 依赖包列表
├── core/               # 核心功能模块
│   ├── gradient_engine.py  # 渐变引擎
│   ├── color_utils.py      # 颜色工具
│   ├── effects.py          # 效果处理
│   └── presets.py          # 预设管理
├── ui/                 # 用户界面模块
│   ├── main_window.py      # 主窗口
│   └── themes.py           # 主题系统
└── utils/              # 工具模块
    ├── export.py           # 导出功能
    ├── favorites.py        # 收藏管理
    └── history.py          # 历史记录
```

## 快捷键

- `Ctrl+S` - 导出 PNG
- `Space/R` - 随机生成渐变
- `Ctrl+Z` - 撤销
- `Ctrl+Y` - 重做

## 开源协议

MIT License