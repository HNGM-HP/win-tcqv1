from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QTextEdit

class DynamicEditor(QObject):
    """
    动态编辑器模块，负责处理文本动态编辑和滚动位置管理
    实现与自动跳转滚动逻辑的解耦
    """
    
    # 定义信号
    text_changed = pyqtSignal(str)  # 文本内容改变信号
    scroll_position_saved = pyqtSignal(object)  # 滚动位置保存信号
    scroll_position_restored = pyqtSignal(object)  # 滚动位置恢复信号
    
    def __init__(self):
        """初始化动态编辑器"""
        super().__init__()
        
        # 滚动位置相关属性
        self.scroll_positions = {}  # 保存每个段落的滚动位置
        self.current_paragraph_index = 0  # 当前段落索引
        self.is_editing = False  # 是否正在编辑
        self.last_known_scroll_positions = {}  # 保存最后已知的滚动位置
        
    def set_current_paragraph(self, index):
        """设置当前段落索引"""
        self.current_paragraph_index = index
        
    def save_scroll_position(self, window):
        """
        保存指定窗口的滚动位置
        
        Args:
            window: 窗口对象，包含text_browser属性
        """
        if hasattr(window, 'text_browser') and hasattr(window, 'scroll_position'):
            # 保存滚动条位置和自定义滚动位置
            scroll_bar_value = window.text_browser.verticalScrollBar().value()
            scroll_position = window.scroll_position
            
            # 计算滚动百分比（相对于文本总高度）
            scroll_bar = window.text_browser.verticalScrollBar()
            max_value = scroll_bar.maximum()
            scroll_percentage = scroll_bar_value / max_value if max_value > 0 else 0
            
            # 保存完整的滚动状态
            scroll_state = {
                'scroll_bar_value': scroll_bar_value,
                'scroll_position': scroll_position,
                'scroll_percentage': scroll_percentage,
                'is_scrolling': window.is_scrolling
            }
            
            # 保存到当前段落
            self.last_known_scroll_positions[self.current_paragraph_index] = scroll_state
            
            # 发出信号通知滚动位置已保存
            self.scroll_position_saved.emit(scroll_state)
            
            return scroll_state
        return None
    
    def restore_scroll_position(self, window, is_paragraph_switch=False):
        """
        恢复指定窗口的滚动位置
        
        Args:
            window: 窗口对象，包含text_browser属性
            is_paragraph_switch: 是否是段落切换
        """
        # 如果是段落切换，不恢复滚动位置（让自动跳转逻辑处理）
        if is_paragraph_switch:
            return False
        
        # 检查是否有保存的滚动位置
        if self.current_paragraph_index not in self.last_known_scroll_positions:
            return False
        
        scroll_state = self.last_known_scroll_positions[self.current_paragraph_index]
        
        # 关闭滚动定时器
        was_scrolling = window.is_scrolling
        if was_scrolling:
            window.pause_scroll()
        
        try:
            # 计算新的滚动条位置（基于滚动百分比）
            scroll_bar = window.text_browser.verticalScrollBar()
            new_max_value = scroll_bar.maximum()
            
            if new_max_value > 0:
                # 使用滚动百分比计算新的滚动条位置，确保不受内容长度变化影响
                new_scroll_bar_value = int(scroll_state['scroll_percentage'] * new_max_value)
                
                # 设置滚动条位置
                scroll_bar.setValue(new_scroll_bar_value)
                
                # 恢复自定义滚动位置
                window.scroll_position = scroll_state['scroll_position']
                
                # 恢复滚动状态
                if was_scrolling:
                    window.start_scroll()
                
                # 发出信号通知滚动位置已恢复
                self.scroll_position_restored.emit(scroll_state)
                
                return True
        except Exception as e:
            print(f"恢复滚动位置失败: {e}")
        
        return False
    
    @pyqtSlot(str)
    def on_text_changed(self, text, is_dynamic_edit=True):
        """
        处理文本变化
        
        Args:
            text: 新的文本内容
            is_dynamic_edit: 是否是动态编辑
        """
        self.is_editing = is_dynamic_edit
        self.text_changed.emit(text)
    
    def reset(self):
        """重置编辑器状态"""
        self.scroll_positions.clear()
        self.last_known_scroll_positions.clear()
        self.current_paragraph_index = 0
        self.is_editing = False
    
    def get_scroll_state(self, paragraph_index=None):
        """
        获取指定段落的滚动状态
        
        Args:
            paragraph_index: 段落索引，默认为当前段落
        
        Returns:
            滚动状态字典
        """
        if paragraph_index is None:
            paragraph_index = self.current_paragraph_index
        
        return self.last_known_scroll_positions.get(paragraph_index, None)
    
    def set_scroll_state(self, scroll_state, paragraph_index=None):
        """
        设置指定段落的滚动状态
        
        Args:
            scroll_state: 滚动状态字典
            paragraph_index: 段落索引，默认为当前段落
        """
        if paragraph_index is None:
            paragraph_index = self.current_paragraph_index
        
        self.last_known_scroll_positions[paragraph_index] = scroll_state