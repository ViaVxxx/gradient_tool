# Gradient Tool - Web 版

**现代化 Web 界面，支持玻璃态设计、复杂阴影和圆角效果的渐变色图像生成器**

## ✨ 特性

- 🎨 **现代化 UI**: 玻璃态设计、复杂阴影、圆角效果
- 🌈 **Vue 3 + TailwindCSS**: 响应式、流畅的用户体验
- 🔥 **热重载**: 开发模式支持代码热更新
- 📦 **小体积**: 比 Electron 打包体积更小（~30-35MB）
- 🚀 **跨平台**: Windows、macOS、Linux 全平台支持
- ✨ **专业效果**: 噪点、晕影、纹理效果
- ⭐ **收藏系统**: 保存和管理喜爱的渐变

## 🚀 快速开始

### 环境要求
```
Python 3.7+
Node.js 16+
PyWebView >= 4.0.0
```

### 启动方式

**方式 1：使用 Python 启动脚本（推荐）**
```bash
# 运行启动脚本（自动检查并安装依赖）
python start_web.py
```

**方式 2：使用批处理文件（Windows）**
```bash
start_web_en.bat
```

**方式 3：手动启动**
```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装前端依赖
cd web
npm install

# 启动前端开发服务器（新终端）
npm run dev

# 启动 Python 后端（新终端）
python main_web.py
```

## 📖 使用指南

### 基础操作
1. **选择渐变类型**: 线性或径向渐变
2. **调整角度**: 使用圆盘选择器拖动调节
3. **编辑色标**: 在水平渐变条上编辑颜色和位置
4. **应用效果**: 勾选效果开关，调节强度滑块
5. **使用预设**: 从2列网格预设中快速选择
6. **导出图像**: 支持 PNG/JPG 格式

### 高级功能
- **实时预览**: 所有操作都有即时视觉反馈
- **效果管理**: 开关式效果控制，仅开启时显示强度调节
- **预设库**: 分类预设，2列紧凑布局
- **随机生成**: 一键生成创意渐变

## 🏗️ 项目结构

```
web-version/
├── main_web.py                 # Python 后端入口
├── start_web.py                # 启动脚本
├── start_web_en.bat            # Windows 启动脚本
├── requirements.txt            # Python 依赖
├── web/                        # Vue 前端项目
│   ├── src/                    # 源代码
│   ├── package.json            # 前端依赖
│   └── dist/                   # 构建输出
├── core/                       # 核心功能模块
│   ├── gradient_engine.py      # 渐变渲染引擎
│   ├── color_utils.py          # 颜色处理工具
│   ├── effects.py              # 效果处理系统
│   └── presets.py              # 预设管理器
├── utils/                      # 工具函数库
│   ├── export.py               # 图像导出功能
│   ├── favorites.py            # 收藏管理系统
│   └── history.py              # 历史记录管理
└── favorites/                  # 收藏数据
```

## 🛠️ 技术栈

### 后端
- **桥接框架**: PyWebView
- **图像处理**: Pillow (PIL Fork)
- **API 设计**: RESTful API 风格

### 前端
- **框架**: Vue 3 + Composition API
- **构建工具**: Vite
- **样式**: TailwindCSS
- **UI 组件**: 自定义组件库

## 🎨 界面特色

- ✨ 玻璃态（glassmorphism）设计
- 🌈 复杂的阴影效果
- 🎨 平滑的渐变背景
- 🔵 圆角设计
- 💫 悬停动画效果
- 📱 响应式布局

## 🔧 开发模式

启动开发模式后：
- 前端支持热重载（HMR）
- 后端 API 自动重启
- 浏览器开发者工具可用
- 实时调试和测试

## 📄 开源协议

本项目基于 MIT License 开源协议。