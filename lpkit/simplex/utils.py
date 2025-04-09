import numpy as np
import pandas as pd

def display_tableau(tableau, all_vars, entering_index=None, title="Quadro Simplex Atual:", verbose=True):
    if not verbose:
        return

    columns = [str(v) for v in all_vars] + ["Z"]
    df = pd.DataFrame(tableau, columns=columns)
    df.index = ["L0"] + [f"L{i+1}" for i in range(len(df) - 1)]

    show_block = False
    bloqueios = [np.nan]

    if entering_index is not None:
        col = tableau[1:, entering_index]
        b = tableau[1:, -1]
        for i in range(len(col)):
            if col[i] > 0:
                bloqueios.append(b[i] / col[i])
                show_block = True
            else:
                bloqueios.append(np.nan)
    else:
        bloqueios += [np.nan] * (len(df) - 1)

    if show_block:
        df["B"] = bloqueios

    print(f"\n📊 {title}")
    print(df)

def build_simplex_table(objective_expr, constraints, variables, verbose=True):
    decision_vars = sorted([v for v in variables if str(v).startswith("x")], key=lambda x: str(x))
    slack_vars = sorted([v for v in variables if str(v).startswith("s")], key=lambda x: str(x))
    all_vars = decision_vars + slack_vars

    A = []
    b = []
    for eq in constraints:
        row = [eq.lhs.coeff(v) for v in all_vars]
        A.append(row)
        b.append(eq.rhs)

    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array([-objective_expr.coeff(v) for v in all_vars], dtype=float)

    tableau = np.hstack([A, b.reshape(-1, 1)])
    objective_row = np.hstack([c, [0]])
    tableau = np.vstack([objective_row, tableau])

    display_tableau(tableau, all_vars, entering_index=None, title="Quadro Simplex Inicial", verbose=verbose)
    return tableau, all_vars

def get_entering_variable(tableau, all_vars, verbose=True):
    objective_row = tableau[0, :-1]
    min_value = np.min(objective_row)

    if min_value >= 0:
        if verbose:
            print("\n✅ Todos os coeficientes da função objetivo são >= 0. A solução atual é ótima.")
        return None, None

    col_index = np.argmin(objective_row)
    entering_var = all_vars[col_index]

    if verbose:
        print(f"\n1º Passo: Variável que entra na base: {entering_var} (coeficiente: {min_value})")
    return entering_var, col_index

def get_leaving_variable(tableau, entering_index, verbose=True):
    b_column = tableau[1:, -1]
    col = tableau[1:, entering_index]

    ratios = []
    for i in range(len(col)):
        if col[i] > 0:
            ratio = b_column[i] / col[i]
            ratios.append(ratio)
        else:
            ratios.append(np.inf)

    min_ratio = np.min(ratios)
    if min_ratio == np.inf:
        if verbose:
            print("\n❌ Nenhuma razão válida encontrada: solução ilimitada.")
        return None

    row_index = np.argmin(ratios) + 1
    if verbose:
        print(f"2º Passo: Variável que sai da base está na linha R{row_index} (razão mínima: {min_ratio:.4f})")
    return row_index

def pivot_tableau(tableau, pivot_row, pivot_col, verbose=True):
    if verbose:
        print(f"\n🔄 Pivotamento: Linha pivô = R{pivot_row}, Coluna pivô = {pivot_col}")

    new_tableau = tableau.copy().astype(float)
    pivot_element = new_tableau[pivot_row, pivot_col]
    if np.isclose(pivot_element, 0.0):
        raise ValueError("Elemento pivô é zero — impossível pivotar.")

    new_tableau[pivot_row, :] = new_tableau[pivot_row, :] / pivot_element

    for i in range(len(new_tableau)):
        if i != pivot_row:
            factor = new_tableau[i, pivot_col]
            new_tableau[i, :] -= factor * new_tableau[pivot_row, :]

    return new_tableau
