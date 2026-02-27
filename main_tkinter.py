#!/usr/bin/env python3
"""
OPPO Live Photo Viewer - Tkinter版本
无需额外依赖，使用Python内置库
"""

import os
import platform
import subprocess
import sys
import tempfile
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


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
                raise ValueError("未找到MP4数据标记")

            # 找到完整的MP4文件
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


class LivePhotoApp:
    """Live Photo查看器主窗口"""

    def __init__(self, root):
        self.root = root
        self.root.title("OPPO Live Photo Viewer")
        self.root.geometry("1000x700")

        self.current_photo = None
        self.temp_jpeg = None
        self.temp_mp4 = None

        self.setup_ui()

    def setup_ui(self):
        """设置UI"""
        # 主布局
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左侧面板
        left_frame = ttk.Frame(main_paned, width=250)
        main_paned.add(left_frame)

        # 右侧面板
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame)

        # 左侧内容
        self.setup_left_panel(left_frame)

        # 右侧内容
        self.setup_right_panel(right_frame)

        # 初始化拖放（仅支持部分平台）
        self.setup_drag_drop()

    def setup_left_panel(self, parent):
        """设置左侧面板"""
        # 标题
        title = ttk.Label(parent, text="文件列表", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        # 按钮
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(btn_frame, text="打开文件", command=self.open_file).pack(
            fill=tk.X, pady=2
        )
        ttk.Button(btn_frame, text="打开文件夹", command=self.open_folder).pack(
            fill=tk.X, pady=2
        )

        # 文件列表
        list_frame = ttk.Frame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.file_listbox.bind("<<ListboxSelect>>", self.on_file_selected)

        scrollbar.config(command=self.file_listbox.yview)

    def setup_right_panel(self, parent):
        """设置右侧面板"""
        # 图片显示区域
        self.image_label = tk.Label(
            parent, text="请选择一个Live Photo文件", bg="#f0f0f0"
        )
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 控制按钮
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(control_frame, text="播放Live视频", command=self.play_video).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(control_frame, text="查看静态图", command=self.show_static).pack(
            side=tk.LEFT, padx=5
        )

        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN)
        status_label.pack(fill=tk.X, padx=5, pady=5)

    def setup_drag_drop(self):
        """设置拖放（仅支持部分平台）"""
        # Tkinter原生不支持跨平台拖放，需要使用第三方库
        # 这里简化处理，只提供按钮打开
        pass

    def open_file(self):
        """打开文件"""
        file_path = filedialog.askopenfilename(
            title="选择Live Photo文件",
            filetypes=[
                ("Live Photo", "*.live.jpeg"),
                ("JPEG", "*.jpeg *.jpg"),
                ("所有文件", "*.*"),
            ],
        )

        if file_path:
            self.load_photo(file_path)

    def open_folder(self):
        """打开文件夹"""
        folder_path = filedialog.askdirectory(title="选择文件夹")

        if folder_path:
            self.scan_folder(folder_path)

    def scan_folder(self, folder_path):
        """扫描文件夹"""
        self.file_listbox.delete(0, tk.END)

        folder = Path(folder_path)
        patterns = ["*.live.jpeg", "*.jpeg", "*.jpg"]

        for pattern in patterns:
            for file_path in sorted(folder.glob(pattern)):
                self.file_listbox.insert(tk.END, str(file_path))

        count = self.file_listbox.size()
        self.status_var.set(f"找到 {count} 个文件")

    def on_file_selected(self, event):
        """文件被选中"""
        selection = self.file_listbox.curselection()
        if selection:
            file_path = self.file_listbox.get(selection[0])
            self.load_photo(file_path)

    def load_photo(self, file_path):
        """加载Live Photo"""
        try:
            photo = OPPOLivePhoto(file_path)
            if photo.parse():
                self.current_photo = photo
                self.status_var.set(f"已加载: {Path(file_path).name}")
                self.show_static()
            else:
                messagebox.showerror("错误", "无法解析Live Photo文件")
        except Exception as e:
            messagebox.showerror("错误", f"加载失败: {str(e)}")

    def show_static(self):
        """显示静态图片"""
        if not self.current_photo:
            return

        try:
            jpeg_data = self.current_photo.get_jpeg()

            # 保存到临时文件
            if self.temp_jpeg and os.path.exists(self.temp_jpeg):
                os.unlink(self.temp_jpeg)

            self.temp_jpeg = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            self.temp_jpeg.write(jpeg_data)
            self.temp_jpeg.close()

            # 使用PIL加载图片（如果可用）
            try:
                from PIL import Image, ImageTk

                image = Image.open(self.temp_jpeg.name)

                # 缩放图片适应窗口
                width = self.image_label.winfo_width() - 20
                height = self.image_label.winfo_height() - 20
                if width > 100 and height > 100:
                    image.thumbnail((width, height), Image.Resampling.LANCZOS)

                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo  # 保持引用
            except ImportError:
                # PIL不可用，使用外部查看器
                self.image_label.config(
                    image="", text="静态图片已加载，点击下方按钮使用外部查看器打开"
                )

        except Exception as e:
            self.image_label.config(text=f"加载图片失败: {str(e)}")

    def play_video(self):
        """播放视频"""
        if not self.current_photo:
            return

        try:
            mp4_data = self.current_photo.get_mp4()

            # 保存到临时文件
            if self.temp_mp4 and os.path.exists(self.temp_mp4):
                os.unlink(self.temp_mp4)

            self.temp_mp4 = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            self.temp_mp4.write(mp4_data)
            self.temp_mp4.close()

            # 使用系统默认播放器打开
            self.status_var.set("正在播放视频...")
            system = platform.system()

            if system == "Linux":
                subprocess.run(["xdg-open", self.temp_mp4.name], check=True)
            elif system == "Windows":
                os.startfile(self.temp_mp4.name)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", self.temp_mp4.name], check=True)

        except Exception as e:
            messagebox.showerror("错误", f"播放视频失败: {str(e)}")

    def on_closing(self):
        """关闭窗口时的清理"""
        if self.temp_jpeg and os.path.exists(self.temp_jpeg):
            os.unlink(self.temp_jpeg)
        if self.temp_mp4 and os.path.exists(self.temp_mp4):
            os.unlink(self.temp_mp4)
        self.root.destroy()


def main():
    """主函数"""
    root = tk.Tk()
    app = LivePhotoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
