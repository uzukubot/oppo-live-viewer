#!/bin/bash
# 直接运行源码（需要Python和GUI支持）

echo "🚀 OPPO Live Photo Viewer - 源码运行"
echo ""

cd "$(dirname "$0")"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi

# 尝试运行PyQt6版本
echo "📦 尝试运行 PyQt6 版本..."
python3 main.py 2>&1 | head -5

if [ $? -eq 0 ]; then
    echo "✅ PyQt6 版本运行成功"
    exit 0
fi

# 如果PyQt6失败，尝试tkinter版本
echo "⚠️  PyQt6 不可用，尝试运行 Tkinter 版本..."
python3 main_tkinter.py

if [ $? -eq 0 ]; then
    echo "✅ Tkinter 版本运行成功"
    exit 0
fi

echo "❌ 两个版本都无法运行，请检查GUI支持"
echo ""
echo "可能的解决方案："
echo "  1. 安装 PyQt6: pip install PyQt6 PyQt6-Qt-Multimedia"
echo "  2. 安装 tkinter: sudo apt-get install python3-tk"
echo ""
echo "或者使用打包脚本创建独立可执行文件"
