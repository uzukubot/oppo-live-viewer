# 🪟 OPPO Live Photo Viewer - Windows 版本打包指南

## 📋 前置要求

在Windows上打包需要：

1. **Python 3.9 或更高版本**
   - 下载地址：https://www.python.org/downloads/
   - 安装时勾选"Add Python to PATH"

2. **pip**
   - 通常随Python一起安装
   - 验证：打开CMD，输入 `pip --version`

3. **网络连接**
   - 需要下载PyQt6和PyInstaller

---

## 🚀 快速打包（推荐）

### 方法1：使用打包脚本

1. **复制文件到Windows**
   - 将 `oppo-live-viewer` 文件夹复制到Windows机器
   - 或通过USB/网络传输

2. **运行打包脚本**
   - 双击 `build_windows.bat`
   - 或在CMD中运行：
     ```cmd
     build_windows.bat
     ```

3. **等待完成**
   - 脚本会自动：
     - 检查Python和pip
     - 安装依赖
     - 打包应用
     - 清理临时文件

4. **找到可执行文件**
   ```
   dist\OPPO-Live-Viewer.exe
   ```

---

## 🔧 手动打包

### 步骤1：安装Python

1. 下载Python 3.9+
   - 访问：https://www.python.org/downloads/
   - 选择Windows安装包
   - 下载并安装

2. 安装时勾选：
   - ✅ "Add Python to PATH"
   - ✅ "Install for all users"（可选）

3. 验证安装
   ```cmd
   python --version
   ```

### 步骤2：安装依赖

打开命令提示符（CMD）或PowerShell，运行：

```cmd
# 1. 升级pip
python -m pip install --upgrade pip

# 2. 安装PyQt6
python -m pip install PyQt6 PyQt6-Qt-Multimedia PyQt6-Qt-MultimediaWidgets

# 3. 安装PyInstaller
python -m pip install pyinstaller
```

### 步骤3：打包应用

```cmd
# 1. 进入项目目录
cd oppo-live-viewer

# 2. 打包
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py

# 3. 等待完成（首次打包需要5-10分钟）
```

### 步骤4：运行应用

```cmd
# 1. 进入dist目录
cd dist

# 2. 运行
OPPO-Live-Viewer.exe

# 或双击文件
```

---

## 📦 打包选项

### 基本打包
```cmd
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py
```

### 添加图标
```cmd
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" --icon=app.ico main.py
```

### 包含额外文件
```cmd
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" --add-data="README.md:." main.py
```

### 添加管理员权限
```cmd
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" --uac-admin main.py
```

---

## 🐛 常见问题

### 问题1：找不到Python

**症状：**
```
python is not recognized as an internal or external command
```

**解决方案：**
1. 重新安装Python，勾选"Add Python to PATH"
2. 或手动添加到PATH：
   - 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
   - 在"系统变量"中找到Path，编辑
   - 添加Python安装路径（例如：`C:\Python39`）

### 问题2：PyQt6安装失败

**症状：**
```
ERROR: Could not find a version that satisfies the requirement PyQt6
```

**解决方案：**
```cmd
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
python -m pip install PyQt6 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3：打包后无法运行

**症状：**
双击.exe后无反应

**解决方案：**
1. 安装Visual C++ Redistributable
   - 下载：https://aka.ms/vs/17/release/vc_redist.x64.exe
   - 安装后重试

2. 检查Windows版本
   - 支持Windows 10/11
   - 不支持Windows 7/8/8.1

---

## 💡 打包优化

### 减小文件大小

创建 `build_optimized.bat`：
```cmd
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" ^
  --strip ^
  --noupx ^
  --optimize=2 ^
  main.py
```

### 加快打包速度

首次打包后，PyInstaller会缓存，后续打包会更快。

---

## 📊 预期文件大小

| 配置 | 预期大小 |
|------|----------|
| 基本打包 | 约80-100 MB |
| 优化打包（--strip） | 约60-80 MB |

---

## 🎯 验证打包成功

### 运行测试

1. 双击 `OPPO-Live-Viewer.exe`
2. 打开一个Live Photo文件
3. 验证功能正常

### 检查依赖

使用工具检查exe依赖：
- **Dependencies Walker**：https://www.dependencywalker.com/
- **Dependencies**：https://github.com/lucasg/Dependencies

---

## 📖 详细文档

- `build_windows.bat` - Windows自动打包脚本
- `README_COMPLETE.md` - 完整功能说明
- `CHANGELOG_v1.7.md` - v1.7新功能说明

---

## 🔄 跨平台打包

如果需要在多个平台上打包：

### Windows（当前）
- 使用 `build_windows.bat`
- 产物：`OPPO-Live-Viewer.exe`

### macOS
```bash
cd oppo-live-viewer
pip install PyQt6 PyQt6-Qt-Multimedia pyinstaller
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py
```
- 产物：`OPPO-Live-Viewer`

### Linux
```bash
cd oppo-live-viewer
pip install PyQt6 PyQt6-Qt-Multimedia pyinstaller
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py
```
- 产物：`OPPO-Live-Viewer`

---

## 💡 提示

1. **首次打包慢**：首次打包需要下载依赖，需要5-10分钟
2. **缓存加速**：后续打包会更快
3. **测试先打包**：建议先测试main.py是否能正常运行
4. **杀毒软件**：打包前暂时关闭杀毒软件，避免干扰
5. **管理员权限**：可能需要管理员权限来写入某些目录

---

**打包完成后，你可以在任何Windows机器上运行 `OPPO-Live-Viewer.exe`！** 🎉

---

**更多帮助：**
- 查看各版本的CHANGELOG文件了解功能
- 查看README_COMPLETE.md了解所有功能
- 运行test脚本验证功能
