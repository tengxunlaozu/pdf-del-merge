from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, 
                               QPushButton, QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor


class HomePage(QWidget):
    # 定义信号，用于通知主窗口切换页面
    navigate_to_page = Signal(int)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # 标题
        title_label = QLabel("PDF处理器")
        title_font = QFont("Microsoft YaHei", 28, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50;")
        
        # 副标题
        subtitle_label = QLabel("简单易用的PDF处理工具")
        subtitle_font = QFont("Microsoft YaHei", 14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d;")
        
        # 功能按钮区域
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setAlignment(Qt.AlignCenter)
        
        # 合并按钮
        merge_btn = self.create_nav_button("合并", "合并多个PDF文件为一个", "#3498db", "#2980b9")
        merge_btn.clicked.connect(lambda: self.navigate_to_page.emit(1))
        
        # 删除按钮
        delete_btn = self.create_nav_button("删除", "从单个PDF文件删除指定页面", "#e74c3c", "#c0392b")
        delete_btn.clicked.connect(lambda: self.navigate_to_page.emit(2))
        
        # 批量删除按钮
        batch_delete_btn = self.create_nav_button("批量删除", "批量删除目录中所有PDF的指定页面", "#9b59b6", "#8e44ad")
        batch_delete_btn.clicked.connect(lambda: self.navigate_to_page.emit(3))
        
        buttons_layout.addWidget(merge_btn)
        buttons_layout.addWidget(delete_btn)
        buttons_layout.addWidget(batch_delete_btn)
        
        # 添加到主布局
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addLayout(buttons_layout)
        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # 版本信息
        version_label = QLabel("https://github.com/tengxunlaozu/pdf-del-merge")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #bdc3c7; font-size: 12px;")
        layout.addWidget(version_label)
    
    def create_nav_button(self, title, description, color, hover_color):
        """创建导航按钮"""
        button = QPushButton()
        button.setFixedSize(200, 120)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        
        # 创建按钮内部布局
        layout = QVBoxLayout(button)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setSpacing(8)
        
        # 标题
        title_label = QLabel(title)
        title_font = QFont("Microsoft YaHei", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; background: transparent;")
        
        # 描述
        desc_label = QLabel(description)
        desc_font = QFont("Microsoft YaHei", 9)
        desc_label.setFont(desc_font)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); background: transparent;")
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        
        return button
