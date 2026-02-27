#!/usr/bin/env python3
"""
OPPO Live Photo Viewer 打包脚本
使用PyInstaller创建跨平台可执行文件
"""

import subprocess
import sys
import platform


def build():
    """打包应用"""
    system = platform.system()

    if system == "Darwin":
        print("🍎 检测到 macOS")
        icon = ""  # macOS 使用 .icns
    elif system == "Windows":
        print("🪟 检测到 Windows")
        icon = "--icon=app.ico"
    else:
        print("🐧 检测到 Linux")
        icon = ""

    # PyInstaller命令
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=OPPO-Live-Viewer",
        f"--add-data=main.py:.",
    ]

    if icon:
        cmd.append(icon)

    cmd.append("main.py")

    print(f"📦 执行打包命令: {' '.join(cmd)}")

    # 检查是否安装了PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("⚠️  PyInstaller 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)

    # 执行打包
    result = subprocess.run(cmd, check=False)

    if result.returncode == 0:
        print(f"✅ 打包成功！可执行文件在: dist/")
    else:
        print("❌ 打包失败")
        sys.exit(1)


if __name__ == '__main__':
    build()
