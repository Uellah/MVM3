import numpy as np

TaskNumber = 1

X = 0.5
Y = 0.5

Nx = 31
Ny = 31

def u_an(x, y):
    return 1.

def f(x, y):
    return 0

# лишние переменные обьявлены для универсальности реализации получения сеточной аппроксимации
def g_l(x, y):
    return 1.

def g_r(x, y):
    return 1.

def g_down(x, y):
    return 1.

def g_up(x, y):
    return 1.

def v1(x, y):
    return x
def v2(x, y):
    return y

