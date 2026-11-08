import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate


def quadratic_function(x):
    """Цільова функція для інтегрування: f(x) = x^2."""
    return x ** 2


def monte_carlo_integrate(function, lower_bound: float, upper_bound: float, sample_count: int = 100_000) -> float:
    """
    Обчислення визначеного інтеграла методом Монте-Карло (геометричний метод).
    """
    # Знаходимо максимальне значення функції на інтервалі [lower_bound, upper_bound] для висоти прямокутника
    x_grid = np.linspace(lower_bound, upper_bound, 1000)
    maximum_value = float(np.max(function(x_grid)))

    # Генеруємо випадкові точки (x, y) всередині обмежувального прямокутника
    x_random = np.random.uniform(lower_bound, upper_bound, sample_count)
    y_random = np.random.uniform(0, maximum_value, sample_count)

    # Рахуємо кількість точок, що потрапили під криву: y <= f(x)
    points_under_curve = np.sum(y_random <= function(x_random))

    # Площа прямокутника * частка точок під кривою
    rectangle_area = (upper_bound - lower_bound) * maximum_value
    integral_estimate = rectangle_area * (points_under_curve / sample_count)

    return integral_estimate


def plot_function(function, lower_bound: float, upper_bound: float):
    """Побудова графіка функції та області інтегрування згідно з умовою."""
    x_values = np.linspace(-0.5, 2.5, 400)
    y_values = function(x_values)

    _, axes = plt.subplots(figsize=(8, 5))
    axes.plot(x_values, y_values, "r", linewidth=2, label="f(x) = x^2")

    integration_x = np.linspace(lower_bound, upper_bound, 200)
    integration_y = function(integration_x)
    axes.fill_between(integration_x, integration_y, color="gray", alpha=0.3, label="Площа інтеграла")

    axes.set_xlim((x_values[0], x_values[-1]))
    axes.set_ylim((0, max(y_values) + 0.1))
    axes.set_xlabel("x")
    axes.set_ylabel("f(x)")
    axes.axvline(x=lower_bound, color="gray", linestyle="--")
    axes.axvline(x=upper_bound, color="gray", linestyle="--")
    axes.set_title(f"Графік інтегрування f(x) = x^2 від {lower_bound} до {upper_bound}")
    axes.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    np.random.seed(42)  # Фіксуємо seed для відтворюваності результатів

    lower_bound = 0
    upper_bound = 2

    # 1. Точне значення за допомогою scipy.integrate.quad та аналітично
    quad_result, quad_error = integrate.quad(quadratic_function, lower_bound, upper_bound)
    analytical_result = (upper_bound**3 / 3) - (lower_bound**3 / 3)  # Первісна x^3 / 3

    print(f"Аналітичний результат:       {analytical_result:.8f}")
    print(f"Результат scipy.quad:        {quad_result:.8f} (похибка: {quad_error:.2e})\n")

    # 2. Експерименти методом Монте-Карло для різної кількості точок
    sample_sizes = [1_000, 10_000, 100_000, 1_000_000]
    print(f"{'Кількість точок (N)':<22} | {'Монте-Карло':<15} | {'Абс. похибка':<15} | {'Відн. похибка (%)'}")
    print("-" * 75)

    for sample_count in sample_sizes:
        monte_carlo_result = monte_carlo_integrate(
            quadratic_function, lower_bound, upper_bound, sample_count=sample_count
        )
        absolute_error = abs(monte_carlo_result - quad_result)
        relative_error = (absolute_error / quad_result) * 100
        print(f"{sample_count:<22} | {monte_carlo_result:<15.8f} | {absolute_error:<15.8f} | {relative_error:.4f}%")

    # 3. Візуалізація графіка
    plot_function(quadratic_function, lower_bound, upper_bound)
