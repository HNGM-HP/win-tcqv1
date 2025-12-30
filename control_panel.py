from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QPushButton, 
                             QLabel, QSlider, QSpinBox, QFileDialog, QColorDialog, 
                             QLineEdit, QTextEdit, QProgressBar, QCheckBox, QGroupBox, 
                             QDoubleSpinBox, QFormLayout, QFrame, QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor

from help_dialog import HelpDialog

class ControlPanel(QWidget):
    """控制面板，集成所有功能控制选项"""
    
    # 定义信号
    # 文件操作信号
    open_file = pyqtSignal(str)
    save_file = pyqtSignal(str)
    save_as_file = pyqtSignal(str)
    clear_text = pyqtSignal()
    
    # 文本内容信号
    text_changed = pyqtSignal(str)
    
    # 滚动控制信号
    start_scroll = pyqtSignal()
    pause_scroll = pyqtSignal()
    reset_scroll = pyqtSignal()
    scroll_speed_changed = pyqtSignal(int)
    
    # 段落控制信号
    paragraph_changed = pyqtSignal(int)
    paragraph_duration_changed = pyqtSignal(int)
    paragraph_scroll_changed = pyqtSignal(float)
    paragraph_time_control_mode_changed = pyqtSignal(str)
    
    # 样式控制信号
    font_size_changed = pyqtSignal(int)
    background_color_changed = pyqtSignal(QColor)
    text_color_changed = pyqtSignal(QColor)
    
    # 屏幕控制信号
    toggle_secondary_screen = pyqtSignal(bool)
    toggle_main_window_topmost = pyqtSignal(bool)
    toggle_secondary_window_topmost = pyqtSignal(bool)
    main_window_width_changed = pyqtSignal(int)
    main_window_height_changed = pyqtSignal(int)
    main_window_x_changed = pyqtSignal(int)
    main_window_y_changed = pyqtSignal(int)
    secondary_window_x_changed = pyqtSignal(int)
    secondary_window_y_changed = pyqtSignal(int)
    
    # 配置控制信号
    save_config = pyqtSignal()
    reset_config = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置窗口属性
        self.setWindowTitle("控制面板")
        self.setGeometry(100, 100, 400, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        
        # 初始化属性
        self.current_file_path = None
        self.is_scrolling = False
        
        # 创建UI组件
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI组件"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        
        # 创建各个标签页
        self.text_tab = self.create_text_tab()
        self.scroll_tab = self.create_scroll_tab()
        self.paragraph_tab = self.create_paragraph_tab()
        self.style_tab = self.create_style_tab()
        self.screen_tab = self.create_screen_tab()
        
        # 添加标签页到标签页控件
        self.tab_widget.addTab(self.text_tab, "文本管理")
        self.tab_widget.addTab(self.scroll_tab, "滚动控制")
        self.tab_widget.addTab(self.paragraph_tab, "段落设置")
        self.tab_widget.addTab(self.style_tab, "样式定制")
        self.tab_widget.addTab(self.screen_tab, "多屏设置")
        
        # 创建底部按钮布局
        bottom_layout = QHBoxLayout()
        
        # 创建配置按钮
        self.save_config_btn = QPushButton("保存配置")
        self.reset_config_btn = QPushButton("重置配置")
        self.help_btn = QPushButton("帮助")
        
        # 连接信号
        self.save_config_btn.clicked.connect(self.on_save_config)
        self.reset_config_btn.clicked.connect(self.on_reset_config)
        self.help_btn.clicked.connect(self.show_help)
        
        # 添加按钮到底部布局
        bottom_layout.addWidget(self.save_config_btn)
        bottom_layout.addWidget(self.reset_config_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.help_btn)
        
        # 创建异常提示标签
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("QLabel { color: red; font-size: 12px; }")
        self.error_label.setAlignment(Qt.AlignCenter)
        
        # 添加标签页控件、底部布局和异常提示到主布局
        main_layout.addWidget(self.tab_widget)
        main_layout.addLayout(bottom_layout)
        main_layout.addWidget(self.error_label)
    
    def create_text_tab(self):
        """创建文本管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 文件操作按钮组
        file_group = QGroupBox("文件操作")
        file_layout = QHBoxLayout(file_group)
        
        self.open_btn = QPushButton("打开")
        self.save_btn = QPushButton("保存")
        self.save_as_btn = QPushButton("另存为")
        self.clear_btn = QPushButton("清空")
        
        file_layout.addWidget(self.open_btn)
        file_layout.addWidget(self.save_btn)
        file_layout.addWidget(self.save_as_btn)
        file_layout.addWidget(self.clear_btn)
        
        # 文本编辑区域
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("请输入或粘贴提词文本，使用({分:秒})分隔段落...")
        
        # 连接信号
        self.open_btn.clicked.connect(self.on_open_file)
        self.save_btn.clicked.connect(self.on_save_file)
        self.save_as_btn.clicked.connect(self.on_save_as_file)
        self.clear_btn.clicked.connect(self.on_clear_text)
        self.text_edit.textChanged.connect(self.on_text_changed)
        
        # 添加到布局
        layout.addWidget(file_group)
        layout.addWidget(self.text_edit)
        
        return tab
    
    def create_scroll_tab(self):
        """创建滚动控制标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 滚动控制按钮组
        control_group = QGroupBox("滚动控制")
        control_layout = QHBoxLayout(control_group)
        
        self.start_pause_btn = QPushButton("开始")
        self.reset_btn = QPushButton("重置")
        
        control_layout.addWidget(self.start_pause_btn)
        control_layout.addWidget(self.reset_btn)
        
        # 滚动速度控制
        speed_group = QGroupBox("滚动速度")
        speed_layout = QVBoxLayout(speed_group)
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(200, 100000)
        self.speed_slider.setValue(1000)
        self.speed_value = QLabel("1000")
        
        # 添加数值输入框
        speed_input_layout = QHBoxLayout()
        speed_input_layout.addWidget(QLabel("精确数值:"))
        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setRange(200, 100000)
        self.speed_spinbox.setValue(1000)
        speed_input_layout.addWidget(self.speed_spinbox)
        speed_input_layout.addStretch()
        
        # 添加滚动一行时间显示
        self.scroll_time_label = QLabel("滚动一行所需时间约: -- 秒")
        self.scroll_time_label.setAlignment(Qt.AlignCenter)
        
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_value, alignment=Qt.AlignCenter)
        speed_layout.addLayout(speed_input_layout)
        speed_layout.addWidget(self.scroll_time_label)
        
        # 连接信号
        self.start_pause_btn.clicked.connect(self.on_start_pause)
        self.reset_btn.clicked.connect(self.reset_scroll)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        self.speed_spinbox.valueChanged.connect(self.on_speed_spinbox_changed)
        
        # 添加到布局
        layout.addWidget(control_group)
        layout.addWidget(speed_group)
        
        return tab
    
    def create_paragraph_tab(self):
        """创建段落设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 段落切换控制
        nav_group = QGroupBox("段落导航")
        nav_layout = QHBoxLayout(nav_group)
        
        self.prev_paragraph_btn = QPushButton("上一段")
        self.next_paragraph_btn = QPushButton("下一段")
        self.current_paragraph_label = QLabel("段落 1 / 1")
        
        nav_layout.addWidget(self.prev_paragraph_btn)
        nav_layout.addWidget(self.current_paragraph_label)
        nav_layout.addWidget(self.next_paragraph_btn)
        
        # 段落停留时间
        duration_group = QGroupBox("段落停留时间")
        duration_layout = QVBoxLayout(duration_group)
        
        # 时间控制方式选择
        control_mode_layout = QHBoxLayout()
        control_mode_layout.addWidget(QLabel("控制方式:"))
        self.time_control_mode_combo = QComboBox()
        self.time_control_mode_combo.addItems(["全局统一控制", "文本标识控制"])
        self.time_control_mode_combo.setCurrentIndex(0)
        control_mode_layout.addWidget(self.time_control_mode_combo)
        control_mode_layout.addStretch()
        
        # 全局停留时间设置
        global_duration_layout = QHBoxLayout()
        global_duration_layout.addWidget(QLabel("全局停留时间（秒）:"))
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(1, 3600)
        self.duration_spinbox.setValue(10)
        global_duration_layout.addWidget(self.duration_spinbox)
        global_duration_layout.addStretch()
        
        duration_layout.addLayout(control_mode_layout)
        duration_layout.addLayout(global_duration_layout)
        
        # 段落进度条
        progress_group = QGroupBox("段落进度")
        progress_layout = QVBoxLayout(progress_group)
        
        self.paragraph_progress = QProgressBar()
        self.paragraph_progress.setValue(0)
        self.paragraph_progress.setMinimum(0)
        self.paragraph_progress.setMaximum(100)
        self.paragraph_progress.setMouseTracking(True)
        self.paragraph_progress.mousePressEvent = self.on_paragraph_progress_mouse_press
        self.paragraph_progress.mouseMoveEvent = self.on_paragraph_progress_mouse_move
        
        self.overall_progress = QProgressBar()
        self.overall_progress.setValue(0)
        self.overall_progress.setMinimum(0)
        self.overall_progress.setMaximum(100)
        self.overall_progress.setMouseTracking(True)
        self.overall_progress.mousePressEvent = self.on_overall_progress_mouse_press
        self.overall_progress.mouseMoveEvent = self.on_overall_progress_mouse_move
        
        progress_layout.addWidget(QLabel("当前段落:"))
        progress_layout.addWidget(self.paragraph_progress)
        progress_layout.addWidget(QLabel("整体进度:"))
        progress_layout.addWidget(self.overall_progress)
        
        # 连接信号
        self.prev_paragraph_btn.clicked.connect(self.on_prev_paragraph)
        self.next_paragraph_btn.clicked.connect(self.on_next_paragraph)
        self.duration_spinbox.valueChanged.connect(self.paragraph_duration_changed)
        self.time_control_mode_combo.currentIndexChanged.connect(self.on_time_control_mode_changed)
        # 连接信号，确保时间控制方式变化时能保存到配置
        self.time_control_mode_combo.currentIndexChanged.connect(self.save_config)
        
        # 添加到布局
        layout.addWidget(nav_group)
        layout.addWidget(duration_group)
        layout.addWidget(progress_group)
        
        return tab
    
    def create_style_tab(self):
        """创建样式定制标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 字体大小控制
        font_group = QGroupBox("字体大小")
        font_layout = QHBoxLayout(font_group)
        
        self.font_size_spinbox = QSpinBox()
        self.font_size_spinbox.setRange(12, 120)
        self.font_size_spinbox.setValue(36)
        
        font_layout.addWidget(self.font_size_spinbox)
        
        # 颜色控制
        color_group = QGroupBox("颜色设置")
        color_layout = QFormLayout(color_group)
        
        # 背景色
        bg_layout = QHBoxLayout()
        self.bg_color_btn = QPushButton("选择背景色")
        self.bg_color_display = QLabel("#000000")
        self.bg_color_display.setFixedWidth(100)
        self.bg_color_display.setAlignment(Qt.AlignCenter)
        self.bg_color_display.setStyleSheet("background-color: #000000; color: white; border: 1px solid gray;")
        
        bg_layout.addWidget(self.bg_color_btn)
        bg_layout.addWidget(self.bg_color_display)
        
        # 文本色
        text_layout = QHBoxLayout()
        self.text_color_btn = QPushButton("选择文本色")
        self.text_color_display = QLabel("#ffffff")
        self.text_color_display.setFixedWidth(100)
        self.text_color_display.setAlignment(Qt.AlignCenter)
        self.text_color_display.setStyleSheet("background-color: #ffffff; color: black; border: 1px solid gray;")
        
        text_layout.addWidget(self.text_color_btn)
        text_layout.addWidget(self.text_color_display)
        
        color_layout.addRow("背景色:", bg_layout)
        color_layout.addRow("文本色:", text_layout)
        
        # 连接信号
        self.font_size_spinbox.valueChanged.connect(self.font_size_changed)
        self.bg_color_btn.clicked.connect(self.on_bg_color_clicked)
        self.text_color_btn.clicked.connect(self.on_text_color_clicked)
        
        # 添加到布局
        layout.addWidget(font_group)
        layout.addWidget(color_group)
        
        return tab
    
    def create_screen_tab(self):
        """创建多屏设置标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 显示窗口设置
        main_window_group = QGroupBox("显示窗口设置")
        main_window_layout = QFormLayout(main_window_group)
        
        # 主窗口大小控制
        self.main_width_spinbox = QSpinBox()
        self.main_width_spinbox.setRange(400, 2000)
        self.main_width_spinbox.setValue(800)
        
        self.main_height_spinbox = QSpinBox()
        self.main_height_spinbox.setRange(300, 1500)
        self.main_height_spinbox.setValue(600)
        
        # 主窗口坐标控制
        main_coords_layout = QHBoxLayout()
        self.main_x_spinbox = QSpinBox()
        self.main_x_spinbox.setRange(-2000, 4000)
        self.main_x_spinbox.setValue(100)
        self.main_y_spinbox = QSpinBox()
        self.main_y_spinbox.setRange(-2000, 4000)
        self.main_y_spinbox.setValue(100)
        main_coords_layout.addWidget(QLabel("X:"))
        main_coords_layout.addWidget(self.main_x_spinbox)
        main_coords_layout.addWidget(QLabel("Y:"))
        main_coords_layout.addWidget(self.main_y_spinbox)
        main_coords_layout.addStretch()
        
        # 主窗口置顶
        self.main_topmost_check = QCheckBox("主窗口置顶")
        
        main_window_layout.addRow("宽度:", self.main_width_spinbox)
        main_window_layout.addRow("高度:", self.main_height_spinbox)
        main_window_layout.addRow("坐标:", main_coords_layout)
        main_window_layout.addRow(self.main_topmost_check)
        
        # 副屏设置
        secondary_group = QGroupBox("副屏设置")
        secondary_layout = QFormLayout(secondary_group)
        
        # 副屏控制选项
        self.secondary_screen_check = QCheckBox("启用副屏")
        self.secondary_topmost_check = QCheckBox("副屏置顶")
        
        # 副屏坐标控制
        secondary_coords_layout = QHBoxLayout()
        self.secondary_x_spinbox = QSpinBox()
        self.secondary_x_spinbox.setRange(-2000, 4000)
        self.secondary_x_spinbox.setValue(1000)
        self.secondary_y_spinbox = QSpinBox()
        self.secondary_y_spinbox.setRange(-2000, 4000)
        self.secondary_y_spinbox.setValue(100)
        secondary_coords_layout.addWidget(QLabel("X:"))
        secondary_coords_layout.addWidget(self.secondary_x_spinbox)
        secondary_coords_layout.addWidget(QLabel("Y:"))
        secondary_coords_layout.addWidget(self.secondary_y_spinbox)
        secondary_coords_layout.addStretch()
        
        # 添加控件到布局
        secondary_layout.addRow(self.secondary_screen_check)
        secondary_layout.addRow("坐标:", secondary_coords_layout)
        secondary_layout.addRow(self.secondary_topmost_check)
        
        # 连接信号
        self.main_width_spinbox.valueChanged.connect(self.on_main_window_width_changed)
        self.main_height_spinbox.valueChanged.connect(self.on_main_window_height_changed)
        # 修改为editingFinished信号，仅在用户完成输入后更新
        self.main_x_spinbox.editingFinished.connect(self.on_main_window_x_editing_finished)
        self.main_y_spinbox.editingFinished.connect(self.on_main_window_y_editing_finished)
        self.secondary_x_spinbox.editingFinished.connect(self.on_secondary_window_x_editing_finished)
        self.secondary_y_spinbox.editingFinished.connect(self.on_secondary_window_y_editing_finished)
        self.secondary_screen_check.stateChanged.connect(self.on_secondary_screen_toggled)
        self.secondary_topmost_check.stateChanged.connect(self.on_secondary_topmost_toggled)
        self.main_topmost_check.stateChanged.connect(self.on_main_topmost_toggled)
        
        # 添加到布局
        layout.addWidget(main_window_group)
        layout.addWidget(secondary_group)
        
        return tab
    
    # 槽函数实现
    @pyqtSlot()
    def on_open_file(self):
        """打开文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文本文件", "", "文本文件 (*.txt)")
        if file_path:
            self.open_file.emit(file_path)
    
    @pyqtSlot()
    def on_save_file(self):
        """保存文件"""
        if self.current_file_path:
            self.save_file.emit(self.current_file_path)
        else:
            self.on_save_as_file()
    
    @pyqtSlot()
    def on_save_as_file(self):
        """另存为文件"""
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文本文件", "", "文本文件 (*.txt)")
        if file_path:
            self.current_file_path = file_path
            self.save_as_file.emit(file_path)
    
    @pyqtSlot()
    def on_clear_text(self):
        """清空文本"""
        self.text_edit.clear()
        self.clear_text.emit()
    
    @pyqtSlot()
    def on_text_changed(self):
        """文本内容改变"""
        self.text_changed.emit(self.text_edit.toPlainText())
    
    @pyqtSlot()
    def on_start_pause(self):
        """开始/暂停滚动"""
        if self.is_scrolling:
            self.start_pause_btn.setText("开始")
            self.pause_scroll.emit()
        else:
            self.start_pause_btn.setText("暂停")
            self.start_scroll.emit()
        self.is_scrolling = not self.is_scrolling
    
    @pyqtSlot(int)
    def on_speed_changed(self, value):
        """滚动速度改变"""
        # 同步更新输入框值（避免循环触发信号）
        if self.speed_spinbox.value() != value:
            self.speed_spinbox.blockSignals(True)
            self.speed_spinbox.setValue(value)
            self.speed_spinbox.blockSignals(False)
        
        self.speed_value.setText(str(value))
        self.scroll_speed_changed.emit(value)
        
        # 更新滚动一行时间显示
        self.update_scroll_time(value)
    
    @pyqtSlot(int)
    def on_speed_spinbox_changed(self, value):
        """滚动速度输入框值改变"""
        # 同步更新滑块值（避免循环触发信号）
        if self.speed_slider.value() != value:
            self.speed_slider.blockSignals(True)
            self.speed_slider.setValue(value)
            self.speed_slider.blockSignals(False)
        
        self.speed_value.setText(str(value))
        self.scroll_speed_changed.emit(value)
        
        # 更新滚动一行时间显示
        self.update_scroll_time(value)
    
    def update_scroll_time(self, speed_value, line_height=None):
        """
        更新滚动一行所需时间显示
        
        Args:
            speed_value: 滑块速度值（对应优化后的滚动速度公式）
            line_height: 可选，行高值（像素），不提供则使用默认值
        """
        try:
            import math
            
            # 限制最大值，确保滚动不会完全停止
            max_speed_value = 99999
            speed_value = min(speed_value, max_speed_value)
            
            # 计算实际滚动速度（与main.py中的公式保持一致）
            numerator = 100000 - speed_value + 1000  # 增加偏移量确保数值有效
            log_value = math.log10(numerator / 1000)
            actual_speed = 0.1 + (1000 - 0.1) * (log_value / 3)  # 映射到0.1-1000像素/秒
            
            # 计算行高
            if line_height is None:
                # 获取当前字体大小
                font_size = self.font_size_spinbox.value()
                # 计算行高（假设行高为字体大小的1.2倍）
                line_height = font_size * 1.2
            
            # 计算滚动一行所需时间（秒）
            if actual_speed > 0:
                time_per_line = line_height / actual_speed
                # 保留2位小数
                self.scroll_time_label.setText(f"滚动一行所需时间: {time_per_line:.2f} 秒")
            else:
                self.scroll_time_label.setText("滚动一行所需时间: -- 秒")
        except Exception as e:
            self.scroll_time_label.setText("滚动一行所需时间: -- 秒")
    
    @pyqtSlot()
    def on_prev_paragraph(self):
        """上一段"""
        # 这个功能将通过连接到文本处理器来实现
        pass
    
    @pyqtSlot()
    def on_next_paragraph(self):
        """下一段"""
        # 这个功能将通过连接到文本处理器来实现
        pass
    
    @pyqtSlot()
    def on_bg_color_clicked(self):
        """选择背景色"""
        color = QColorDialog.getColor(QColor(0, 0, 0), self, "选择背景色")
        if color.isValid():
            self.bg_color_display.setText(color.name())
            self.bg_color_display.setStyleSheet(f"background-color: {color.name()}; color: white; border: 1px solid gray;")
            self.background_color_changed.emit(color)
    
    @pyqtSlot()
    def on_text_color_clicked(self):
        """选择文本色"""
        color = QColorDialog.getColor(QColor(255, 255, 255), self, "选择文本色")
        if color.isValid():
            self.text_color_display.setText(color.name())
            self.text_color_display.setStyleSheet(f"background-color: {color.name()}; color: black; border: 1px solid gray;")
            self.text_color_changed.emit(color)
    
    @pyqtSlot(int)
    def on_secondary_screen_toggled(self, state):
        """副屏开关切换"""
        self.toggle_secondary_screen.emit(state == Qt.Checked)
    
    @pyqtSlot(int)
    def on_secondary_topmost_toggled(self, state):
        """副屏置顶切换"""
        self.toggle_secondary_window_topmost.emit(state == Qt.Checked)
    
    @pyqtSlot(int)
    def on_main_topmost_toggled(self, state):
        """主窗口置顶切换"""
        self.toggle_main_window_topmost.emit(state == Qt.Checked)
    
    @pyqtSlot(int)
    def on_main_window_width_changed(self, width):
        """主窗口宽度改变"""
        self.main_window_width_changed.emit(width)
    
    @pyqtSlot(int)
    def on_main_window_height_changed(self, height):
        """主窗口高度改变"""
        self.main_window_height_changed.emit(height)
    
    def on_main_window_x_editing_finished(self):
        """主窗口X坐标编辑完成"""
        x = self.main_x_spinbox.value()
        # 验证坐标值是否在有效范围内
        if not (-2000 <= x <= 4000):
            self.error_label.setText("主窗口X坐标超出有效范围(-2000~4000)")
        else:
            # 清除异常提示
            self.error_label.setText("")
        self.main_window_x_changed.emit(x)
    
    def on_main_window_y_editing_finished(self):
        """主窗口Y坐标编辑完成"""
        y = self.main_y_spinbox.value()
        # 验证坐标值是否在有效范围内
        if not (-2000 <= y <= 4000):
            self.error_label.setText("主窗口Y坐标超出有效范围(-2000~4000)")
        else:
            # 清除异常提示
            self.error_label.setText("")
        self.main_window_y_changed.emit(y)
    
    def on_secondary_window_x_editing_finished(self):
        """副屏X坐标编辑完成"""
        x = self.secondary_x_spinbox.value()
        # 验证坐标值是否在有效范围内
        if not (-2000 <= x <= 4000):
            self.error_label.setText("副屏X坐标超出有效范围(-2000~4000)")
        else:
            # 清除异常提示
            self.error_label.setText("")
        self.secondary_window_x_changed.emit(x)
    
    def on_secondary_window_y_editing_finished(self):
        """副屏Y坐标编辑完成"""
        y = self.secondary_y_spinbox.value()
        # 验证坐标值是否在有效范围内
        if not (-2000 <= y <= 4000):
            self.error_label.setText("副屏Y坐标超出有效范围(-2000~4000)")
        else:
            # 清除异常提示
            self.error_label.setText("")
        self.secondary_window_y_changed.emit(y)
    
    @pyqtSlot(int)
    def on_time_control_mode_changed(self, index):
        """时间控制方式改变"""
        # 将UI索引转换为内部模式字符串
        mode = "global" if index == 0 else "local"
        self.paragraph_time_control_mode_changed.emit(mode)
    
    # 公共方法，用于更新UI状态
    def set_text(self, text):
        """设置文本内容"""
        self.text_edit.setPlainText(text)
    
    def update_paragraph_info(self, current_index, total_paragraphs):
        """更新段落信息"""
        self.current_paragraph_label.setText(f"段落 {current_index + 1} / {total_paragraphs}")
        self.overall_progress.setRange(0, total_paragraphs - 1)
        self.overall_progress.setValue(current_index)
    
    def update_paragraph_progress(self, progress):
        """更新段落内进度"""
        self.paragraph_progress.setValue(int(progress * 100))
    
    def update_from_config(self, config):
        """从配置更新UI状态"""
        # 滚动速度 - 转换回滑块值
        scroll_speed = config.get("scroll_speed", 1000)
        # 反向计算滑块值：滑块值 = 100000 - (scroll_speed * 100)
        slider_value = int(100000 - (scroll_speed * 100))
        self.speed_slider.setValue(slider_value)
        self.speed_value.setText(str(slider_value))
        
        # 段落停留时间
        paragraph_duration = config.get("paragraph_duration", 10)
        self.duration_spinbox.setValue(paragraph_duration)
        
        # 段落停留时间控制方式
        paragraph_time_control_mode = config.get("paragraph_time_control_mode", "global")
        self.time_control_mode_combo.setCurrentIndex(0 if paragraph_time_control_mode == "global" else 1)
        
        # 字体大小
        font_size = config.get("font_size", 36)
        self.font_size_spinbox.setValue(font_size)
        
        # 窗口大小和位置
        main_window = config.get("main_window", {"width": 800, "height": 600, "x": 100, "y": 100})
        self.main_width_spinbox.setValue(main_window["width"])
        self.main_height_spinbox.setValue(main_window["height"])
        self.main_x_spinbox.setValue(main_window["x"])
        self.main_y_spinbox.setValue(main_window["y"])
        
        # 副屏位置
        secondary_window = config.get("secondary_window", {"x": 1000, "y": 100})
        self.secondary_x_spinbox.setValue(secondary_window["x"])
        self.secondary_y_spinbox.setValue(secondary_window["y"])
        
        # 置顶设置
        self.main_topmost_check.setChecked(config.get("main_window_topmost", False))
        self.secondary_topmost_check.setChecked(config.get("secondary_screen_topmost", False))
        
        # 副屏启用状态 - 固定默认为False，不读取配置
        self.secondary_screen_check.setChecked(False)
    
    def show_help(self):
        """显示帮助对话框"""
        self.help_dialog = HelpDialog(self)
        self.help_dialog.exec_()
    
    def on_save_config(self):
        """保存配置"""
        self.save_config.emit()
    
    def on_reset_config(self):
        """重置配置"""
        self.reset_config.emit()
    
    def on_paragraph_progress_mouse_press(self, event):
        """段落内进度条鼠标按下事件"""
        self.update_progress_from_mouse(event, self.paragraph_progress)
    
    def on_paragraph_progress_mouse_move(self, event):
        """段落内进度条鼠标移动事件"""
        if event.buttons() & Qt.LeftButton:
            self.update_progress_from_mouse(event, self.paragraph_progress)
    
    def on_overall_progress_mouse_press(self, event):
        """整体进度条鼠标按下事件"""
        self.update_progress_from_mouse(event, self.overall_progress)
    
    def on_overall_progress_mouse_move(self, event):
        """整体进度条鼠标移动事件"""
        if event.buttons() & Qt.LeftButton:
            self.update_progress_from_mouse(event, self.overall_progress)
    
    def update_progress_from_mouse(self, event, progress_bar):
        """根据鼠标位置更新进度条值"""
        rect = progress_bar.rect()
        pos = event.pos().x() / rect.width()
        value = int(pos * (progress_bar.maximum() - progress_bar.minimum())) + progress_bar.minimum()
        progress_bar.setValue(value)
        
        # 发出信号通知主应用程序进度变化
        if progress_bar == self.paragraph_progress:
            # 段落内进度变化，计算滚动位置比例
            scroll_progress = pos
            self.paragraph_scroll_changed.emit(scroll_progress)
        elif progress_bar == self.overall_progress:
            # 整体进度变化，切换到对应段落
            # 直接使用value作为段落索引，因为overall_progress的range已经是0到total_paragraphs-1
            self.paragraph_changed.emit(value)
