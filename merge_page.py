import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QListWidget, QFileDialog, QGroupBox,
                               QCheckBox, QComboBox, QLineEdit, QFormLayout,
                               QMessageBox, QProgressBar, QFrame, QListWidgetItem)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor, QIcon
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


class MergeThread(QThread):
    progress = Signal(int)
    finished = Signal(bool, str)
    
    def __init__(self, files, output_path, settings):
        super().__init__()
        self.files = files
        self.output_path = output_path
        self.settings = settings
    
    def run(self):
        try:
            merger = PdfMerger()
            
            for i, file_path in enumerate(self.files):
                reader = PdfReader(file_path)
                
                # 获取页码范围
                page_range = self.settings.get('page_range', '')
                if page_range:
                    pages = self.parse_page_range(page_range, len(reader.pages))
                    merger.append(file_path, pages=pages)
                else:
                    merger.append(file_path)
                
                # 更新进度
                progress = int((i + 1) / len(self.files) * 100)
                self.progress.emit(progress)
            
            # 写入输出文件
            merger.write(self.output_path)
            merger.close()
            
            self.finished.emit(True, "合并完成！")
        except Exception as e:
            self.finished.emit(False, f"合并失败：{str(e)}")
    
    def parse_page_range(self, range_str, total_pages):
        """解析页码范围字符串，返回页码列表"""
        pages = []
        parts = range_str.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-', 1)
                start = int(start) if start else 1
                end = int(end) if end else total_pages
                pages.extend(range(start - 1, min(end, total_pages)))
            else:
                page_num = int(part)
                if 1 <= page_num <= total_pages:
                    pages.append(page_num - 1)
        
        return pages


class MergePage(QWidget):
    def __init__(self):
        super().__init__()
        self.files = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("合并PDF文件")
        title_font = QFont("Microsoft YaHei", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        
        # 文件列表区域
        file_group = QGroupBox("文件列表")
        file_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        file_layout = QVBoxLayout(file_group)
        
        # 文件列表按钮
        file_buttons_layout = QHBoxLayout()
        
        add_file_btn = QPushButton("添加文件")
        add_file_btn.setFixedSize(100, 35)
        add_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        add_file_btn.clicked.connect(self.add_files)
        
        remove_file_btn = QPushButton("移除文件")
        remove_file_btn.setFixedSize(100, 35)
        remove_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        remove_file_btn.clicked.connect(self.remove_file)
        
        clear_files_btn = QPushButton("清空列表")
        clear_files_btn.setFixedSize(100, 35)
        clear_files_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        clear_files_btn.clicked.connect(self.clear_files)
        
        move_up_btn = QPushButton("上移")
        move_up_btn.setFixedSize(60, 35)
        move_up_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        move_up_btn.clicked.connect(self.move_up)
        
        move_down_btn = QPushButton("下移")
        move_down_btn.setFixedSize(60, 35)
        move_down_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        move_down_btn.clicked.connect(self.move_down)
        
        file_buttons_layout.addWidget(add_file_btn)
        file_buttons_layout.addWidget(remove_file_btn)
        file_buttons_layout.addWidget(clear_files_btn)
        file_buttons_layout.addWidget(move_up_btn)
        file_buttons_layout.addWidget(move_down_btn)
        file_buttons_layout.addStretch()
        
        # 文件列表
        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self.file_list.setMinimumHeight(150)
        
        file_layout.addLayout(file_buttons_layout)
        file_layout.addWidget(self.file_list)
        
        # 设置区域
        settings_group = QGroupBox("合并设置")
        settings_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        settings_layout = QFormLayout(settings_group)
        settings_layout.setSpacing(10)
        
        # 页码范围
        self.page_range_edit = QLineEdit()
        self.page_range_edit.setPlaceholderText("例如：1-3, 5, 7-10（留空表示全部页面）")
        self.page_range_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        
        # 书签设置
        self.bookmark_combo = QComboBox()
        self.bookmark_combo.addItems(["保留所有书签", "丢弃书签", "为每个文件创建书签"])
        self.bookmark_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        
        # 目录设置
        self.toc_checkbox = QCheckBox("添加目录页")
        self.toc_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
            }
        """)
        
        settings_layout.addRow("页码范围:", self.page_range_edit)
        settings_layout.addRow("书签设置:", self.bookmark_combo)
        settings_layout.addRow("", self.toc_checkbox)
        
        # 输出设置
        output_group = QGroupBox("输出设置")
        output_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        output_layout = QHBoxLayout(output_group)
        
        self.output_path_edit = QLineEdit()
        self.output_path_edit.setPlaceholderText("选择输出文件路径...")
        self.output_path_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        
        browse_btn = QPushButton("浏览")
        browse_btn.setFixedSize(80, 35)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        browse_btn.clicked.connect(self.browse_output)
        
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(browse_btn)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 5px;
            }
        """)
        
        # 运行按钮
        run_btn = QPushButton("开始合并")
        run_btn.setFixedSize(120, 40)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        run_btn.clicked.connect(self.run_merge)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(run_btn)
        
        # 主布局
        layout.addWidget(title_label)
        layout.addWidget(file_group)
        layout.addWidget(settings_group)
        layout.addWidget(output_group)
        layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)
        
        # 状态栏
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout.addWidget(self.status_label)
    
    def add_files(self):
        """添加PDF文件"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择PDF文件", "", "PDF文件 (*.pdf)"
        )
        
        for file_path in files:
            if file_path not in self.files:
                self.files.append(file_path)
                item = QListWidgetItem(os.path.basename(file_path))
                item.setToolTip(file_path)
                self.file_list.addItem(item)
        
        self.update_status()
    
    def remove_file(self):
        """移除选中的文件"""
        current_row = self.file_list.currentRow()
        if current_row >= 0:
            self.files.pop(current_row)
            self.file_list.takeItem(current_row)
            self.update_status()
    
    def clear_files(self):
        """清空文件列表"""
        self.files.clear()
        self.file_list.clear()
        self.update_status()
    
    def move_up(self):
        """上移选中的文件"""
        current_row = self.file_list.currentRow()
        if current_row > 0:
            # 交换数据
            self.files[current_row], self.files[current_row - 1] = \
                self.files[current_row - 1], self.files[current_row]
            
            # 交换列表项
            item = self.file_list.takeItem(current_row)
            self.file_list.insertItem(current_row - 1, item)
            self.file_list.setCurrentRow(current_row - 1)
    
    def move_down(self):
        """下移选中的文件"""
        current_row = self.file_list.currentRow()
        if current_row < len(self.files) - 1:
            # 交换数据
            self.files[current_row], self.files[current_row + 1] = \
                self.files[current_row + 1], self.files[current_row]
            
            # 交换列表项
            item = self.file_list.takeItem(current_row)
            self.file_list.insertItem(current_row + 1, item)
            self.file_list.setCurrentRow(current_row + 1)
    
    def browse_output(self):
        """浏览输出文件路径"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存合并后的PDF文件", "", "PDF文件 (*.pdf)"
        )
        if file_path:
            self.output_path_edit.setText(file_path)
    
    def update_status(self):
        """更新状态栏"""
        count = len(self.files)
        if count == 0:
            self.status_label.setText("就绪")
        else:
            self.status_label.setText(f"已添加 {count} 个文件")
    
    def run_merge(self):
        """执行合并操作"""
        if not self.files:
            QMessageBox.warning(self, "警告", "请先添加要合并的PDF文件！")
            return
        
        output_path = self.output_path_edit.text().strip()
        if not output_path:
            QMessageBox.warning(self, "警告", "请选择输出文件路径！")
            return
        
        # 确保输出文件以.pdf结尾
        if not output_path.lower().endswith('.pdf'):
            output_path += '.pdf'
        
        # 获取设置
        settings = {
            'page_range': self.page_range_edit.text().strip(),
            'bookmark': self.bookmark_combo.currentIndex(),
            'toc': self.toc_checkbox.isChecked()
        }
        
        # 禁用按钮
        self.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # 创建并启动合并线程
        self.merge_thread = MergeThread(self.files, output_path, settings)
        self.merge_thread.progress.connect(self.update_progress)
        self.merge_thread.finished.connect(self.merge_finished)
        self.merge_thread.start()
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def merge_finished(self, success, message):
        """合并完成"""
        self.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.critical(self, "错误", message)
        
        self.status_label.setText("就绪")
