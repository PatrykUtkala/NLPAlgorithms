from scipy import signal
import numpy as np
from matplotlib import pyplot as plt

ddelt = np.zeros(100)
ddelt[0] = 1
h = np.ones(100)
h3 = np.copy(h)
h3[0: 3] = 0
h4 = np.copy(h)
h4[0: 4] = 0
h1 = np.copy(h)
h1[0] = 0


# def diff(num):
#     num = np.pad(num, (0, 1), 'constant', constant_values=(0, 0))
#     num1 = np.roll(num, 1)
#     print(num, num1, num - num1)
#     return num - num1


def func(arg):
    a1 = (2 * (-1) ** arg) * (h - h3) + 3 * np.roll(ddelt, 1)
    b1 = -3 * h1 - 3 * ddelt + 2 * np.roll(ddelt, 3) + 3 * h4
    print(a1)
    print(b1)
    print(np.convolve(b1,a1))
    pass


# a = np.array([1, 2, -3, -8, -4])
# b = np.convolve(-a, a)
# c = np.roots(a)
# r, p, k = signal.residue(a, a + 1)
a = np.arange(100)
func(a)
