import sys
import os

# 添加数学库路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from geometry import Vector, Matrix

class Renderer:
    """渲染器类，负责将3D场景渲染到屏幕上"""
    
    def __init__(self, widget):
        self.widget = widget  # 渲染窗口组件
        self.width = 800
        self.height = 600
    
    def set_size(self, width, height):
        """设置渲染区域大小"""
        self.width = width
        self.height = height
    
    def clear(self, color=(0, 0, 0)):
        """清空渲染区域"""
        # 这里将使用Windows API实现
        pass
    
    def render_mesh(self, game_object, camera):
        """渲染网格"""
        if not game_object.mesh:
            return
        
        # 获取世界变换矩阵
        world_matrix = game_object.get_world_transform()
        
        # 遍历所有三角形
        for i in range(0, len(game_object.mesh.indices), 3):
            # 获取三角形的三个顶点索引
            v0_idx = game_object.mesh.indices[i]
            v1_idx = game_object.mesh.indices[i+1]
            v2_idx = game_object.mesh.indices[i+2]
            
            # 获取顶点坐标
            v0 = game_object.mesh.vertices[v0_idx]
            v1 = game_object.mesh.vertices[v1_idx]
            v2 = game_object.mesh.vertices[v2_idx]
            
            # 应用世界变换
            v0_world = world_matrix * v0
            v1_world = world_matrix * v1
            v2_world = world_matrix * v2
            
            # 应用视图投影变换
            v0_proj = camera.project(v0_world)
            v1_proj = camera.project(v1_world)
            v2_proj = camera.project(v2_world)
            
            # 将归一化设备坐标转换为屏幕坐标
            v0_screen = self._ndc_to_screen(v0_proj)
            v1_screen = self._ndc_to_screen(v1_proj)
            v2_screen = self._ndc_to_screen(v2_proj)
            
            # 绘制三角形
            self.draw_triangle(v0_screen, v1_screen, v2_screen, game_object.material)
    
    def _ndc_to_screen(self, ndc_point):
        """将归一化设备坐标转换为屏幕坐标"""
        x = (ndc_point.vec.x + 1) * 0.5 * self.width
        y = (1 - ndc_point.vec.y) * 0.5 * self.height
        return (x, y)
    
    def draw_triangle(self, v0, v1, v2, material):
        """绘制三角形"""
        # 这里将使用Windows API实现
        pass
    
    def draw_line(self, p0, p1, color=(255, 255, 255)):
        """绘制线段"""
        # 这里将使用Windows API实现
        pass
    
    def draw_axis(self, camera):
        """绘制坐标系"""
        # 绘制X轴（红色）
        x_axis_start = camera.project(Vector(0, 0, 0))
        x_axis_end = camera.project(Vector(1, 0, 0))
        self.draw_line(
            self._ndc_to_screen(x_axis_start),
            self._ndc_to_screen(x_axis_end),
            (255, 0, 0)
        )
        
        # 绘制Y轴（绿色）
        y_axis_start = camera.project(Vector(0, 0, 0))
        y_axis_end = camera.project(Vector(0, 1, 0))
        self.draw_line(
            self._ndc_to_screen(y_axis_start),
            self._ndc_to_screen(y_axis_end),
            (0, 255, 0)
        )
        
        # 绘制Z轴（蓝色）
        z_axis_start = camera.project(Vector(0, 0, 0))
        z_axis_end = camera.project(Vector(0, 0, 1))
        self.draw_line(
            self._ndc_to_screen(z_axis_start),
            self._ndc_to_screen(z_axis_end),
            (0, 0, 255)
        )

class WindowsRenderer(Renderer):
    """基于Windows API的渲染器"""
    
    def __init__(self, widget):
        super().__init__(widget)
        # 这里将初始化Windows API相关资源
    
    def clear(self, color=(0, 0, 0)):
        """清空渲染区域"""
        # 使用Windows API清空窗口
        pass
    
    def draw_triangle(self, v0, v1, v2, material):
        """绘制三角形"""
        # 使用Windows API绘制三角形
        pass
    
    def draw_line(self, p0, p1, color=(255, 255, 255)):
        """绘制线段"""
        # 使用Windows API绘制线段
        pass
