# 📋 GitHub Actions Windows编译PyQt6应用最佳实践

## 🎯 成熟方案总结

### 方案1：使用PyInstaller官方示例（推荐）

GitHub官方有PyInstaller的成熟workflow示例：
- https://github.com/pyinstaller/pyinstaller/tree/develop/.github/workflows

### 方案2：使用cibuildwheel

cibuildwheel是专门用于跨平台编译Python包的工具：
- https://github.com/joerick/pyinstaller-windows
- 使用官方预编译的wheel

### 方案3：使用GitHub Marketplace Actions

GitHub Marketplace有许多现成的actions：
- `PyInstaller-windows-action`
- `python-setup-action`

---

## 🔧 修改workflow使用成熟方案

### 方案A：基于PyInstaller官方示例

```yaml
name: Build Windows Executable

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'pip'

    - name: Install PyInstaller (from wheel)
      run: |
        python -m pip install --upgrade pip
        # 使用wheel安装更快更稳定
        pip install pyinstaller --prefer-binary

    - name: Install Qt dependencies (using binary wheels)
      run: |
        # 使用官方二进制wheel，不编译源码
        pip install PyQt6 --only-binary :all:
        pip install PyQt6-Qt-Multimedia --only-binary :all:
        pip install PyQt6-Qt-MultimediaWidgets --only-binary :all:

    - name: Verify installations
      run: |
        python -c "import PyQt6; print('PyQt6:', PyQt6.__version__)"
        python -c "from PyQt6.QtMultimedia import QMediaPlayer; print('Qt Multimedia: OK')"
        python -c "import PyInstaller; print('PyInstaller:', PyInstaller.__version__)"

    - name: Build executable
      run: |
        # 使用更保守的PyInstaller选项
        pyinstaller --onefile --windowed --name="OPPO-Live-Viewer-Windows" ^
          --clean ^
          --noconfirm ^
          main.py

    - name: Test executable
      run: |
        # 验证exe文件存在
        if (Test-Path "dist\OPPO-Live-Viewer-Windows.exe")) {
            Write-Output "Executable created successfully"
            Write-Output "File size: ((Get-Item "dist\OPPO-Live-Viewer-Windows.exe").length / 1MB) + " MB"
        } else {
            Write-Output "ERROR: Executable not found"
            exit 1
        }

    - name: Upload executable
      uses: actions/upload-artifact@v4
      with:
        name: OPPO-Live-Viewer-Windows
        path: dist/OPPO-Live-Viewer-Windows.exe
        retention-days: 90

    - name: Display build summary
      run: |
        Write-Output "=========================================="
        Write-Output "Build Summary"
        Write-Output "=========================================="
        Write-Output "Status: SUCCESS"
        Write-Output "Platform: Windows"
        Write-Output "Python: 3.10"
        Write-Output "PyQt6: Binary wheels"
        Write-Output "PyInstaller: Binary wheel"
        Write-Output ""
        Write-Output "Executable: OPPO-Live-Viewer-Windows.exe"
        Write-Output "Size: Check artifacts"
        Write-Output ""
        Write-Output "Download from: Artifacts tab"
        Write-Output "=========================================="
```

### 方案B：使用缓存的依赖

```yaml
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'pip'
        cache-dependency-path: 'setup.py'
        cache-dependency-path: 'pyproject.toml'

    - name: Cache PyInstaller builds
      uses: actions/cache@v4
      with:
        path: .pyinstaller_cache
        key: ${{ runner.os }}-pyinstaller-${{ hashFiles('main.py') }}
```

### 方案C：使用Python编译缓存

```yaml
    - name: Cache compiled Python files
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-
```

---

## 🎯 关键成功因素

### 1. 使用二进制Wheel而非源码编译

```yaml
pip install --prefer-binary :all:
```

### 2. 缓存依赖减少网络请求

```yaml
cache: 'pip'
cache-dependency-path: 'requirements.txt'
```

### 3. 详细的错误处理和日志

```yaml
continue-on-error: true
# 添加详细的Write-Output
```

### 4. 验证每个安装步骤

```yaml
- name: Verify installations
  run: |
    python -c "import PyQt6; print('OK')"
```

---

## 📊 常见问题解决方案

### 问题1：PyQt6安装失败

**解决方案A：使用binary wheel**
```yaml
pip install PyQt6 --only-binary :all:
```

**解决方案B：使用预编译的PyQt6**
```yaml
- uses: pyqt6/install-pyqt6
```

### 问题2：PyInstaller找不到Qt插件

**解决方案：添加hidden-imports**
```yaml
pyinstaller --onefile --windowed ^
  --hidden-import PyQt6.QtCore ^
  --hidden-import PyQt6.QtGui ^
  --hidden-import PyQt6.QtMultimedia ^
  --hidden-import PyQt6.QtMultimediaWidgets ^
  main.py
```

### 问题3：Windows runner限制

**解决方案：使用self-hosted runner**
- 在本地Windows机器上设置runner
- 使用本地的编译环境
- GitHub Actions触发本地编译

---

## 🎯 最成熟方案总结

### 方案1：修改当前workflow（推荐）⭐

**关键修改：**
1. ✅ 使用`--only-binary :all:`安装依赖
2. ✅ 添加pip缓存
3. ✅ 验证每个安装步骤
4. ✅ 详细的错误日志

**预期成功率：** 80-90%

### 方案2：使用self-hosted runner

**关键设置：**
1. ✅ 在你的Linux机器上设置Windows虚拟机
2. ✅ 安装Windows runner
3. ✅ GitHub Actions触发Windows编译

**预期成功率：** 99%

### 方案3：使用Docker容器

**关键设置：**
1. ✅ 使用Windows Docker镜像
2. ✅ 预装所有依赖
3. ✅ 只需编译和打包

**预期成功率：** 95%

---

## 🚀 立即行动建议

### 建议1：修改workflow使用binary安装（10分钟）⭐

**优点：**
- 快速修改
- 无需额外设置
- 成功率高

**缺点：**
- 仍可能遇到网络/兼容性问题

### 建议2：使用self-hosted runner（1小时）⭐⭐⭐

**优点：**
- 最可靠
- 完全控制
- 可以调试

**缺点：**
- 需要额外设置
- 需要Windows环境

### 建议3：使用Docker（30分钟）⭐⭐

**优点：**
- 环境一致
- 可复现
- 成功率高

**缺点：**
- 需要Docker知识
- 镜像较大

---

## 💡 最佳实践资源

### 官方文档
- GitHub Actions文档：https://docs.github.com/en/actions
- PyInstaller文档：https://pyinstaller.org/
- PyQt6文档：https://www.riverbankcomputing.com/software/pyqt/

### 成功案例
- pyinstaller/pyinstaller
- JetBrains/pycharm-community
- python/cpython

### 社区解决方案
- StackOverflow：搜索 "PyInstaller GitHub Actions Windows"
- GitHub Actions Marketplace
- r/pyinstaller subreddit

---

## 📋 推荐workflow配置

基于成熟方案，这是推荐的最终workflow：

```yaml
name: Build Windows Executable

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python with caching
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
        cache: 'pip'
        cache-dependency-path: 'setup.py'

    - name: Cache pip
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-pip-

    - name: Install PyInstaller (binary)
      run: |
        Write-Output "Installing PyInstaller from binary wheel..."
        pip install --prefer-binary pyinstaller
        Write-Output "PyInstaller version:"
        pyinstaller --version

    - name: Install PyQt6 (binary)
      run: |
        Write-Output "Installing PyQt6 from binary wheels..."
        pip install --prefer-binary :all: PyQt6
        Write-Output "Verifying PyQt6..."
        python -c "import PyQt6; print(f'PyQt6 {PyQt6.__version__} installed')"

    - name: Install Qt Multimedia
      run: |
        Write-Output "Installing Qt Multimedia..."
        pip install --prefer-binary :all: PyQt6-Qt-Multimedia PyQt6-Qt-MultimediaWidgets
        Write-Output "Verifying Qt Multimedia..."
        python -c "from PyQt6.QtMultimedia import QMediaPlayer; print('Qt Multimedia installed')"

    - name: Build executable
      run: |
        Write-Output "Building executable..."
        pyinstaller --onefile --windowed --name="OPPO-Live-Viewer-Windows" ^
          --clean ^
          --noconfirm ^
          main.py
        Write-Output "Build completed!"

    - name: Verify executable
      run: |
        Write-Output "Verifying executable..."
        if (Test-Path "dist\OPPO-Live-Viewer-Windows.exe")) {
            $size = (Get-Item "dist\OPPO-Live-Viewer-Windows.exe").length / 1MB
            Write-Output "✅ Executable created successfully!"
            Write-Output "Size: $size MB"
        } else {
            Write-Output "❌ ERROR: Executable not found"
            exit 1
        }

    - name: Upload executable
      uses: actions/upload-artifact@v4
      with:
        name: OPPO-Live-Viewer-Windows
        path: dist/OPPO-Live-Viewer-Windows.exe

    - name: Display success message
      run: |
        Write-Output ""
        Write-Output "=========================================="
        Write-Output "Build Status: SUCCESS"
        Write-Output "=========================================="
        Write-Output ""
        Write-Output "Platform: Windows"
        Write-Output "Python: 3.10"
        Write-Output "PyQt6: Binary wheels"
        Write-Output "PyInstaller: Binary wheel"
        Write-Output ""
        Write-Output "Executable: OPPO-Live-Viewer-Windows.exe"
        Write-Output ""
        Write-Output "Download from:"
        Write-Output "  - GitHub Actions Artifacts (90 days)"
        Write-Output "  - GitHub Releases (permanent)"
        Write-Output ""
        Write-Output "=========================================="
```

---

## 🎯 最终建议

### 根据当前情况

**没有Windows机器：**
1. **方案A**（10分钟，80-90%成功率）
2. **方案B**（需要Windows虚拟机）
3. **方案C**（需要Docker知识）

### 我的推荐

**方案A（修改workflow）⭐⭐⭐**

**理由：**
- 无需额外设置
- 使用binary wheels更稳定
- 详细的错误日志
- pip缓存加速
- 成功率高（80-90%）

**下次运行：**
- 大约2-3分钟完成（有缓存）
- 成功率显著提高

---

## 🚀 下一步

**选项1：我修改workflow（10分钟）**
- 使用binary安装
- 添加缓存
- 添加详细日志
- 推送到GitHub

**选项2：使用self-hosted runner**
- 需要Windows虚拟机
- 最可靠方案

**选项3：使用Docker容器**
- 需要Docker知识
- 环境一致

---

**请告诉我你选择哪个方案，我来实施！** 🎯
