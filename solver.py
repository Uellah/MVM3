import numpy as np
from utils import out_to_file
from task import *
X = 2.
Y = 2.

class Solver:
    def __init__(self, Nx, Ny):
        self.Nx = Nx
        self.Ny = Ny
        self.p = np.zeros((self.Ny, self.Nx))
        self.h_x = X / (self.Nx - 1)
        self.h_y = Y / (self.Ny - 1)
        self.reverse_sq = (1 / np.power(self.h_x, 2) + 1 / np.power(self.h_y, 2))*2.

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

    def A(self, i, j):
        return (self.der_xx(i, j) + self.der_yy(i, j) + self.get_grid_func(f, i, j)) / self.reverse_sq

    def solve(self):
        for iter in range(0, 500):
            for j in range(self.Nx - 2, 0, -1):
                for i in range(1, self.Ny - 1):
                    self.p[i, j] = self.A(i, j)
        print(np.round(self.p,2))
