from setuptools import setup, find_packages

setup(
    name="lpkit",
    version="0.1.4",
    description="Ferramentas para visualização e resolução de modelos de Programação Linear.",
    author="Pedro Eckel",
    author_email="pedroeckel@ufpr.br",
    url="https://github.com/pedroeckel/lpkit",
    packages=find_packages(),
    install_requires=[
        "sympy",
        "matplotlib",
        "numpy",
        "pandas",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
