import PyQt6
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

# 重命名常用组件以保持代码兼容性
QMainWindow = QtWidgets.QMainWindow
QMenuBar = QtWidgets.QMenuBar
QToolBar = QtWidgets.QToolBar
QStatusBar = QtWidgets.QStatusBar
QDockWidget = QtWidgets.QDockWidget
QWidget = QtWidgets.QWidget
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QMenu = QtWidgets.QMenu
QLabel = QtWidgets.QLabel
from src.ui.render_widget import RenderWidget
from src.ui.property_panel import PropertyPanel
from src.ui.tool_panel import ToolPanel

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self, core_app):
        super().__init__()
        self.core_app = core_app
        self.property_panel = None
        self.init_ui()
        
        # 连接信号，当选择对象变化时更新属性面板
        # 注意：这里简化处理，实际应用中可能需要使用信号槽机制
        # 暂时在每次渲染时检查选择状态
    
    def init_ui(self):
        """初始化UI"""
        try:
            # 设置窗口标题和大小
            self.setWindowTitle("3D Modeling Software")
            self.setGeometry(100, 100, 1200, 800)
            
            # 创建菜单栏
            self.create_menu_bar()
            
            # 创建工具栏
            self.create_tool_bar()
            
            # 创建中央渲染区域
            self.render_widget = RenderWidget(self.core_app)
            self.setCentralWidget(self.render_widget)
            
            # 创建右侧属性面板
            self.create_property_panel()
            
            # 创建左侧工具面板
            self.create_tool_panel()
            
            # 创建状态栏
            self.create_status_bar()
            
            # 设置渲染器
            self.core_app.set_renderer(self.render_widget)
            
        except Exception as e:
            print(f"Error initializing UI: {e}")
            import traceback
            traceback.print_exc()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        try:
            menu_bar = QMenuBar()
            
            # 文件菜单
            file_menu = QMenu("File", self)
            file_menu.addAction("New")
            file_menu.addAction("Open")
            file_menu.addAction("Save")
            file_menu.addSeparator()
            file_menu.addAction("Exit")
            menu_bar.addMenu(file_menu)
            
            # 编辑菜单
            edit_menu = QMenu("Edit", self)
            edit_menu.addAction("Undo")
            edit_menu.addAction("Redo")
            edit_menu.addSeparator()
            edit_menu.addAction("Cut")
            edit_menu.addAction("Copy")
            edit_menu.addAction("Paste")
            menu_bar.addMenu(edit_menu)
            
            # 视图菜单
            view_menu = QMenu("View", self)
            view_menu.addAction("Reset View")
            view_menu.addAction("Wireframe")
            view_menu.addAction("Solid")
            menu_bar.addMenu(view_menu)
            
            # 帮助菜单
            help_menu = QMenu("Help", self)
            help_menu.addAction("About")
            menu_bar.addMenu(help_menu)
            
            self.setMenuBar(menu_bar)
            
        except Exception as e:
            print(f"Error creating menu bar: {e}")
    
    def create_tool_bar(self):
        """创建工具栏"""
        try:
            tool_bar = QToolBar("Main Toolbar")
            
            # 添加工具按钮
            tool_bar.addAction("Select")
            tool_bar.addAction("Move")
            tool_bar.addAction("Rotate")
            tool_bar.addAction("Scale")
            tool_bar.addSeparator()
            tool_bar.addAction("Cube")
            tool_bar.addAction("Sphere")
            tool_bar.addAction("Cylinder")
            
            self.addToolBar(tool_bar)
            
        except Exception as e:
            print(f"Error creating tool bar: {e}")
    
    def create_property_panel(self):
        """创建属性面板"""
        try:
            property_dock = QDockWidget("Properties", self)
            self.property_panel = PropertyPanel(self.core_app)
            property_dock.setWidget(self.property_panel)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, property_dock)
            
        except Exception as e:
            print(f"Error creating property panel: {e}")
    
    def create_tool_panel(self):
        """创建工具面板"""
        try:
            tool_dock = QDockWidget("Tools", self)
            tool_panel = ToolPanel(self.core_app)
            tool_dock.setWidget(tool_panel)
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, tool_dock)
            
        except Exception as e:
            print(f"Error creating tool panel: {e}")
    
    def create_status_bar(self):
        """创建状态栏"""
        try:
            status_bar = QStatusBar()
            status_bar.addWidget(QLabel("Ready"))
            self.setStatusBar(status_bar)
            
        except Exception as e:
            print(f"Error creating status bar: {e}")
    
    def update_property_panel(self):
        """更新属性面板"""
        try:
            if self.property_panel:
                self.property_panel.update_properties(self.core_app.selected_object)
        except Exception as e:
            print(f"Error updating property panel: {e}")
    
    def set_selected_object(self, obj):
        """设置选中对象"""
        try:
            self.core_app.selected_object = obj
            self.update_property_panel()
        except Exception as e:
            print(f"Error setting selected object: {e}")
