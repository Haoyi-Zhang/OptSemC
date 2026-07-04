from setuptools import setup

setup(
    name="optsemc",
    version="0.0.0",
    description="Public optimizer-contract semantics, probes, and reproducibility checks.",
    packages=["optsemc"],
    package_dir={"optsemc": "optsemc"},
    python_requires=">=3.10",
    install_requires=["PyYAML>=6.0"],
    extras_require={
        "paper": ["pypdf>=4.0"],
        "realengines": ["duckdb>=1.0.0", "psycopg[binary]>=3.1"],
    },
    entry_points={"console_scripts": ["optsemc=optsemc.cli:main"]},
)
