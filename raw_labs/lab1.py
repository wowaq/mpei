"""
Приближение функций
"""

from socketserver import DatagramRequestHandler

import matplotlib.pyplot as plt
import numpy as np


class Task1:
    """
    Функция $y=f(x)$ задана таблицей значений в точках $x_0, x_1, \ldots, x_n$

    Используя метод наименьших квадратов(МНК), найти многочлен
    $$P_m(x) = a_0 + a_1x + \ldots + a_mx^m$$
    наилучшего среднеквадратичного приближения оптимальной степени $m=m^*$

    За оптимальное значение принять степень многочлена, начиная с которой величина
    $$\sigma_m = \sqrt \frac{1}{n-m} \sum_{k=0}{(P_m(x_k) - y_k)^2$$
    """

    pass


tasks = [Task1]
