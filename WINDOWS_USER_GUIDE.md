# 🪟 OPPO Live Photo Viewer - Windows 版本使用指南

## 📋 项目文件说明

在Windows上打包需要这些文件：

### 必需文件
```
main.py                              主程序（必须）
requirements.txt                     Python依赖（必须）
```

### 打包脚本
```
build_windows.bat                  Windows自动打包脚本（推荐）
```

### 文档文件
```
WINDOWS_BUILD_GUIDE.md             Windows打包详细指南
README_COMPLETE.md                 完整功能说明
FINAL_DELIVERY.md                   完整交付文档
各版本 CHANGELOG 文件               版本更新日志
```

### 测试脚本（可选）
```
test_parser_simple.py             解析器测试
test_normal_images.py              普通图片和Live Photo测试
test_v1.1.py                       v1.1功能测试
```

---

## 🚀 快速开始

### 方法1：使用自动打包脚本（推荐）

1. **复制项目到Windows**
   - 将整个 `oppo-live-viewer` 文件夹复制到Windows机器
   - 或通过网络共享访问

2. **安装Python**
   - 下载：https://www.python.org/downloads/
   - 安装时勾选 "Add Python to PATH"

3. **运行打包脚本**
   - 双击 `build_windows.bat`
   - 或在CMD中运行：
     ```cmd
     build_windows.bat
     ```

4. **等待完成**
   - 脚本会自动：
     - 检查Python和pip
     - 安装依赖（PyQt6, PyInstaller）
     - 打包应用
     - 清理临时文件

5. **运行应用**
   - 进入 `dist` 目录
   - 双击 `OPPO-Live-Viewer.exe`

### 方法2：手动打包

如果自动脚本失败，请参考 `WINDOWS_BUILD_GUIDE.md` 进行手动打包。

---

## 📦 Windows版本文件

打包完成后，可执行文件位于：
```
dist\OPPO-Live-Viewer.exe
```

**文件大小：** 约80-100 MB
**依赖：** Windows 10/11（不支持Windows 7/8）

---

## ⚙️ 运行时要求

### 系统要求
- ✅ Windows 10 或 Windows 11
- ✅ x64架构
- ❌ 不支持Windows 7/8/8.1

### 可选依赖
- **Visual C++ Redistributable**：如果无法运行，可能需要安装
  - 下载：https://aka.ms/vs/17/release/vc_redist.x64.exe
- **DirectX 11**：通常已包含在Windows中

---

## 💡 使用技巧

### 打包前准备
1. **关闭杀毒软件**：避免影响打包过程
2. **使用管理员权限**：如果遇到权限问题
3. **确保网络连接**：需要下载PyQt6和PyInstaller

### 打包优化
如果想减小文件大小，可以：
1. 修改 `build_windows.bat`，添加优化参数
2. 或参考 `WINDOWS_BUILD_GUIDE.md` 中的优化章节

### 首次运行
首次运行可能比较慢，因为需要加载库，后续运行会快很多。

---

## 🐛 常见问题

### 问题1：找不到Python

**症状：**
```
python is not recognized as an internal or external command
```

**解决方案：**
1. 重新安装Python，勾选 "Add Python to PATH"
2. 或手动添加到环境变量：
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
# 1. 升级pip
python -m pip install --upgrade pip

# 2. 使用国内镜像
python -m pip install PyQt6 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3：打包后无法运行

**症状：**
双击exe后无反应

**解决方案：**
1. 安装 Visual C++ Redistributable
2. 检查Windows版本（需要Windows 10+）
3. 右键exe → 兼容性 → 以管理员身份运行

---

## 📖 详细文档

### 打包指南
- `WINDOWS_BUILD_GUIDE.md` - 完整的Windows打包指南

### 功能说明
- `README_COMPLETE.md` - 完整功能说明（所有版本）
- `FINAL_DELIVERY.md` - 完整交付文档

### 版本日志
- `CHANGELOG_v1.7.md` - v1.7功能说明
- `CHANGELOG_v1.6.md` - v1.6功能说明
- ... (其他版本)

---

## 🔄 跨平台打包

如果需要在多个平台上打包：

### Windows（本指南）
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

1. **打包时间**：首次打包需要5-10分钟，后续会更快
2. **缓存加速**：PyInstaller会缓存依赖，加快后续打包
3. **临时文件**：脚本会自动清理build和spec文件
4. **杀毒软件**：打包前暂时关闭，避免影响
5. **测试先打包**：建议先用 `python main.py` 测试是否能正常运行

---

## 🚀 快速测试

在打包前，可以先测试main.py：

```cmd
cd oppo-live-viewer
python main.py
```

如果main.py能正常运行，再进行打包。

---

**准备好了吗？在Windows上运行 `build_windows.bat` 即可打包！** 🎉

**打包完成后，你会在 `dist` 目录中找到 `OPPO-Live-Viewer.exe`！**
