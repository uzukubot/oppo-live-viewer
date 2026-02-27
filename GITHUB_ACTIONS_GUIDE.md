# 🪟 GitHub Actions 自动跨平台编译

## 🚀 一键自动编译

不需要你手动操作！只需要把代码推送到GitHub，GitHub Actions会自动：
1. 在Windows上编译应用
2. 打包成.exe文件
3. 上传到GitHub Artifacts

---

## 📋 使用步骤

### 1. 创建GitHub仓库

1. 在GitHub上创建一个新仓库
2. 命名为：`oppo-live-viewer`
3. 选择Public或Private
4. 不要初始化README

### 2. 上传代码

**方法1：使用Git命令**
```bash
cd /home/yezichao/.openclaw/workspace/oppo-live-viewer

# 初始化git仓库（如果还没有）
git init
git add .
git commit -m "Initial commit: OPPO Live Photo Viewer v1.7"

# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/oppo-live-viewer.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

**方法2：使用GitHub网页**
1. 在GitHub仓库页面，点击"Upload files"
2. 拖拽整个`oppo-live-viewer`文件夹
3. 点击"Commit changes"

### 3. 触发编译

编译会自动触发：

**自动触发：**
- ✅ 推送代码到`main`或`master`分支
- ✅ 推送tag（例如`v1.7`）
- ✅ 使用"Run workflow"手动触发

**等待编译：**
- ⏱️ 大约需要5-10分钟
- 📧 GitHub会发邮件通知（如果配置了）
- 🔄 可以在Actions页面查看进度

### 4. 下载编译好的exe

**方法1：从GitHub Actions页面**
1. 打开GitHub仓库
2. 点击"Actions"标签
3. 选择最新的workflow运行
4. 在页面底部找到"Artifacts"
5. 点击"OPPO-Live-Viewer-Windows"下载

**方法2：从Releases页面**
1. 打开GitHub仓库
2. 点击"Releases"标签
3. 选择最新的Release
4. 在Assets部分下载`OPPO-Live-Viewer-Windows.exe`

---

## 🔧 工作流程说明

### 自动触发场景

| 触发事件 | 操作 | 结果 |
|---------|------|------|
| 推送代码 | `git push` | 自动编译 |
| 推送tag | `git push origin v1.7` | 自动编译 |
| 手动触发 | "Run workflow"按钮 | 手动编译 |

### 编译过程

```
代码推送
    ↓
GitHub Actions自动触发
    ↓
Windows环境准备（2-3分钟）
    ├─ 检出代码
    ├─ 安装Python 3.10
    └─ 安装PyQt6和PyInstaller
    ↓
编译打包（3-5分钟）
    ├─ PyInstaller编译
    ├─ 打包成exe文件
    └─ 上传Artifacts
    ↓
完成！
    └─ 下载exe文件（约80-100 MB）
```

---

## 💡 使用技巧

### 技巧1：快速发布新版本

```bash
# 1. 修改代码
# 2. 提交代码
git add .
git commit -m "Fix bug: xyz"

# 3. 创建tag（会自动编译并发布）
git tag v1.8
git push origin v1.8

# 4. 等待编译完成，从Releases下载
```

### 技巧2：查看编译日志

1. 打开GitHub仓库
2. 点击"Actions"
3. 点击最新的workflow运行
4. 可以看到详细的编译日志

### 技巧3：重新编译

如果编译失败，可以在Actions页面点击"Re-run failed jobs"按钮，会重新编译。

---

## 📊 支持的平台

| 平台 | 编译方式 | 文件名 | 大小 |
|------|---------|--------|------|
| **Windows** | GitHub Actions自动编译 | `OPPO-Live-Viewer-Windows.exe` | ~80-100 MB |
| Linux | 手动编译（当前已提供） | `OPPO-Live-Viewer` | ~76 MB |
| macOS | 手动编译（本地） | `OPPO-Live-Viewer` | ~70-80 MB |

---

## 🎯 完整发布流程

### 从代码到用户

```
你（开发者）
    ↓
1. 修改代码
    ↓
2. 提交代码：git commit -m "..."
    ↓
3. 推送到GitHub：git push
    ↓
GitHub Actions（自动）
    ↓
4. 在Windows上编译
    ↓
5. 打包成exe
    ↓
6. 上传到Artifacts
    ↓
GitHub（平台）
    ↓
7. 用户从Releases下载
    ↓
8. 双击exe运行
```

**整个过程你只需要做：git push！** 🚀

---

## 🔐 私有仓库

如果仓库是Private的：
- ✅ GitHub Actions会自动运行
- ✅ 只有仓库成员可以下载Artifacts
- ✅ 适合内部使用

---

## 📖 文件说明

### Workflow文件
```
.github/workflows/build-windows.yml
```
**说明：** GitHub Actions工作流配置文件
**作用：** 定义Windows编译的步骤

### 关键配置

**触发条件：**
```yaml
on:
  push:
    branches: [ main, master ]  # 推送到这些分支时触发
  tags:
      - 'v*'                         # 推送tag时触发
  workflow_dispatch:                # 手动触发
```

**编译环境：**
```yaml
runs-on: windows-latest  # 使用最新的Windows环境
```

**编译步骤：**
1. 检出代码
2. 安装Python 3.10
3. 安装依赖
4. PyInstaller编译
5. 上传Artifacts

---

## 🐛 常见问题

### 问题1：编译失败

**解决方案：**
1. 在Actions页面查看详细日志
2. 检查代码语法是否正确
3. 检查requirements.txt是否正确
4. 点击"Re-run failed jobs"重新编译

### 问题2：Artifacts过期

**解决方案：**
- GitHub Artifacts保留90天
- 建议及时下载
- 或创建GitHub Release永久保存

### 问题3：编译时间过长

**解决方案：**
- 首次编译需要5-10分钟（下载依赖）
- 后续编译会更快（使用缓存）
- 可以在workflow中添加缓存配置

---

## 🚀 快速开始

### 第一次使用

```bash
# 1. 创建GitHub仓库（网页操作）

# 2. 上传代码
cd /home/yezichao/.openclaw/workspace/oppo-live-viewer
git init
git add .
git commit -m "Initial commit: OPPO Live Photo Viewer v1.7"
git branch -M main

# 3. 连接到GitHub（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/oppo-live-viewer.git

# 4. 推送代码（会自动触发编译）
git push -u origin main
```

### 后续更新

```bash
# 1. 修改代码

# 2. 提交代码
git add .
git commit -m "Update: new feature"

# 3. 推送代码（会自动触发编译）
git push

# 4. 等待编译，从Actions下载exe
```

### 发布新版本

```bash
# 1. 修改代码

# 2. 提交代码
git add .
git commit -m "Release v1.8"

# 3. 创建tag
git tag v1.8

# 4. 推送代码和tag
git push
git push origin v1.8

# 5. 从Releases下载新版本exe
```

---

## 💡 优势

### 对你（开发者）
- ✅ **完全自动化**：只需要`git push`
- ✅ **无需Windows机器**：GitHub提供Windows环境
- ✅ **无需手动操作**：一切自动完成
- ✅ **跨平台编译**：轻松支持多个平台
- ✅ **CI/CD集成**：持续集成和部署

### 对用户
- ✅ **一键下载**：从Releases直接下载
- ✅ **版本管理**：清晰的历史版本
- ✅ **自动更新**：可以配置自动更新检查

---

## 📂 文件结构

添加到GitHub的文件：
```
oppo-live-viewer/
├── main.py                              # 主程序
├── requirements.txt                     # Python依赖
├── .github/
│   └── workflows/
│       └── build-windows.yml          # ⭐ GitHub Actions配置
├── CHANGELOG_v1.7.md                   # v1.7版本日志
├── README_COMPLETE.md                 # 完整功能说明
├── FINAL_PROJECT_DELIVERY.md          # 项目总结
└── ... （其他文档和脚本）
```

**关键是：** 把`.github/workflows/build-windows.yml`文件也上传！

---

## 🎉 总结

**你只需要：**
1. 创建GitHub仓库
2. 推送代码：`git push`

**GitHub Actions会自动：**
1. 在Windows上编译
2. 打包成exe
3. 上传供下载

**用户可以：**
1. 从Releases下载exe
2. 双击运行

**整个过程自动化！** 🚀

---

**开始使用吧！只需要一次`git push`，Windows版本就自动编译好了！** 🎉
