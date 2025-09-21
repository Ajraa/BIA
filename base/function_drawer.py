import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import functions

def plot_3d(func, x_range=(-5, 5), y_range=(-5, 5), points=200, title="3D Function"):
    x = np.linspace(x_range[0], x_range[1], points)
    y = np.linspace(y_range[0], y_range[1], points)
    X, Y = np.meshgrid(x, y)
    Z = np.array([[func([xi, yi]) for xi in x] for yi in y])

    # 3D povrchový graf
    fig = plt.figure(figsize=(12, 5))

    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.set_zlabel('f(X,Y)')
    ax1.set_title(title)

    # Konturový graf
    ax2 = fig.add_subplot(1, 2, 2)
    contour = ax2.contourf(X, Y, Z, levels=50, cmap='viridis')
    fig.colorbar(contour, ax=ax2)
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    ax2.set_title(f"{title} - Contour")

    plt.show()