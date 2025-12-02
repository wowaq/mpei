def kurs():
    import matplotlib.pyplot as plt
    import numpy as np
    import streamlit as st
    import sympy as sp
    from mpl_toolkits.mplot3d import Axes3D

    from raw_labs.kurs import HeatConductionSolver, InputData, Parametrs, TestCase

    st.set_page_config(page_title="Моделирование теплопроводности", layout="wide")

    st.title("Численное моделирование нелинейного уравнения теплопроводности")
    st.markdown("""
    Реализация явной и неявной разностных схем для решения уравнения теплопроводности
    с нелинейными краевыми условиями теплового излучения.
    """)

    x, t = sp.symbols("x t")

    PREDEFINED_TESTS = {
        "Линейное решение": {
            "u_exact": x + t,
            "phi": x,
            "description": "u(x,t) = x + t - простое линейное решение",
        },
        "Квадратичное решение": {
            "u_exact": x**2 + t,
            "phi": x**2,
            "description": "u(x,t) = x² + t - квадратичная зависимость по пространству",
        },
        "Экспоненциальное решение": {
            "u_exact": sp.exp(-x) + t,
            "phi": sp.exp(-x),
            "description": "u(x,t) = exp(-x) + t - экспоненциальное затухание",
        },
        "Синусоидальное решение": {
            "u_exact": sp.sin(sp.pi * x) * sp.exp(-t),
            "phi": sp.sin(sp.pi * x),
            "description": "u(x,t) = sin(πx)exp(-t) - затухающая синусоида",
        },
    }

    def compute_functions_from_exact(u_exact_sym, phi_sym):
        """Вычисление f, g1, g2 из точного решения с использованием sympy"""
        u_t = sp.diff(u_exact_sym, t)
        u_x = sp.diff(u_exact_sym, x)
        u_xx = sp.diff(u_exact_sym, x, x)
        f_sym = u_t - u_xx

        u_0_sym = u_exact_sym.subs(x, 0)
        u_1_sym = u_exact_sym.subs(x, 1)
        u_x_0_sym = u_x.subs(x, 0)
        u_x_1_sym = u_x.subs(x, 1)
        g1_sym = -u_x_0_sym + u_0_sym**4
        g2_sym = u_x_1_sym + u_1_sym**4

        f_func = sp.lambdify((x, t), f_sym, "numpy")
        g1_func = sp.lambdify(t, g1_sym, "numpy")
        g2_func = sp.lambdify(t, g2_sym, "numpy")
        phi_func = sp.lambdify(x, phi_sym, "numpy")
        u_exact_func = sp.lambdify((x, t), u_exact_sym, "numpy")

        return f_sym, g1_sym, g2_sym, f_func, g1_func, g2_func, phi_func, u_exact_func

    def create_3d_plot(params, results, scheme_type):
        """Создание 3D графика"""
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection="3d")

        X, T = np.meshgrid(params.xi, params.tn)

        if scheme_type == "explicit" and "explicit" in results:
            Z = results["explicit"].T
            title = "Явная схема"
        elif scheme_type == "implicit" and "implicit" in results:
            Z = results["implicit"].T
            title = "Неявная схема"
        else:
            Z = results["exact"].T
            title = "Точное решение"

        surf = ax.plot_surface(
            X, T, Z, cmap="hot", alpha=0.8, linewidth=0, antialiased=True
        )

        ax.set_xlabel("Пространство, x")
        ax.set_ylabel("Время, t")
        ax.set_zlabel("Температура, u(x,t)")
        ax.set_title(f"3D визуализация: {title}")

        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, label="Температура")

        return fig

    st.sidebar.header("Настройки расчета")

    predefined_names = list(PREDEFINED_TESTS.keys())
    selected_predefined = st.sidebar.selectbox(
        "Выберите тестовый случай:", predefined_names
    )

    test_info = PREDEFINED_TESTS[selected_predefined]
    u_exact_sym = test_info["u_exact"]
    phi_sym = test_info["phi"]

    f_sym, g1_sym, g2_sym, f_func, g1_func, g2_func, phi_func, u_exact_func = (
        compute_functions_from_exact(u_exact_sym, phi_sym)
    )

    test_case = TestCase(
        name=selected_predefined,
        input_data=InputData(f=f_func, g1=g1_func, g2=g2_func, phi=phi_func),
        exact_solution=u_exact_func,
        description=test_info["description"],
    )

    st.sidebar.subheader("Функции задачи")
    st.sidebar.latex(f"u(x,t) = {sp.latex(u_exact_sym)}")
    st.sidebar.latex(f"\\varphi(x) = {sp.latex(phi_sym)}")
    st.sidebar.latex(f"f(x,t) = {sp.latex(f_sym)}")
    st.sidebar.latex(f"g_1(t) = {sp.latex(g1_sym)}")
    st.sidebar.latex(f"g_2(t) = {sp.latex(g2_sym)}")

    st.sidebar.markdown(f"**Описание:** {test_case.description}")

    st.sidebar.subheader("Параметры сетки")
    N = st.sidebar.slider("Количество узлов по пространству (N):", 10, 200, 50)
    M = st.sidebar.slider("Количество узлов по времени (M):", 100, 5000, 1000)

    tau = 1.0 / M
    h = 1.0 / N
    stability_ratio = tau / h**2
    is_explicit_stable = stability_ratio <= 0.5

    st.sidebar.subheader("Параметры методов")
    use_explicit = st.sidebar.checkbox(
        "Использовать явную схему",
        value=is_explicit_stable,
        disabled=not is_explicit_stable,
    )
    use_implicit = st.sidebar.checkbox("Использовать неявную схему", value=True)
    eps_iter = st.sidebar.number_input(
        "Остановка неявной схемы:", value=1e-6, format="%.0e"
    )
    max_iter = st.sidebar.number_input("Максимум итераций МПИ:", 10, 1000, 100)

    st.sidebar.subheader("Визуализация")
    show_3d = st.sidebar.checkbox("Показать 3D графики", value=False)

    st.sidebar.subheader("Стабильность схем")
    if is_explicit_stable:
        st.sidebar.success(f"✅ Явная схема стабильна: {stability_ratio:.4f} ≤ 0.5")
    else:
        st.sidebar.error(f"❌ Явная схема нестабильна: {stability_ratio:.4f} > 0.5")
        st.sidebar.info("Увеличьте M или уменьшите N для стабильности явной схемы")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Результаты расчета")

        if st.button("Запустить расчет", type="primary"):
            try:
                params = Parametrs(N=N, M=M)
                solver = HeatConductionSolver(test_case.input_data, params)

                progress_bar = st.progress(0)
                status_text = st.empty()

                results = {}

                if use_explicit and is_explicit_stable:
                    status_text.text("Вычисление явной схемы...")
                    results["explicit"] = solver.explicit_solve()
                    progress_bar.progress(0.33)
                else:
                    progress_bar.progress(0.1)

                if use_implicit:
                    status_text.text("Вычисление неявной схемы...")
                    results["implicit"] = solver.implicit_solve(
                        eps_iter=eps_iter, max_iter=max_iter
                    )
                    progress_bar.progress(
                        0.66 if use_explicit and is_explicit_stable else 0.5
                    )

                status_text.text("Вычисление точного решения...")
                exact_solution = np.zeros((N + 1, M + 1))
                for j in range(M + 1):
                    for i in range(N + 1):
                        exact_solution[i, j] = test_case.exact_solution(
                            params.xi[i], params.tn[j]
                        )
                results["exact"] = exact_solution
                progress_bar.progress(1.0)

                status_text.text("Расчет завершен!")
                # Визуализация результатов
                st.subheader(
                    "Распределение средней максимальной по времени погрешности по пространству"
                )

                fig, ax = plt.subplots(figsize=(10, 6))

                if use_explicit and is_explicit_stable and "explicit" in results:
                    explicit_error = np.max(
                        np.abs(results["explicit"] - results["exact"]), axis=1
                    )
                    ax.plot(
                        params.xi,
                        explicit_error,
                        "b-",
                        linewidth=2,
                        label="Погрешность явной схемы",
                    )

                if use_implicit and "implicit" in results:
                    implicit_error = np.max(
                        np.abs(results["implicit"] - results["exact"]), axis=1
                    )
                    ax.plot(
                        params.xi,
                        implicit_error,
                        "r-",
                        linewidth=2,
                        label="Погрешность неявной схемы",
                    )

                if (
                    use_explicit
                    and is_explicit_stable
                    and "explicit" in results
                    and use_implicit
                    and "implicit" in results
                ):
                    schemes_diff = np.max(
                        np.abs(results["explicit"] - results["implicit"]), axis=1
                    )
                    ax.plot(
                        params.xi,
                        schemes_diff,
                        "g--",
                        linewidth=2,
                        label="Разность схем",
                    )

                ax.set_xlabel("Пространство, x")
                ax.set_ylabel("Максимальная погрешность")
                ax.set_title(
                    "Максимальная по времени погрешность для каждой точки пространства"
                )
                ax.legend()
                ax.grid(True, alpha=0.3)

                st.pyplot(fig)

                st.subheader("Анализ ошибок")

                col_err1, col_err2, col_err3 = st.columns(3)

                with col_err1:
                    if use_explicit and is_explicit_stable and "explicit" in results:
                        error_explicit = np.max(
                            np.abs(results["explicit"] - results["exact"])
                        )
                        st.metric("Макс. ошибка явной схемы", f"{error_explicit:.2e}")
                    else:
                        st.metric("Макс. ошибка явной схемы", "N/A")

                with col_err2:
                    if use_implicit and "implicit" in results:
                        error_implicit = np.max(
                            np.abs(results["implicit"] - results["exact"])
                        )
                        st.metric("Макс. ошибка неявной схемы", f"{error_implicit:.2e}")
                    else:
                        st.metric("Макс. ошибка неявной схемы", "N/A")

                with col_err3:
                    if (
                        use_explicit
                        and is_explicit_stable
                        and "explicit" in results
                        and use_implicit
                        and "implicit" in results
                    ):
                        diff_schemes = np.max(
                            np.abs(results["explicit"] - results["implicit"])
                        )
                        st.metric("Разность схем", f"{diff_schemes:.2e}")
                    else:
                        st.metric("Разность схем", "N/A")

                if show_3d:
                    st.subheader("3D визуализация")

                    cols_3d = st.columns(3)

                    with cols_3d[0]:
                        if (
                            use_explicit
                            and is_explicit_stable
                            and "explicit" in results
                        ):
                            fig_3d_explicit = create_3d_plot(
                                params, results, "explicit"
                            )
                            st.pyplot(fig_3d_explicit)

                    with cols_3d[1]:
                        if use_implicit and "implicit" in results:
                            fig_3d_implicit = create_3d_plot(
                                params, results, "implicit"
                            )
                            st.pyplot(fig_3d_implicit)

                    with cols_3d[2]:
                        fig_3d_exact = create_3d_plot(params, results, "exact")
                        st.pyplot(fig_3d_exact)
                st.subheader("Пространственно-временные диаграммы")

                if (use_explicit and is_explicit_stable and "explicit" in results) or (
                    use_implicit and "implicit" in results
                ):
                    cols_heat = st.columns(3)

                    with cols_heat[0]:
                        if (
                            use_explicit
                            and is_explicit_stable
                            and "explicit" in results
                        ):
                            fig_heat1, ax_heat1 = plt.subplots(figsize=(8, 6))
                            X, T = np.meshgrid(params.xi, params.tn)
                            im1 = ax_heat1.contourf(
                                X, T, results["explicit"].T, levels=50, cmap="hot"
                            )
                            ax_heat1.set_xlabel("Пространство, x")
                            ax_heat1.set_ylabel("Время, t")
                            ax_heat1.set_title("Явная схема")
                            plt.colorbar(im1, ax=ax_heat1, label="Температура")
                            st.pyplot(fig_heat1)

                    with cols_heat[1]:
                        if use_implicit and "implicit" in results:
                            fig_heat2, ax_heat2 = plt.subplots(figsize=(8, 6))
                            X, T = np.meshgrid(params.xi, params.tn)
                            im2 = ax_heat2.contourf(
                                X, T, results["implicit"].T, levels=50, cmap="hot"
                            )
                            ax_heat2.set_xlabel("Пространство, x")
                            ax_heat2.set_ylabel("Время, t")
                            ax_heat2.set_title("Неявная схема")
                            plt.colorbar(im2, ax=ax_heat2, label="Температура")
                            st.pyplot(fig_heat2)

                    with cols_heat[2]:
                        fig_heat3, ax_heat3 = plt.subplots(figsize=(8, 6))
                        X, T = np.meshgrid(params.xi, params.tn)
                        im3 = ax_heat3.contourf(
                            X, T, results["exact"].T, levels=50, cmap="hot"
                        )
                        ax_heat3.set_xlabel("Пространство, x")
                        ax_heat3.set_ylabel("Время, t")
                        ax_heat3.set_title("Неявная схема")
                        plt.colorbar(im3, ax=ax_heat3, label="Температура")
                        st.pyplot(fig_heat3)
            except Exception as e:
                st.error(f"Ошибка при расчете: {str(e)}")
                st.info("Попробуйте изменить параметры сетки")

    with col2:
        st.header("Информация о задаче")

        st.subheader("Уравнение теплопроводности")
        st.latex(r"""
        \frac{\partial u}{\partial t} = \frac{\partial^2 u}{\partial x^2} + f(x,t)
        """)

        st.subheader("Начальное условие")
        st.latex(r"""
        u(0,x) = \varphi(x)
        """)

        st.subheader("Граничные условия")
        st.latex(r"""
        -\frac{\partial u}{\partial x} + u^4(t,0) = g_1(t)
        """)
        st.latex(r"""
        \frac{\partial u}{\partial x} + u^4(t,1) = g_2(t)
        """)

        st.subheader("Методы решения")
        st.markdown("""
        - **Явная схема**: Условно устойчива, требует малого шага по времени
        - **Неявная схема**: Безусловно устойчива, решается методом простых итераций (МПИ)
        - **МПИ**: Начальное приближение - предикция по явной схеме
        """)

        st.subheader("Текущий тест")
        st.markdown(f"**{test_case.name}**")
        st.markdown(test_case.description)

        st.subheader("Параметры расчета")
        st.markdown(f"""
        - Узлов по пространству: **{N}**
        - Узлов по времени: **{M}**
        - Шаг по пространству: **{h:.4f}**
        - Шаг по времени: **{tau:.6f}**
        - Отношение τ/h²: **{stability_ratio:.4f}**
        """)

    st.markdown("---")
    st.markdown("**Курсовая работа по дисциплине 'Численное моделирование'**")
    st.markdown("Тема: Нелинейное уравнение теплопроводности")
