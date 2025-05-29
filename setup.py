#!/usr/bin/env python3
"""
Setup script for ld-agent Python.
Dynamic linking for agentic systems.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ld-agent",
    version="1.0.0",
    author="ld-agent Team",
    description="Dynamic linking for agentic systems in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ld-agent",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pydantic>=2.0.0",
        "python-dotenv",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "mcp": [
            "fastmcp",
        ],
        "ai": [
            "pydantic-ai",
        ],
    },
    entry_points={
        "console_scripts": [
            "ld-agent=ldagent.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Software Distribution",
    ],
    keywords="ld-agent dynamic-linking ai agents plugins composable-ai mcp",
    project_urls={
        "Bug Reports": "https://github.com/your-org/ld-agent/issues",
        "Source": "https://github.com/your-org/ld-agent",
        "Documentation": "https://github.com/your-org/ld-agent/blob/main/README.md",
    },
    include_package_data=True,
) 
