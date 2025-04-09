
# LPKit 📊

[![PyPI](https://img.shields.io/pypi/v/lpkit.svg)](https://pypi.org/project/lpkit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**LPKit** é uma biblioteca Python para visualização e resolução de modelos de Programação Linear.

Ideal para fins didáticos, acadêmicos ou aplicações simples com:

✅ Região factível (método gráfico)  
✅ Vetor gradiente e curvas de nível  
✅ Método Simplex  
✅ Ponto ótimo e valor da função objetivo  

---

## ✨ Instalação

```bash
pip install lpkit
```

Ou para desenvolvimento local:

```bash
git clone https://github.com/pedroeckel/lpkit.git
cd lpkit
pip install -e .
```

---

## 🚀 Exemplo de uso: método gráfico e Simplex

```python
from lpkit import solve_with_graphics

model_text = '''
Max Z = 5*x1 + 2*x2
x1 <= 3
x2 <= 4
x1 + 2*x2 <= 9
x1 - 2*x2 <= 2
x1 >= 0
x2 >= 0
'''

solve_with_graphics(model_text, verbose={
    "show_gradient": True,
    "show_level_curves": True,
    "show_objective_value": True,
    "show_vertex_points": True,
    "show_optimal_point": True
})
```

---

## 🧠 Exemplo de uso: método Simplex

```python
from lpkit import solve_with_simplex

model_text = '''
Max Z = 5*x1 + 2*x2
x1 <= 3
x2 <= 4
x1 + 2*x2 <= 9
x1 - 2*x2 <= 2
x1 >= 0
x2 >= 0
'''

solve_with_simplex(model_text, verbose={
    "simplex_tableau": True,
    "entering_leaving": True,
    "pivot": True,
    "basic_vars": True,
    "constraints_validation": True,
    "z_per_iteration": True,
    "history_summary": True
})
```
---

## 📄 Licença

Distribuído sob a [Licença MIT](LICENSE).

---

## 🤝 Contribuindo

Pull requests são bem-vindos!  
Se quiser sugerir melhorias ou reportar bugs, abra uma issue.
