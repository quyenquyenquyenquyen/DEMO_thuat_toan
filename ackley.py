import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. Định nghĩa hàm Ackley (Phiên bản 2 chiều để vẽ hình)
def ackley_function_2d(x, y):
    # Công thức chuẩn của Ackley
    term1 = -20 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2)))
    term2 = -np.exp(0.5 * (np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)))
    return term1 + term2 + 20 + np.e

# 2. Tạo dữ liệu lưới (Grid)
# Miền tìm kiếm [-5, 5] như trong báo cáo 
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = ackley_function_2d(X, Y)

# 3. Vẽ biểu đồ 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Vẽ bề mặt (Surface plot)
surf = ax.plot_surface(X, Y, Z, cmap='viridis', 
                       edgecolor='none', alpha=0.8)

# Đánh dấu điểm cực trị toàn cục (Global Minimum) tại (0,0)
ax.scatter(0, 0, 0, color='red', s=100, label='Global Minimum (0,0)')

# Trang trí biểu đồ
ax.set_title('Ackley Function Surface (Search Space: [-5, 5])', fontsize=15)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Cost (Z)')
fig.colorbar(surf, shrink=0.5, aspect=10)
ax.legend()

# Hiển thị
plt.show()