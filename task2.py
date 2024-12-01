import numpy as np

TaskNumber = 2

X = 1
Y = 1

Nx = 31
Ny = 31

def u_an(x, y):
    return x + y

def f(x, y):
    return x + y

# лишние переменные обьявлены для универсальности реализации получения сеточной аппроксимации
def g_l(x, y):
    return y

def g_r(x, y):
    return X + y

def g_down(x, y):
    return x

def g_up(x, y):
    return x + Y

def v1(x, y):
    return x

def v2(x, y):
    return y

