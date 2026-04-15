import PyQt6
from PyQt6 import QtWidgets
import sys
import os

# 添加数学库路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from geometry import Vector

# 重命名常用组件以保持代码兼容性
QWidget = QtWidgets.QWidget
QVBoxLayout = QtWidgets.QVBoxLayout
QGroupBox = QtWidgets.QGroupBox
QLabel = QtWidgets.QLabel
QLineEdit = QtWidgets.QLineEdit
QPushButton = QtWidgets.QPushButton
QFormLayout = QtWidgets.QFormLayout

class PropertyPanel(QWidget):
    """属性面板，用于显示和编辑选中对象的属性"""
    
    def __init__(self, core_app):
        super().__init__()
        self.core_app = core_app
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        try:
            layout = QVBoxLayout()
            
            # 创建变换属性组
            transform_group = QGroupBox("Transform")
            transform_layout = QFormLayout()
            
            # 位置属性
            transform_layout.addRow(QLabel("Position:"))
            self.position_x = QLineEdit("0.0")
            self.position_y = QLineEdit("0.0")
            self.position_z = QLineEdit("0.0")
            transform_layout.addRow("X:", self.position_x)
            transform_layout.addRow("Y:", self.position_y)
            transform_layout.addRow("Z:", self.position_z)
            
            # 旋转属性
            transform_layout.addRow(QLabel("Rotation:"))
            self.rotation_x = QLineEdit("0.0")
            self.rotation_y = QLineEdit("0.0")
            self.rotation_z = QLineEdit("0.0")
            transform_layout.addRow("X:", self.rotation_x)
            transform_layout.addRow("Y:", self.rotation_y)
            transform_layout.addRow("Z:", self.rotation_z)
            
            # 缩放属性
            transform_layout.addRow(QLabel("Scale:"))
            self.scale_x = QLineEdit("1.0")
            self.scale_y = QLineEdit("1.0")
            self.scale_z = QLineEdit("1.0")
            transform_layout.addRow("X:", self.scale_x)
            transform_layout.addRow("Y:", self.scale_y)
            transform_layout.addRow("Z:", self.scale_z)
            
            transform_group.setLayout(transform_layout)
            layout.addWidget(transform_group)
            
            # 创建材质属性组
            material_group = QGroupBox("Material")
            material_layout = QFormLayout()
            
            self.material_color = QLineEdit("#FFFFFF")
            material_layout.addRow("Color:", self.material_color)
            
            self.material_shininess = QLineEdit("32.0")
            material_layout.addRow("Shininess:", self.material_shininess)
            
            material_group.setLayout(material_layout)
            layout.addWidget(material_group)
            
            # 添加应用按钮
            apply_button = QPushButton("Apply")
            apply_button.clicked.connect(self.apply_properties)
            layout.addWidget(apply_button)
            
            # 添加拉伸因子，使面板内容靠上
            layout.addStretch()
            
            self.setLayout(layout)
            
        except Exception as e:
            print(f"Error initializing property panel: {e}")
            import traceback
            traceback.print_exc()
    
    def apply_properties(self):
        """应用属性更改"""
        try:
            # 获取选中对象
            selected_obj = self.core_app.selected_object
            if not selected_obj:
                return
            
            # 应用位置属性
            try:
                x = float(self.position_x.text())
                y = float(self.position_y.text())
                z = float(self.position_z.text())
                selected_obj.transform.set_position(x, y, z)
            except ValueError:
                print("Invalid position values")
            
            # 应用旋转属性
            try:
                x = float(self.rotation_x.text())
                y = float(self.rotation_y.text())
                z = float(self.rotation_z.text())
                selected_obj.transform.set_rotation_euler(x, y, z)
            except ValueError:
                print("Invalid rotation values")
            
            # 应用缩放属性
            try:
                x = float(self.scale_x.text())
                y = float(self.scale_y.text())
                z = float(self.scale_z.text())
                selected_obj.transform.set_scale(x, y, z)
            except ValueError:
                print("Invalid scale values")
            
            # 应用材质属性
            if selected_obj.material:
                # 应用颜色
                color_str = self.material_color.text()
                # 简单的颜色解析，实际应用中可能需要更复杂的解析
                if color_str.startswith('#') and len(color_str) == 7:
                    try:
                        r = int(color_str[1:3], 16) / 255.0
                        g = int(color_str[3:5], 16) / 255.0
                        b = int(color_str[5:7], 16) / 255.0
                        selected_obj.material.color = Vector(r, g, b)
                    except ValueError:
                        print("Invalid color value")
                
                # 应用 shininess
                try:
                    shininess = float(self.material_shininess.text())
                    selected_obj.material.shininess = shininess
                except ValueError:
                    print("Invalid shininess value")
        except Exception as e:
            print(f"Error applying properties: {e}")
    
    def update_properties(self, obj):
        """更新属性面板以显示选中对象的属性"""
        try:
            if not obj:
                # 清空属性面板
                self.position_x.setText("0.0")
                self.position_y.setText("0.0")
                self.position_z.setText("0.0")
                self.rotation_x.setText("0.0")
                self.rotation_y.setText("0.0")
                self.rotation_z.setText("0.0")
                self.scale_x.setText("1.0")
                self.scale_y.setText("1.0")
                self.scale_z.setText("1.0")
                self.material_color.setText("#FFFFFF")
                self.material_shininess.setText("32.0")
                return
            
            # 更新位置属性
            self.position_x.setText(f"{obj.transform.position.vec.x:.2f}")
            self.position_y.setText(f"{obj.transform.position.vec.y:.2f}")
            self.position_z.setText(f"{obj.transform.position.vec.z:.2f}")
            
            # 更新旋转属性
            # 注意：这里简化处理，实际应用中需要从四元数转换到欧拉角
            self.rotation_x.setText("0.0")
            self.rotation_y.setText("0.0")
            self.rotation_z.setText("0.0")
            
            # 更新缩放属性
            self.scale_x.setText(f"{obj.transform.scale.vec.x:.2f}")
            self.scale_y.setText(f"{obj.transform.scale.vec.y:.2f}")
            self.scale_z.setText(f"{obj.transform.scale.vec.z:.2f}")
            
            # 更新材质属性
            if obj.material:
                # 更新颜色
                r = int(obj.material.color.vec.x * 255)
                g = int(obj.material.color.vec.y * 255)
                b = int(obj.material.color.vec.z * 255)
                color_str = f"#{r:02x}{g:02x}{b:02x}"
                self.material_color.setText(color_str)
                
                # 更新 shininess
                self.material_shininess.setText(f"{obj.material.shininess:.1f}")
        except Exception as e:
            print(f"Error updating properties: {e}")
