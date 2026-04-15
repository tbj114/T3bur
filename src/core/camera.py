from geometry import Vector, Matrix, Quat
import math

class Camera:
    """相机类，负责处理3D视图的投影和视图变换"""
    
    def __init__(self):
        self.position = Vector(0, 0, 10)  # 默认相机位置
        self.target = Vector(0, 0, 0)     # 默认目标点
        self.up = Vector(0, 1, 0)         # 默认上方向
        self.fov = 60.0                   # 视场角（度）
        self.near = 0.1                   # 近裁剪面
        self.far = 1000.0                 # 远裁剪面
        self.aspect = 1.0                 # 宽高比
        
        self._view_matrix = None
        self._projection_matrix = None
        self._view_projection_matrix = None
        self._view_dirty = True
        self._projection_dirty = True
    
    @property
    def view_matrix(self):
        """获取视图矩阵"""
        if self._view_dirty:
            self._update_view_matrix()
        return self._view_matrix
    
    @property
    def projection_matrix(self):
        """获取投影矩阵"""
        if self._projection_dirty:
            self._update_projection_matrix()
        return self._projection_matrix
    
    @property
    def view_projection_matrix(self):
        """获取视图投影矩阵"""
        if self._view_dirty or self._projection_dirty:
            self._view_projection_matrix = self.projection_matrix * self.view_matrix
        return self._view_projection_matrix
    
    def _update_view_matrix(self):
        """更新视图矩阵"""
        # 计算相机的前向、右向和上向向量
        forward = (self.target - self.position).normalize()
        right = forward.cross(self.up).normalize()
        up = right.cross(forward)
        
        # 创建视图矩阵（ LookAt 矩阵）
        # 视图矩阵 = 平移矩阵 * 旋转矩阵
        # 平移矩阵：将相机位置移到原点
        translation_mat = Matrix.translation(self.position * -1)
        
        # 旋转矩阵：将世界坐标系转换为相机坐标系
        rotation_mat = Matrix()
        rotation_mat.mat.data[0][0] = right.vec.x
        rotation_mat.mat.data[0][1] = right.vec.y
        rotation_mat.mat.data[0][2] = right.vec.z
        rotation_mat.mat.data[1][0] = up.vec.x
        rotation_mat.mat.data[1][1] = up.vec.y
        rotation_mat.mat.data[1][2] = up.vec.z
        rotation_mat.mat.data[2][0] = -forward.vec.x
        rotation_mat.mat.data[2][1] = -forward.vec.y
        rotation_mat.mat.data[2][2] = -forward.vec.z
        
        # 计算视图矩阵
        self._view_matrix = rotation_mat * translation_mat
        self._view_dirty = False
    
    def _update_projection_matrix(self):
        """更新投影矩阵"""
        # 创建透视投影矩阵
        fov_rad = math.radians(self.fov)
        tan_half_fov = math.tan(fov_rad * 0.5)
        
        projection_mat = Matrix()
        projection_mat.mat.data[0][0] = 1.0 / (self.aspect * tan_half_fov)
        projection_mat.mat.data[1][1] = 1.0 / tan_half_fov
        projection_mat.mat.data[2][2] = -(self.far + self.near) / (self.far - self.near)
        projection_mat.mat.data[2][3] = -1.0
        projection_mat.mat.data[3][2] = -(2.0 * self.far * self.near) / (self.far - self.near)
        projection_mat.mat.data[3][3] = 0.0
        
        self._projection_matrix = projection_mat
        self._projection_dirty = False
    
    def set_position(self, x, y, z):
        """设置相机位置"""
        self.position = Vector(x, y, z)
        self._view_dirty = True
    
    def set_target(self, x, y, z):
        """设置目标点"""
        self.target = Vector(x, y, z)
        self._view_dirty = True
    
    def set_up(self, x, y, z):
        """设置上方向"""
        self.up = Vector(x, y, z)
        self._view_dirty = True
    
    def set_fov(self, fov):
        """设置视场角"""
        self.fov = fov
        self._projection_dirty = True
    
    def set_near_far(self, near, far):
        """设置近远裁剪面"""
        self.near = near
        self.far = far
        self._projection_dirty = True
    
    def set_aspect(self, aspect):
        """设置宽高比"""
        self.aspect = aspect
        self._projection_dirty = True
    
    def look_at(self, target):
        """看向目标点"""
        self.target = target
        self._view_dirty = True
    
    def move_forward(self, distance):
        """向前移动"""
        forward = (self.target - self.position).normalize()
        self.position = self.position + forward * distance
        self.target = self.target + forward * distance
        self._view_dirty = True
    
    def move_backward(self, distance):
        """向后移动"""
        self.move_forward(-distance)
    
    def move_left(self, distance):
        """向左移动"""
        forward = (self.target - self.position).normalize()
        right = forward.cross(self.up).normalize()
        left = right * -1
        self.position = self.position + left * distance
        self.target = self.target + left * distance
        self._view_dirty = True
    
    def move_right(self, distance):
        """向右移动"""
        self.move_left(-distance)
    
    def move_up(self, distance):
        """向上移动"""
        self.position = self.position + self.up * distance
        self.target = self.target + self.up * distance
        self._view_dirty = True
    
    def move_down(self, distance):
        """向下移动"""
        self.move_up(-distance)
    
    def rotate_yaw(self, angle):
        """绕Y轴旋转（偏航）"""
        # 计算相机到目标的向量
        camera_to_target = self.target - self.position
        distance = camera_to_target.length()
        
        # 创建旋转四元数
        q = Quat.from_axis_angle(angle, self.up)
        
        # 旋转相机到目标的向量
        rotated_vector = q.rotate(camera_to_target)
        
        # 更新目标点
        self.target = self.position + rotated_vector
        self._view_dirty = True
    
    def rotate_pitch(self, angle):
        """绕X轴旋转（俯仰）"""
        # 计算相机到目标的向量
        camera_to_target = self.target - self.position
        distance = camera_to_target.length()
        
        # 计算右向量
        forward = camera_to_target.normalize()
        right = forward.cross(self.up).normalize()
        
        # 创建旋转四元数
        q = Quat.from_axis_angle(angle, right)
        
        # 旋转相机到目标的向量
        rotated_vector = q.rotate(camera_to_target)
        
        # 检查旋转后是否接近垂直，避免万向锁
        dot = rotated_vector.dot(self.up)
        if abs(dot) < 0.999:
            # 更新目标点
            self.target = self.position + rotated_vector
            # 更新上方向
            new_up = q.rotate(self.up)
            self.up = new_up.normalize()
            self._view_dirty = True
    
    def project(self, point):
        """将3D点投影到屏幕空间"""
        # 应用视图投影矩阵
        projected = self.view_projection_matrix * point
        
        # 透视除法
        if projected.vec.z != 0:
            projected = projected / projected.vec.z
        
        return projected
    
    def unproject(self, screen_point, viewport):
        """将屏幕空间点反投影到3D空间"""
        # 视口参数：[x, y, width, height]
        x, y, width, height = viewport
        
        # 将屏幕坐标转换为NDC（归一化设备坐标）
        ndc_x = (screen_point.vec.x - x) / width * 2 - 1
        ndc_y = 1 - (screen_point.vec.y - y) / height * 2
        ndc_z = screen_point.vec.z
        
        # 创建NDC点
        ndc_point = Vector(ndc_x, ndc_y, ndc_z)
        
        # 计算视图投影矩阵的逆矩阵
        view_proj_inv = self.view_projection_matrix.inverse()
        
        # 应用逆矩阵
        world_point = view_proj_inv * ndc_point
        
        # 透视除法
        if world_point.vec.w != 0:
            world_point = world_point / world_point.vec.w
        
        return world_point
