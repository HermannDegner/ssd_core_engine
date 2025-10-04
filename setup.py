#!/usr/bin/env python3
"""
setup.py for SSD Core Engine
構造主観力学 汎用AIエンジンのセットアップスクリプト
"""

from setuptools import setup, find_packages
import os

# 長い説明をREADMEから読み込み
def read_long_description():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "SSD Core Engine - 構造主観力学理論の完全実装"

# バージョン情報
VERSION = "1.0.0"

# 依存関係
REQUIREMENTS = [
    "numpy>=1.20.0",
    "typing-extensions>=4.0.0",  # Python 3.8以下のサポート用
]

# 開発用依存関係
DEV_REQUIREMENTS = [
    "pytest>=6.0",
    "pytest-cov>=2.0",
    "black>=21.0",
    "flake8>=3.8",
    "mypy>=0.800",
]

# 分類子
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name="ssd-core-engine",
    version=VERSION,
    author="Hermann Degner",
    author_email="hermann.degner@example.com",  # 適切なメールアドレスに変更
    description="構造主観力学（SSD）理論の完全実装 - 汎用AIコアエンジン",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/HermannDegner/ssd_core_engine",
    project_urls={
        "Bug Reports": "https://github.com/HermannDegner/ssd_core_engine/issues",
        "Source": "https://github.com/HermannDegner/ssd_core_engine",
        "Documentation": "https://github.com/HermannDegner/ssd_core_engine/tree/main/docs",
        "Theory Repository": "https://github.com/HermannDegner/Structural-Subjectivity-Dynamics",
    },
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    python_requires=">=3.8",
    install_requires=REQUIREMENTS,
    extras_require={
        "dev": DEV_REQUIREMENTS,
        "test": ["pytest>=6.0", "pytest-cov>=2.0"],
    },
    entry_points={
        "console_scripts": [
            "ssd-demo=scripts.demo_enhanced:main",
            "ssd-check=scripts.final_check:main",
            "ssd-territory-test=scripts.detailed_territory_test:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.rst"],
    },
    zip_safe=False,
    keywords=[
        "ai", "artificial-intelligence", "cognitive-science", 
        "structural-subjectivity-dynamics", "ssd", "psychology",
        "complex-systems", "emergence", "consciousness"
    ],
    license="MIT",
)