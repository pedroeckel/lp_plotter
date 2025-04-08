import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from itertools import combinations


# --- Verifica se um ponto satisfaz todas as restrições ---
def is_feasible_point(point: tuple, constraints: list, variables: list) -> bool:
    substitutions = {str(var): point[i] for i, var in enumerate(variables)}
    for lhs, operator, rhs in constraints:
        evaluated = float(lhs.subs(substitutions))
        if operator == "<=" and evaluated > rhs + 1e-5:
            return False
        elif operator == ">=" and evaluated < rhs - 1e-5:
            return False
        elif operator == "==" and abs(evaluated - rhs) > 1e-5:
            return False
    return True


# --- Plotagem do modelo ---
def plot_linear_program(
    objective_type: str,
    objective_expr: sp.Expr,
    constraints: list,
    show_gradient: bool = True,
    show_level_curves: bool = True,
    show_objective_value: bool = True,
    show_vertex_points: bool = True,
    show_optimal_point: bool = True,
):
    variables = sorted(objective_expr.free_symbols, key=lambda v: str(v))
    if len(variables) != 2:
        raise ValueError("Este gráfico só suporta modelos com exatamente 2 variáveis.")

    all_symbols_in_constraints = set()
    for lhs, _, _ in constraints:
        all_symbols_in_constraints.update(lhs.free_symbols)
    if not set(variables).issubset(all_symbols_in_constraints):
        raise ValueError(
            "Nem todas as variáveis da função objetivo aparecem nas restrições."
        )

    var_x, var_y = variables
    xy_vars = [var_x, var_y]

    x_range = np.linspace(0, 10, 400)
    plt.figure(figsize=(9, 5))
    all_equations = []

    # --- Desenhar as restrições ---
    for lhs, operator, rhs in constraints:
        equation = lhs - rhs
        all_equations.append(equation)

        expr_y = sp.solve(equation, var_y)
        if expr_y:
            y_expr = expr_y[0]
            if var_x in y_expr.free_symbols:
                y_func = sp.lambdify(var_x, y_expr, "numpy")
                y_values = y_func(x_range)
                plt.plot(x_range, y_values, label=f"{sp.pretty(lhs)} {operator} {rhs}")
            else:
                y_const = float(y_expr)
                plt.plot(
                    x_range,
                    [y_const] * len(x_range),
                    label=f"{sp.pretty(lhs)} {operator} {rhs}",
                )
        else:
            expr_x = sp.solve(equation, var_x)
            if expr_x:
                x_expr = expr_x[0]
                if var_y in x_expr.free_symbols:
                    x_func = sp.lambdify(var_y, x_expr, "numpy")
                    y_range = np.linspace(0, 10, 400)
                    x_values = x_func(y_range)
                    plt.plot(
                        x_values, y_range, label=f"{sp.pretty(lhs)} {operator} {rhs}"
                    )
                else:
                    x_const = float(x_expr)
                    plt.plot(
                        [x_const] * len(x_range),
                        x_range,
                        label=f"{sp.pretty(lhs)} {operator} {rhs}",
                    )

    # --- Encontrar pontos viáveis e solução ótima ---
    feasible_points = []
    for eq1, eq2 in combinations(all_equations, 2):
        solution = sp.solve([eq1, eq2], (var_x, var_y), dict=True)
        if solution:
            sol = solution[0]
            try:
                px = float(sol[var_x])
                py = float(sol[var_y])
                if is_feasible_point((px, py), constraints, xy_vars):
                    feasible_points.append((px, py))
            except:
                continue

    optimal_point = None
    optimal_value = -np.inf if objective_type == "max" else np.inf

    if feasible_points:
        feasible_points = np.array(feasible_points)
        centroid = np.mean(feasible_points, axis=0)
        ordered_points = sorted(
            feasible_points,
            key=lambda p: np.arctan2(p[1] - centroid[1], p[0] - centroid[0]),
        )
        px, py = zip(*ordered_points)
        plt.fill(px, py, color="gray", alpha=0.5)

        if show_vertex_points:
            for vx, vy in ordered_points:
                plt.plot(vx, vy, "ko", markersize=4)

        for point in ordered_points:
            z_value = float(objective_expr.subs({var_x: point[0], var_y: point[1]}))
            if (objective_type == "max" and z_value > optimal_value) or (
                objective_type == "min" and z_value < optimal_value
            ):
                optimal_value = z_value
                optimal_point = point

    # --- Vetor Gradiente ---
    gradient_x = float(objective_expr.coeff(var_x))
    gradient_y = float(objective_expr.coeff(var_y))
    if show_gradient:
        plt.arrow(
            0,
            0,
            gradient_x,
            gradient_y,
            head_width=0.3,
            head_length=0.5,
            fc="red",
            ec="red",
            label="Gradiente",
        )

    # --- Curvas de nível ---
    if optimal_point is not None and show_level_curves:
        z_star = optimal_value
        z_levels = np.linspace(z_star - 15, z_star, 5)
        for z in z_levels:
            try:
                y_expr_level = sp.solve(objective_expr - z, var_y)[0]
                y_func = sp.lambdify(var_x, y_expr_level, "numpy")
                y_values = y_func(x_range)
                plt.plot(x_range, y_values, "r--", alpha=0.5)
                for xi in np.linspace(0, 9, 50):
                    try:
                        yi = y_func(xi)
                        if 0 <= yi <= 7:
                            plt.text(xi, yi, f"Z={z:.1f}", color="red", fontsize=8)
                            break
                    except:
                        continue
            except:
                continue

    # --- Ponto ótimo e valor da função objetivo ---
    if optimal_point is not None:
        if show_optimal_point:
            plt.plot(*optimal_point, "ro")
            plt.text(
                optimal_point[0] + 0.1,
                optimal_point[1],
                f"Ótimo ({optimal_point[0]:.1f}, {optimal_point[1]:.1f})",
                color="red",
            )
        if show_objective_value:
            plt.text(
                optimal_point[0] + 0.1,
                optimal_point[1] - 0.4,
                f"Z = {optimal_value:.1f}",
                color="red",
            )

    # --- Finalização ---
    plt.xlim(0, 9)
    plt.ylim(0, 7)
    plt.xlabel(str(var_x))
    plt.ylabel(str(var_y))
    plt.title("Método gráfico para Programação Linear")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()
