import numpy as np
from utils import OutToFile
import time
import matplotlib.pyplot as plt
import os
from task4 import *

class Solver:
    def __init__(self):
        self.Nx = Nx
        self.Ny = Ny
        self.h_x = X / (self.Nx - 1)
        self.h_y = Y / (self.Ny - 1)
        self.Pe = 1

        self.p = np.zeros((self.Ny, self.Nx))

        self.reverse_sq = (1 / np.power(self.h_x, 2) + 1 / np.power(self.h_y, 2))*2.
        self.reverse_hx = 1/self.h_x
        self.reverse_hy = 1/self.h_y

    def init(self):
        for j in range(self.Nx):
            self.p[0, j] = self.get_grid_func(g_down, j, 0)
            self.p[self.Ny - 1, j] = self.get_grid_func(g_up, j, 0)

        for i in range(self.Ny):
            self.p[i, 0] = self.get_grid_func(g_l, 0, i)
            self.p[i, self.Nx - 1] = self.get_grid_func(g_r, 0, i)

    def get_grid_func(self, func, i, j):
        return func(i * self.h_x, j * self.h_y)

    def out(self):
        o = OutToFile('out_'+ str(TaskNumber))
        o.write_numpy_to_csv(self.p)

    def der_xx(self, i, j):
        return (self.p[i, j+1] + self.p[i, j-1])/np.power(self.h_x, 2)

    def der_yy(self, i, j):
        return (self.p[i+1, j] + self.p[i-1, j])/np.power(self.h_y, 2)

    def Dx(self, i, j):
        v1_ = self.get_grid_func(v1, j, i)
        if v1_ > 0:
            return  v1_ * self.p[i, j - 1] / self.h_x, v1_ * self.reverse_hx
        return v1_ * (-self.p[i, j + 1]) / self.h_x, v1_ * (-self.reverse_hx)

    def Dy(self, i, j):
        v2_ = self.get_grid_func(v2, j, i)
        if v2_ > 0:
            return v2_ * self.p[i - 1, j] / self.h_y,  v2_ * self.reverse_hy
        return v2_ *  (-self.p[i + 1, j]) / self.h_y,  v2_ * (-self.reverse_hy)

    # одна из возможных проблем перепутаны i, j в f!!!
    def A(self, i, j):
        dx = self.Dx(i, j)
        dy = self.Dy(i, j)
        return (self.der_xx(i, j) + self.der_yy(i, j) + self.Pe * (self.get_grid_func(f, j, i) + dx[0] + dy[0])) / (self.reverse_sq + dx[1] +dy[1])

    def solve(self, tol=1e-2, max_time=10):
        start_time = time.time()
        iter = 0

        while True:
            s = 0
            for j in range(self.Nx - 2, 0, -1):
                for i in range(1, self.Ny - 1):
                    old = self.p[i, j]
                    self.p[i, j] = self.A(i, j)
                    s += np.power(self.p[i, j] - old, 2)

            if np.sqrt(s) < tol:
                print(f"Сошелся за {iter} итераций.")
                break

            if time.time() - start_time > max_time:
                print(f"Остановился по истечении {max_time} секунд. \n  Точность: {np.round(np.sqrt(s), 2)}")
                break

            iter += 1

    def plot_heatmap(self):
        """
        Plot a heatmap of the temperature distribution.
        """
        plt.figure(figsize=(8, 6))
        plt.imshow(self.p, extent=[0, X, 0, Y], origin='lower', cmap='inferno', aspect='auto')
        plt.colorbar(label='Температура')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Распределение температуры')
        output_path = os.path.join('out_im', 'heatmap_' + str(TaskNumber) +'.png')
        plt.savefig(output_path)
        plt.show()
