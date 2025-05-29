#!/usr/bin/env python3
"""
Setup script for ld-agent Python
Dynamic linking for agentic systems
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(req_path):
        with open(req_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return ['pydantic>=2.0.0']

setup(
    name='ld-agent',
    version='1.0.0',
    description='Dynamic linking for agentic systems in Python',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='ld-agent Team',
    author_email='team@ld-agent.dev',
    url='https://github.com/your-org/ld-agent',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.0.0',
        ],
    },
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='ai agents plugins dynamic-linking composable-ai mcp',
    entry_points={
        'console_scripts': [
            'ld-agent=ldagent.cli:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/your-org/ld-agent/issues',
        'Source': 'https://github.com/your-org/ld-agent',
        'Documentation': 'https://github.com/your-org/ld-agent/blob/main/README.md',
    },
) 
