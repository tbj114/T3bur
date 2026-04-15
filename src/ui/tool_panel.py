from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QPushButton,
    QRadioButton, QButtonGroup
)

class ToolPanel(QWidget):
    """工具面板，用于显示和选择各种3D建模工具"""
    
    def __init__(self, core_app):
        super().__init__()
        self.core_app = core_app
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        try:
            layout = QVBoxLayout()
            
            # 创建选择工具组
            selection_group = QGroupBox("Selection Tools")
            selection_layout = QVBoxLayout()
            
            self.select_button = QPushButton("Select")
            self.select_button.clicked.connect(lambda: self.set_tool("select"))
            selection_layout.addWidget(self.select_button)
            
            selection_group.setLayout(selection_layout)
            layout.addWidget(selection_group)
            
            # 创建变换工具组
            transform_group = QGroupBox("Transform Tools")
            transform_layout = QVBoxLayout()
            
            self.move_button = QPushButton("Move")
            self.move_button.clicked.connect(lambda: self.set_tool("move"))
            transform_layout.addWidget(self.move_button)
            
            self.rotate_button = QPushButton("Rotate")
            self.rotate_button.clicked.connect(lambda: self.set_tool("rotate"))
            transform_layout.addWidget(self.rotate_button)
            
            self.scale_button = QPushButton("Scale")
            self.scale_button.clicked.connect(lambda: self.set_tool("scale"))
            transform_layout.addWidget(self.scale_button)
            
            transform_group.setLayout(transform_layout)
            layout.addWidget(transform_group)
            
            # 创建几何体工具组
            geometry_group = QGroupBox("Geometry Tools")
            geometry_layout = QVBoxLayout()
            
            self.cube_button = QPushButton("Cube")
            self.cube_button.clicked.connect(lambda: self.create_geometry("cube"))
            geometry_layout.addWidget(self.cube_button)
            
            self.sphere_button = QPushButton("Sphere")
            self.sphere_button.clicked.connect(lambda: self.create_geometry("sphere"))
            geometry_layout.addWidget(self.sphere_button)
            
            self.cylinder_button = QPushButton("Cylinder")
            self.cylinder_button.clicked.connect(lambda: self.create_geometry("cylinder"))
            geometry_layout.addWidget(self.cylinder_button)
            
            geometry_group.setLayout(geometry_layout)
            layout.addWidget(geometry_group)
            
            # 添加拉伸因子，使面板内容靠上
            layout.addStretch()
            
            self.setLayout(layout)
            
        except Exception as e:
            print(f"Error initializing tool panel: {e}")
            import traceback
            traceback.print_exc()
    
    def set_tool(self, tool_name):
        """设置当前工具"""
        try:
            self.core_app.set_tool(tool_name)
        except Exception as e:
            print(f"Error setting tool: {e}")
    
    def create_geometry(self, geometry_type):
        """创建几何体"""
        try:
            # 这里将实现几何体创建逻辑
            pass
        except Exception as e:
            print(f"Error creating geometry: {e}")
