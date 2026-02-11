from setuptools import setup, find_packages

setup(
    name="job-apply",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer[all]>=0.9.0",
        "openai>=1.0.0",
        "anthropic>=0.18.0",
        "reportlab>=4.0.0",
        "PyYAML>=6.0",
        "playwright>=1.40.0",
        "python-docx>=1.0.0",
        "PyPDF2>=3.0.0",
        "rich>=13.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "job-apply=src.cli:app",
        ],
    },
    python_requires=">=3.10",
)
