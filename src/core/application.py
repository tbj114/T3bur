from .camera import Camera
from .scene import Scene, GameObject, Mesh, Material
from .renderer import Renderer

class Application:
    """应用核心类，管理整个3D建模软件的状态和逻辑"""
    
    def __init__(self):
        self.renderer = None
        self.camera = Camera()
        self.scene = Scene()
        self.selected_object = None
        self.current_tool = "select"
        self._initialize_scene()
    
    def _initialize_scene(self):
        """初始化场景"""
        # 创建一个立方体
        cube = GameObject("Cube")
        cube.mesh = self._create_cube_mesh()
        cube.material = Material()
        self.scene.add_game_object(cube)
    
    def _create_cube_mesh(self):
        """创建立方体网格"""
        mesh = Mesh()
        
        # 添加顶点
        mesh.add_vertex(-1, -1, -1)
        mesh.add_vertex(1, -1, -1)
        mesh.add_vertex(1, 1, -1)
        mesh.add_vertex(-1, 1, -1)
        mesh.add_vertex(-1, -1, 1)
        mesh.add_vertex(1, -1, 1)
        mesh.add_vertex(1, 1, 1)
        mesh.add_vertex(-1, 1, 1)
        
        # 添加三角形
        # 前面
        mesh.add_triangle(0, 1, 2)
        mesh.add_triangle(0, 2, 3)
        # 后面
        mesh.add_triangle(4, 6, 5)
        mesh.add_triangle(4, 7, 6)
        # 左面
        mesh.add_triangle(0, 3, 7)
        mesh.add_triangle(0, 7, 4)
        # 右面
        mesh.add_triangle(1, 5, 6)
        mesh.add_triangle(1, 6, 2)
        # 上面
        mesh.add_triangle(3, 2, 6)
        mesh.add_triangle(3, 6, 7)
        # 下面
        mesh.add_triangle(0, 4, 5)
        mesh.add_triangle(0, 5, 1)
        
        return mesh
    
    def set_renderer(self, renderer):
        """设置渲染器"""
        try:
            self.renderer = renderer
        except Exception as e:
            print(f"Error setting renderer: {e}")
    
    def set_tool(self, tool):
        """设置当前工具"""
        try:
            self.current_tool = tool
        except Exception as e:
            print(f"Error setting tool: {e}")
    
    def update(self, delta_time):
        """更新应用状态"""
        try:
            if self.scene:
                self.scene.update(delta_time)
        except Exception as e:
            print(f"Error updating application: {e}")
    
    def render(self):
        """渲染场景"""
        try:
            if self.renderer and self.scene:
                self.renderer.clear()
                self.scene.render(self.renderer, self.camera)
                self.renderer.draw_axis(self.camera)
        except Exception as e:
            print(f"Error rendering scene: {e}")
    
    def create_cube(self):
        """创建立方体"""
        try:
            cube = GameObject("Cube")
            cube.mesh = self._create_cube_mesh()
            cube.material = Material()
            self.scene.add_game_object(cube)
        except Exception as e:
            print(f"Error creating cube: {e}")
    
    def create_sphere(self):
        """创建球体"""
        try:
            sphere = GameObject("Sphere")
            sphere.mesh = self._create_sphere_mesh()
            sphere.material = Material()
            self.scene.add_game_object(sphere)
        except Exception as e:
            print(f"Error creating sphere: {e}")
    
    def _create_sphere_mesh(self):
        """创建球体网格"""
        mesh = Mesh()
        # 简化实现，创建一个八面体作为球体的近似
        mesh.add_vertex(0, 1, 0)  # 顶部顶点
        mesh.add_vertex(1, 0, 0)  # 右顶点
        mesh.add_vertex(0, 0, 1)  # 前顶点
        mesh.add_vertex(-1, 0, 0)  # 左顶点
        mesh.add_vertex(0, 0, -1)  # 后顶点
        mesh.add_vertex(0, -1, 0)  # 底部顶点
        
        # 添加三角形
        mesh.add_triangle(0, 1, 2)
        mesh.add_triangle(0, 2, 3)
        mesh.add_triangle(0, 3, 4)
        mesh.add_triangle(0, 4, 1)
        mesh.add_triangle(5, 2, 1)
        mesh.add_triangle(5, 3, 2)
        mesh.add_triangle(5, 4, 3)
        mesh.add_triangle(5, 1, 4)
        
        return mesh
    
    def create_cylinder(self):
        """创建圆柱体"""
        try:
            cylinder = GameObject("Cylinder")
            cylinder.mesh = self._create_cylinder_mesh()
            cylinder.material = Material()
            self.scene.add_game_object(cylinder)
        except Exception as e:
            print(f"Error creating cylinder: {e}")
    
    def _create_cylinder_mesh(self):
        """创建圆柱体网格"""
        mesh = Mesh()
        # 简化实现，创建一个棱柱作为圆柱体的近似
        sides = 8  # 8边形
        import math
        
        # 添加顶部和底部的顶点
        top_center = len(mesh.vertices)
        mesh.add_vertex(0, 1, 0)
        bottom_center = len(mesh.vertices)
        mesh.add_vertex(0, -1, 0)
        
        # 添加侧面顶点
        for i in range(sides):
            angle = 2 * math.pi * i / sides
            x = math.cos(angle)
            z = math.sin(angle)
            mesh.add_vertex(x, 1, z)  # 顶部边缘
            mesh.add_vertex(x, -1, z)  # 底部边缘
        
        # 添加顶部三角形
        for i in range(sides):
            v0 = top_center
            v1 = top_center + 1 + i * 2
            v2 = top_center + 1 + ((i + 1) % sides) * 2
            mesh.add_triangle(v0, v1, v2)
        
        # 添加底部三角形
        for i in range(sides):
            v0 = bottom_center
            v1 = bottom_center + 1 + i * 2 + 1
            v2 = bottom_center + 1 + ((i + 1) % sides) * 2 + 1
            mesh.add_triangle(v0, v2, v1)
        
        # 添加侧面四边形（分解为两个三角形）
        for i in range(sides):
            v0 = top_center + 1 + i * 2
            v1 = top_center + 1 + ((i + 1) % sides) * 2
            v2 = top_center + 1 + ((i + 1) % sides) * 2 + 1
            v3 = top_center + 1 + i * 2 + 1
            mesh.add_triangle(v0, v1, v2)
            mesh.add_triangle(v0, v2, v3)
        
        return mesh
    
    def handle_key_event(self, event):
        """处理键盘事件"""
        try:
            # 这里可以添加键盘事件处理逻辑
            pass
        except Exception as e:
            print(f"Error handling key event: {e}")
    
    def handle_mouse_event(self, event):
        """处理鼠标事件"""
        try:
            # 这里可以添加鼠标事件处理逻辑
            pass
        except Exception as e:
            print(f"Error handling mouse event: {e}")
    
    def get_objects(self):
        """获取所有对象"""
        return self.scene.game_objects
    
    def clear_scene(self):
        """清空场景"""
        try:
            # 清空场景中的所有对象
            for obj in self.scene.game_objects[:]:
                self.scene.remove_game_object(obj)
        except Exception as e:
            print(f"Error clearing scene: {e}")
