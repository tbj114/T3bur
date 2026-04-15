from geometry import Vector, Matrix, Quat

class Transform:
    """变换类，管理物体的位置、旋转和缩放"""
    
    def __init__(self):
        self.position = Vector(0, 0, 0)
        self.rotation = Quat(1, 0, 0, 0)  # 单位四元数
        self.scale = Vector(1, 1, 1)
        self._model_matrix = None
        self._model_matrix_dirty = True
    
    @property
    def model_matrix(self):
        """获取模型矩阵"""
        if self._model_matrix_dirty:
            self._update_model_matrix()
        return self._model_matrix
    
    def _update_model_matrix(self):
        """更新模型矩阵"""
        # 创建缩放矩阵
        scale_mat = Matrix.scale(self.scale)
        
        # 创建旋转矩阵
        rotation_mat = self.rotation.to_matrix()
        
        # 创建平移矩阵
        translation_mat = Matrix.translation(self.position)
        
        # 计算模型矩阵：平移 * 旋转 * 缩放
        self._model_matrix = translation_mat * rotation_mat * scale_mat
        self._model_matrix_dirty = False
    
    def set_position(self, x, y, z):
        """设置位置"""
        self.position = Vector(x, y, z)
        self._model_matrix_dirty = True
    
    def set_rotation(self, quat):
        """设置旋转（四元数）"""
        self.rotation = quat
        self._model_matrix_dirty = True
    
    def set_rotation_euler(self, x, y, z):
        """设置旋转（欧拉角）"""
        # 从欧拉角创建旋转矩阵
        rotation_mat = Matrix.rotation(Vector(x, y, z))
        # 这里需要从旋转矩阵转换到四元数
        # 简化实现，直接使用欧拉角创建四元数
        # 注意：这不是标准的欧拉角到四元数的转换，实际应用中需要使用更精确的方法
        import math
        # 绕X轴旋转
        qx = Quat.from_axis_angle(x, Vector(1, 0, 0))
        # 绕Y轴旋转
        qy = Quat.from_axis_angle(y, Vector(0, 1, 0))
        # 绕Z轴旋转
        qz = Quat.from_axis_angle(z, Vector(0, 0, 1))
        # 组合旋转
        self.rotation = qz * qy * qx
        self._model_matrix_dirty = True
    
    def set_scale(self, x, y, z):
        """设置缩放"""
        self.scale = Vector(x, y, z)
        self._model_matrix_dirty = True
    
    def translate(self, x, y, z):
        """平移"""
        self.position = self.position + Vector(x, y, z)
        self._model_matrix_dirty = True
    
    def rotate(self, angle, axis):
        """绕轴旋转"""
        # 创建旋转四元数
        q = Quat.from_axis_angle(angle, axis)
        # 与当前旋转相乘
        self.rotation = q * self.rotation
        self._model_matrix_dirty = True
    
    def rotate_euler(self, x, y, z):
        """欧拉角旋转"""
        self.set_rotation_euler(
            self.rotation.x + x,
            self.rotation.y + y,
            self.rotation.z + z
        )
    
    def scale_by(self, x, y, z):
        """缩放"""
        self.scale = self.scale * Vector(x, y, z)
        self._model_matrix_dirty = True
    
    def get_local_to_world_matrix(self):
        """获取局部到世界的变换矩阵"""
        return self.model_matrix
    
    def get_world_to_local_matrix(self):
        """获取世界到局部的变换矩阵"""
        return self.model_matrix.inverse()
