from lp_plotter import parse_model_from_text, plot_linear_program

model_text = """
Max Z = 5*x1 + 2*x2
x1 <= 3
x2 <= 4
x1 + 2*x2 <= 9
x1 - 2*x2 <= 2
x1 >= 0
x2 >= 0
"""

sense, objective, constraints = parse_model_from_text(model_text)

plot_linear_program(
    sense,
    objective,
    constraints,
    show_gradient=True,
    show_level_curves=True,
    show_objective_value=True,
    show_vertex_points=True,
    show_optimal_point=True
)
