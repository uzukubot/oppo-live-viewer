# OPPO Live Photo Viewer

跨平台OPPO Live Photo查看器，支持macOS/Windows/Linux。

## 功能特点

- ✅ 直接读取OPPO Live Photo文件（.live.jpeg）
- ✅ 不需要导出额外文件，内存中解析
- ✅ 自动播放Live效果
- ✅ 支持拖拽文件打开
- ✅ 支持文件夹浏览
- ✅ 真正跨平台（macOS/Windows/Linux）

## 安装

### 前置要求

- Python 3.9+
- pip

### 安装依赖

```bash
cd oppo-live-viewer
pip install -r requirements.txt
```

## 使用

### 启动应用

```bash
python main.py
```

### 基本操作

1. **打开文件**：点击"打开文件"按钮选择Live Photo文件
2. **打开文件夹**：点击"打开文件夹"按钮扫描文件夹
3. **拖拽文件**：直接将.live.jpeg文件拖到窗口中
4. **查看Live效果**：打开文件后会自动播放Live效果

### 文件格式

支持的文件扩展名：
- `.live.jpeg`（OPPO Live Photo）
- `.jpeg`（标准JPEG）
- `.jpg`（标准JPEG）

## 技术细节

### OPPO Live Photo格式

OPPO的Live Photo采用**嵌入MP4到JPEG**的方式：

- JPEG静态图在文件开头
- MP4视频数据嵌入在JPEG之后
- 通过搜索`ftypmp42`标记找到MP4起始位置
- 文件大小通常约15-20MB

### 核心实现

1. 读取二进制文件
2. 搜索MP4标记（`ftypmp42`或`ftypisom`）
3. 提取JPEG和MP4数据流
4. 在内存中处理，不导出额外文件
5. 使用PyQt6的多媒体组件播放视频

## 跨平台打包

### 使用PyInstaller打包

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "OPPO-Live-Viewer" main.py
```

打包后的可执行文件在`dist/`目录中。

### macOS打包

```bash
pyinstaller --onefile --windowed --name "OPPO-Live-Viewer" --icon=app.icns main.py
```

### Windows打包

```bash
pyinstaller --onefile --windowed --name "OPPO-Live-Viewer.exe" --icon=app.ico main.py
```

## 故障排除

### 视频无法播放

如果视频无法播放，可能是：
1. 文件不是有效的OPPO Live Photo
2. 系统缺少多媒体解码器（Linux用户可能需要安装`gstreamer`）

### Linux多媒体支持

Ubuntu/Debian:
```bash
sudo apt-get install gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
```

Fedora:
```bash
sudo dnf install gstreamer-plugins-good gstreamer-plugins-bad gstreamer-plugins-ugly
```

## 许可证

MIT License

## 贡献

欢迎提交问题和拉取请求！
