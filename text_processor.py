import re
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class TextProcessor(QObject):
    """文本处理器，负责文本分段和管理"""
    
    # 定义信号
    paragraphs_updated = pyqtSignal(list)  # 段落列表更新
    current_paragraph_changed = pyqtSignal(int)  # 当前段落索引改变
    
    def __init__(self):
        super().__init__()
        
        # 初始化属性
        self.raw_text = ""
        self.paragraphs = []
        self.current_paragraph_index = 0
        self.paragraph_duration = 10  # 默认每段停留10秒
        self.is_auto_playing = False  # 是否自动播放
        self.remaining_time = 0  # 暂停时的剩余时间
        self.time_control_mode = "global"  # 时间控制方式："global"全局控制，"local"局部文本标识控制
        self.paragraph_durations = {}  # 存储每个段落的自定义持续时间
        
        # 段落自动跳转定时器
        self.paragraph_timer = QTimer(self)
        self.paragraph_timer.timeout.connect(self.auto_next_paragraph)
        
        # 正则表达式模式，用于匹配({时间})格式的段落标识，时间格式为分:秒
        self.paragraph_pattern = re.compile(r'\(\{([0-9]+:[0-9]+)\}\)')
    
    def set_text(self, text):
        """设置原始文本并进行分段处理"""
        # 保存当前段落索引，避免重置
        current_index = self.current_paragraph_index
        # 保存自动播放状态
        was_playing = self.is_auto_playing
        
        self.raw_text = text
        self.parse_paragraphs()
        
        # 确保当前段落索引不超出新的段落数量范围
        if current_index >= len(self.paragraphs):
            current_index = max(0, len(self.paragraphs) - 1)
        self.current_paragraph_index = current_index
        
        self.paragraphs_updated.emit(self.paragraphs)
        self.current_paragraph_changed.emit(self.current_paragraph_index)
        
        # 恢复自动播放状态
        if was_playing and not self.is_auto_playing:
            self.start_auto_play()
    
    def parse_paragraphs(self):
        """解析文本，识别({时间})格式的段落标识并分段"""
        # 重置段落持续时间字典
        self.paragraph_durations = {}
        
        # 使用正则表达式查找所有匹配的段落标识和位置
        matches = list(self.paragraph_pattern.finditer(self.raw_text))
        
        # 如果没有匹配，整个文本作为一个段落
        if not matches:
            self.paragraphs = [self.raw_text.strip() if self.raw_text.strip() else ""]
            return
        
        # 初始化段落列表
        self.paragraphs = []
        
        # 处理第一个段落
        start_pos = 0
        first_match = matches[0]
        first_paragraph = self.raw_text[start_pos:first_match.start()].strip()
        if first_paragraph:
            self.paragraphs.append(first_paragraph)
        
        # 处理中间段落
        for i in range(len(matches)):
            match = matches[i]
            # 解析时间格式：分:秒
            time_str = match.group(1)
            minutes, seconds = map(int, time_str.split(':'))
            duration = minutes * 60 + seconds
            
            # 确定下一个段落的开始位置
            if i < len(matches) - 1:
                next_match = matches[i + 1]
                next_paragraph = self.raw_text[match.end():next_match.start()].strip()
            else:
                # 最后一个匹配，处理到文本末尾
                next_paragraph = self.raw_text[match.end():].strip()
            
            # 如果段落内容不为空，添加到段落列表并存储持续时间
            if next_paragraph:
                # 存储该段落的持续时间（索引是当前段落列表的长度，即下一个段落的索引）
                self.paragraph_durations[len(self.paragraphs)] = duration
                self.paragraphs.append(next_paragraph)
        
        # 如果没有段落，添加一个空段落
        if not self.paragraphs:
            self.paragraphs = [""]
    
    def get_current_paragraph(self):
        """获取当前段落文本"""
        if 0 <= self.current_paragraph_index < len(self.paragraphs):
            return self.paragraphs[self.current_paragraph_index]
        return ""
    
    def next_paragraph(self):
        """切换到下一段"""
        if self.current_paragraph_index < len(self.paragraphs) - 1:
            self.current_paragraph_index += 1
            self.current_paragraph_changed.emit(self.current_paragraph_index)
            # 重置倒计时计时器
            self.restart_paragraph_timer()
            return True
        return False
    
    def prev_paragraph(self):
        """切换到上一段"""
        if self.current_paragraph_index > 0:
            self.current_paragraph_index -= 1
            self.current_paragraph_changed.emit(self.current_paragraph_index)
            # 重置倒计时计时器
            self.restart_paragraph_timer()
            return True
        return False
    
    def set_current_paragraph(self, index):
        """直接设置当前段落索引"""
        if 0 <= index < len(self.paragraphs):
            self.current_paragraph_index = index
            self.current_paragraph_changed.emit(self.current_paragraph_index)
            # 重置倒计时计时器
            self.restart_paragraph_timer()
            return True
        return False
    
    def set_paragraph_duration(self, duration):
        """设置每段停留时间"""
        if duration > 0:
            self.paragraph_duration = duration
            # 立即重启计时器以应用新的停留时间
            self.restart_paragraph_timer()
    
    def set_time_control_mode(self, mode):
        """设置时间控制方式："global"或"local"""
        if mode in ["global", "local"]:
            self.time_control_mode = mode
            # 重启计时器以应用新的控制方式
            self.restart_paragraph_timer()
    
    def start_auto_play(self):
        """开始自动播放 - 如果有剩余时间则从剩余时间继续"""
        self.is_auto_playing = True
        if self.remaining_time > 0:
            # 从剩余时间继续
            self.paragraph_timer.start(self.remaining_time)
        else:
            # 根据时间控制方式选择初始持续时间
            if self.time_control_mode == "local" and self.current_paragraph_index in self.paragraph_durations:
                # 使用段落自定义持续时间
                duration = self.paragraph_durations[self.current_paragraph_index]
            else:
                # 使用全局持续时间
                duration = self.paragraph_duration
            self.paragraph_timer.start(duration * 1000)
    
    def stop_auto_play(self):
        """停止自动播放 - 保存剩余时间"""
        if self.paragraph_timer.isActive():
            # 保存剩余时间
            self.remaining_time = self.paragraph_timer.remainingTime()
        self.is_auto_playing = False
        self.paragraph_timer.stop()
    
    def restart_paragraph_timer(self):
        """重新启动段落定时器 - 用于重置或切换段落时"""
        self.remaining_time = 0  # 重置剩余时间
        if self.is_auto_playing:
            self.paragraph_timer.stop()
            # 根据时间控制方式选择持续时间
            if self.time_control_mode == "local" and self.current_paragraph_index in self.paragraph_durations:
                # 使用段落自定义持续时间
                duration = self.paragraph_durations[self.current_paragraph_index]
            else:
                # 使用全局持续时间
                duration = self.paragraph_duration
            self.paragraph_timer.start(duration * 1000)
    
    def auto_next_paragraph(self):
        """自动跳转到下一段"""
        if not self.next_paragraph():
            # 已经是最后一段，停止自动播放
            self.stop_auto_play()
    
    def get_total_paragraphs(self):
        """获取总段落数"""
        return len(self.paragraphs)
    
    def get_paragraph_progress(self):
        """获取当前段落进度（0.0 - 1.0）"""
        if len(self.paragraphs) == 0:
            return 0.0
        return self.current_paragraph_index / len(self.paragraphs)
    
    def clear(self):
        """清空文本和段落"""
        self.raw_text = ""
        self.paragraphs = [""]
        self.current_paragraph_index = 0
        self.paragraphs_updated.emit(self.paragraphs)
        self.current_paragraph_changed.emit(self.current_paragraph_index)
