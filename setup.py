from setuptools import setup, find_packages

setup(
    name="pygame_sudoku",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "sudoku = main:main"
        ]
    },
    python_requires=">=3.7",
)
