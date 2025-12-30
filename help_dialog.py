from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextBrowser, QTabWidget, QWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QPalette, QColor

class HelpDialog(QDialog):
    """帮助对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置窗口属性
        self.setWindowTitle("帮助")
        self.setGeometry(100, 100, 600, 500)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # 创建UI组件
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI组件"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        
        # 创建各个标签页
        self.intro_tab = self.create_intro_tab()
        self.usage_tab = self.create_usage_tab()
        self.features_tab = self.create_features_tab()
        self.faq_tab = self.create_faq_tab()
        
        # 添加标签页到标签页控件
        self.tab_widget.addTab(self.intro_tab, "功能介绍")
        self.tab_widget.addTab(self.usage_tab, "操作指南")
        self.tab_widget.addTab(self.features_tab, "功能详解")
        self.tab_widget.addTab(self.faq_tab, "常见问题")
        
        # 创建关闭按钮
        self.close_btn = QPushButton("关闭")
        self.close_btn.clicked.connect(self.close)
        
        # 添加组件到主布局
        main_layout.addWidget(self.tab_widget)
        main_layout.addWidget(self.close_btn, alignment=Qt.AlignRight)
    
    def create_intro_tab(self):
        """创建功能介绍标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建文本浏览器
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        
        # 设置内容
        content = """
        <h1>提词器功能介绍</h1>
        <p>提词器是一款专业的提示词程序，适用于Windows操作系统，具备以下核心功能：</p>
        <ul>
            <li>高性能多行文本渲染引擎</li>
            <li>平滑滚动系统</li>
            <li>智能分段管理</li>
            <li>视觉样式定制</li>
            <li>多屏幕扩展支持</li>
            <li>独立控制面板</li>
        </ul>
        <p>提词器适合直播、演讲、会议等多种场景使用，帮助用户流畅地展示提示文本。</p>
        <hr>
        <p style="text-align: center;">&copy; 2025 光脉科技. All rights reserved.</p>
        """
        
        text_browser.setHtml(content)
        layout.addWidget(text_browser)
        
        return tab
    
    def create_usage_tab(self):
        """创建操作指南标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建文本浏览器
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        
        # 设置内容
        content = """
        <h1>操作指南</h1>
        <h2>基本操作</h2>
        <ol>
            <li>在控制面板的"文本管理"标签页中输入或粘贴提词文本</li>
            <li>使用({})分隔不同段落</li>
            <li>在"滚动控制"标签页中调节滚动速度</li>
            <li>点击"开始"按钮开始滚动</li>
            <li>点击"暂停"按钮暂停滚动</li>
            <li>点击"重置"按钮重置滚动位置</li>
        </ol>
        <h2>高级操作</h2>
        <ul>
            <li>在"样式定制"标签页中调整字体大小和颜色</li>
            <li>在"多屏设置"标签页中启用副屏显示</li>
            <li>使用"文件操作"功能保存和加载文本文件</li>
        </ul>
        """
        
        text_browser.setHtml(content)
        layout.addWidget(text_browser)
        
        return tab
    
    def create_features_tab(self):
        """创建功能详解标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建文本浏览器
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        
        # 设置内容
        content = """
        <h1>功能详解</h1>
        <h2>文本显示系统</h2>
        <p>实现高性能多行文本渲染引擎，支持自动换行算法，确保长文本在不同窗口尺寸下均能完整显示。</p>
        
        <h2>平滑滚动引擎</h2>
        <p>基于时间插值的线性滚动系统，实现无卡顿视觉效果，滚动速度调节范围为200-100000像素/秒。</p>
        
        <h2>智能分段管理</h2>
        <p>基于正则表达式的文本解析器，自动识别({分:秒})格式的段落标识并进行分段处理，支持两种停留时间控制方式：</p>
        <ul>
        <li>全局统一控制：通过控制面板设置所有段落的统一停留时间</li>
        <li>局部文本标识控制：在每个段落标识中指定该段落的停留时间，格式为分:秒，如({00:10})表示停留10秒</li>
        </ul>
        
        <h2>视觉样式定制</h2>
        <p>集成RGB/HEX双模式颜色选择器，支持背景色和字体颜色的自定义设置，所有调整实时生效。</p>
        
        <h2>多屏幕扩展</h2>
        <p>支持副屏显示，主副屏完全同步，包括文本内容、滚动位置、字体大小、背景色、字体色以及窗口尺寸。副屏尺寸与主窗口尺寸保持一致，无需单独设置。</p>
        
        <h2>中央控制中心</h2>
        <p>独立于主显示窗口的控制面板，集中所有功能控制选项，包括文件操作、视图控制等。</p>
        """
        
        text_browser.setHtml(content)
        layout.addWidget(text_browser)
        
        return tab
    
    def create_faq_tab(self):
        """创建常见问题标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 创建文本浏览器
        text_browser = QTextBrowser()
        text_browser.setOpenExternalLinks(True)
        
        # 设置内容
        content = """
        <h1>常见问题</h1>
        <h2>Q: 如何分隔段落？</h2>
        <p>A: 使用({分:秒})作为段落分隔符，其中分:秒是该段落的停留时间，例如：</p>
        <pre>第一段内容({00:10})第二段内容({00:15})第三段内容</pre>
        <p>您可以在控制面板的"段落设置"标签页中选择时间控制方式，支持全局统一控制或局部文本标识控制。</p>
        
        <h2>Q: 如何调节滚动速度？</h2>
        <p>A: 在控制面板的"滚动控制"标签页中，使用滚动速度滑块调节，范围为200-100000像素/秒。</p>
        
        <h2>Q: 如何启用副屏显示？</h2>
        <p>A: 在控制面板的"多屏设置"标签页中，勾选"启用副屏"选项。</p>
        
        <h2>Q: 如何调整窗口位置？</h2>
        <p>A: 在控制面板的"多屏设置"标签页中，您可以：</p>
        <ul>
        <li>直接拖动窗口进行位置调整</li>
        <li>在坐标输入框中输入X和Y坐标值，按下回车键后生效</li>
        <li>坐标范围：-2000 ~ 4000</li>
        </ul>
        <p>注意：坐标修改后需要按下回车键才会生效，避免意外移动窗口。</p>
        
        <h2>Q: 如何保存当前设置？</h2>
        <p>A: 在控制面板的"文本管理"标签页中，点击"保存"或"另存为"按钮保存文本文件，或点击底部的"保存配置"按钮保存所有设置。</p>
        
        <h2>Q: 如何设置窗口置顶？</h2>
        <p>A: 在控制面板的"多屏设置"标签页中，勾选"主窗口置顶"或"副屏置顶"选项。</p>
        """
        
        text_browser.setHtml(content)
        layout.addWidget(text_browser)
        
        return tab
