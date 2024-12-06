import numpy as np
import sympy as sp

# Определяем переменные
x, y = sp.symbols('x y')

# Параметр сглаживания
alpha = 1

# Сглаженная функция u_an(x, y)
u_an_ = ((x - 1.5)**2 + (y-1)**2 - 1)**3 - (x-1.5)**2*(y-1)**3

# Первая производная по x
u_an_x = sp.diff(u_an_, x)

# Первая производная по y
u_an_y = sp.diff(u_an_, y)

# Вторая производная по x
u_an_xx = sp.diff(u_an_x, x)

# Вторая производная по y
u_an_yy = sp.diff(u_an_y, y)

# Преобразуем функции в числовые
u_an_func = sp.lambdify((x, y), u_an_, "numpy")
u_an_xx_func = sp.lambdify((x, y), u_an_xx, "numpy")
u_an_yy_func = sp.lambdify((x, y), u_an_yy, "numpy")

TaskNumber = 6

X = 3.
Y = 2.5

# Функция f
def f(u, v):
    return -(u_an_xx_func(u, v) + u_an_yy_func(u, v))

# Граничные условия
def g_l(u, v):
    return u_an_func(0, v)

def g_r(u, v):
    return u_an_func(X, v)

def g_down(u, v):
    return u_an_func(u, 0)

def g_up(u, v):
    return u_an_func(u, Y)

# Скорости
def v1(u, v):
    return 0.

def v2(u, v):
    return 0.
