import numpy as np
from utils import out_to_file
from task import *



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
        print(self.p)

    def get_grid_func(self, func, i, j):
        return func(i * self.h_x, j * self.h_y)

    def out(self):
        o = out_to_file('out_p')
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

    def solve(self):
        for iter in range(0, 500):
            for j in range(self.Nx - 2, 0, -1):
                for i in range(1, self.Ny - 1):
                    self.p[i, j] = self.A(i, j)
        print(np.round(self.p,2))
