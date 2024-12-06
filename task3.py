import numpy as np

TaskNumber = 3

X = 3
Y = 3


def u_an(x, y):
    return x + 1

def f(x, y):
    return 0

# лишние переменные обьявлены для универсальности реализации получения сеточной аппроксимации
def g_l(x, y):
    return 1

def g_r(x, y):
    return 4

def g_down(x, y):
    return x + 1

def g_up(x, y):
    return x + 1

def v1(x, y):
    return 0
def v2(x, y):
    return 0

