import sympy as sp

def to_standard_form(model_text: str):
    # Parse inicial
    lines = model_text.strip().split("\n")
    objective_line = lines[0].strip()
    constraint_lines = lines[1:]

    # Variáveis auxiliares
    slack_count = 1
    objective_type, expression = objective_line.split("=", 1)
    objective_type = objective_type.strip().split()[0].lower()
    objective_expr = sp.sympify(expression.strip())

    constraints = []
    slack_vars = []
    variables = list(objective_expr.free_symbols)

    for line in constraint_lines:
        line = line.strip()

        # Ignora as restrições do tipo "x >= 0"
        if ">=" in line and line.strip().endswith(">= 0"):
            continue

        if "<=" in line:
            lhs, rhs = line.split("<=")
            lhs_expr = sp.sympify(lhs.strip())
            rhs_val = float(rhs.strip())

            slack_var = sp.Symbol(f"s{slack_count}")
            slack_count += 1
            slack_vars.append(slack_var)
            new_lhs = lhs_expr + slack_var
            constraints.append(sp.Eq(new_lhs, rhs_val))

        elif ">=" in line:
            lhs, rhs = line.split(">=")
            lhs_expr = sp.sympify(lhs.strip())
            rhs_val = float(rhs.strip())

            slack_var = sp.Symbol(f"s{slack_count}")
            slack_count += 1
            slack_vars.append(slack_var)
            new_lhs = lhs_expr - slack_var
            constraints.append(sp.Eq(new_lhs, rhs_val))

        elif "=" in line:
            lhs, rhs = line.split("=")
            lhs_expr = sp.sympify(lhs.strip())
            rhs_val = float(rhs.strip())
            constraints.append(sp.Eq(lhs_expr, rhs_val))

        else:
            raise ValueError(f"Restrição mal formatada: '{line}'")

    all_vars = list(set(variables + slack_vars))

    return objective_type, objective_expr, constraints, all_vars