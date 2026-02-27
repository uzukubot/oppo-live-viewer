# 📦 OPPO Live Photo Viewer - 打包指南

## 快速打包（推荐）

### 方法 1: 使用简化脚本（需要Python和pip）

如果你的系统已经安装了Python 3.9+和pip：

```bash
cd /home/yezichao/.openclaw/workspace/oppo-live-viewer
./build_simple.sh
```

等待完成，打包好的文件在：`dist/OPPO-Live-Viewer`

双击即可运行！

---

### 方法 2: 完整安装脚本（需要sudo权限）

如果你的系统缺少依赖：

```bash
cd /home/yezichao/.openclaw/workspace/oppo-live-viewer
sudo ./install_and_build.sh
```

这会自动安装所有系统依赖和Python包，然后打包。

---

### 方法 3: 手动打包

如果你想完全控制每一步：

```bash
# 1. 安装pip（如果没有）
sudo apt-get install python3-pip

# 2. 安装系统依赖
sudo apt-get install python3-dev build-essential libgstreamer1.0-dev \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    libglib2.0-dev libcairo2-dev

# 3. 进入项目目录
cd /home/yezichao/.openclaw/workspace/oppo-live-viewer

# 4. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 6. 打包
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py

# 7. 完成！
# 可执行文件在 dist/OPPO-Live-Viewer
```

---

## 打包完成后的使用

### Linux
```bash
cd dist
./OPPO-Live-Viewer
```

或在文件管理器中双击 `OPPO-Live-Viewer` 文件

### macOS
```bash
cd dist
./OPPO-Live-Viewer
```

或在Finder中双击 `OPPO-Live-Viewer` 文件

### Windows
双击 `OPPO-Live-Viewer.exe` 文件

---

## 打包选项说明

如果需要更高级的打包选项，可以修改 `build.py` 脚本：

```python
# 基本打包
pyinstaller --onefile --windowed main.py

# 添加图标
pyinstaller --onefile --windowed --icon=app.ico main.py

# 自定义名称
pyinstaller --onefile --windowed --name="MyViewer" main.py

# 添加额外数据文件
pyinstaller --onefile --windowed --add-data="data:." main.py
```

---

## 故障排除

### 错误: pip not found
```bash
sudo apt-get install python3-pip
```

### 错误: Missing gstreamer
```bash
sudo apt-get install gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
```

### 错误: PyQt6 not found
确保在虚拟环境中安装：
```bash
source venv/bin/activate
pip install PyQt6
```

---

## 不同平台的注意事项

### Linux
- 需要安装gstreamer多媒体库
- 建议使用Ubuntu 20.04+或Debian 11+

### macOS
- 需要Xcode命令行工具
- `xcode-select --install`

### Windows
- 需要Visual C++ Redistributable
- 建议使用Windows 10+

---

## 联系支持

如果遇到问题，请检查：
1. Python版本是否 >= 3.9
2. 所有依赖是否正确安装
3. 系统是否安装了多媒体库

---

**提示：** 首次打包可能需要5-10分钟，请耐心等待！
