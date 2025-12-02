import math
import os
import tempfile

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import sympy as sp
from kurs import HeatConductionSolver, InputData, Parametrs, TestCase
from matplotlib import animation

plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "Helvetica",
        "text.latex.preamble": r"""
        \usepackage[utf8]{inputenc}
        \usepackage[russian]{babel}
        """,
    }
)


def extract_order_of_10(number):
    if number == 0:
        return 0
    order = math.floor(math.log10(abs(number)))
    return 10**order


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
    g1_sym = -u_x_0_sym + u_0_sym**4  # pyright: ignore[reportOperatorIssue]
    g2_sym = u_x_1_sym + u_1_sym**4

    f_func = sp.lambdify((x, t), f_sym, "numpy")
    g1_func = sp.lambdify(t, g1_sym, "numpy")
    g2_func = sp.lambdify(t, g2_sym, "numpy")
    phi_func = sp.lambdify(x, phi_sym, "numpy")
    u_exact_func = sp.lambdify((x, t), u_exact_sym, "numpy")

    return f_sym, g1_sym, g2_sym, f_func, g1_func, g2_func, phi_func, u_exact_func


x, t = sp.symbols("x t")

# Complex test cases with various behaviors
PREDEFINED_TESTS = {
    # Simple cases
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
    # Exponential and trigonometric cases
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
    # More complex cases
    "Полиномиальное решение": {
        "u_exact": x**3 - 2 * x**2 + x + sp.sin(t),
        "phi": x**3 - 2 * x**2 + x,
        "description": "u(x,t) = x³ - 2x² + x + sin(t) - полином с осцилляциями во времени",
    },
    "Гауссов пакет": {
        "u_exact": sp.exp(-((x - 0.5) ** 2) / (0.1 + 0.05 * t)) * sp.cos(2 * sp.pi * t),
        "phi": sp.exp(-((x - 0.5) ** 2) / 0.1),
        "description": "u(x,t) = exp(-(x-0.5)²/(0.1+0.05t))cos(2πt) - движущийся гауссов пакет",
    },
    "Ступенчатая функция": {
        "u_exact": (1 + sp.tanh(10 * (x - 0.5 - 0.1 * t))) / 2 + 0.1 * sp.sin(5 * t),
        "phi": (1 + sp.tanh(10 * (x - 0.5))) / 2,
        "description": "u(x,t) = 0.5(1+tanh(10(x-0.5-0.1t))) + 0.1sin(5t) - движущийся фронт",
    },
    "Бегущая волна": {
        "u_exact": sp.sin(2 * sp.pi * (x - t)) * sp.exp(-0.1 * t),
        "phi": sp.sin(2 * sp.pi * x),
        "description": "u(x,t) = sin(2π(x-t))exp(-0.1t) - бегущая волна с затуханием",
    },
    "Сложная осцилляция": {
        "u_exact": sp.sin(3 * sp.pi * x) * sp.cos(2 * sp.pi * t)
        + 0.5 * sp.sin(5 * sp.pi * x) * sp.sin(sp.pi * t),
        "phi": sp.sin(3 * sp.pi * x) + 0.5 * sp.sin(5 * sp.pi * x),
        "description": "u(x,t) = sin(3πx)cos(2πt) + 0.5sin(5πx)sin(πt) - сложные осцилляции",
    },
    "Рациональная функция": {
        "u_exact": (x + 0.1) / (1 + 0.5 * t) + 0.1 * sp.sin(2 * sp.pi * x * t),
        "phi": (x + 0.1),
        "description": "u(x,t) = (x+0.1)/(1+0.5t) + 0.1sin(2πxt) - рациональная зависимость с осцилляциями",
    },
    "Двойной источник": {
        "u_exact": sp.exp(-20 * (x - 0.3) ** 2) * sp.exp(-t)
        + sp.exp(-20 * (x - 0.7) ** 2) * sp.exp(-0.5 * t),
        "phi": sp.exp(-20 * (x - 0.3) ** 2) + sp.exp(-20 * (x - 0.7) ** 2),
        "description": "u(x,t) = два гауссовых источника с разной скоростью затухания",
    },
    "Периодическая модуляция": {
        "u_exact": (1 + 0.5 * sp.sin(4 * sp.pi * x))
        * sp.exp(-0.2 * t)
        * sp.sin(2 * sp.pi * t),
        "phi": (1 + 0.5 * sp.sin(4 * sp.pi * x)) * sp.sin(2 * sp.pi * 0),
        "description": "u(x,t) = модулированная осциллирующая функция",
    },
    "Логарифмическая зависимость": {
        "u_exact": sp.log(1 + x + t) * sp.sin(sp.pi * x),
        "phi": sp.log(1 + x) * sp.sin(sp.pi * x),
        "description": "u(x,t) = log(1+x+t)sin(πx) - логарифмический рост",
    },
    "Степенная функция": {
        "u_exact": (x**0.5 + 0.1) * (t**0.3 + 0.1) * sp.exp(-0.5 * x),
        "phi": (x**0.5 + 0.1) * (0.1) * sp.exp(-0.5 * x),
        "description": "u(x,t) = степенная зависимость по пространству и времени",
    },
    "Комбинированная экспонента": {
        "u_exact": sp.exp(-x * t) * sp.sin(2 * sp.pi * x)
        + sp.exp(-(1 - x) * t) * sp.cos(2 * sp.pi * x),
        "phi": sp.exp(0) * sp.sin(2 * sp.pi * x) + sp.exp(0) * sp.cos(2 * sp.pi * x),
        "description": "u(x,t) = комбинация экспонент с разным поведением на границах",
    },
    "Быстрые осцилляции": {
        "u_exact": sp.sin(10 * sp.pi * x) * sp.exp(-2 * t)
        + 0.1 * sp.sin(50 * sp.pi * x) * sp.exp(-5 * t),
        "phi": sp.sin(10 * sp.pi * x) + 0.1 * sp.sin(50 * sp.pi * x),
        "description": "u(x,t) = быстрые пространственные осцилляции с разным затуханием",
    },
    "Несимметричное решение": {
        "u_exact": x * (1 - x) ** 2 * (1 + 0.5 * sp.sin(3 * t))
        + 0.1 * x**3 * sp.cos(2 * t),
        "phi": x * (1 - x) ** 2 + 0.1 * x**3,
        "description": "u(x,t) = несимметричное полиномиальное решение с осцилляциями",
    },
    "Сложная фаза": {
        "u_exact": sp.sin(2 * sp.pi * x + t) * sp.exp(-0.3 * x * t)
        + 0.2 * sp.cos(4 * sp.pi * x - 2 * t),
        "phi": sp.sin(2 * sp.pi * x) + 0.2 * sp.cos(4 * sp.pi * x),
        "description": "u(x,t) = решения со сложной фазовой модуляцией",
    },
    "Мультискалярное решение": {
        "u_exact": sp.sin(2 * sp.pi * x)
        * (1 + 0.1 * sp.sin(20 * sp.pi * x))
        * sp.exp(-t),
        "phi": sp.sin(2 * sp.pi * x) * (1 + 0.1 * sp.sin(20 * sp.pi * x)),
        "description": "u(x,t) = мультискалярное решение с быстрыми и медленными осцилляциями",
    },
    "Радиальная функция": {
        "u_exact": sp.exp(-10 * ((x - 0.5) ** 2 + (t - 0.5) ** 2))
        * sp.sin(5 * sp.pi * x),
        "phi": sp.exp(-10 * ((x - 0.5) ** 2 + (0.5) ** 2)) * sp.sin(5 * sp.pi * x),
        "description": "u(x,t) = радиально-симметричная функция в пространстве-времени",
    },
}


def create_optimized_animation(test_case_name, params, output_dir="animations"):
    """Создает оптимизированную анимацию для заданного тестового случая"""

    test_info = PREDEFINED_TESTS[test_case_name]
    u_exact_sym = test_info["u_exact"]
    phi_sym = test_info["phi"]

    f_sym, g1_sym, g2_sym, f_func, g1_func, g2_func, phi_func, u_exact_func = (
        compute_functions_from_exact(u_exact_sym, phi_sym)
    )

    test_case = TestCase(
        name=test_case_name,
        input_data=InputData(f=f_func, g1=g1_func, g2=g2_func, phi=phi_func),
        exact_solution=u_exact_func,
        description=test_info["description"],
    )

    solver = HeatConductionSolver(test_case.input_data, params)

    # Precompute all solutions
    result = {}
    result["explicit"] = solver.explicit_solve()
    result["implicit"] = solver.implicit_solve()
    result["exact"] = np.array(
        [[u_exact_func(i, j) for j in params.tn] for i in params.xi],
        dtype=result["explicit"].dtype,
    )

    # Optimized animation parameters
    fps = 15  # Reduced for better performance
    duration = 8  # Slightly longer for better visualization
    total_frames = min(duration * fps, params.M)  # Don't exceed available time steps

    # Precompute error metrics for all time steps
    implicit_errors = np.mean(np.abs(result["implicit"] - result["exact"]), axis=0)
    explicit_errors = np.mean(np.abs(result["explicit"] - result["exact"]), axis=0)
    method_differences = np.max(np.abs(result["implicit"] - result["explicit"]), axis=0)

    fig, (ax_main, ax_inset) = plt.subplots(1, 2, figsize=(16, 6))

    # Main plot
    (line_exact,) = ax_main.plot(
        params.xi,
        result["exact"][:, 0],
        label="Точное решение",
        linewidth=2,
        color="blue",
    )
    (line_explicit,) = ax_main.plot(
        params.xi,
        result["explicit"][:, 0],
        label="Явный метод",
        linestyle="--",
        linewidth=2,
        color="red",
    )
    (line_implicit,) = ax_main.plot(
        params.xi,
        result["implicit"][:, 0],
        label="Неявный метод",
        linestyle="--",
        linewidth=2,
        color="green",
    )

    # Inset plot
    (line_exact_inset,) = ax_inset.plot(
        params.xi, result["exact"][:, 0], label="Точное", linewidth=1, color="blue"
    )
    (line_explicit_inset,) = ax_inset.plot(
        params.xi,
        result["explicit"][:, 0],
        label="Явный",
        linestyle="--",
        linewidth=1,
        color="red",
    )
    (line_implicit_inset,) = ax_inset.plot(
        params.xi,
        result["implicit"][:, 0],
        label="Неявный",
        linestyle="--",
        linewidth=1,
        color="green",
    )

    # Setup main plot
    ax_main.set_xlabel("$x$", fontsize=12)
    ax_main.set_ylabel("$u(x,t)$", fontsize=12)
    ax_main.grid(True, alpha=0.3)
    ax_main.legend()

    # Setup inset plot
    ax_inset.set_title("Увеличенный масштаб", fontsize=10)
    ax_inset.grid(True, alpha=0.3)
    ax_inset.set_xlabel("$x$", fontsize=8)
    ax_inset.set_ylabel("$u(x,t)$", fontsize=8)

    # Text annotations
    tauh_text = params.tau / (params.h**2)
    tau_h = ax_main.text(
        0.02,
        0.98,
        f"$\\frac{{\\tau}}{{h^2}} = {tauh_text:.4f}$",
        transform=ax_main.transAxes,
        verticalalignment="top",
        fontsize=10,
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
    )
    error_text = ax_main.text(
        0.02,
        0.75,
        "",
        transform=ax_main.transAxes,
        verticalalignment="top",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.8),
    )

    formula_text = fig.text(
        0.02,
        0.02,
        "",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.8),
    )
    # Display formulas
    formula_info = (
        f"Точное решение: ${sp.latex(u_exact_sym)}$\n"
        f"Начальное условие: $\\phi(x) = {sp.latex(phi_sym)}$\n"
        f"Правая часть: $f(x,t) = {sp.latex(f_sym.simplify())}$\n"
        f"Граничное условие 1: $g_1(t) = {sp.latex(g1_sym.simplify())}$\n"
        f"Граничное условие 2: $g_2(t) = {sp.latex(g2_sym.simplify())}$\n"
        f"Шаг по времени: $\\tau = {params.tau:.6e}$\n"
        f"Шаг по пространству: $h = {params.h:.6e}$"
    )
    formula_text.set_text(formula_info)
    # Получаем порядок погрешности неявного метода
    error_order = math.floor(math.log10(implicit_errors.mean() + 1e-16))
    zoom_factor = 10 ** (error_order + 1)  # на 1 порядок больше погрешности

    # Ограничиваем разумными пределами
    zoom_factor = max(1e-10, min(1e-3, zoom_factor))

    def update_frame(frame):
        # Calculate time index with proper distribution
        time_idx = min(int(frame * params.M / total_frames), params.M - 1)
        current_time = params.tn[time_idx]

        # Update plots
        y_exact = result["exact"][:, time_idx]
        y_explicit = result["explicit"][:, time_idx]
        y_implicit = result["implicit"][:, time_idx]

        line_exact.set_ydata(y_exact)
        line_explicit.set_ydata(y_explicit)
        line_implicit.set_ydata(y_implicit)

        line_exact_inset.set_ydata(y_exact)
        line_explicit_inset.set_ydata(y_explicit)
        line_implicit_inset.set_ydata(y_implicit)

        # Update main plot limits
        y_min_inset = np.min(y_exact)
        y_max_inset = np.max(y_exact)
        y_min = min(y_min_inset, np.min(y_explicit), np.min(y_implicit))
        y_max = max(y_max_inset, np.max(y_explicit), np.max(y_implicit))
        y_range = y_max - y_min
        y_range_inset = y_max_inset - y_min_inset
        ax_main.set_ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)
        ax_main.set_title(
            f"{test_case_name}\nВремя: t = {current_time:.3f}", fontsize=12
        )

        # Update inset plot limits (zoomed view around center)
        center_idx = len(params.xi) // 2
        x_center = params.xi[center_idx]
        y_center = y_exact[center_idx]

        x_range = (params.xi[-1] - params.xi[0]) * zoom_factor
        y_range_inset = y_range_inset * zoom_factor

        ax_inset.set_xlim(x_center - x_range / 2, x_center + x_range / 2)
        ax_inset.set_ylim(y_center - y_range_inset / 2, y_center + y_range_inset / 2)
        ax_inset.set_title(f"Увеличенный масштаб ($10^{math.log10(zoom_factor)}$)")

        error_info = (
            f"Погрешности (t={current_time:.3f}):\n"
            f"Неявный метод: {implicit_errors[time_idx]:.2e}\n"
            f"Явный метод: {explicit_errors[time_idx]:.2e}\n"
            f"Разность методов: {method_differences[time_idx]:.2e}"
        )
        error_text.set_text(error_info)

        return (
            line_exact,
            line_explicit,
            line_implicit,
            line_exact_inset,
            line_explicit_inset,
            line_implicit_inset,
            tau_h,
            error_text,
            formula_text,
        )

    anim = animation.FuncAnimation(
        fig, update_frame, frames=total_frames, interval=1000 / fps, blit=False
    )

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Save animation
    filename = (
        f"{output_dir}/{test_case_name.replace(' ', '_')}_N{params.N}_M{params.M}.mp4"
    )

    # Use lower quality for faster rendering
    anim.save(
        filename,
        writer="ffmpeg",
        fps=fps,
        dpi=100,
        bitrate=1000,
        extra_args=["-preset", "fast"],
    )

    plt.close(fig)  # Close figure to free memory
    return filename


def main():
    st.title("Численное решение уравнения теплопроводности")

    st.sidebar.header("Параметры вычислений")

    # Parameter sets
    param_sets = {
        "Небольшой h": Parametrs(N=1000, M=20_000),
        "В 10 раз меньше h": Parametrs(N=100, M=20_000),
    }

    selected_param_name = st.sidebar.selectbox(
        "Выберите набор параметров:", list(param_sets.keys())
    )
    params = param_sets[selected_param_name]

    st.sidebar.write(f"Параметры сетки: N={params.N}, M={params.M}")
    st.sidebar.write(f"Шаг по пространству: h = {params.h:.4f}")
    st.sidebar.write(f"Шаг по времени: τ = {params.tau:.4f}")
    st.sidebar.write(f"Критерий устойчивости: τ/h² = {params.tau / params.h**2:.4f}")

    # Test case selection
    test_cases = list(PREDEFINED_TESTS.keys())
    selected_tests = st.sidebar.multiselect(
        "Выберите тестовые случаи для анимации:",
        test_cases,
        default=test_cases[:19],
    )

    if st.sidebar.button("Создать все анимации"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        output_dir = "heat_equation_animations"
        created_files = []

        for i, test_case in enumerate(selected_tests):
            status_text.text(
                f"Создание анимации: {test_case} ({i + 1}/{len(selected_tests)})"
            )

            try:
                filename = create_optimized_animation(test_case, params, output_dir)
                created_files.append((test_case, filename))
            except Exception as e:
                st.error(f"Ошибка при создании анимации для {test_case}: {str(e)}")

            progress_bar.progress((i + 1) / len(selected_tests))

        status_text.text("Все анимации созданы!")

        # Display created animations
        st.header("Созданные анимации")

        for test_case, filename in created_files:
            st.subheader(test_case)
            st.write(f"**Описание:** {PREDEFINED_TESTS[test_case]['description']}")

            # Display video
            try:
                with open(filename, "rb") as video_file:
                    video_bytes = video_file.read()
                st.video(video_bytes)
            except Exception as e:
                st.error(f"Не удалось отобразить видео: {str(e)}")

            # Download link
            with open(filename, "rb") as file:
                st.download_button(
                    label=f"Скачать {test_case}",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="video/mp4",
                    key=f"download_{test_case}",
                )

            st.markdown("---")

    # Single test case preview
    st.sidebar.header("Быстрый предпросмотр")
    preview_case = st.sidebar.selectbox(
        "Выберите случай для предпросмотра:", test_cases
    )

    if st.sidebar.button("Быстрый предпросмотр"):
        st.header(f"Предпросмотр: {preview_case}")

        with st.spinner("Создание анимации..."):
            temp_dir = tempfile.mkdtemp()
            filename = create_optimized_animation(preview_case, params, temp_dir)

            # Display information
            test_info = PREDEFINED_TESTS[preview_case]
            u_exact_sym = test_info["u_exact"]
            phi_sym = test_info["phi"]

            f_sym, g1_sym, g2_sym, _, _, _, _, _ = compute_functions_from_exact(
                u_exact_sym, phi_sym
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Формулы")
                st.latex(f"u(x,t) = {sp.latex(u_exact_sym)}")
                st.latex(f"\\phi(x) = {sp.latex(phi_sym)}")
                st.latex(f"f(x,t) = {sp.latex(f_sym.simplify())}")
                st.latex(f"g_1(t) = {sp.latex(g1_sym.simplify())}")
                st.latex(f"g_2(t) = {sp.latex(g2_sym.simplify())}")

            with col2:
                st.subheader("Параметры")
                st.write(f"**Описание:** {test_info['description']}")
                st.write(f"**Сетка:** N={params.N}, M={params.M}")
                st.write(f"**Шаг по пространству:** h = {params.h:.6f}")
                st.write(f"**Шаг по времени:** τ = {params.tau:.6f}")
                st.write(
                    f"**Критерий устойчивости:** τ/h² = {params.tau / params.h**2:.6f}"
                )

            # Display animation
            st.subheader("Анимация")
            try:
                with open(filename, "rb") as video_file:
                    video_bytes = video_file.read()
                st.video(video_bytes)
            except Exception as e:
                st.error(f"Не удалось отобразить анимацию: {str(e)}")


if __name__ == "__main__":
    main()
