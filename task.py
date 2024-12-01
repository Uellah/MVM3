import numpy as np
X = 1
Y = 1

Ny = 50
Nx = 25

def f(x, y):
    return x + y
# лишние переменные обьявлены для универсальности реализации получения сеточной аппроксимации
def g_l(x, y):
    return 1.

def g_r(x, y):
    return 3.

def g_down(x, y):
    return x+1

def g_up(x, y):
    return x+1

v1 = np.ones((Ny, Nx))
v2 = np.ones((Ny, Nx))
