"""
# Лабораторная работа 5
Численные методы.<br>
**Приближение функций.**
"""
<<<<<<< HEAD

import matplotlib.pyplot as plt
=======
>>>>>>> ad6478ce48c4d06d1c28cade0a5f54c8826099f8
import numpy as np
class Task1:
    r"""
    Функция $y=f(x)$ задана таблицей значений в точках $x_0, x_1, \ldots, x_n$.

    Используя метод наименьших квадратов(МНК), найти 
    многочлен наилучшего среднеквадратичного приближения
    $$P_m(x) = a_0 + a_1 x + a_2 x^2 + \ldots + a_m x^m$$
    оптимальной степени $m=m^*$
    
    За оптимальное значение $m^*$ принять степень многочлена, начиная с которой величина 
    $$\sigma_m = \sqrt{\frac{1}{n-m} \sum_{k=0}^n (P_m(x_k) - y_k)}^2$$
    стабилизируется или начинает возрастать
    """
<<<<<<< HEAD
    # Задача 5.1
    Функция $y=f(x)$ задана таблицей значений в точках $x_0, x_1, \ldots, x_n$
=======
    global mnk
    def __init__(self):
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        mnk(4, np.array([1,2,3]), np.array([1,2,2]))
    def step1(self):
        """
        Задать векторы $x$ и $y$ исходных данных
        """
        x = []
        y = []
>>>>>>> ad6478ce48c4d06d1c28cade0a5f54c8826099f8

        self.x = np.array(x)
        self.y = np.array(y)
    def step2(self):
        r"""
        Составиьт программу, реализующую построение многочленов
        $$P_m(x) = a_0 + a_1 x + a_2 x^2 + \ldots + a_m x^m,\ m = 0, 1, 2, \ldots, m^*$$
        по методу наименьших квадратов

        Вычислить соответствующие им значения $\sigma_m$
        """
        global mnk
        def mnk(m: int, x: np.ndarray, y: np.ndarray):
            n = len(x) if len(x) >= len(y) else len(y)
            G = np.zeros((n, m), x.dtype)
            print(G)
    def step3(self):
        r"""
        Анализируя значения $\sigma_m$ выбрать оптимальную степень $m^*$ 
        многочлена наилучшего среднеквадратичного приближения
        """

<<<<<<< HEAD
    def __init__(self):
        self.steps = [self.step1]
        for step in self.steps:
            step()

    def step1(self):
        """
        1) Задаём векторы исходных данных:\\
        `x` - вектор значений аргумента функции\\
        `y` - вектор значений функции
        """
        self.x = np.array(
            [
                0,
                0.375,
                0.563,
                0.75,
                1.125,
                1.313,
                1.5,
                1.69,
                1.875,
                2.063,
                2.25,
                2.438,
                2.625,
                2.813,
                3,
            ]
        )
        self.y = np.array(
            [
                4.568,
                3.365,
                2.810,
                2.624,
                0.674,
                0.557,
                0.384,
                -0.566,
                -1.44,
                -1.696,
                -1.91,
                -2.819,
                -3.625,
                -3.941,
                -4.367,
            ]
        )

    def step2(self):
        """
        2.1) Составим программу реализующую построение многочленов\\
        $$P_m,\\  m = 0, 1, 2, \\ldots $$\\
        по методу наименьших квадратов

        2.2) Вычислим соответствующие им значения $sigma_m$
        """

        def get_P(m):
            x = self.x
            y = self.y


            coefs =
            def P_m(x):
                return np.sum([coefs * np.power(x, np.arange(m + 1))], axis=1)

        self.get_P = get_P


tasks = [Task1]
import numpy as np

t = np.zeros((3, 3))
np.triu_indices(5, 1)
=======
        pass
    def step4(self):
        r"""
        На одном чертеже построить графики многочленов $P_m,\ m = 0, 1, 2, \dots, m^*$
        и точечный график исходной функции
        """
        pass

>>>>>>> ad6478ce48c4d06d1c28cade0a5f54c8826099f8
