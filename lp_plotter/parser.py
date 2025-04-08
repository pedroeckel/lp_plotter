import sympy as sp

def parse_model_from_text(model_text: str):
    try:
        lines = model_text.strip().split("\n")
        objective_line = lines[0].strip()
        constraint_lines = lines[1:]

        objective_type, expression = objective_line.split("=", 1)
        objective_type = objective_type.strip().split()[0].lower()
        objective_expr = sp.sympify(expression.strip())

        constraints = []
        for line in constraint_lines:
            if "<=" in line:
                lhs, rhs = line.split("<=")
                constraints.append((sp.sympify(lhs.strip()), "<=", float(rhs)))
            elif ">=" in line:
                lhs, rhs = line.split(">=")
                constraints.append((sp.sympify(lhs.strip()), ">=", float(rhs)))
            elif "=" in line:
                lhs, rhs = line.split("=")
                constraints.append((sp.sympify(lhs.strip()), "==", float(rhs)))
            else:
                raise ValueError(f"Restrição mal formatada: '{line}'")

        return objective_type, objective_expr, constraints
    except Exception as e:
        raise ValueError(f"Erro ao interpretar o modelo: {e}")
