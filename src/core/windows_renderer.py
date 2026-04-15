import sys
import os

# 添加数学库路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from geometry import Vector, Matrix

class WindowsRenderer:
    """基于Windows API的渲染器"""
    
    def __init__(self, hwnd):
        self.hwnd = hwnd  # 窗口句柄
        self.width = 800
        self.height = 600
        self.hdc = None  # 设备上下文
    
    def set_size(self, width, height):
        """设置渲染区域大小"""
        self.width = width
        self.height = height
    
    def begin_render(self):
        """开始渲染"""
        import ctypes
        from ctypes.wintypes import HDC, HGDIOBJ, RECT
        
        # 获取设备上下文
        self.hdc = ctypes.windll.user32.GetDC(self.hwnd)
        if not self.hdc:
            return False
        
        # 清空背景
        rect = RECT(0, 0, self.width, self.height)
        ctypes.windll.gdi32.FillRect(self.hdc, ctypes.byref(rect), ctypes.windll.gdi32.CreateSolidBrush(0x222222))  # 深色背景
        
        return True
    
    def end_render(self):
        """结束渲染"""
        if self.hdc:
            import ctypes
            ctypes.windll.user32.ReleaseDC(self.hwnd, self.hdc)
            self.hdc = None
    
    def clear(self, color=(0, 0, 0)):
        """清空渲染区域"""
        # 已在begin_render中处理
        pass
    
    def render_mesh(self, game_object, camera):
        """渲染网格"""
        if not game_object.mesh or not self.hdc:
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
        return (int(x), int(y))
    
    def draw_triangle(self, v0, v1, v2, material):
        """绘制三角形"""
        if not self.hdc:
            return
        
        import ctypes
        from ctypes.wintypes import POINT
        
        # 设置画笔颜色
        color = 0xFFFFFF  # 默认白色
        if material:
            r = int(material.color.vec.x * 255)
            g = int(material.color.vec.y * 255)
            b = int(material.color.vec.z * 255)
            color = (r) | (g << 8) | (b << 16)
        
        # 创建画笔
        pen = ctypes.windll.gdi32.CreatePen(0, 1, color)
        if not pen:
            return
        
        # 选择画笔
        old_pen = ctypes.windll.gdi32.SelectObject(self.hdc, pen)
        
        # 创建点数组
        points = (POINT * 4)()
        points[0].x, points[0].y = v0
        points[1].x, points[1].y = v1
        points[2].x, points[2].y = v2
        points[3].x, points[3].y = v0  # 闭合多边形
        
        # 绘制线条
        ctypes.windll.gdi32.Polyline(self.hdc, ctypes.byref(points), 4)
        
        # 恢复旧画笔
        ctypes.windll.gdi32.SelectObject(self.hdc, old_pen)
        ctypes.windll.gdi32.DeleteObject(pen)
    
    def draw_line(self, p0, p1, color=(255, 255, 255)):
        """绘制线段"""
        if not self.hdc:
            return
        
        import ctypes
        
        # 转换颜色
        r, g, b = color
        win_color = (r) | (g << 8) | (b << 16)
        
        # 创建画笔
        pen = ctypes.windll.gdi32.CreatePen(0, 1, win_color)
        if not pen:
            return
        
        # 选择画笔
        old_pen = ctypes.windll.gdi32.SelectObject(self.hdc, pen)
        
        # 绘制线条
        ctypes.windll.gdi32.MoveToEx(self.hdc, int(p0[0]), int(p0[1]), None)
        ctypes.windll.gdi32.LineTo(self.hdc, int(p1[0]), int(p1[1]))
        
        # 恢复旧画笔
        ctypes.windll.gdi32.SelectObject(self.hdc, old_pen)
        ctypes.windll.gdi32.DeleteObject(pen)
    
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
