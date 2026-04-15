import PyQt6
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt
import sys
import os
import platform

# 重命名常用组件以保持代码兼容性
QWidget = QtWidgets.QWidget
QVBoxLayout = QtWidgets.QVBoxLayout
QLabel = QtWidgets.QLabel

# 添加核心模块路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.core.renderer import Renderer

# 尝试导入 Windows 渲染器
try:
    from src.core.windows_renderer import WindowsRenderer
except ImportError as e:
    print(f"Error importing WindowsRenderer: {e}")
    WindowsRenderer = None

class QtRenderer(Renderer):
    """基于Qt的渲染器"""
    
    def __init__(self, widget):
        super().__init__(widget)
        self.painter = None
    
    def clear(self, color=(0, 0, 0)):
        """清空渲染区域"""
        # 使用Qt的painter清空窗口
        pass
    
    def draw_triangle(self, v0, v1, v2, material):
        """绘制三角形"""
        if not self.painter:
            return
        
        # 设置画笔颜色
        color = (255, 255, 255)  # 默认白色
        if material:
            color = (int(material.color.vec.x * 255), 
                     int(material.color.vec.y * 255), 
                     int(material.color.vec.z * 255))
        
        pen = QtGui.QPen(QtGui.QColor(*color))
        self.painter.setPen(pen)
        
        # 绘制三角形的三条边
        self.painter.drawLine(int(v0[0]), int(v0[1]), int(v1[0]), int(v1[1]))
        self.painter.drawLine(int(v1[0]), int(v1[1]), int(v2[0]), int(v2[1]))
        self.painter.drawLine(int(v2[0]), int(v2[1]), int(v0[0]), int(v0[1]))
    
    def draw_line(self, p0, p1, color=(255, 255, 255)):
        """绘制线段"""
        if not self.painter:
            return
        
        pen = QtGui.QPen(QtGui.QColor(*color))
        self.painter.setPen(pen)
        self.painter.drawLine(int(p0[0]), int(p0[1]), int(p1[0]), int(p1[1]))
    
    def set_painter(self, painter):
        """设置painter"""
        self.painter = painter

class RenderWidget(QWidget):
    """渲染组件，负责显示3D场景"""
    
    def __init__(self, core_app):
        super().__init__()
        self.core_app = core_app
        
        # 根据平台选择渲染器
        if platform.system() == 'Windows' and WindowsRenderer:
            # 在Windows平台上使用Windows API渲染器
            try:
                # 获取窗口句柄
                hwnd = self.winId()
                self.renderer = WindowsRenderer(hwnd)
                print("Using WindowsRenderer")
            except Exception as e:
                print(f"Error creating WindowsRenderer: {e}")
                # 回退到Qt渲染器
                self.renderer = QtRenderer(self)
                print("Falling back to QtRenderer")
        else:
            # 在其他平台上使用Qt渲染器
            self.renderer = QtRenderer(self)
            print("Using QtRenderer")
        
        self.core_app.set_renderer(self.renderer)
        self.init_ui()
        self.last_time = QtCore.QTime.currentTime()
    
    def init_ui(self):
        """初始化UI"""
        try:
            layout = QVBoxLayout()
            
            # 创建渲染区域
            self.render_area = QWidget()
            self.render_area.setStyleSheet("background-color: #222222;")
            
            layout.addWidget(self.render_area)
            self.setLayout(layout)
            
            # 设置大小
            self.setMinimumSize(800, 600)
            
            # 启动定时器，用于更新场景
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_scene)
            self.timer.start(33)  # 约30 FPS
            
        except Exception as e:
            print(f"Error initializing render widget: {e}")
            import traceback
            traceback.print_exc()
    
    def paintEvent(self, event):
        """绘制事件"""
        try:
            painter = QtGui.QPainter(self.render_area)
            painter.fillRect(self.render_area.rect(), QtGui.QColor(34, 34, 34))  # 深色背景
            
            # 设置painter到渲染器
            self.renderer.set_painter(painter)
            
            # 渲染场景
            self.core_app.render()
            
            painter.end()
        except Exception as e:
            print(f"Error in paintEvent: {e}")
            import traceback
            traceback.print_exc()
    
    def resizeEvent(self, event):
        """调整大小事件"""
        try:
            size = self.render_area.size()
            self.renderer.set_size(size.width(), size.height())
            # 更新相机的宽高比
            if size.width() > 0 and size.height() > 0:
                self.core_app.camera.set_aspect(size.width() / size.height())
        except Exception as e:
            print(f"Error in resizeEvent: {e}")
    
    def update_scene(self):
        """更新场景"""
        try:
            # 计算时间差
            current_time = QtCore.QTime.currentTime()
            delta_time = self.last_time.msecsTo(current_time) / 1000.0
            self.last_time = current_time
            
            # 更新应用状态
            self.core_app.update(delta_time)
            
            # 重绘
            self.update()
        except Exception as e:
            print(f"Error updating scene: {e}")
            import traceback
            traceback.print_exc()
    
    def keyPressEvent(self, event):
        """键盘按下事件"""
        try:
            self.core_app.handle_key_event(event)
        except Exception as e:
            print(f"Error in keyPressEvent: {e}")
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        try:
            # 处理鼠标按下事件
            if event.button() == PyQt6.QtCore.Qt.MouseButton.LeftButton:
                # 转换鼠标坐标到渲染区域的坐标系
                pos = event.pos()
                render_pos = self.render_area.mapFromParent(pos)
                
                # 执行射线检测，选择对象
                self._pick_object(render_pos.x(), render_pos.y())
            
            self.core_app.handle_mouse_event(event)
        except Exception as e:
            print(f"Error in mousePressEvent: {e}")
    
    def _pick_object(self, x, y):
        """选择对象"""
        try:
            # 获取渲染区域的大小
            width = self.render_area.width()
            height = self.render_area.height()
            
            # 计算归一化设备坐标
            ndc_x = (x / width) * 2 - 1
            ndc_y = 1 - (y / height) * 2
            
            # 创建射线
            ray_origin = self.core_app.camera.position
            
            # 计算射线方向
            # 这里简化处理，使用相机的前向向量
            ray_direction = (self.core_app.camera.target - self.core_app.camera.position).normalize()
            
            # 遍历场景中的对象，进行射线检测
            closest_object = None
            closest_distance = float('inf')
            
            for obj in self.core_app.scene.game_objects:
                if obj.mesh:
                    # 简化的射线检测，实际应用中需要更复杂的算法
                    # 这里我们假设对象是一个包围球
                    distance = (obj.transform.position - ray_origin).length() - 1.0  # 假设半径为1
                    if distance < closest_distance:
                        closest_object = obj
                        closest_distance = distance
            
            # 设置选中对象
            if closest_object:
                # 通知主窗口更新选中对象
                if hasattr(self.parent(), 'set_selected_object'):
                    self.parent().set_selected_object(closest_object)
        except Exception as e:
            print(f"Error picking object: {e}")
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        try:
            self.core_app.handle_mouse_event(event)
        except Exception as e:
            print(f"Error in mouseMoveEvent: {e}")

