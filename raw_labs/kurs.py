"""
Курсовая работа по численным методам
"""

from dataclasses import dataclass
from typing import Callable, Tuple

import numpy as np


@dataclass
class InputData:
    f: Callable[[float, float], float]
    g1: Callable[[float], float]
    g2: Callable[[float], float]
    phi: Callable[[float | np.ndarray], float]


@dataclass
class TestCase:
    name: str
    input_data: InputData
    exact_solution: Callable[[float, float], float]
    description: str


@dataclass
class Parametrs:
    N: int = 100
    M: int = 1000

    def __post_init__(self):
        self.h = 1 / self.N
        self.tau = 1 / self.M
        # if self.tau / self.h**2 > 0.5:
        #     raise ValueError("Нарушено условие устойчивости явной схемы")
        self.xi = np.linspace(0, 1, self.N + 1)
        self.tn = np.linspace(0, 1, self.M + 1)


class HeatConductionSolver:
    def __init__(self, input_data: InputData, parametrs: Parametrs):
        self.input_data = input_data
        self.parametrs = parametrs
        self.N = parametrs.N
        self.M = parametrs.M
        self.h = parametrs.h
        self.tau = parametrs.tau
        self.xi = parametrs.xi
        self.tn = parametrs.tn
        self.sigma = self.tau / self.h**2

    def explicit_solve(self) -> np.ndarray:
        """Явная схема"""
        u = np.zeros((self.N + 1, self.M + 1))
        u[:, 0] = self.input_data.phi(self.xi)

        # Предварительные вычисления
        tau_h2 = self.tau / self.h**2
        h_inv = 1 / self.h

        for j in range(self.M):
            u[1:-1, j + 1] = (
                u[1:-1, j]
                + tau_h2 * (u[:-2, j] - 2 * u[1:-1, j] + u[2:, j])
                + self.tau * self._f_vector(1, j)
            )

            # Граничные точки
            u[0, j + 1] = self._left_boundary(u[:, j + 1], u[0, j], self.tn[j + 1])
            u[-1, j + 1] = self._right_boundary(u[:, j + 1], u[-1, j], self.tn[j + 1])

        return u

    def implicit_solve(self, eps_iter: float = 1e-6, max_iter: int = 100) -> np.ndarray:
        """Неявная схема с МПИ"""
        u = np.zeros((self.N + 1, self.M + 1))
        u[:, 0] = self.input_data.phi(self.xi)

        for j in range(self.M):
            # Предикция по явной схеме
            u_pred = self._explicit_predictor(u[:, j], j)
            u_new = u_pred.copy()

            # МПИ
            for k in range(max_iter):
                u_old = u_new.copy()

                # Решение системы для внутренних точек
                u_new[1:-1] = self._solve_internal_points(u_new, u[:, j], j)

                # Граничные условия
                u_new[0] = self._left_boundary(u_new, u[0, j], self.tn[j + 1])
                u_new[-1] = self._right_boundary(u_new, u[-1, j], self.tn[j + 1])

                if np.max(np.abs(u_new - u_old)) < eps_iter:
                    break

            u[:, j + 1] = u_new

        return u

    def _explicit_predictor(self, u_prev: np.ndarray, j: int) -> np.ndarray:
        """Векторизованный предиктор для неявной схемы"""
        u_pred = u_prev.copy()
        u_pred[1:-1] = (
            u_prev[1:-1]
            + self.sigma * (u_prev[:-2] - 2 * u_prev[1:-1] + u_prev[2:])
            + self.tau * self._f_vector(1, j)
        )
        return u_pred

    def _solve_internal_points(
        self, u_current: np.ndarray, u_prev: np.ndarray, j: int
    ) -> np.ndarray:
        """Векторизованное решение для внутренних точек методом прогонки"""
        n = self.N - 1
        a = np.full(n, -self.sigma)
        b = np.full(n, 1 + 2 * self.sigma)
        c = np.full(n, -self.sigma)
        d = u_prev[1:-1] + self.tau * self._f_vector(1, j + 1)

        # Учет граничных условий
        d[0] += self.sigma * u_current[0]
        d[-1] += self.sigma * u_current[-1]

        return self._vectorized_tridiagonal_solve(a, b, c, d)

    def _vectorized_tridiagonal_solve(
        self, a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray
    ) -> np.ndarray:
        """Метод прогонки"""
        n = len(d)
        alpha = np.zeros(n)
        beta = np.zeros(n)

        # Прямой ход
        alpha[0] = -c[0] / b[0]
        beta[0] = d[0] / b[0]

        for i in range(1, n):
            denom = b[i] + a[i] * alpha[i - 1]
            alpha[i] = -c[i] / denom
            beta[i] = (d[i] - a[i] * beta[i - 1]) / denom

        # Обратный ход
        x = np.zeros(n)
        x[-1] = beta[-1]

        for i in range(n - 2, -1, -1):
            x[i] = alpha[i] * x[i + 1] + beta[i]

        return x

    def _f_vector(self, start: int, j: int) -> np.ndarray:
        """Векторизованное вычисление f(x,t)"""
        return np.array(
            [self.input_data.f(x, self.tn[j]) for x in self.xi[start:-start]]
        )

    def _left_boundary(self, u_current: np.ndarray, u_prev: float, t: float) -> float:
        """Левое граничное условие"""
        h_inv = 1 / self.h
        return (u_current[1] * h_inv + self.input_data.g1(t) + 3 * u_prev**4) / (
            h_inv + 4 * u_prev**3
        )

    def _right_boundary(self, u_current: np.ndarray, u_prev: float, t: float) -> float:
        """Правое граничное условие"""
        h_inv = 1 / self.h
        return (u_current[-2] * h_inv + self.input_data.g2(t) + 3 * u_prev**4) / (
            h_inv + 4 * u_prev**3
        )
