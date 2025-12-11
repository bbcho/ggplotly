from setuptools import setup, find_packages

setup(
    name="ggplotly",
    version="0.3.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "plotly",
        "numpy",
        "scikit-learn",
        "scipy",
        "statsmodels",
    ],
    author="Ben Cho",
    description="An advanced ggplot2-like plotting system for Python built on top of Plotly",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bbcho/ggplotly",  # Add your GitHub URL here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires=">=3.6",
)
