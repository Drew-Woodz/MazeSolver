from setuptools import setup, find_packages

setup(
    name="mazegen",
    version="0.1",
    packages=find_packages(include=["mazegen", "mazegen.*"]),
    entry_points={
        "console_scripts": [
            "mazegen=mazegen.cli:main",
        ],
    },
)
