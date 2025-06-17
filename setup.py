from setuptools import setup, find_packages

setup(
    name="leaksmith",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "typer",
        "weasyprint",
        "pillow",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "leaksmith=core.cli:app",
        ],
    },
) 