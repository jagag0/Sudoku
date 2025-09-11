from setuptools import setup, find_packages

setup(name="Sudoku",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pygame>=2.0.0"],
    entry_points={"console_scripts": ["sudoku = src.main:main"]},
    classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"],
    python_requires=">=3.7")
