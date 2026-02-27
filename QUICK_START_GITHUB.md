# 🪟 OPPO Live Photo Viewer - GitHub Actions 自动编译

## 🚀 一键跨平台编译

**你只需要：** `git push`

**GitHub Actions会自动：**
- ✅ 在Windows上编译应用
- ✅ 打包成.exe文件
- ✅ 上传供下载

---

## 🎯 完整流程

```
你（开发者）
    ↓
修改代码
    ↓
git push（推送到GitHub）
    ↓
GitHub Actions（自动）
    ↓
在Windows上编译
    ↓
打包成exe
    ↓
上传到GitHub
    ↓
用户（下载）
    ↓
从GitHub下载exe
    ↓
双击运行
```

**你只需要做：git push！** 🚀

---

## 📋 第一次设置

### 1. 创建GitHub仓库

1. 访问：https://github.com/new
2. 仓库名：`oppo-live-viewer`
3. 选择Public或Private
4. 点击"Create repository"

### 2. 上传代码

**方法A：使用命令行**
```bash
cd /home/yezichao/.openclaw/workspace/oppo-live-viewer

# 初始化git仓库
git init
git add .
git commit -m "Initial commit: OPPO Live Photo Viewer v1.7"
git branch -M main

# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/oppo-live-viewer.git

# 推送到GitHub（会自动触发编译）
git push -u origin main
```

**方法B：使用网页**
1. 在GitHub仓库页面，点击"Upload files"
2. 拖拽整个`oppo-live-viewer`文件夹
3. 点击"Commit changes"

---

## 🔄 后续更新

### 每次推送代码都会自动编译

```bash
# 1. 修改代码

# 2. 提交代码
git add .
git commit -m "Update: new feature"

# 3. 推送到GitHub（自动触发编译）
git push
```

### 发布新版本（推荐）

```bash
# 1. 修改代码

# 2. 提交代码
git add .
git commit -m "Release v1.8"

# 3. 创建tag（会自动编译并发布）
git tag v1.8
git push
git push origin v1.8

# 4. 用户可以从Releases下载新版本
```

---

## 📥 下载Windows版本

### 方法1：从GitHub Actions下载

1. 打开GitHub仓库
2. 点击"Actions"标签
3. 选择最新的workflow运行
4. 滚动到底部，找到"Artifacts"
5. 点击"OPPO-Live-Viewer-Windows"下载

### 方法2：从Releases下载（推荐）

1. 打开GitHub仓库
2. 点击"Releases"标签
3. 选择最新的Release
4. 在Assets部分下载`OPPO-Live-Viewer-Windows.exe`

---

## 🎛 工作流

### 日常开发

```
修改代码 → git commit → git push → 等待5-10分钟 → 下载exe
```

### 发布新版本

```
修改代码 → git commit → git tag v1.8 → git push → 下载exe
```

---

## 💡 优势

### 对你（开发者）
- ✅ **完全自动化**：只需要`git push`
- ✅ **无需Windows机器**：GitHub提供Windows环境
- ✅ **跨平台编译**：支持Windows, macOS, Linux
- ✅ **持续集成**：每次push都自动编译
- ✅ **版本管理**：清晰的版本历史

### 对用户
- ✅ **一键下载**：从Releases直接下载
- ✅ **最新版本**：总是可以使用最新编译的版本
- ✅ **历史版本**：可以下载任何历史版本

---

## 🔧 配置说明

### 自动触发条件

| 事件 | 条件 | 说明 |
|------|------|------|
| 代码推送 | push到main/master | 自动编译 |
| 版本发布 | push tag (v*) | 自动编译并发布 |
| 手动编译 | 点击"Run workflow" | 手动触发编译 |

### 编译环境

```
平台：Windows
Python：3.10
PyQt6：Latest
PyInstaller：Latest
```

---

## 📊 编译信息

### 编译时间
- **首次编译**：约5-10分钟（下载依赖）
- **后续编译**：约3-5分钟（使用缓存）

### 文件大小
- **Windows版本**：约80-100 MB
- **文件名**：`OPPO-Live-Viewer-Windows.exe`

---

## 🐛 常见问题

### 问题1：编译失败

**解决方案：**
1. 在GitHub Actions页面查看详细日志
2. 检查代码语法
3. 点击"Re-run failed jobs"重新编译

### 问题2：Artifacts下载失败

**解决方案：**
1. 刷新页面
2. 检查网络连接
3. 尝试从Releases页面下载

### 问题3：找不到workflow

**解决方案：**
1. 确保`.github/workflows/`文件夹已上传
2. 确保文件名是`build-windows.yml`
3. 推送代码后会自动显示

---

## 📖 详细文档

- `GITHUB_ACTIONS_GUIDE.md` - 完整的GitHub Actions指南
- `WINDOWS_BUILD_GUIDE.md` - Windows打包详细指南
- `WINDOWS_USER_GUIDE.md` - Windows版本快速使用指南
- `FINAL_PROJECT_DELIVERY.md` - 完整项目总结

---

## 🚀 立即开始

### 快速开始

```bash
# 1. 创建GitHub仓库
https://github.com/new

# 2. 推送代码（会自动触发编译）
cd /home/yezichao/.openclaw/workspace/oppo-live-viewer
git init
git add .
git commit -m "Initial commit: OPPO Live Photo Viewer v1.7"
git branch -M main

# 3. 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/oppo-live-viewer.git

# 4. 推送到GitHub（自动触发编译）
git push -u origin main

# 5. 等待5-10分钟，从Actions或Releases下载exe
```

---

## 🎉 总结

**你需要的：**
- ✅ GitHub账号
- ✅ git命令行工具
- ✅ `git push`命令

**GitHub Actions会自动：**
- ✅ 在Windows上编译
- ✅ 打包成exe
- ✅ 上传供下载

**用户只需要：**
- ✅ 从GitHub下载exe
- ✅ 双击运行

---

**开始使用吧！只需要一次`git push`，Windows版本就自动编译好了！** 🎉🪟
