#!/usr/bin/env python3
"""
测试OPPO Live Photo解析器（独立版本，不依赖PyQt6）
"""


class OPPOLivePhoto:
    """OPPO Live Photo解析器"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.jpeg_data = None
        self.mp4_data = None
        self.mp4_offset = 0

    def parse(self):
        """解析Live Photo文件"""
        try:
            with open(self.filepath, "rb") as f:
                data = f.read()

            # 搜索MP4起始标记 'ftypmp42'
            mp4_marker = b"ftypmp42"
            offset = data.find(mp4_marker)

            if offset == -1:
                # 尝试其他可能的标记
                mp4_marker = b"ftypisom"
                offset = data.find(mp4_marker)

            if offset == -1:
                raise ValueError("未找到MP4数据标记，这不是有效的OPPO Live Photo文件")

            # 找到完整的MP4文件（前缀有一些box结构）
            # fyp前面可能有4字节的大小，所以回退4字节
            ftyp_offset = max(0, offset - 4)

            # 提取JPEG数据（MP4之前的数据）
            self.jpeg_data = data[:ftyp_offset]

            # 提取MP4数据（从ftyp开始到文件末尾）
            self.mp4_data = data[ftyp_offset:]
            self.mp4_offset = ftyp_offset

            return True

        except Exception as e:
            print(f"解析错误: {e}")
            return False

    def get_jpeg(self) -> bytes:
        """获取JPEG数据"""
        return self.jpeg_data

    def get_mp4(self) -> bytes:
        """获取MP4数据"""
        return self.mp4_data


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

        # 提取MP4到文件用于测试
        import tempfile

        temp_mp4 = "/tmp/test_live_video.mp4"
        with open(temp_mp4, "wb") as f:
            f.write(mp4_data)
        print(f"💾 MP4已保存到: {temp_mp4}")

        return True
    else:
        print("❌ 解析失败")
        return False


if __name__ == "__main__":
    from pathlib import Path

    success = test_parser()
    exit(0 if success else 1)
