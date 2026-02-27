#!/bin/bash
# OPPO Live Photo Viewer - 简化打包脚本（假设依赖已安装）

set -e

echo "========================================="
echo "OPPO Live Photo Viewer - 打包脚本"
echo "========================================="
echo ""

# 进入脚本所在目录
cd "$(dirname "$0")"

# 检查Python和pip
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

# 打包
echo "📦 开始打包..."
pyinstaller --onefile --windowed --name="OPPO-Live-Viewer" main.py

echo ""
echo "✅ 打包完成！"
echo ""
echo "可执行文件: dist/OPPO-Live-Viewer"
echo ""
echo "使用方法:"
echo "  ./dist/OPPO-Live-Viewer"
echo ""
echo "========================================="
