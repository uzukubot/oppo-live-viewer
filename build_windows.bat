@echo off
REM OPPO Live Photo Viewer - Windows 打包脚本

echo ==========================================
echo OPPO Live Photo Viewer - Windows 打包脚本
echo ==========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo 请先安装 Python 3.9 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python 已安装
echo.

REM 检查pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [警告] pip 可能未正确安装
    echo 尝试安装 pip...
    python -m ensurepip --upgrade
)

echo [OK] pip 可用
echo.

REM 进入脚本所在目录
cd /d "%~dp0"

echo ==========================================
echo 步骤 1/3: 安装依赖
echo ==========================================
echo.

echo 正在安装 PyQt6...
python -m pip install PyQt6 PyQt6-Qt-Multimedia PyQt6-Qt-MultimediaWidgets
if errorlevel 1 (
    echo [错误] PyQt6 安装失败
    pause
    exit /b 1
)
echo [OK] PyQt6 安装成功
echo.

echo 正在安装 PyInstaller...
python -m pip install pyinstaller
if errorlevel 1 (
    echo [错误] PyInstaller 安装失败
    pause
    exit /b 1
)
echo [OK] PyInstaller 安装成功
echo.

echo ==========================================
echo 步骤 2/3: 打包应用
echo ==========================================
echo.

echo 正在打包...
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py
if errorlevel 1 (
    echo [错误] 打包失败
    pause
    exit /b 1
)
echo [OK] 打包成功
echo.

echo ==========================================
echo 步骤 3/3: 清理临时文件
echo ==========================================
echo.

echo 正在清理临时文件...
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"
echo [OK] 临时文件清理完成
echo.

echo ==========================================
echo 打包完成！
echo ==========================================
echo.
echo 可执行文件位置: dist\OPPO-Live-Viewer.exe
echo.
echo 下一步:
echo   1. 进入 dist 目录
echo   2. 双击 OPPO-Live-Viewer.exe 运行
echo.
echo ==========================================
pause
