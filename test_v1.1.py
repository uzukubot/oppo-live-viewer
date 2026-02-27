#!/usr/bin/env python3
"""
测试v1.1版本的解析和加载逻辑
"""

import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from main import OPPOLivePhoto, LivePhotoWidget

# 测试文件
test_file = "/home/yezichao/.openclaw/workspace/20260227-144315.live.jpeg"

if not Path(test_file).exists():
    print(f"❌ 测试文件不存在: {test_file}")
    sys.exit(1)

print("="*50)
print("测试 v1.1 改进功能")
print("="*50)

# 测试1：解析器
print("\n1. 测试解析器...")
try:
    photo = OPPOLivePhoto(test_file)
    if photo.parse():
        print("   ✅ 解析成功")
        print(f"   📸 JPEG大小: {len(photo.get_jpeg()) / 1024 / 1024:.2f} MB")
        print(f"   🎬 MP4大小: {len(photo.get_mp4()) / 1024 / 1024:.2f} MB")
    else:
        print("   ❌ 解析失败")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ 解析错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试2：LivePhotoWidget创建
print("\n2. 测试LivePhotoWidget创建...")
try:
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    widget = LivePhotoWidget()
    print("   ✅ LivePhotoWidget 创建成功")
except Exception as e:
    print(f"   ❌ 创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试3：加载照片
print("\n3. 测试加载照片...")
try:
    widget.load_photo(photo)
    print("   ✅ 照片加载成功")
except Exception as e:
    print(f"   ❌ 加载失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试4：循环控制
print("\n4. 测试循环控制...")
try:
    widget.set_loop_playback(False)
    print("   ✅ 关闭循环成功")

    widget.set_loop_playback(True)
    print("   ✅ 开启循环成功")
except Exception as e:
    print(f"   ❌ 循环控制失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试5：静音控制
print("\n5. 测试静音控制...")
try:
    widget.set_muted(False)
    print("   ✅ 关闭静音成功")

    widget.set_muted(True)
    print("   ✅ 开启静音成功")
except Exception as e:
    print(f"   ❌ 静音控制失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
print("✅ 所有测试通过！")
print("="*50)
print("\n如果仍然闪退，请检查GUI环境:")
print("  echo $DISPLAY")
print("如果为空，说明没有GUI环境")
