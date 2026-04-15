class Application:
    """应用核心类，管理整个应用的状态和功能"""
    
    def __init__(self):
        self.scene = None
        self.objects = []
        self.current_tool = None
        self.renderer = None
        
    def set_scene(self, scene):
        """设置场景"""
        try:
            self.scene = scene
        except Exception as e:
            print(f"Error setting scene: {e}")
    
    def add_object(self, obj):
        """添加对象到场景"""
        try:
            self.objects.append(obj)
        except Exception as e:
            print(f"Error adding object: {e}")
    
    def remove_object(self, obj):
        """从场景中移除对象"""
        try:
            if obj in self.objects:
                self.objects.remove(obj)
        except Exception as e:
            print(f"Error removing object: {e}")
    
    def set_tool(self, tool):
        """设置当前工具"""
        try:
            self.current_tool = tool
        except Exception as e:
            print(f"Error setting tool: {e}")
    
    def set_renderer(self, renderer):
        """设置渲染器"""
        try:
            self.renderer = renderer
        except Exception as e:
            print(f"Error setting renderer: {e}")
    
    def get_objects(self):
        """获取所有对象"""
        return self.objects
    
    def clear_scene(self):
        """清空场景"""
        try:
            self.objects.clear()
        except Exception as e:
            print(f"Error clearing scene: {e}")
