import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QListWidget, QStackedWidget, QLabel,
                               QListWidgetItem, QFrame)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QIcon

from home_page import HomePage
from merge_page import MergePage
from delete_page import DeletePage
from batch_delete_page import BatchDeletePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF处理器")
        self.setMinimumSize(1000, 700)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 左侧导航栏
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(200)
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: #2c3e50;
                color: white;
                border: none;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 15px 20px;
                border-bottom: 1px solid #34495e;
            }
            QListWidget::item:selected {
                background-color: #3498db;
            }
            QListWidget::item:hover {
                background-color: #34495e;
            }
        """)
        
        # 添加导航项
        nav_items = ["首页", "合并", "删除", "批量删除"]
        for item_text in nav_items:
            item = QListWidgetItem(item_text)
            item.setTextAlignment(Qt.AlignCenter)
            self.nav_list.addItem(item)
        
        # 右侧内容区域
        self.content_stack = QStackedWidget()
        
        # 创建各个页面
        self.home_page = HomePage()
        self.merge_page = MergePage()
        self.delete_page = DeletePage()
        self.batch_delete_page = BatchDeletePage()
        
        # 添加页面到堆叠部件
        self.content_stack.addWidget(self.home_page)
        self.content_stack.addWidget(self.merge_page)
        self.content_stack.addWidget(self.delete_page)
        self.content_stack.addWidget(self.batch_delete_page)
        
        # 连接信号
        self.nav_list.currentRowChanged.connect(self.switch_page)
        self.home_page.navigate_to_page.connect(self.navigate_to_page)
        
        # 布局
        main_layout.addWidget(self.nav_list)
        main_layout.addWidget(self.content_stack)
        
        # 默认选中首页
        self.nav_list.setCurrentRow(0)
    
    def switch_page(self, index):
        self.content_stack.setCurrentIndex(index)
    
    def navigate_to_page(self, index):
        """从首页导航到指定页面"""
        self.nav_list.setCurrentRow(index)


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序字体
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
