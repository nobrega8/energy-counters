"""
Setup script for nemotek-counters package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nemotek-counters",
    version="1.0.0",
    author="Nemotek",
    author_email="afonso.nobrega@nemotek.pt",
    description="A Python library for reading data from various electrical energy counters",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nemotek-GTC/contadores«",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="energy meters, counters, modbus, carlo gavazzi, lovato, schneider",
    project_urls={
        "Bug Reports": "https://github.com/Nemotek-GTC/contadores/issues",
        "Source": "https://github.com/Nemotek-GTC/contadores",
    },
)