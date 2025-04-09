import numpy as np

def analyze_tableau(tableau, all_vars, constraints, objective_expr, verbose=None):
    if verbose is None:
        verbose = {
            "basic_vars": False,
            "constraints_validation": False,
            "z_per_iteration": False,
        }

    basis = []
    A_no_obj = tableau[1:, :-1]
    for col_idx in range(len(all_vars)):
        col = A_no_obj[:, col_idx]
        ones = np.isclose(col, 1.0)
        zeros = np.isclose(col, 0.0)
        if np.sum(ones) == 1 and np.sum(zeros) == len(col) - 1:
            row_idx = np.where(ones)[0][0]
            basis.append((all_vars[col_idx], row_idx + 1))

    basis = sorted(basis, key=lambda x: str(x[0]))
    basic_vars = [v for v, _ in basis]
    non_basic_vars = [v for v in all_vars if v not in basic_vars]

    solution_dict = {str(v): 0 for v in all_vars}
    for var, row in basis:
        solution_dict[str(var)] = tableau[row, -1]

    if verbose.get("basic_vars"):
        print("\n🔧 Variáveis bases:")
        for var, row in basis:
            value = tableau[row, -1]
            print(f"  {var} na linha L{row} = {value:.4f}")

        print("\n📎 Variáveis não básicas:")
        for var in sorted(non_basic_vars, key=lambda x: str(x)):
            print(f"  {var} = 0.0000")

    b_values = tableau[1:, -1]
    if verbose.get("basic_vars"):
        if np.all(b_values >= 0):
            print("\n✅ A solução básica atual é factível.")
        else:
            print("\n❌ A solução básica atual NÃO é factível.")

    z_value = tableau[0, -1]
    if verbose.get("z_per_iteration"):
        print(f"\n🎯 Valor atual de Z: {z_value}")

    if verbose.get("constraints_validation"):
        print("\n🔍 Validação das restrições:")
        for i, eq in enumerate(constraints):
            lhs_expr = eq.lhs
            rhs_val = float(eq.rhs)
            try:
                evaluated_lhs = float(lhs_expr.evalf(subs=solution_dict))
            except Exception as e:
                print(f"  Erro ao avaliar R{i+1}: {e}")
                evaluated_lhs = np.nan

            print(
                f"  Restrição R{i+1}: {lhs_expr} = {evaluated_lhs:.4f} {'✅' if np.isclose(evaluated_lhs, rhs_val) else '❌'} (esperado: {rhs_val})"
            )

        z_calc = sum(
            float(objective_expr.coeff(v)) * solution_dict[str(v)]
            for v in all_vars
            if str(v).startswith("x")
        )
        print(
            f"\n🎯 Z calculado: {z_calc:.4f} | Z no quadro: {z_value:.4f} {'✅' if np.isclose(z_calc, z_value) else '❌'}"
        )

    return basic_vars, non_basic_vars, z_value, solution_dict
