#!/usr/bin/env python3
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 添加数学库路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import PyQt6
from PyQt6 import QtWidgets
from src.ui.main_window import MainWindow
from src.core.application import Application

if __name__ == "__main__":
    try:
        # 创建Qt应用
        app = QtWidgets.QApplication(sys.argv)
        
        # 创建应用核心
        core_app = Application()
        
        # 创建主窗口
        main_window = MainWindow(core_app)
        main_window.show()
        
        # 运行应用
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
