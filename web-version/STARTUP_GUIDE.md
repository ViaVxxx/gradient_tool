# Gradient Tool 启动指南

## 🚀 快速启动

### Windows 用户（推荐）
双击运行 `start_dev.bat` 文件，会自动启动开发模式。

### 命令行启动
```bash
# 进入 web-version 目录
cd web-version

# 自动启动开发模式（无需交互）
python start_dev_auto.py

# 或者使用交互式启动器
python start_web.py
```

## 📋 启动模式说明

### 1. 开发模式（推荐）
- **特点**：支持热重载，代码修改后自动刷新
- **适用**：开发和调试时使用
- **启动**：`python start_dev_auto.py` 或 `start_dev.bat`

### 2. 生产模式
- **特点**：构建优化后的版本，性能更好
- **适用**：正式使用或演示
- **启动**：`python start_web.py` 选择模式 2

## 🔧 故障排除

### 问题1：Node.js 未找到
**解决方案**：
1. 访问 https://nodejs.org/ 下载安装 Node.js
2. 重启命令行窗口
3. 重新运行启动脚本

### 问题2：前端依赖安装失败
**解决方案**：
```bash
cd web-version/web
npm install
```

### 问题3：PyWebView 安装失败
**解决方案**：
```bash
pip install pywebview
```

### 问题4：路径错误
**确保**：
- 在 `web-version` 目录中运行启动脚本
- 不要在项目根目录运行

## 📁 文件说明

- `start_dev.bat` - Windows 一键启动（推荐）
- `start_dev_auto.py` - 自动启动开发模式
- `start_web.py` - 交互式启动器
- `main_web.py` - 主应用程序

## 🌐 访问地址

启动成功后，应用会自动打开窗口。如果需要在浏览器中访问：
- **开发模式**：http://localhost:5173
- **生产模式**：应用窗口直接显示

## ✨ 使用优化版UI

如果要使用优化版的UI界面：

1. **备份原文件**：
   ```bash
   cd web/src
   copy App.vue App_backup.vue
   ```

2. **使用优化版本**：
   ```bash
   copy App_optimized.vue App.vue
   ```

3. **重启应用**即可看到优化后的界面

## 📞 技术支持

如果遇到问题：
1. 检查 Node.js 版本（推荐 v18+）
2. 检查 Python 版本（推荐 3.8+）
3. 确保在正确目录运行脚本
4. 查看错误信息并按照提示操作

---

**最后更新**：2025-12-22  
**版本**：v2.0