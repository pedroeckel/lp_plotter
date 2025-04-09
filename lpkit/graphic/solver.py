
from .parser import parse_model_from_text
from .plotter import plot_linear_problem

def solve_with_graphics(model_text: str, verbose: dict = None):
    """
    Resolve e plota um problema de PL usando o método gráfico.

    Parâmetros:
    - model_text: texto do modelo em formato LP
    - verbose: dicionário com flags booleanas para controle de exibição:
        {
            'show_gradient': True,
            'show_level_curves': True,
            'show_objective_value': True,
            'show_vertex_points': True,
            'show_optimal_point': True
        }
    """
    if verbose is None:
        verbose = {
            "show_gradient": True,
            "show_level_curves": True,
            "show_objective_value": True,
            "show_vertex_points": True,
            "show_optimal_point": True,
        }

    objective_type, objective_expr, constraints = parse_model_from_text(model_text)

    plot_linear_problem(
        objective_type,
        objective_expr,
        constraints,
        show_gradient=verbose.get("show_gradient", True),
        show_level_curves=verbose.get("show_level_curves", True),
        show_objective_value=verbose.get("show_objective_value", True),
        show_vertex_points=verbose.get("show_vertex_points", True),
        show_optimal_point=verbose.get("show_optimal_point", True),
    )
