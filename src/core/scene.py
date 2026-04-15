from .transform import Transform
from geometry import Vector

class GameObject:
    """游戏对象类，包含变换和其他组件"""
    
    def __init__(self, name="GameObject"):
        self.name = name
        self.transform = Transform()
        self.mesh = None  # 网格数据
        self.material = None  # 材质数据
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        """添加子对象"""
        self.children.append(child)
        child.parent = self
    
    def remove_child(self, child):
        """移除子对象"""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
    
    def get_world_transform(self):
        """获取世界变换矩阵"""
        if self.parent:
            return self.parent.get_world_transform() * self.transform.model_matrix
        else:
            return self.transform.model_matrix
    
    def update(self, delta_time):
        """更新游戏对象"""
        # 更新自身
        self._update(delta_time)
        
        # 更新子对象
        for child in self.children:
            child.update(delta_time)
    
    def _update(self, delta_time):
        """具体的更新逻辑，由子类实现"""
        pass
    
    def render(self, renderer, camera):
        """渲染游戏对象"""
        # 渲染自身
        if self.mesh:
            renderer.render_mesh(self, camera)
        
        # 渲染子对象
        for child in self.children:
            child.render(renderer, camera)

class Mesh:
    """网格类，存储顶点数据"""
    
    def __init__(self):
        self.vertices = []  # 顶点列表
        self.indices = []   # 索引列表
    
    def add_vertex(self, x, y, z):
        """添加顶点"""
        self.vertices.append(Vector(x, y, z))
    
    def add_triangle(self, v0, v1, v2):
        """添加三角形"""
        self.indices.extend([v0, v1, v2])

class Material:
    """材质类，存储材质属性"""
    
    def __init__(self):
        self.color = Vector(1, 1, 1)  # 颜色
        self.shininess = 32.0         #  shininess

class Scene:
    """场景类，管理所有游戏对象"""
    
    def __init__(self):
        self.root = GameObject("Root")
        self.game_objects = []
    
    def add_game_object(self, game_object):
        """添加游戏对象"""
        self.root.add_child(game_object)
        self.game_objects.append(game_object)
    
    def remove_game_object(self, game_object):
        """移除游戏对象"""
        self.root.remove_child(game_object)
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)
    
    def update(self, delta_time):
        """更新场景"""
        self.root.update(delta_time)
    
    def render(self, renderer, camera):
        """渲染场景"""
        self.root.render(renderer, camera)
    
    def get_game_object_by_name(self, name):
        """通过名称查找游戏对象"""
        def search(obj):
            if obj.name == name:
                return obj
            for child in obj.children:
                result = search(child)
                if result:
                    return result
            return None
        return search(self.root)
