from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextBrowser, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPoint, QDateTime, pyqtSignal
from PyQt5.QtGui import QTextOption, QFont, QColor

class MainDisplayWindow(QMainWindow):
    """主显示窗口，用于显示滚动文本"""
    
    # 定义信号
    window_resized_signal = pyqtSignal(object)
    window_moved_signal = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置窗口属性
        self.setWindowTitle("提词器主窗口")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        
        # 初始化文本显示组件
        self.text_browser = QTextBrowser()
        self.text_browser.setAlignment(Qt.AlignCenter)
        self.text_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 设置默认样式
        self.font_size = 36
        self.background_color = QColor(0, 0, 0)
        self.text_color = QColor(255, 255, 255)
        self.update_style()
        
        # 初始化滚动相关属性
        self.is_scrolling = False
        self.scroll_speed = 1000  # 滚动速度，像素/秒
        self.scroll_position = 0
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.update_scroll)
        self.last_scroll_time = 0
        
        # 设置中心部件
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.text_browser)
        self.setCentralWidget(central_widget)
    
    def update_style(self):
        """更新窗口样式"""
        # 设置字体
        font = QFont()
        font.setPointSize(self.font_size)
        self.text_browser.setFont(font)
        
        # 设置样式表
        style_sheet = "QTextBrowser {{ background-color: {0}; color: {1}; padding: 20px; }}".format(
            self.background_color.name(), self.text_color.name())
        self.text_browser.setStyleSheet(style_sheet)
    
    def set_text(self, text):
        """设置显示文本"""
        # 保存当前滚动位置
        current_scroll_value = self.text_browser.verticalScrollBar().value()
        current_scroll_position = self.scroll_position
        is_scrolling = self.is_scrolling
        
        # 更新文本
        self.text_browser.setPlainText(text)
        
        # 恢复滚动位置
        self.text_browser.verticalScrollBar().setValue(current_scroll_value)
        self.scroll_position = current_scroll_position
        
        # 确保滚动定时器状态正确
        if is_scrolling and not self.is_scrolling:
            self.start_scroll()
    
    def start_scroll(self):
        """开始滚动"""
        if not self.is_scrolling:
            self.is_scrolling = True
            self.last_scroll_time = QDateTime.currentMSecsSinceEpoch()
            self.scroll_timer.start(30)  # 约33fps
    
    def pause_scroll(self):
        """暂停滚动"""
        if self.is_scrolling:
            self.is_scrolling = False
            self.scroll_timer.stop()
    
    def reset_scroll(self):
        """重置滚动位置"""
        # 保存当前滚动状态
        was_scrolling = self.is_scrolling
        
        # 重置位置
        self.scroll_position = 0
        self.text_browser.verticalScrollBar().setValue(0)
        
        # 如果之前在滚动，继续滚动
        if was_scrolling:
            self.start_scroll()
    
    def update_scroll(self):
        """更新滚动位置"""
        if not self.is_scrolling:
            return
        
        # 计算时间差
        current_time = QDateTime.currentMSecsSinceEpoch()
        delta_time = (current_time - self.last_scroll_time) / 1000.0  # 转换为秒
        self.last_scroll_time = current_time
        
        # 计算滚动距离
        scroll_distance = self.scroll_speed * delta_time
        self.scroll_position += scroll_distance
        
        # 更新滚动条位置
        scroll_bar = self.text_browser.verticalScrollBar()
        scroll_bar.setValue(int(self.scroll_position))
    
    def set_scroll_speed(self, speed):
        """设置滚动速度"""
        self.scroll_speed = speed
    
    def set_font_size(self, size):
        """设置字体大小"""
        self.font_size = size
        self.update_style()
    
    def set_background_color(self, color):
        """设置背景颜色"""
        self.background_color = color
        self.update_style()
    
    def set_text_color(self, color):
        """设置文本颜色"""
        self.text_color = color
        self.update_style()
    
    def set_topmost(self, is_topmost):
        """设置窗口是否置顶"""
        if is_topmost:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()
    
    def resizeEvent(self, event):
        """窗口大小改变事件"""
        super().resizeEvent(event)
        # 通知主应用程序窗口大小改变
        if hasattr(self.parent(), 'on_main_window_resized'):
            self.parent().on_main_window_resized(event.size())
        elif hasattr(self, 'window_resized_signal'):
            self.window_resized_signal.emit(event.size())
    
    def moveEvent(self, event):
        """窗口移动事件"""
        super().moveEvent(event)
        # 通知主应用程序窗口位置改变
        if hasattr(self.parent(), 'on_main_window_moved'):
            self.parent().on_main_window_moved(event.pos())
        elif hasattr(self, 'window_moved_signal'):
            self.window_moved_signal.emit(event.pos())
