from setuptools import setup, find_packages

setup(
    name="autofix-logs",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer",
        "python-dotenv",
        "google-genai",
        "rich",
        "pyfiglet",
        "watchdog"
    ],
    entry_points={
        "console_scripts": [
            "autofix=autofix.cli:app",
        ],
    },
)