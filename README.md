# LP Plotter 📊

[![PyPI](https://img.shields.io/pypi/v/lp_plotter.svg)](https://pypi.org/project/lp_plotter/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**LP Plotter** é uma biblioteca Python para visualização gráfica de modelos de Programação Linear com duas variáveis.

Ideal para fins didáticos e demonstrações com:

✅ Região factível  
✅ Vetor gradiente  
✅ Curvas de nível  
✅ Ponto ótimo e valor da função objetivo

---

## ✨ Instalação

```bash
pip install lp_plotter
```

Ou para desenvolvimento local:

```bash
git clone https://github.com/pedroeckel/lp_plotter.git
cd lp_plotter
pip install -e .
```

---

## 🚀 Exemplo de uso

```python
from lp_plotter import parse_model_from_text, plot_linear_program

model_text = '''
Max Z = 5*x1 + 2*x2
x1 <= 3
x2 <= 4
x1 + 2*x2 <= 9
x1 - 2*x2 <= 2
x1 >= 0
x2 >= 0
'''

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
```

---

## ⚙️ Parâmetros opcionais

Todos os parâmetros abaixo são opcionais e têm `True` como padrão:

| Parâmetro               | Descrição                                            |
|------------------------|-------------------------------------------------------|
| `show_gradient`        | Exibe a seta do vetor gradiente                       |
| `show_level_curves`    | Exibe as curvas de nível da função objetivo           |
| `show_objective_value` | Mostra o valor de Z no ponto ótimo                    |
| `show_vertex_points`   | Marca todos os vértices da região viável              |
| `show_optimal_point`   | Mostra o ponto ótimo no gráfico                       |

---

## 📄 Licença

Distribuído sob a [Licença MIT](LICENSE).

---

## 🤝 Contribuindo

Pull requests são bem-vindos!  
Se quiser sugerir melhorias ou reportar bugs, abra uma issue.
