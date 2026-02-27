@echo off
REM OPPO Live Photo Viewer 启动脚本 (Windows)

cd /d "%~dp0"

echo 🚀 启动 OPPO Live Photo Viewer...
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo 请先安装 Python 3.9 或更高版本
    pause
    exit /b 1
)

REM 检查依赖
echo 📦 检查依赖...
python -c "import PyQt6" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyQt6 未安装，正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 安装依赖失败
        pause
        exit /b 1
    )
)

REM 运行程序
echo ✅ 启动程序...
python main.py
pause
