import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFileDialog, QGroupBox,
                               QLineEdit, QMessageBox, 
                               QProgressBar, QTextEdit, QListWidget,
                               QScrollArea)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont
from PyPDF2 import PdfReader, PdfWriter


class BatchDeleteThread(QThread):
    progress = Signal(int)
    file_progress = Signal(str, int, int)  # 文件名, 当前索引, 总数
    finished = Signal(bool, str)
    
    def __init__(self, pdf_files, pages_to_delete, output_dir):
        super().__init__()
        self.pdf_files = pdf_files
        self.pages_to_delete = pages_to_delete
        self.output_dir = output_dir
    
    def run(self):
        try:
            total_files = len(self.pdf_files)
            success_count = 0
            error_files = []
            
            for idx, input_path in enumerate(self.pdf_files):
                filename = os.path.basename(input_path)
                self.file_progress.emit(filename, idx + 1, total_files)
                
                try:
                    reader = PdfReader(input_path)
                    writer = PdfWriter()
                    total_pages = len(reader.pages)
                    
                    # 确定要保留的页面
                    pages_to_keep = []
                    for i in range(total_pages):
                        if i not in self.pages_to_delete:
                            pages_to_keep.append(i)
                    
                    # 如果所有页面都被删除，跳过此文件
                    if not pages_to_keep:
                        error_files.append(f"{filename}（所有页面都被删除）")
                        continue
                    
                    # 复制要保留的页面
                    for page_num in pages_to_keep:
                        writer.add_page(reader.pages[page_num])
                    
                    # 生成输出文件名：原文件名_del.pdf
                    name_without_ext = os.path.splitext(filename)[0]
                    output_filename = f"{name_without_ext}_del.pdf"
                    output_path = os.path.join(self.output_dir, output_filename)
                    
                    # 写入输出文件
                    with open(output_path, 'wb') as output_file:
                        writer.write(output_file)
                    
                    success_count += 1
                    
                    # 更新总体进度
                    progress = int((idx + 1) / total_files * 100)
                    self.progress.emit(progress)
                    
                except Exception as e:
                    error_files.append(f"{filename}（{str(e)}）")
            
            # 生成结果消息
            if error_files:
                error_msg = "\n".join(error_files)
                message = f"批量删除完成！\n成功：{success_count} 个文件\n失败：{len(error_files)} 个文件\n\n失败文件：\n{error_msg}"
            else:
                message = f"批量删除完成！\n成功处理了 {success_count} 个文件"
            
            self.finished.emit(len(error_files) == 0, message)
            
        except Exception as e:
            self.finished.emit(False, f"批量删除失败：{str(e)}")


class BatchDeletePage(QWidget):
    def __init__(self):
        super().__init__()
        self.pdf_files = []
        self.init_ui()
    
    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f5f5;
            }
        """)
        
        # 创建滚动内容widget
        scroll_content = QWidget()
        layout = QVBoxLayout(scroll_content)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("批量删除PDF页面")
        title_font = QFont("Microsoft YaHei", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        
        # 目录选择区域
        dir_group = QGroupBox("选择目录")
        dir_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        dir_layout = QHBoxLayout(dir_group)
        
        self.dir_path_edit = QLineEdit()
        self.dir_path_edit.setPlaceholderText("选择包含PDF文件的目录...")
        self.dir_path_edit.setReadOnly(True)
        self.dir_path_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                background-color: #f8f9fa;
            }
        """)
        
        browse_dir_btn = QPushButton("浏览目录")
        browse_dir_btn.setFixedSize(100, 35)
        browse_dir_btn.setStyleSheet("""
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
        browse_dir_btn.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(self.dir_path_edit)
        dir_layout.addWidget(browse_dir_btn)
        
        # 文件列表区域
        file_list_group = QGroupBox("PDF文件列表")
        file_list_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        file_list_layout = QVBoxLayout(file_list_group)
        
        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(150)
        self.file_list.setMaximumHeight(200)
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #ecf0f1;
            }
        """)
        
        self.file_count_label = QLabel("未选择目录")
        self.file_count_label.setStyleSheet("color: #7f8c8d; font-size: 12px; padding: 5px;")
        
        file_list_layout.addWidget(self.file_list)
        file_list_layout.addWidget(self.file_count_label)
        
        # 删除设置区域
        settings_group = QGroupBox("删除设置")
        settings_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        settings_layout = QVBoxLayout(settings_group)
        
        # 页码输入说明
        hint_label = QLabel("请输入要删除的页码（支持单页和连续页）：")
        hint_label.setStyleSheet("color: #2c3e50; font-size: 12px;")
        
        # 页码输入示例
        example_label = QLabel("示例：1, 3, 5-8, 10-15, 20")
        example_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        
        # 页码输入框
        self.pages_edit = QLineEdit()
        self.pages_edit.setPlaceholderText("例如：1, 3, 5-8, 10-15, 20")
        self.pages_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        
        # 页码输入帮助
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setMaximumHeight(80)
        help_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f8f9fa;
                font-size: 11px;
                color: #7f8c8d;
            }
        """)
        help_text.setPlainText(
            "输入格式说明：\n"
            "• 单页：直接输入页码，如 1, 3, 5\n"
            "• 连续页：用连字符表示范围，如 5-8\n"
            "• 多个页码/范围：用逗号分隔，如 1, 3, 5-8, 10-15\n"
            "• 页码从1开始计数"
        )
        
        settings_layout.addWidget(hint_label)
        settings_layout.addWidget(example_label)
        settings_layout.addWidget(self.pages_edit)
        settings_layout.addWidget(help_text)
        
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
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        output_layout = QVBoxLayout(output_group)
        
        # 输出目录说明
        output_hint = QLabel("输出目录：默认为源文件所在目录，文件命名格式：原文件名_del.pdf")
        output_hint.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        
        output_dir_layout = QHBoxLayout()
        
        self.output_dir_edit = QLineEdit()
        self.output_dir_edit.setPlaceholderText("选择输出目录（留空则保存到源文件目录）...")
        self.output_dir_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
        """)
        
        output_browse_btn = QPushButton("浏览目录")
        output_browse_btn.setFixedSize(100, 35)
        output_browse_btn.setStyleSheet("""
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
        output_browse_btn.clicked.connect(self.browse_output_dir)
        
        output_dir_layout.addWidget(self.output_dir_edit)
        output_dir_layout.addWidget(output_browse_btn)
        
        output_layout.addWidget(output_hint)
        output_layout.addLayout(output_dir_layout)
        
        # 进度区域
        progress_group = QGroupBox("处理进度")
        progress_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        progress_layout = QVBoxLayout(progress_group)
        
        self.current_file_label = QLabel("")
        self.current_file_label.setStyleSheet("color: #2c3e50; font-size: 12px;")
        self.current_file_label.setVisible(False)
        
        self.file_progress_bar = QProgressBar()
        self.file_progress_bar.setVisible(False)
        self.file_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-size: 12px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #e74c3c;
                border-radius: 5px;
            }
        """)
        
        self.overall_progress_bar = QProgressBar()
        self.overall_progress_bar.setVisible(False)
        self.overall_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-size: 12px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 5px;
            }
        """)
        
        progress_layout.addWidget(self.current_file_label)
        progress_layout.addWidget(self.file_progress_bar)
        progress_layout.addWidget(self.overall_progress_bar)
        
        # 运行按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        run_btn = QPushButton("开始批量删除")
        run_btn.setFixedSize(150, 40)
        run_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        run_btn.clicked.connect(self.run_batch_delete)
        button_layout.addWidget(run_btn)
        button_layout.addStretch()
        
        # 添加到滚动内容布局
        layout.addWidget(title_label)
        layout.addWidget(dir_group)
        layout.addWidget(file_list_group)
        layout.addWidget(settings_group)
        layout.addWidget(output_group)
        layout.addWidget(progress_group)
        layout.addLayout(button_layout)
        
        # 状态栏
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #7f8c8d; font-size: 12px; padding: 5px;")
        layout.addWidget(self.status_label)
        
        # 设置滚动区域
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def browse_directory(self):
        """浏览选择目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择包含PDF文件的目录"
        )
        if dir_path:
            self.dir_path_edit.setText(dir_path)
            self.load_pdf_files(dir_path)
    
    def browse_output_dir(self):
        """浏览选择输出目录"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "选择输出目录"
        )
        if dir_path:
            self.output_dir_edit.setText(dir_path)
    
    def load_pdf_files(self, dir_path):
        """加载目录中的PDF文件"""
        self.pdf_files = []
        self.file_list.clear()
        
        try:
            # 获取目录中所有PDF文件并排序
            pdf_files = []
            for filename in os.listdir(dir_path):
                if filename.lower().endswith('.pdf'):
                    full_path = os.path.join(dir_path, filename)
                    pdf_files.append((filename, full_path))
            
            # 按文件名排序
            pdf_files.sort(key=lambda x: x[0].lower())
            
            # 添加到列表
            for filename, full_path in pdf_files:
                self.pdf_files.append(full_path)
                self.file_list.addItem(filename)
            
            # 更新文件计数
            count = len(self.pdf_files)
            if count > 0:
                self.file_count_label.setText(f"找到 {count} 个PDF文件")
                self.file_count_label.setStyleSheet("color: #27ae60; font-size: 12px; padding: 5px;")
            else:
                self.file_count_label.setText("目录中没有找到PDF文件")
                self.file_count_label.setStyleSheet("color: #e74c3c; font-size: 12px; padding: 5px;")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"读取目录失败：{str(e)}")
    
    def parse_page_numbers(self, page_str, total_pages):
        """解析页码字符串，返回要删除的页码列表（0-based）"""
        pages_to_delete = set()
        
        # 分割逗号分隔的部分
        parts = page_str.split(',')
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # 检查是否是范围（包含连字符）
            if '-' in part:
                try:
                    start, end = part.split('-', 1)
                    start = int(start.strip())
                    end = int(end.strip())
                    
                    # 验证范围
                    if start < 1 or end < start or end > total_pages:
                        raise ValueError(f"无效的页码范围：{part}")
                    
                    # 添加范围内的所有页码（转换为0-based）
                    for page in range(start, end + 1):
                        pages_to_delete.add(page - 1)
                except ValueError as e:
                    raise ValueError(f"解析页码范围失败：{part} - {str(e)}")
            else:
                # 单页
                try:
                    page = int(part)
                    if page < 1 or page > total_pages:
                        raise ValueError(f"页码 {page} 超出范围（1-{total_pages}）")
                    pages_to_delete.add(page - 1)
                except ValueError as e:
                    raise ValueError(f"解析页码失败：{part} - {str(e)}")
        
        return list(pages_to_delete)
    
    def run_batch_delete(self):
        """执行批量删除操作"""
        if not self.pdf_files:
            QMessageBox.warning(self, "警告", "请先选择包含PDF文件的目录！")
            return
        
        pages_text = self.pages_edit.text().strip()
        if not pages_text:
            QMessageBox.warning(self, "警告", "请输入要删除的页码！")
            return
        
        # 确定输出目录
        output_dir = self.output_dir_edit.text().strip()
        if not output_dir:
            # 使用源文件目录
            output_dir = os.path.dirname(self.pdf_files[0])
        
        try:
            # 获取第一个文件的总页数来验证页码
            reader = PdfReader(self.pdf_files[0])
            total_pages = len(reader.pages)
            
            # 解析要删除的页码
            pages_to_delete = self.parse_page_numbers(pages_text, total_pages)
            
            if not pages_to_delete:
                QMessageBox.warning(self, "警告", "没有有效的页码被指定！")
                return
            
            # 确认删除
            pages_to_delete_display = [p + 1 for p in pages_to_delete]
            confirm_msg = f"确定要对 {len(self.pdf_files)} 个文件删除以下页码吗？\n{', '.join(map(str, sorted(pages_to_delete_display)))}\n\n输出目录：{output_dir}"
            
            reply = QMessageBox.question(
                self, "确认批量删除", confirm_msg,
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # 禁用界面
            self.setEnabled(False)
            self.current_file_label.setVisible(True)
            self.file_progress_bar.setVisible(True)
            self.overall_progress_bar.setVisible(True)
            self.file_progress_bar.setValue(0)
            self.overall_progress_bar.setValue(0)
            
            # 创建并启动批量删除线程
            self.batch_delete_thread = BatchDeleteThread(
                self.pdf_files, pages_to_delete, output_dir
            )
            self.batch_delete_thread.progress.connect(self.update_overall_progress)
            self.batch_delete_thread.file_progress.connect(self.update_file_progress)
            self.batch_delete_thread.finished.connect(self.batch_delete_finished)
            self.batch_delete_thread.start()
            
        except ValueError as e:
            QMessageBox.critical(self, "错误", f"页码格式错误：{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"发生错误：{str(e)}")
    
    def update_file_progress(self, filename, current, total):
        """更新当前文件处理进度"""
        self.current_file_label.setText(f"正在处理：{filename} ({current}/{total})")
    
    def update_overall_progress(self, value):
        """更新总体进度条"""
        self.overall_progress_bar.setValue(value)
    
    def batch_delete_finished(self, success, message):
        """批量删除完成"""
        self.setEnabled(True)
        self.current_file_label.setVisible(False)
        self.file_progress_bar.setVisible(False)
        self.overall_progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.warning(self, "完成", message)
        
        self.status_label.setText("就绪")
