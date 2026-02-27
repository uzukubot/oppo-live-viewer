#!/usr/bin/env python3
"""
OPPO Live Photo Viewer
跨平台OPPO Live Photo查看器
支持macOS/Windows/Linux
"""

import os
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image
from PyQt6.QtCore import Qt, QTimer, QUrl, pyqtSignal
from PyQt6.QtGui import (
    QAction,
    QColor,
    QDragEnterEvent,
    QDropEvent,
    QImage,
    QKeySequence,
    QPixmap,
    QShortcut,
)
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


class OPPOLivePhoto:
    """OPPO Live Photo解析器"""

    def __init__(self, filepath):
        self.filepath = filepath
        self.jpeg_data = None
        self.mp4_data = None
        self.mp4_offset = 0
        self.is_live = False  # 是否是Live Photo

    def parse(self):
        """解析Live Photo文件或普通图片"""
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

            if offset != -1:
                # 找到MP4标记，这是Live Photo
                self.is_live = True

                # 找到完整的MP4文件
                ftyp_offset = max(0, offset - 4)

                # 提取JPEG数据（MP4之前的数据）
                self.jpeg_data = data[:ftyp_offset]

                # 提取MP4数据（从ftyp开始到文件末尾）
                self.mp4_data = data[ftyp_offset:]
                self.mp4_offset = ftyp_offset
            else:
                # 没有找到MP4标记，这是普通图片
                self.is_live = False
                self.jpeg_data = data
                self.mp4_data = None

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

    def is_live_photo(self) -> bool:
        """是否是Live Photo"""
        return self.is_live


def smart_scale_pixmap(jpeg_data: bytes, target_size: tuple) -> QPixmap:
    """
    智能缩放图片：
    - 缩小时使用 Mitchell 算法（更平滑，适合缩略图）
    - 放大时使用 Lanczos3 算法（更锐利，适合放大显示）
    """
    # 使用 Pillow 加载图片
    img = Image.open(BytesIO(jpeg_data))

    # 转换为 RGB 模式（处理 RGBA 等）
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    orig_width, orig_height = img.size
    target_width, target_height = target_size

    # 计算保持宽高比的目标尺寸
    ratio = min(target_width / orig_width, target_height / orig_height)
    new_width = int(orig_width * ratio)
    new_height = int(orig_height * ratio)

    # 选择缩放算法
    if new_width < orig_width or new_height < orig_height:
        # 缩小：使用 Mitchell 算法
        resample = Image.Resampling.BICUBIC  # Mitchell 近似
    else:
        # 放大：使用 Lanczos 算法
        resample = Image.Resampling.LANCZOS

    # 缩放图片
    scaled_img = img.resize((new_width, new_height), resample)

    # 转换为 QPixmap
    data = scaled_img.tobytes("raw", "RGB")
    qimage = QImage(data, new_width, new_height, new_width * 3, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(qimage)


class LivePhotoWidget(QWidget):
    """Live Photo展示组件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_photo = None
        self.is_playing = False
        self.auto_play = True  # 默认自动播放

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 使用StackedWidget在静态图和视频之间切换
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # 静态图片标签
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #1e1e1e;")
        self.stack.addWidget(self.image_label)

        # 视频播放器
        self.video_widget = QVideoWidget()
        self.stack.addWidget(self.video_widget)

        # 媒体播放器
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

        # 默认不循环
        self.player.setLoops(QMediaPlayer.Loops.Once)

        # 连接信号
        self.player.positionChanged.connect(self.on_position_changed)
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)

        # 自动播放定时器
        self.play_timer = QTimer()
        self.play_timer.setSingleShot(True)
        self.play_timer.timeout.connect(self.start_video)

    def load_photo(self, photo: OPPOLivePhoto):
        """加载Live Photo或普通图片"""
        self.current_photo = photo

        # 加载JPEG
        jpeg_data = photo.get_jpeg()
        if jpeg_data:
            try:
                scaled_pixmap = smart_scale_pixmap(
                    jpeg_data, 
                    (self.image_label.width(), self.image_label.height())
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.image_label.setText("")
            except Exception as e:
                self.image_label.setText(f"无法加载图片: {e}")
        else:
            self.image_label.setText("无法加载图片")

        # 加载MP4（只有Live Photo才有）
        mp4_data = photo.get_mp4()
        if mp4_data:
            # 保存到临时文件用于播放
            import tempfile

            self.temp_mp4 = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            self.temp_mp4.write(mp4_data)
            self.temp_mp4.close()

            self.player.setSource(QUrl.fromLocalFile(self.temp_mp4.name))
        else:
            self.player.setSource(QUrl())

        # 显示静态图
        self.stack.setCurrentIndex(0)
        self.is_playing = False

        # 如果是Live Photo且启用了自动播放，延迟启动视频
        if photo.is_live_photo() and self.auto_play:
            self.play_timer.start(500)  # 500ms后自动播放

    def start_video(self):
        """开始播放视频"""
        if self.current_photo and self.current_photo.get_mp4():
            self.stack.setCurrentIndex(1)
            self.player.play()
            self.is_playing = True

    def stop_video(self):
        """停止视频，显示静态图"""
        if self.is_playing:
            self.player.stop()
            self.stack.setCurrentIndex(0)
            self.is_playing = False

    def toggle_live(self):
        """切换Live效果"""
        if self.is_playing:
            self.stop_video()
        else:
            self.start_video()

    def set_loop_playback(self, loop: bool):
        """设置循环播放"""
        if loop:
            self.player.setLoops(QMediaPlayer.Loops.Infinite)
        else:
            self.player.setLoops(QMediaPlayer.Loops.Once)

    def set_muted(self, muted: bool):
        """设置静音"""
        self.audio_output.setMuted(muted)

    def on_position_changed(self, position):
        """位置改变时保持显示"""
        pass

    def on_media_status_changed(self, status):
        """媒体状态改变"""
        # 当媒体播放完成且不循环时，切换回静态图
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.stop_video()

    def resizeEvent(self, event):
        """窗口大小改变时重新缩放图片"""
        super().resizeEvent(event)
        if self.current_photo and not self.is_playing:
            # 重新加载并缩放静态图
            jpeg_data = self.current_photo.get_jpeg()
            if jpeg_data:
                try:
                    scaled_pixmap = smart_scale_pixmap(
                        jpeg_data,
                        (self.image_label.width(), self.image_label.height())
                    )
                    self.image_label.setPixmap(scaled_pixmap)
                except Exception:
                    pass


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OPPO Live Photo Viewer")
        self.setGeometry(100, 100, 1200, 800)
        self.current_folder = None  # 当前文件夹路径
        self.current_files = {}  # 文件名到完整路径的映射
        self.dark_mode = False  # 深色模式
        self.is_left_panel_visible = True  # 左侧面板可见性
        self.left_panel_original_width = 300  # 左侧面板原始宽度
        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        """设置UI"""
        # 中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QHBoxLayout(central_widget)

        # 分割器
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)

        # 左侧：文件列表
        left_panel = self.create_file_panel()
        self.left_panel = left_panel
        self.splitter.addWidget(left_panel)

        # 右侧：图片展示和控制
        right_panel = self.create_right_panel()
        self.splitter.addWidget(right_panel)

        # 设置分割器比例
        self.splitter.setSizes([300, 900])

        # 状态栏
        self.statusBar().showMessage("就绪")

        # 设置拖放
        self.setAcceptDrops(True)

    def create_file_panel(self) -> QWidget:
        """创建文件面板"""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # 标题
        title = QLabel("文件列表")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        layout.addWidget(title)

        # 文件夹路径标签
        self.folder_path_label = QLabel("当前文件夹: 未选择")
        self.folder_path_label.setStyleSheet(
            "font-size: 11px; color: #666666; padding: 5px;"
        )
        self.folder_path_label.setWordWrap(True)
        layout.addWidget(self.folder_path_label)

        # 按钮
        button_layout = QHBoxLayout()

        open_btn = QPushButton("打开文件")
        open_btn.clicked.connect(self.open_file)
        layout.addWidget(open_btn)

        open_folder_btn = QPushButton("打开文件夹")
        open_folder_btn.clicked.connect(self.open_folder)
        layout.addWidget(open_folder_btn)

        layout.addLayout(button_layout)

        # 文件列表
        self.file_list = QListWidget()
        self.file_list.currentItemChanged.connect(self.on_file_selected)
        layout.addWidget(self.file_list)

        return panel

    def create_right_panel(self) -> QWidget:
        """创建右侧面板"""
        panel = QFrame()
        panel.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # 顶部工具栏（包含折叠按钮和Live指示器）
        top_bar = QWidget()
        top_bar.setObjectName("top_bar")  # 添加objectName用于主题切换
        top_bar.setFixedHeight(40)
        top_bar.setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(10, 0, 10, 0)

        # 折叠按钮
        self.collapse_button = QPushButton("◀")
        self.collapse_button.setFixedSize(30, 30)
        self.collapse_button.clicked.connect(self.toggle_left_panel)
        self.collapse_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #ffffff;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """
        )
        top_bar_layout.addWidget(self.collapse_button)

        # Live指示器
        self.live_label = QLabel("❌ Live Photo")
        self.live_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        top_bar_layout.addWidget(self.live_label)
        top_bar_layout.addStretch()

        # 深色模式切换提示
        self.theme_hint = QLabel("按 D 键切换主题")
        self.theme_hint.setStyleSheet("font-size: 11px; color: #888888;")
        top_bar_layout.addWidget(self.theme_hint)

        layout.addWidget(top_bar)

        # 图片展示组件
        self.photo_widget = LivePhotoWidget()
        layout.addWidget(self.photo_widget)

        # 底部控制栏（固定高度）
        bottom_bar = QWidget()
        bottom_bar.setObjectName("bottom_bar")  # 添加objectName用于主题切换
        bottom_bar.setFixedHeight(40)
        bottom_bar.setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")
        bottom_bar_layout = QHBoxLayout(bottom_bar)
        bottom_bar_layout.setContentsMargins(10, 0, 10, 0)

        # 循环播放checkbox
        self.loop_checkbox = QCheckBox("循环播放")
        self.loop_checkbox.setChecked(False)  # 默认不循环
        self.loop_checkbox.stateChanged.connect(self.on_loop_changed)
        bottom_bar_layout.addWidget(self.loop_checkbox)

        # 静音checkbox
        self.mute_checkbox = QCheckBox("静音")
        self.mute_checkbox.setChecked(False)  # 默认不静音
        self.mute_checkbox.stateChanged.connect(self.on_mute_changed)
        bottom_bar_layout.addWidget(self.mute_checkbox)

        bottom_bar_layout.addStretch()

        layout.addWidget(bottom_bar)

        return panel

    def update_live_indicator(self, is_live: bool):
        """更新Live指示器"""
        if is_live:
            self.live_label.setText("✅ Live Photo")
            self.live_label.setStyleSheet(
                "color: #2e7d32; font-size: 14px; font-weight: bold;"
            )
            self.loop_checkbox.setEnabled(True)
            self.mute_checkbox.setEnabled(True)
        else:
            self.live_label.setText("❌ Live Photo")
            self.live_label.setStyleSheet(
                "color: #757575; font-size: 14px; font-weight: bold;"
            )
            self.loop_checkbox.setEnabled(False)
            self.mute_checkbox.setEnabled(False)

    def on_loop_changed(self, state):
        """循环播放改变"""
        loop = state == Qt.CheckState.Checked.value
        self.photo_widget.set_loop_playback(loop)
        # 如果当前正在播放，重新加载当前文件以使设置生效
        if self.photo_widget.current_photo:
            self.reload_current_photo()

    def reload_current_photo(self):
        """重新加载当前显示的图片"""
        if self.photo_widget.current_photo:
            # 保存当前的播放状态
            was_playing = self.photo_widget.is_playing

            # 如果正在播放，先停止
            if was_playing:
                self.photo_widget.stop_video()

            # 重新加载
            self.photo_widget.load_photo(self.photo_widget.current_photo)

    def on_mute_changed(self, state):
        """静音改变"""
        muted = state == Qt.CheckState.Checked.value
        self.photo_widget.set_muted(muted)

    def open_file(self):
        """打开单个文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片文件",
            "",
            "所有图片 (*.live.jpeg *.jpeg *.jpg);;所有文件 (*.*)",
        )

        if file_path:
            self.load_photo(file_path)

    def open_folder(self):
        """打开文件夹"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")

        if folder_path:
            self.scan_folder(folder_path)

    def scan_folder(self, folder_path):
        """扫描文件夹中的图片"""
        self.file_list.clear()
        self.current_files.clear()
        self.current_folder = Path(folder_path)

        # 更新文件夹路径标签
        self.folder_path_label.setText(f"当前文件夹: {self.current_folder}")

        # 查找所有可能的图片文件
        patterns = ["*.live.jpeg", "*.jpeg", "*.jpg"]

        for pattern in patterns:
            for file_path in sorted(self.current_folder.glob(pattern)):
                # 只显示文件名
                filename = file_path.name
                # 创建列表项，存储完整路径在数据中
                item = self.file_list.addItem(filename)
                self.current_files[filename] = str(file_path)

        if self.file_list.count() > 0:
            self.statusBar().showMessage(f"找到 {self.file_list.count()} 个文件")
        else:
            self.statusBar().showMessage("未找到文件")

    def on_file_selected(self, current_item, previous_item=None):
        """文件被选中（支持鼠标点击和键盘操作）"""
        # 如果没有选中项（例如清空列表），不做处理
        if current_item is None:
            return

        filename = current_item.text()
        # 从映射中获取完整路径
        if filename in self.current_files:
            file_path = self.current_files[filename]
            self.load_photo(file_path)
        else:
            # 如果映射中没有，使用完整路径（向后兼容）
            self.load_photo(filename)

    def load_photo(self, file_path):
        """加载图片（Live Photo或普通图片）"""
        try:
            photo = OPPOLivePhoto(file_path)
            if photo.parse():
                self.photo_widget.load_photo(photo)
                self.update_live_indicator(photo.is_live_photo())
                self.statusBar().showMessage(f"已加载: {Path(file_path).name}")
            else:
                QMessageBox.warning(self, "错误", "无法解析图片文件")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载失败: {str(e)}")

    def dragEnterEvent(self, event: QDragEnterEvent):
        """拖拽进入"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """拖拽放下"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if os.path.isfile(file_path):
                self.load_photo(file_path)

    def toggle_left_panel(self):
        """切换左侧面板显示/隐藏"""
        if self.is_left_panel_visible:
            # 隐藏左侧面板
            self.left_panel_original_width = self.splitter.sizes()[0]
            self.splitter.setSizes([0, self.width()])
            self.collapse_button.setText("▶")
            self.is_left_panel_visible = False
        else:
            # 显示左侧面板
            self.splitter.setSizes(
                [
                    self.left_panel_original_width,
                    self.width() - self.left_panel_original_width,
                ]
            )
            self.collapse_button.setText("◀")
            self.is_left_panel_visible = True

    def setup_shortcuts(self):
        """设置快捷键"""
        # D键切换深色/浅色模式
        self.theme_shortcut = QShortcut(QKeySequence("D"), self)
        self.theme_shortcut.activated.connect(self.toggle_theme)

    def wheelEvent(self, event):
        """鼠标滚轮事件 - 在文件夹内切换文件"""
        # 只有在文件列表有内容时才响应
        if self.file_list.count() == 0:
            super().wheelEvent(event)
            return

        # 检测鼠标位置是否在文件列表区域内
        cursor_pos = self.mapFromGlobal(self.cursor().pos())
        list_rect = self.left_panel.rect()

        # 如果鼠标在左侧面板区域内，让列表自己处理滚动
        if list_rect.contains(cursor_pos):
            super().wheelEvent(event)
            return

        # 获取当前选中行
        current_row = self.file_list.currentRow()

        # 根据滚轮方向切换文件
        # 滚轮向上（delta > 0）: 上一张
        # 滚轮向下（delta < 0）: 下一张
        delta = event.angleDelta().y()

        if delta > 0 and current_row > 0:
            # 上一张
            self.file_list.setCurrentRow(current_row - 1)
        elif delta < 0 and current_row < self.file_list.count() - 1:
            # 下一张
            self.file_list.setCurrentRow(current_row + 1)

        # 事件已处理，不传递给父类
        event.accept()

    def toggle_theme(self):
        """切换深色/浅色模式"""
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            # 深色模式
            self.apply_dark_theme()
        else:
            # 浅色模式
            self.apply_light_theme()

    def apply_light_theme(self):
        """应用浅色主题"""
        # 主窗口
        self.setStyleSheet("")

        # 顶部工具栏 - 固定样式
        self.findChild(QWidget, "top_bar").setStyleSheet(
            """
            QWidget {
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """
        )

        # 底部控制栏 - 固定样式
        self.findChild(QWidget, "bottom_bar").setStyleSheet(
            """
            QWidget {
                background-color: #f0f0f0;
                border-radius: 5px;
            }
        """
        )

        # 折叠按钮
        self.collapse_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: #ffffff;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """
        )

        # 文件列表
        self.file_list.setStyleSheet("")
        self.left_panel.setStyleSheet("")

        # 图片显示背景
        self.photo_widget.image_label.setStyleSheet("background-color: #1e1e1e;")

        # 提示文字
        self.theme_hint.setText("按 D 键切换深色模式")
        self.theme_hint.setStyleSheet("font-size: 11px; color: #888888;")

        # Live指示器 - 浅色模式下恢复默认颜色
        if (
            self.photo_widget.current_photo
            and self.photo_widget.current_photo.is_live_photo()
        ):
            self.live_label.setStyleSheet(
                "color: #2e7d32; font-size: 14px; font-weight: bold;"
            )
        else:
            self.live_label.setStyleSheet(
                "color: #757575; font-size: 14px; font-weight: bold;"
            )

    def apply_dark_theme(self):
        """应用深色主题"""
        # 主窗口
        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QLabel {
                color: #e0e0e0;
            }
            QListWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #4a4a4a;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #e0e0e0;
                border: 1px solid #4a4a4a;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QCheckBox {
                color: #e0e0e0;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 3px;
                padding: 5px;
            }
        """
        )

        # 顶部工具栏 - 深色
        self.findChild(QWidget, "top_bar").setStyleSheet(
            """
            QWidget {
                background-color: #2d2d2d;
                border-radius: 5px;
            }
        """
        )

        # 底部控制栏 - 深色
        self.findChild(QWidget, "bottom_bar").setStyleSheet(
            """
            QWidget {
                background-color: #2d2d2d;
                border-radius: 5px;
            }
        """
        )

        # 折叠按钮 - 深色
        self.collapse_button.setStyleSheet(
            """
            QPushButton {
                border: 1px solid #4a4a4a;
                border-radius: 5px;
                background-color: #3d3d3d;
                color: #e0e0e0;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """
        )

        # 图片显示背景
        self.photo_widget.image_label.setStyleSheet("background-color: #000000;")

        # 提示文字
        self.theme_hint.setText("按 D 键切换浅色模式")
        self.theme_hint.setStyleSheet("font-size: 11px; color: #888888;")

        # Live指示器 - 深色模式下使用较亮的颜色
        if (
            self.photo_widget.current_photo
            and self.photo_widget.current_photo.is_live_photo()
        ):
            self.live_label.setStyleSheet(
                "color: #4caf50; font-size: 14px; font-weight: bold;"
            )
        else:
            self.live_label.setStyleSheet(
                "color: #9e9e9e; font-size: 14px; font-weight: bold;"
            )


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
