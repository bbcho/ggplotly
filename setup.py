from setuptools import setup, find_packages

setup(
    name="ggplotly",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "plotly",
        "numpy",
        "scikit-learn",
        "scipy",
    ],
    author="Ben Cho",
    description="An advanced ggplot2-like plotting system for Python built on top of Plotly",
)
