import numpy as np
from utils import OutToFile
import time
import matplotlib.pyplot as plt
import os
from task3 import *

class Solver:
    def __init__(self):
        self.Nx = Nx
        self.Ny = Ny
        self.h_x = X / (self.Nx - 1)
        self.h_y = Y / (self.Ny - 1)
        self.Pe = 1.

        self.p = np.zeros((self.Ny, self.Nx))

        self.reverse_sq = (1 / np.power(self.h_x, 2) + 1 / np.power(self.h_y, 2))*2.
        self.reverse_hx = 1/self.h_x
        self.reverse_hy = 1/self.h_y

    def init(self, v):
        for j in range(self.Nx):
            v[0, j] = self.get_grid_func(g_down, j, 0)
            v[self.Ny - 1, j] = self.get_grid_func(g_up, j, 0)

        for i in range(self.Ny):
            v[i, 0] = self.get_grid_func(g_l, 0, i)
            v[i, self.Nx - 1] = self.get_grid_func(g_r, 0, i)

    def get_grid_func(self, func, i, j):
        return func(i * self.h_x, j * self.h_y)

    def out(self):
        o = OutToFile('out_'+ str(TaskNumber))
        o.write_numpy_to_csv(self.p)

    def der_xx(self, i, j, p):
        return (p[i, j+1] - 2 * p[i, j] + p[i, j-1])/np.power(self.h_x, 2)

    def der_yy(self, i, j, p):
        return (p[i+1, j] - 2 * p[i, j] + p[i-1, j])/np.power(self.h_y, 2)

    def Dx(self, i, j, p):
        v1_ = self.get_grid_func(v1, j, i)
        if v1_ > 0:
            return  v1_ * (p[i, j] - p[i, j - 1]) / self.h_x
        return v1_ * (p[i, j + 1] - p[i, j]) / self.h_x

    def Dy(self, i, j, p):
        v2_ = self.get_grid_func(v2, j, i)
        if v2_ > 0:
            return v2_ * (p[i,j] - p[i - 1, j]) / self.h_x
        return v2_ *  (p[i + 1, j] - p[i, j]) / self.h_x

    # одна из возможных проблем перепутаны i, j в f!!!
    def A(self, i, j, p):
        return -1/self.Pe*(self.der_xx(i, j, p) + self.der_yy(i, j, p)) + self.Dx(i, j, p) + self.Dy(i, j, p)

    def Au(self, p):
        res = np.zeros((self.Ny, self.Nx))
        for i in range(1, self.Ny - 1):
            for j in range(1, self.Nx - 1):
                res[i, j] = self.A(i, j, p)
        return res

    def sc_mult(self, u, v):
        s = 0
        for i in range(1, self.Ny - 1):
            for j in range(1, self.Nx - 1):
                s += u[i, j] * v[i, j]
        return s

    def solve(self, tol=1e-2, max_time=10, max_iter=100):
        start_time = time.time()

        self.init(self.p)
        r0 = np.zeros((self.Ny, self.Nx))

        for i in range(1, self.Ny - 1):
            for j in range(1, self.Nx - 1):
                r0[i, j] = self.get_grid_func(f, j, i) - self.A(i, j, self.p)

        r = r0.copy()
        rho_old = alpha = omega = 1.0
        v = np.zeros_like(r0)
        p = np.zeros_like(r0)

        iter_count = 0

        while iter_count < max_iter and (time.time() - start_time) < max_time:
            rho_new = self.sc_mult(r0, r)
            if abs(rho_new) < tol:
                print("Прерывание: rho_new слишком мал.")
                break
            if iter_count == 0:
                p = r.copy()
            else:
                beta = (rho_new / rho_old) * (alpha / omega)
                p = r + beta * (p - omega * v)

            v = self.Au(p)
            alpha = rho_new / self.sc_mult(r0, v)

            s = r - alpha * v

            if np.linalg.norm(s) < tol:
                self.p += alpha * p
                break

            t = self.Au(s)
            omega = self.sc_mult(t, s) / self.sc_mult(t, t)

            self.p += alpha * p + omega * s
            r = s - omega * t

            if np.linalg.norm(r) < tol:
                break

            rho_old = rho_new
            iter_count += 1

        return self.p


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

    def do_all(self):
        # self.init()
        # print(self.sc_mult(self.p, self.p))
        self.solve()
        print(self.p)
        # self.plot_heatmap()