#!/usr/bin/env python3
"""
测试修复后的OPPO Live Photo Viewer
"""

import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 测试导入
try:
    print("1. 测试模块导入...")
    from main import OPPOLivePhoto, LivePhotoWidget, MainWindow
    print("   ✅ 所有模块导入成功")
except Exception as e:
    print(f"   ❌ 导入失败: {e}")
    sys.exit(1)

# 测试解析器
print("\n2. 测试Live Photo解析器...")
test_file = "/home/yezichao/.openclaw/workspace/20260227-144315.live.jpeg"
if not Path(test_file).exists():
    print(f"   ❌ 测试文件不存在: {test_file}")
    sys.exit(1)

try:
    photo = OPPOLivePhoto(test_file)
    if photo.parse():
        print(f"   ✅ 解析成功")
        print(f"   📸 JPEG大小: {len(photo.get_jpeg()) / 1024 / 1024:.2f} MB")
        print(f"   🎬 MP4大小: {len(photo.get_mp4()) / 1024 / 1024:.2f} MB")
    else:
        print(f"   ❌ 解析失败")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ 解析错误: {e}")
    sys.exit(1)

# 测试GUI组件（不实际显示窗口）
print("\n3. 测试GUI组件初始化...")
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtMultimedia import QMediaPlayer

    # 创建应用实例
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # 测试播放器创建
    print("   测试QMediaPlayer...")
    player = QMediaPlayer()

    # 测试循环属性（这次应该成功了）
    print("   测试循环播放属性...")
    player.setLoops(QMediaPlayer.Loops.Infinite)
    print("   ✅ QMediaPlayer.Loops.Infinite 设置成功")

    # 测试LivePhotoWidget
    print("   测试LivePhotoWidget...")
    widget = LivePhotoWidget()
    print("   ✅ LivePhotoWidget 创建成功")

    # 测试加载照片
    print("   测试加载照片...")
    widget.load_photo(photo)
    print("   ✅ 照片加载成功")

except Exception as e:
    print(f"   ❌ GUI组件测试失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
print("✅ 所有测试通过！")
print("="*50)
print("\n修复后的可执行文件位置:")
print("dist/OPPO-Live-Viewer")
print("\n现在可以正常使用了！")
