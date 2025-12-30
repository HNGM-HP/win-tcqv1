import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QColor

# 导入各个模块
from main_window import MainDisplayWindow
from control_panel import ControlPanel
from secondary_screen import SecondaryScreenWindow
from text_processor import TextProcessor
from config_manager import ConfigManager
from dynamic_editor import DynamicEditor

class MainApp(QObject):
    """主应用程序类，管理所有窗口和组件"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化应用程序
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("提词器")
        self.app.setApplicationVersion("1.72")
        self.app.setOrganizationName("光脉科技")
        self.app.setOrganizationDomain("hngmjt.com")
        
        # 初始化配置管理器
        self.config_manager = ConfigManager()
        
        # 初始化各个组件
        self.main_window = MainDisplayWindow()
        self.control_panel = ControlPanel()
        self.secondary_screen = SecondaryScreenWindow()
        self.text_processor = TextProcessor()
        self.dynamic_editor = DynamicEditor()
        
        # 应用程序设置
        self.settings = {
            "scroll_speed": self.config_manager.get("scroll_speed"),
            "font_size": self.config_manager.get("font_size"),
            "background_color": self.config_manager.get("background_color"),
            "text_color": self.config_manager.get("text_color"),
            "paragraph_duration": self.config_manager.get("paragraph_duration"),
            "secondary_screen_enabled": False,  # 固定默认为False，不读取配置
            "secondary_screen_topmost": self.config_manager.get("secondary_screen_topmost"),
            "main_window_topmost": self.config_manager.get("main_window_topmost")
        }
        
        # 应用配置到文本处理器
        self.text_processor.set_paragraph_duration(self.settings["paragraph_duration"])
        self.text_processor.set_time_control_mode(self.config_manager.get("paragraph_time_control_mode"))
        
        # 应用配置到窗口
        self.apply_config_to_windows()
        
        # 更新控制面板UI
        self.control_panel.update_from_config(self.config_manager.config)
        
        # 自动恢复上次打开的文件
        last_opened_file = self.config_manager.get("last_opened_file")
        if last_opened_file and os.path.exists(last_opened_file):
            self.open_file(last_opened_file)
    
    def apply_config_to_windows(self):
        """应用配置到窗口"""
        # 应用主窗口配置
        main_win_config = self.config_manager.get("main_window")
        self.main_window.setGeometry(
            main_win_config["x"],
            main_win_config["y"],
            main_win_config["width"],
            main_win_config["height"]
        )
        
        # 应用副屏配置 - 副屏使用主窗口的宽度和高度
        secondary_win_config = self.config_manager.get("secondary_window")
        self.secondary_screen.setGeometry(
            secondary_win_config["x"],
            secondary_win_config["y"],
            main_win_config["width"],  # 副屏使用主窗口宽度
            main_win_config["height"]  # 副屏使用主窗口高度
        )
        
        # 应用其他配置
        self.main_window.set_scroll_speed(self.settings["scroll_speed"])
        self.main_window.set_font_size(self.settings["font_size"])
        self.main_window.set_background_color(QColor(self.settings["background_color"]))
        self.main_window.set_text_color(QColor(self.settings["text_color"]))
        
        self.secondary_screen.set_scroll_speed(self.settings["scroll_speed"])
        self.secondary_screen.set_font_size(self.settings["font_size"])
        self.secondary_screen.set_background_color(QColor(self.settings["background_color"]))
        self.secondary_screen.set_text_color(QColor(self.settings["text_color"]))
        
        # 应用置顶设置
        self.main_window.set_topmost(self.settings["main_window_topmost"])
        self.secondary_screen.set_topmost(self.settings["secondary_screen_topmost"])
    
    def initialize_components(self):
        """初始化所有组件"""
        # 建立信号连接
        self.setup_connections()
        
        # 初始化显示内容
        self.update_display()
    
    def setup_connections(self):
        """建立组件之间的信号连接"""
        # 控制面板信号连接
        
        # 动态编辑信号连接到DynamicEditor
        self.control_panel.text_changed.connect(self.on_dynamic_text_changed)
        self.control_panel.open_file.connect(self.open_file)
        self.control_panel.save_file.connect(self.save_file)
        self.control_panel.save_as_file.connect(self.save_file)
        self.control_panel.clear_text.connect(self.clear_text)
        
        # 滚动控制
        self.control_panel.start_scroll.connect(self.start_scroll)
        self.control_panel.pause_scroll.connect(self.pause_scroll)
        self.control_panel.reset_scroll.connect(self.reset_scroll)
        self.control_panel.scroll_speed_changed.connect(self.set_scroll_speed)
        
        # 样式控制
        self.control_panel.font_size_changed.connect(self.set_font_size)
        self.control_panel.background_color_changed.connect(self.set_background_color)
        self.control_panel.text_color_changed.connect(self.set_text_color)
        
        # 段落停留时间信号
        self.control_panel.paragraph_duration_changed.connect(self.text_processor.set_paragraph_duration)
        # 段落时间控制方式信号
        self.control_panel.paragraph_time_control_mode_changed.connect(self.text_processor.set_time_control_mode)
        
        # 屏幕控制
        self.control_panel.toggle_secondary_screen.connect(self.toggle_secondary_screen)
        self.control_panel.toggle_main_window_topmost.connect(self.set_main_window_topmost)
        self.control_panel.toggle_secondary_window_topmost.connect(self.set_secondary_window_topmost)
        self.control_panel.main_window_width_changed.connect(self.set_main_window_width)
        self.control_panel.main_window_height_changed.connect(self.set_main_window_height)
        self.control_panel.main_window_x_changed.connect(self.set_main_window_x)
        self.control_panel.main_window_y_changed.connect(self.set_main_window_y)
        self.control_panel.secondary_window_x_changed.connect(self.set_secondary_window_x)
        self.control_panel.secondary_window_y_changed.connect(self.set_secondary_window_y)
        
        # 配置控制信号
        self.control_panel.save_config.connect(self.on_save_config)
        self.control_panel.reset_config.connect(self.on_reset_config)
        
        # 文本处理器信号连接
        self.text_processor.current_paragraph_changed.connect(self.on_paragraph_changed)
        self.text_processor.current_paragraph_changed.connect(self.update_display)
        self.text_processor.current_paragraph_changed.connect(self.update_control_panel)
        
        # DynamicEditor信号连接
        self.dynamic_editor.text_changed.connect(self.text_processor.set_text)
        
        # 段落导航信号连接
        self.control_panel.prev_paragraph_btn.clicked.connect(self.text_processor.prev_paragraph)
        self.control_panel.next_paragraph_btn.clicked.connect(self.text_processor.next_paragraph)
        
        # 滚动条位置同步信号
        self.main_window.text_browser.verticalScrollBar().valueChanged.connect(self.on_main_scroll_changed)
        self.secondary_screen.text_browser.verticalScrollBar().valueChanged.connect(self.on_secondary_scroll_changed)
        
        # 进度条信号连接
        self.control_panel.paragraph_changed.connect(self.text_processor.set_current_paragraph)
        self.control_panel.paragraph_scroll_changed.connect(self.on_paragraph_scroll_changed)
        
        # 设置窗口相关连接
        self.setup_window_connections()
    
    def on_dynamic_text_changed(self, text):
        """处理动态文本变化，使用DynamicEditor管理滚动位置"""
        # 保存当前滚动位置
        self.dynamic_editor.save_scroll_position(self.main_window)
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.dynamic_editor.save_scroll_position(self.secondary_screen)
        
        # 通过DynamicEditor处理文本变化
        self.dynamic_editor.on_text_changed(text, is_dynamic_edit=True)
        
        # 恢复滚动位置
        self.dynamic_editor.restore_scroll_position(self.main_window, is_paragraph_switch=False)
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.dynamic_editor.restore_scroll_position(self.secondary_screen, is_paragraph_switch=False)
    
    def on_paragraph_changed(self, index):
        """处理段落切换，更新DynamicEditor的当前段落索引"""
        self.dynamic_editor.set_current_paragraph(index)
    
    def update_display(self, is_paragraph_switch=True):
        """更新显示内容"""
        current_text = self.text_processor.get_current_paragraph()
        
        # 保存当前滚动状态
        was_scrolling = self.main_window.is_scrolling
        
        # 关闭滚动定时器
        if was_scrolling:
            self.main_window.pause_scroll()
            if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
                self.secondary_screen.pause_scroll()
        
        # 更新文本
        self.main_window.set_text(current_text)
        self.secondary_screen.set_text(current_text)
        
        # 根据是否是段落切换决定是否重置滚动位置
        if is_paragraph_switch:
            # 段落切换：重置滚动位置到新段落开头
            self.main_window.reset_scroll()
            if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
                self.secondary_screen.reset_scroll()
        else:
            # 动态编辑：恢复之前的滚动位置
            self.dynamic_editor.restore_scroll_position(self.main_window, is_paragraph_switch=False)
            if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
                self.dynamic_editor.restore_scroll_position(self.secondary_screen, is_paragraph_switch=False)
        
        # 如果之前在滚动，继续滚动
        if was_scrolling:
            self.main_window.start_scroll()
            if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
                self.secondary_screen.start_scroll()
    
    def update_control_panel(self):
        """更新控制面板状态"""
        self.control_panel.update_paragraph_info(
            self.text_processor.current_paragraph_index, 
            self.text_processor.get_total_paragraphs()
        )
    
    def on_main_scroll_changed(self, value):
        """主窗口滚动位置改变时的槽函数"""
        # 同步到副屏
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            # 防止循环触发
            if abs(self.secondary_screen.text_browser.verticalScrollBar().value() - value) > 1:
                self.secondary_screen.text_browser.verticalScrollBar().setValue(value)
                self.secondary_screen.scroll_position = value
    
    def on_secondary_scroll_changed(self, value):
        """副屏滚动位置改变时的槽函数"""
        # 同步到主窗口
        if abs(self.main_window.text_browser.verticalScrollBar().value() - value) > 1:
            self.main_window.text_browser.verticalScrollBar().setValue(value)
            self.main_window.scroll_position = value
    
    def on_paragraph_scroll_changed(self, progress):
        """段落内滚动位置改变时的槽函数"""
        # 计算目标滚动位置
        main_scroll_bar = self.main_window.text_browser.verticalScrollBar()
        max_value = main_scroll_bar.maximum()
        target_position = int(progress * max_value)
        
        # 设置主窗口滚动位置
        self.main_window.text_browser.verticalScrollBar().setValue(target_position)
        self.main_window.scroll_position = target_position
        
        # 同步到副屏
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.text_browser.verticalScrollBar().setValue(target_position)
            self.secondary_screen.scroll_position = target_position
    
    def on_main_window_resized(self, size):
        """主窗口大小改变时的槽函数"""
        # 同步到副屏
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.resize(size)
        
        # 更新配置
        width, height = size.width(), size.height()
        self.config_manager.set("main_window.width", width)
        self.config_manager.set("main_window.height", height)
        
        # 更新控制面板显示数值
        self.control_panel.main_width_spinbox.setValue(width)
        self.control_panel.main_height_spinbox.setValue(height)
    
    def on_main_window_moved(self, pos):
        """主窗口位置改变时的槽函数"""
        # 获取新的窗口位置
        x, y = pos.x(), pos.y()
        
        # 避免重复更新（只有当数值发生变化时才更新）
        if (self.control_panel.main_x_spinbox.value() != x or 
            self.control_panel.main_y_spinbox.value() != y):
            # 更新配置
            self.config_manager.set("main_window.x", x)
            self.config_manager.set("main_window.y", y)
            
            # 更新控制面板显示数值（使用blockSignals避免触发valueChanged信号）
            self.control_panel.main_x_spinbox.blockSignals(True)
            self.control_panel.main_y_spinbox.blockSignals(True)
            self.control_panel.main_x_spinbox.setValue(x)
            self.control_panel.main_y_spinbox.setValue(y)
            self.control_panel.main_x_spinbox.blockSignals(False)
            self.control_panel.main_y_spinbox.blockSignals(False)
    
    def on_secondary_window_moved(self, pos):
        """副屏位置改变时的槽函数"""
        # 获取新的窗口位置
        x, y = pos.x(), pos.y()
        
        # 避免重复更新（只有当数值发生变化时才更新）
        if (self.control_panel.secondary_x_spinbox.value() != x or 
            self.control_panel.secondary_y_spinbox.value() != y):
            # 更新配置
            self.config_manager.set("secondary_window.x", x)
            self.config_manager.set("secondary_window.y", y)
            
            # 更新控制面板显示数值（使用blockSignals避免触发valueChanged信号）
            self.control_panel.secondary_x_spinbox.blockSignals(True)
            self.control_panel.secondary_y_spinbox.blockSignals(True)
            self.control_panel.secondary_x_spinbox.setValue(x)
            self.control_panel.secondary_y_spinbox.setValue(y)
            self.control_panel.secondary_x_spinbox.blockSignals(False)
            self.control_panel.secondary_y_spinbox.blockSignals(False)
    
    def setup_window_connections(self):
        """设置窗口相关连接"""
        # 窗口关闭信号
        self.main_window.closeEvent = self.on_main_window_closed
        self.control_panel.closeEvent = self.on_control_panel_closed
        
        # 窗口大小变化信号连接
        self.main_window.window_resized_signal.connect(self.on_main_window_resized)
        
        # 窗口移动信号连接
        self.main_window.window_moved_signal.connect(self.on_main_window_moved)
        self.secondary_screen.window_moved_signal.connect(self.on_secondary_window_moved)
    
    def on_main_window_closed(self, event):
        """主窗口关闭事件"""
        self.close_all_windows()
        event.accept()
    
    def on_control_panel_closed(self, event):
        """控制面板关闭事件"""
        self.close_all_windows()
        event.accept()
    
    def close_all_windows(self):
        """关闭所有窗口"""
        # 保存配置
        self.config_manager.save_config()
        
        # 关闭所有窗口
        self.main_window.close()
        self.control_panel.close()
        self.secondary_screen.close()
        
        # 退出应用程序
        self.app.quit()
    
    def start_scroll(self):
        """开始滚动"""
        self.main_window.start_scroll()
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.start_scroll()
        # 开始自动段落跳转
        self.text_processor.start_auto_play()
    
    def pause_scroll(self):
        """暂停滚动"""
        self.main_window.pause_scroll()
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.pause_scroll()
        # 停止自动段落跳转
        self.text_processor.stop_auto_play()
    
    def reset_scroll(self):
        """重置滚动"""
        self.main_window.reset_scroll()
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.reset_scroll()
    
    def set_scroll_speed(self, speed):
        """设置滚动速度（倒序逻辑：值越小速度越快，值越大速度越慢）"""
        # 优化滚动速度计算公式，使速度变化更均匀
        # 使用对数函数实现非线性映射，确保在整个范围内变化更均衡
        # 公式：0.1 + (1000 - 0.1) * log10( (100000 - speed + 1000) / 1000 ) / 3
        # 范围从约0.1到1000像素/秒
        import math
        
        # 限制最大值，确保滚动不会完全停止
        max_speed_value = 99999
        speed = min(speed, max_speed_value)
        
        # 计算实际滚动速度，使用对数函数实现更均匀的速度变化
        numerator = 100000 - speed + 1000  # 增加偏移量确保数值有效
        log_value = math.log10(numerator / 1000)
        actual_speed = 0.1 + (1000 - 0.1) * (log_value / 3)  # 映射到0.1-1000像素/秒
        
        self.settings["scroll_speed"] = actual_speed
        self.main_window.set_scroll_speed(actual_speed)
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.set_scroll_speed(actual_speed)
    
    def set_font_size(self, size):
        """设置字体大小"""
        self.settings["font_size"] = size
        self.main_window.set_font_size(size)
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.set_font_size(size)
        
        # 更新控制面板的滚动一行时间显示
        # 计算当前行高
        line_height = size * 1.2  # 假设行高为字体大小的1.2倍
        # 获取当前滚动速度值
        current_speed_value = self.control_panel.speed_slider.value()
        # 更新滚动时间显示，并传递行高值
        self.control_panel.update_scroll_time(current_speed_value, line_height)
    
    def set_background_color(self, color):
        """设置背景颜色"""
        self.settings["background_color"] = color.name()
        self.main_window.set_background_color(color)
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.set_background_color(color)
    
    def set_text_color(self, color):
        """设置文本颜色"""
        self.settings["text_color"] = color.name()
        self.main_window.set_text_color(color)
        if self.settings["secondary_screen_enabled"] and self.secondary_screen.isVisible():
            self.secondary_screen.set_text_color(color)
    
    def toggle_secondary_screen(self, enabled):
        """切换副屏显示"""
        self.settings["secondary_screen_enabled"] = enabled
        if enabled:
            # 同步主窗口状态到副屏
            self.secondary_screen.sync_with_main(self.main_window)
            self.secondary_screen.show()
        else:
            self.secondary_screen.hide()
        
        # 更新控制面板UI
        self.control_panel.secondary_screen_check.setChecked(enabled)
    
    def set_main_window_topmost(self, topmost):
        """设置主窗口置顶"""
        self.settings["main_window_topmost"] = topmost
        self.main_window.set_topmost(topmost)
    
    def set_secondary_window_topmost(self, topmost):
        """设置副屏置顶"""
        self.settings["secondary_screen_topmost"] = topmost
        self.secondary_screen.set_topmost(topmost)
    
    def set_main_window_width(self, width):
        """设置主窗口宽度 - 同时更新副屏宽度"""
        # 获取当前窗口位置和高度
        # 使用geometry()而不是单独获取x()和y()，避免位置不一致问题
        rect = self.main_window.geometry()
        x, y = rect.x(), rect.y()
        height = rect.height()
        
        # 调整主窗口大小
        self.main_window.setGeometry(x, y, width, height)
        
        # 同步调整副屏宽度
        if self.secondary_screen.isVisible():
            secondary_rect = self.secondary_screen.geometry()
            secondary_x, secondary_y = secondary_rect.x(), secondary_rect.y()
            secondary_height = secondary_rect.height()
            self.secondary_screen.setGeometry(secondary_x, secondary_y, width, secondary_height)
        
        # 更新配置
        self.config_manager.set("main_window.width", width)
    
    def set_main_window_height(self, height):
        """设置主窗口高度 - 同时更新副屏高度"""
        # 获取当前窗口位置和宽度
        # 使用geometry()而不是单独获取x()和y()，避免位置不一致问题
        rect = self.main_window.geometry()
        x, y = rect.x(), rect.y()
        width = rect.width()
        
        # 调整主窗口大小
        self.main_window.setGeometry(x, y, width, height)
        
        # 同步调整副屏高度
        if self.secondary_screen.isVisible():
            secondary_rect = self.secondary_screen.geometry()
            secondary_x, secondary_y = secondary_rect.x(), secondary_rect.y()
            secondary_width = secondary_rect.width()
            self.secondary_screen.setGeometry(secondary_x, secondary_y, secondary_width, height)
        
        # 更新配置
        self.config_manager.set("main_window.height", height)
    
    def set_main_window_x(self, x):
        """设置主窗口X坐标"""
        # 获取当前窗口位置和大小
        rect = self.main_window.geometry()
        y, width, height = rect.y(), rect.width(), rect.height()
        
        # 使用blockSignals避免触发valueChanged信号
        self.main_window.blockSignals(True)
        # 调整主窗口位置
        self.main_window.setGeometry(x, y, width, height)
        self.main_window.blockSignals(False)
        
        # 更新配置
        self.config_manager.set("main_window.x", x)
    
    def set_main_window_y(self, y):
        """设置主窗口Y坐标"""
        # 获取当前窗口位置和大小
        rect = self.main_window.geometry()
        x, width, height = rect.x(), rect.width(), rect.height()
        
        # 使用blockSignals避免触发valueChanged信号
        self.main_window.blockSignals(True)
        # 调整主窗口位置
        self.main_window.setGeometry(x, y, width, height)
        self.main_window.blockSignals(False)
        
        # 更新配置
        self.config_manager.set("main_window.y", y)
    
    def set_secondary_window_x(self, x):
        """设置副屏X坐标"""
        # 获取当前窗口位置和大小
        rect = self.secondary_screen.geometry()
        y, width, height = rect.y(), rect.width(), rect.height()
        
        # 使用blockSignals避免触发valueChanged信号
        self.secondary_screen.blockSignals(True)
        # 调整副屏位置
        self.secondary_screen.setGeometry(x, y, width, height)
        self.secondary_screen.blockSignals(False)
        
        # 更新配置
        self.config_manager.set("secondary_window.x", x)
    
    def set_secondary_window_y(self, y):
        """设置副屏Y坐标"""
        # 获取当前窗口位置和大小
        rect = self.secondary_screen.geometry()
        x, width, height = rect.x(), rect.width(), rect.height()
        
        # 使用blockSignals避免触发valueChanged信号
        self.secondary_screen.blockSignals(True)
        # 调整副屏位置
        self.secondary_screen.setGeometry(x, y, width, height)
        self.secondary_screen.blockSignals(False)
        
        # 更新配置
        self.config_manager.set("secondary_window.y", y)
    
    def open_file(self, file_path):
        """打开文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.control_panel.set_text(content)
            self.text_processor.set_text(content)
            self.update_display()
            self.update_control_panel()
            # 更新最后打开的文件路径
            self.config_manager.set("last_opened_file", file_path)
            # 更新控制面板的当前文件路径
            self.control_panel.current_file_path = file_path
        except Exception as e:
            print(f"打开文件失败: {e}")
    
    def save_file(self, file_path):
        """保存文件"""
        try:
            content = self.control_panel.text_edit.toPlainText()
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            # 更新最后打开的文件路径
            self.config_manager.set("last_opened_file", file_path)
            # 更新控制面板的当前文件路径
            self.control_panel.current_file_path = file_path
        except Exception as e:
            print(f"保存文件失败: {e}")
    
    def clear_text(self):
        """清空文本"""
        self.text_processor.clear()
        self.update_display()
        self.update_control_panel()
    
    def on_save_config(self):
        """保存配置"""
        # 更新配置值
        self.config_manager.set("scroll_speed", self.settings["scroll_speed"])
        self.config_manager.set("font_size", self.settings["font_size"])
        self.config_manager.set("background_color", self.settings["background_color"])
        self.config_manager.set("text_color", self.settings["text_color"])
        self.config_manager.set("paragraph_duration", self.text_processor.paragraph_duration)
        self.config_manager.set("paragraph_time_control_mode", self.text_processor.time_control_mode)
        self.config_manager.set("secondary_screen_topmost", self.settings["secondary_screen_topmost"])
        self.config_manager.set("main_window_topmost", self.settings["main_window_topmost"])
        
        # 保存到文件
        self.config_manager.save_config()
    
    def on_reset_config(self):
        """重置配置"""
        # 重置为默认配置
        self.config_manager.config = self.config_manager.default_config.copy()
        self.config_manager.save_config()
        
        # 重新加载配置
        self.settings = {
            "scroll_speed": self.config_manager.get("scroll_speed"),
            "font_size": self.config_manager.get("font_size"),
            "background_color": self.config_manager.get("background_color"),
            "text_color": self.config_manager.get("text_color"),
            "paragraph_duration": self.config_manager.get("paragraph_duration"),
            "secondary_screen_enabled": False,  # 固定默认为False，不读取配置
            "secondary_screen_topmost": self.config_manager.get("secondary_screen_topmost"),
            "main_window_topmost": self.config_manager.get("main_window_topmost")
        }
        
        # 应用配置到窗口
        self.apply_config_to_windows()
        
        # 更新文本处理器
        self.text_processor.set_paragraph_duration(self.settings["paragraph_duration"])
        self.text_processor.set_time_control_mode(self.config_manager.get("paragraph_time_control_mode"))
    
    def start(self):
        """启动应用程序"""
        # 初始化组件
        self.initialize_components()
        
        # 显示主窗口和控制面板
        self.main_window.show()
        self.control_panel.show()
        
        # 确保副屏默认隐藏
        self.secondary_screen.hide()
        
        # 启动事件循环
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    # 创建并启动应用程序
    app = MainApp()
    app.start()
