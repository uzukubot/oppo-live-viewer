#!/bin/bash
# OPPO Live Photo Viewer 启动脚本

cd "$(dirname "$0")"

echo "🚀 启动 OPPO Live Photo Viewer..."
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.9 或更高版本"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  PyQt6 未安装，正在安装依赖..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 安装依赖失败"
        exit 1
    fi
fi

# 运行程序
echo "✅ 启动程序..."
python3 main.py
