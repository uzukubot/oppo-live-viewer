#!/usr/bin/env python3
"""
测试OPPO Live Photo解析器
"""

import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from main import OPPOLivePhoto


def test_parser():
    """测试解析器"""
    # 使用之前下载的测试文件
    test_file = "/home/yezichao/.openclaw/workspace/20260227-144315.live.jpeg"

    if not Path(test_file).exists():
        print("❌ 测试文件不存在")
        return False

    print(f"🔍 解析文件: {test_file}")

    photo = OPPOLivePhoto(test_file)

    if photo.parse():
        print("✅ 解析成功")

        # 检查JPEG数据
        jpeg_data = photo.get_jpeg()
        print(f"📸 JPEG数据大小: {len(jpeg_data) / 1024 / 1024:.2f} MB")

        # 检查MP4数据
        mp4_data = photo.get_mp4()
        print(f"🎬 MP4数据大小: {len(mp4_data) / 1024 / 1024:.2f} MB")
        print(f"📍 MP4偏移位置: {photo.mp4_offset} 字节")

        # 验证JPEG标记
        if jpeg_data[:2] == b"\xff\xd8":
            print("✅ JPEG格式验证通过")

        # 验证MP4标记
        if b"ftypmp42" in mp4_data or b"ftypisom" in mp4_data:
            print("✅ MP4格式验证通过")

        return True
    else:
        print("❌ 解析失败")
        return False


if __name__ == "__main__":
    success = test_parser()
    sys.exit(0 if success else 1)
