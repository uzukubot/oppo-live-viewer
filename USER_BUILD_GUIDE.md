# 📦 OPPO Live Photo Viewer - 用户打包指南

## ⚠️ 重要说明

当前的OpenClaw环境缺少必要的GUI库（PyQt6和tkinter），无法直接打包。

**请在你自己的电脑上（有完整Python环境的机器）执行以下步骤。**

---

## 🚀 快速打包（在你的电脑上）

### Windows

```cmd
cd oppo-live-viewer
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py
```

完成后：双击 `dist\OPPO-Live-Viewer.exe`

---

### macOS / Linux

```bash
cd oppo-live-viewer
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py
```

完成后：`./dist/OPPO-Live-Viewer` 或在文件管理器中双击

---

## 📋 前置要求

在你的电脑上确保：

- ✅ Python 3.9 或更高版本
- ✅ pip 可用
- ✅ 网络连接（用于下载依赖）

---

## 🔧 安装依赖（如果还没有）

### Windows (PowerShell)
```powershell
pip install PyQt6 PyQt6-Qt-Multimedia PyQt6-Qt-MultimediaWidgets pyinstaller
```

### macOS / Linux (Bash)
```bash
pip install PyQt6 PyQt6-Qt-Multimedia PyQt6-Qt-MultimediaWidgets pyinstaller
```

---

## 📂 项目文件说明

```
oppo-live-viewer/
├── main.py                # PyQt6版本（推荐，功能完整）
├── main_tkinter.py        # Tkinter版本（备用，无需额外依赖）
├── requirements.txt       # Python依赖
├── README.md             # 使用说明
├── PROJECT_SUMMARY.md    # 项目总结
└── dist/                 # 打包后的可执行文件目录（打包后生成）
```

---

## 🎯 两种版本选择

### PyQt6 版本（main.py）✨ 推荐
- ✅ 完整GUI界面
- ✅ 内置视频播放器
- ✅ 自动播放Live效果
- ✅ 美观的用户界面

**依赖：** 需要安装PyQt6

### Tkinter 版本（main_tkinter.py） 🔄 备用
- ✅ Python内置，无需额外依赖
- ✅ 轻量级
- ⚠️ 使用外部播放器打开视频
- ⚠️ 界面较简单

**依赖：** 只需标准Python库

---

## 📝 详细打包步骤

### 步骤1: 克隆或下载项目

项目位置：`/home/yezichao/.openclaw/workspace/oppo-live-viewer/`

你可以：
- 直接复制这个文件夹到你的电脑
- 或者通过USB/网络传输

### 步骤2: 打开终端/命令行

- Windows: 打开 PowerShell 或 CMD
- macOS: 打开 Terminal
- Linux: 打开 Terminal

### 步骤3: 进入项目目录

```bash
cd oppo-live-viewer
```

### 步骤4: 安装依赖

**Windows:**
```cmd
pip install PyQt6 PyQt6-Qt-Multimedia PyQt6-Qt-MultimediaWidgets pyinstaller
```

**macOS / Linux:**
```bash
pip install PyQt6 PyQt6-Qt-Multimedia PyQt6-Qt-MultimediaWidgets pyinstaller
```

如果安装失败，可能需要先升级pip：
```bash
pip install --upgrade pip
```

### 步骤5: 打包应用

```bash
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py
```

等待完成（首次打包可能需要5-10分钟）

### 步骤6: 运行应用

**Windows:**
```
dist\OPPO-Live-Viewer.exe
```

**macOS / Linux:**
```bash
cd dist
./OPPO-Live-Viewer
```

或直接在文件管理器中双击文件！

---

## 🐛 常见问题

### 问题1: pip 不是内部或外部命令
**解决方案:**
- 确保安装Python时勾选了"Add Python to PATH"
- 或使用完整路径：`python -m pip ...`

### 问题2: PyQt6 安装失败
**解决方案:**
```bash
pip install --upgrade pip
pip install PyQt6
```

### 问题3: 打包后无法运行
**解决方案:**
- Windows: 可能需要安装 Visual C++ Redistributable
- Linux: 需要安装多媒体库：`sudo apt-get install gstreamer1.0-plugins-*`

### 问题4: 视频无法播放
**解决方案:**
- 确保系统有视频解码器
- Linux: 安装 gstreamer 插件
- macOS: 应该自带支持
- Windows: 通常自带支持

---

## 📱 使用说明

1. **打开应用**：双击可执行文件
2. **打开文件**：点击"打开文件"按钮
3. **拖拽文件**：直接拖拽.live.jpeg文件到窗口
4. **查看Live**：自动播放Live效果（延迟500ms）

---

## 🎨 界面功能

### 左侧面板
- 文件列表
- 打开文件按钮
- 打开文件夹按钮

### 右侧面板
- 图片展示区（显示静态图）
- 鼠标悬停时播放Live效果
- 自动循环播放

---

## 💡 高级选项

### 自定义打包名称
```bash
pyinstaller --onefile --windowed --name="MyViewer" main.py
```

### 添加图标
```bash
pyinstaller --onefile --windowed --icon=app.ico --name="OPPO-Live-Viewer" main.py
```

### 包含额外文件
```bash
pyinstaller --onefile --windowed --add-data="data:." main.py
```

---

## 📞 获取帮助

如果遇到问题：
1. 检查Python版本：`python --version`
2. 检查pip版本：`pip --version`
3. 查看错误日志
4. 参考README.md和PROJECT_SUMMARY.md

---

## ✅ 完成确认

打包成功后，你应该有：

- [ ] 一个可执行文件（dist/OPPO-Live-Viewer或.exe）
- [ ] 双击可以打开应用
- [ ] 可以加载.live.jpeg文件
- [ ] 可以看到Live效果

---

**祝打包顺利！** 🎉
