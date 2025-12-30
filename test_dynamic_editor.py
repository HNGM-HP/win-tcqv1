import sys
import os
import unittest
from PyQt5.QtWidgets import QApplication, QTextBrowser
from main_window import MainDisplayWindow
from dynamic_editor import DynamicEditor

class TestDynamicEditor(unittest.TestCase):
    """测试DynamicEditor模块的功能"""
    
    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        cls.app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    
    def setUp(self):
        """创建测试对象"""
        self.dynamic_editor = DynamicEditor()
        self.main_window = MainDisplayWindow()
    
    def test_scroll_position_save_restore(self):
        """测试滚动位置的保存和恢复功能"""
        # 设置初始文本
        test_text = "\n".join([f"测试行{i}" for i in range(50)])
        self.main_window.set_text(test_text)
        
        # 模拟滚动到某个位置
        scroll_bar = self.main_window.text_browser.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum() // 2)
        self.main_window.scroll_position = 500
        self.main_window.is_scrolling = True
        
        # 保存滚动位置
        saved_state = self.dynamic_editor.save_scroll_position(self.main_window)
        
        # 验证保存的状态
        self.assertIsNotNone(saved_state)
        self.assertEqual(saved_state['scroll_bar_value'], scroll_bar.maximum() // 2)
        self.assertEqual(saved_state['scroll_position'], 500)
        self.assertEqual(saved_state['is_scrolling'], True)
        self.assertGreater(saved_state['scroll_percentage'], 0)
        self.assertLessEqual(saved_state['scroll_percentage'], 1)
        
        # 修改文本长度（模拟编辑）
        new_text = test_text + "\n".join([f"新行{i}" for i in range(20)])
        self.main_window.set_text(new_text)
        
        # 恢复滚动位置
        restored = self.dynamic_editor.restore_scroll_position(self.main_window, is_paragraph_switch=False)
        
        # 验证恢复结果
        self.assertTrue(restored)
        new_scroll_bar = self.main_window.text_browser.verticalScrollBar()
        
        # 验证滚动位置是否基于百分比正确恢复（不受文本长度变化影响）
        expected_value = int(saved_state['scroll_percentage'] * new_scroll_bar.maximum())
        actual_value = new_scroll_bar.value()
        
        # 允许有±5的误差
        self.assertAlmostEqual(actual_value, expected_value, delta=5)
    
    def test_paragraph_switch_behavior(self):
        """测试段落切换时的滚动位置行为"""
        # 设置初始文本
        test_text = "\n".join([f"测试行{i}" for i in range(50)])
        self.main_window.set_text(test_text)
        
        # 模拟滚动到某个位置
        scroll_bar = self.main_window.text_browser.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum() // 2)
        
        # 保存滚动位置
        saved_state = self.dynamic_editor.save_scroll_position(self.main_window)
        
        # 模拟段落切换时恢复滚动位置（应该返回False）
        restored = self.dynamic_editor.restore_scroll_position(self.main_window, is_paragraph_switch=True)
        
        # 验证结果
        self.assertFalse(restored)
    
    def test_dynamic_editor_reset(self):
        """测试DynamicEditor的重置功能"""
        # 设置初始文本和滚动位置
        test_text = "\n".join([f"测试行{i}" for i in range(50)])
        self.main_window.set_text(test_text)
        
        scroll_bar = self.main_window.text_browser.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum() // 2)
        
        # 保存滚动位置
        self.dynamic_editor.save_scroll_position(self.main_window)
        
        # 验证有保存的滚动位置
        self.assertIn(0, self.dynamic_editor.last_known_scroll_positions)
        
        # 重置编辑器
        self.dynamic_editor.reset()
        
        # 验证重置后滚动位置被清空
        self.assertEqual(len(self.dynamic_editor.last_known_scroll_positions), 0)
        self.assertEqual(self.dynamic_editor.current_paragraph_index, 0)
        self.assertEqual(self.dynamic_editor.is_editing, False)
    
    def test_scroll_state_management(self):
        """测试滚动状态的管理功能"""
        # 设置初始文本
        test_text = "\n".join([f"测试行{i}" for i in range(50)])
        self.main_window.set_text(test_text)
        
        # 模拟不同的滚动状态
        scroll_states = [
            {'scroll_bar_value': 100, 'scroll_position': 100, 'is_scrolling': True},
            {'scroll_bar_value': 200, 'scroll_position': 200, 'is_scrolling': False},
            {'scroll_bar_value': 300, 'scroll_position': 300, 'is_scrolling': True}
        ]
        
        for i, state in enumerate(scroll_states):
            # 设置滚动状态
            self.dynamic_editor.set_current_paragraph(i)
            self.main_window.text_browser.verticalScrollBar().setValue(state['scroll_bar_value'])
            self.main_window.scroll_position = state['scroll_position']
            self.main_window.is_scrolling = state['is_scrolling']
            
            # 保存滚动状态
            self.dynamic_editor.save_scroll_position(self.main_window)
        
        # 验证所有滚动状态都被正确保存
        self.assertEqual(len(self.dynamic_editor.last_known_scroll_positions), 3)
        
        # 验证每个滚动状态的准确性
        for i, state in enumerate(scroll_states):
            saved_state = self.dynamic_editor.get_scroll_state(i)
            self.assertIsNotNone(saved_state)
            self.assertAlmostEqual(saved_state['scroll_bar_value'], state['scroll_bar_value'], delta=5)
            self.assertEqual(saved_state['scroll_position'], state['scroll_position'])
            self.assertEqual(saved_state['is_scrolling'], state['is_scrolling'])
    
    def tearDown(self):
        """清理测试对象"""
        self.main_window.close()
    
    @classmethod
    def tearDownClass(cls):
        """清理测试环境"""
        pass

if __name__ == '__main__':
    # 运行测试
    unittest.main()