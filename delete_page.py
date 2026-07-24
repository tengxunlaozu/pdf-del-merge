import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFileDialog, QGroupBox,
                               QLineEdit, QFormLayout, QMessageBox, 
                               QProgressBar, QFrame, QTextEdit)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor
from PyPDF2 import PdfReader, PdfWriter


class DeleteThread(QThread):
    progress = Signal(int)
    finished = Signal(bool, str)
    
    def __init__(self, input_path, output_path, pages_to_delete):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.pages_to_delete = pages_to_delete
    
    def run(self):
        try:
            reader = PdfReader(self.input_path)
            writer = PdfWriter()
            
            total_pages = len(reader.pages)
            pages_to_keep = []
            
            # 确定要保留的页面
            for i in range(total_pages):
                if i not in self.pages_to_delete:
                    pages_to_keep.append(i)
            
            # 复制要保留的页面
            for i, page_num in enumerate(pages_to_keep):
                writer.add_page(reader.pages[page_num])
                
                # 更新进度
                progress = int((i + 1) / len(pages_to_keep) * 100)
                self.progress.emit(progress)
            
            # 写入输出文件
            with open(self.output_path, 'wb') as output_file:
                writer.write(output_file)
            
            self.finished.emit(True, f"删除完成！保留了 {len(pages_to_keep)} 页")
        except Exception as e:
            self.finished.emit(False, f"删除失败：{str(e)}")


class DeletePage(QWidget):
    def __init__(self):
        super().__init__()
        self.input_file = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title_label = QLabel("删除PDF页面")
        title_font = QFont("Microsoft YaHei", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        
        # 文件选择区域
        file_group = QGroupBox("选择文件")
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
        
        file_layout = QHBoxLayout(file_group)
        
        self.file_path_edit = QLineEdit()
        self.file_path_edit.setPlaceholderText("选择要处理的PDF文件...")
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
                background-color: #f8f9fa;
            }
        """)
        
        browse_btn = QPushButton("浏览")
        browse_btn.setFixedSize(80, 35)
        browse_btn.setStyleSheet("""
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
        browse_btn.clicked.connect(self.browse_file)
        
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(browse_btn)
        
        # 文件信息
        self.file_info_label = QLabel("未选择文件")
        self.file_info_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        
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
        help_text.setMaximumHeight(100)
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
        
        output_browse_btn = QPushButton("浏览")
        output_browse_btn.setFixedSize(80, 35)
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
        output_browse_btn.clicked.connect(self.browse_output)
        
        output_layout.addWidget(self.output_path_edit)
        output_layout.addWidget(output_browse_btn)
        
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
                background-color: #e74c3c;
                border-radius: 5px;
            }
        """)
        
        # 运行按钮
        run_btn = QPushButton("开始删除")
        run_btn.setFixedSize(120, 40)
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
        run_btn.clicked.connect(self.run_delete)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(run_btn)
        
        # 主布局
        layout.addWidget(title_label)
        layout.addWidget(file_group)
        layout.addWidget(self.file_info_label)
        layout.addWidget(settings_group)
        layout.addWidget(output_group)
        layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)
        
        # 状态栏
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout.addWidget(self.status_label)
    
    def browse_file(self):
        """浏览选择输入文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择PDF文件", "", "PDF文件 (*.pdf)"
        )
        if file_path:
            self.input_file = file_path
            self.file_path_edit.setText(file_path)
            self.update_file_info()
    
    def browse_output(self):
        """浏览选择输出文件路径"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存删除后的PDF文件", "", "PDF文件 (*.pdf)"
        )
        if file_path:
            self.output_path_edit.setText(file_path)
    
    def update_file_info(self):
        """更新文件信息显示"""
        if self.input_file:
            try:
                reader = PdfReader(self.input_file)
                total_pages = len(reader.pages)
                file_size = os.path.getsize(self.input_file)
                file_size_mb = file_size / (1024 * 1024)
                
                # 检查是否加密
                is_encrypted = reader.is_encrypted
                
                info_text = f"文件：{os.path.basename(self.input_file)} | 页数：{total_pages} | 大小：{file_size_mb:.2f} MB"
                if is_encrypted:
                    info_text += " | [加密文件]"
                
                self.file_info_label.setText(info_text)
                self.file_info_label.setStyleSheet("color: #2c3e50; font-size: 12px;")
            except Exception as e:
                error_msg = str(e)
                if "PyCryptodome" in error_msg or "AES" in error_msg:
                    self.file_info_label.setText("读取失败：需要安装 pycryptodome 库（运行 pip install pycryptodome）")
                elif "password" in error_msg.lower() or "encrypted" in error_msg.lower():
                    self.file_info_label.setText("读取失败：PDF文件已加密，需要密码")
                else:
                    self.file_info_label.setText(f"读取文件信息失败：{error_msg}")
                self.file_info_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
        else:
            self.file_info_label.setText("未选择文件")
            self.file_info_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
    
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
    
    def run_delete(self):
        """执行删除操作"""
        if not self.input_file:
            QMessageBox.warning(self, "警告", "请先选择要处理的PDF文件！")
            return
        
        pages_text = self.pages_edit.text().strip()
        if not pages_text:
            QMessageBox.warning(self, "警告", "请输入要删除的页码！")
            return
        
        output_path = self.output_path_edit.text().strip()
        if not output_path:
            QMessageBox.warning(self, "警告", "请选择输出文件路径！")
            return
        
        # 确保输出文件以.pdf结尾
        if not output_path.lower().endswith('.pdf'):
            output_path += '.pdf'
        
        try:
            # 获取文件总页数
            reader = PdfReader(self.input_file)
            total_pages = len(reader.pages)
            
            # 解析要删除的页码
            pages_to_delete = self.parse_page_numbers(pages_text, total_pages)
            
            if not pages_to_delete:
                QMessageBox.warning(self, "警告", "没有有效的页码被指定！")
                return
            
            # 确认删除
            pages_to_delete_display = [p + 1 for p in pages_to_delete]
            confirm_msg = f"确定要删除以下页码吗？\n{', '.join(map(str, sorted(pages_to_delete_display)))}"
            
            reply = QMessageBox.question(
                self, "确认删除", confirm_msg,
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # 禁用按钮
            self.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # 创建并启动删除线程
            self.delete_thread = DeleteThread(self.input_file, output_path, pages_to_delete)
            self.delete_thread.progress.connect(self.update_progress)
            self.delete_thread.finished.connect(self.delete_finished)
            self.delete_thread.start()
            
        except ValueError as e:
            QMessageBox.critical(self, "错误", f"页码格式错误：{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"发生错误：{str(e)}")
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
    
    def delete_finished(self, success, message):
        """删除完成"""
        self.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "完成", message)
        else:
            QMessageBox.critical(self, "错误", message)
        
        self.status_label.setText("就绪")
