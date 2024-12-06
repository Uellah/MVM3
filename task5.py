import numpy as np

TaskNumber = 5

X = 3
Y = 3

def f(x, y):
    return -4 * ((x - 1.5)**2 + (y - 1.5)**2 - 0.8)**2 + 1.5

def g_l(x, y):
    return 0  # Граничное условие слева

def g_r(x, y):
    return 0  # Граничное условие справа

def g_down(x, y):
    return 0  # Граничное условие снизу

def g_up(x, y):
    return 0  # Граничное условие сверху

def v1(x, y):
    return 0

def v2(x, y):
    return 0
