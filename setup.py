from setuptools import setup, find_packages

setup(
    name="lp_plotter",
    version="0.1.3",
    description="Visualização gráfica de modelos de programação linear com duas variáveis",
    author="Pedro Eckel",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "numpy",
        "sympy",
    ],
    python_requires=">=3.7",
)
