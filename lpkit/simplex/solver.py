# solver.py - algoritmo Simplex principal

from .utils import display_tableau, build_simplex_table, get_entering_variable, get_leaving_variable, pivot_tableau
from .analysis import analyze_tableau
from ..core.model import to_standard_form

def solve_with_simplex(model_text, verbose=None):
    """
    Executa o algoritmo Simplex completo com rastreamento e histórico.
    Parâmetros:
    - model_text: texto com a modelagem do problema
    - verbose: dicionário com flags de controle de saída:
        {
            'simplex_tableau': True,
            'entering_leaving': True,
            'pivot': True,
            'basic_vars': True,
            'constraints_validation': True,
            'z_per_iteration': True,
            'history_summary': True
        }
    """
    if verbose is None:
        verbose = {
            "simplex_tableau": False,
            "entering_leaving": False,
            "pivot": False,
            "basic_vars": False,
            "constraints_validation": False,
            "z_per_iteration": False,
            "history_summary": True,
        }

    _, objective_expr, constraints, variables = to_standard_form(model_text)
    tableau, all_vars = build_simplex_table(
        objective_expr, constraints, variables, verbose=verbose.get("simplex_tableau")
    )

    iteration = 1
    history = []

    while True:
        if verbose.get("simplex_tableau"):
            print(f"\n\n🔁 Iteração {iteration}")

        entering_var, entering_index = get_entering_variable(
            tableau, all_vars, verbose=verbose.get("entering_leaving")
        )

        if entering_var is None:
            if verbose.get("entering_leaving"):
                print("\n🏁 A solução ótima foi encontrada.")
            break

        leaving_row = get_leaving_variable(
            tableau, entering_index, verbose=verbose.get("entering_leaving")
        )
        if leaving_row is None:
            if verbose.get("entering_leaving"):
                print("\n🚨 Problema ilimitado. O algoritmo será interrompido.")
            break

        tableau = pivot_tableau(
            tableau, leaving_row, entering_index, verbose=verbose.get("pivot")
        )

        if verbose.get("simplex_tableau"):
            display_tableau(tableau, all_vars, entering_index, verbose=True)

        basic_vars, non_basic_vars, z_value, solution_dict = analyze_tableau(
            tableau,
            all_vars,
            constraints,
            objective_expr,
            verbose=verbose,
        )

        history.append(
            {
                "iteration": iteration,
                "entering_var": str(entering_var),
                "leaving_row": leaving_row,
                "z_value": z_value,
                "solution": solution_dict.copy(),
            }
        )

        iteration += 1

    if verbose.get("history_summary"):
        print("\n📚 Histórico das iterações:")
        for step in history:
            print(f"Iteração {step['iteration']}:")
            print(f"  Entrou: {step['entering_var']}")
            print(f"  Saiu da linha: R{step['leaving_row']}")
            print(f"  Z = {step['z_value']:.4f}")
            print("  Solução básica:", step["solution"])

    return tableau, z_value, history
