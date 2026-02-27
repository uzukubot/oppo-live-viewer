#!/bin/bash
# OPPO Live Photo Viewer - 自动安装和打包脚本

set -e

echo "========================================="
echo "OPPO Live Photo Viewer - 安装和打包脚本"
echo "========================================="
echo ""

# 检查是否为root或有sudo权限
if [ "$EUID" -ne 0 ]; then
    echo "⚠️  此脚本需要管理员权限来安装系统依赖"
    echo "请使用: sudo ./install_and_build.sh"
    exit 1
fi

echo "📦 步骤 1: 安装系统依赖..."
apt-get update -qq
apt-get install -y python3-pip python3-venv python3-dev build-essential libgstreamer1.0-dev \
    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
    libglib2.0-dev libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev

echo ""
echo "📦 步骤 2: 创建虚拟环境..."
cd "$(dirname "$0")"
python3 -m venv venv
source venv/bin/activate

echo ""
echo "📦 步骤 3: 安装Python依赖..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install pyinstaller

echo ""
echo "📦 步骤 4: 开始打包..."
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" --add-data="main.py:." main.py

echo ""
echo "✅ 打包完成！"
echo ""
echo "可执行文件位置: dist/OPPO-Live-Viewer"
echo ""
echo "使用方法："
echo "  cd dist"
echo "  ./OPPO-Live-Viewer"
echo ""
echo "或者直接双击 dist/OPPO-Live-Viewer 文件"
echo ""
echo "========================================="
