from setuptools import setup, find_packages

setup(
    name="capybara-sui-bot",
    version="0.1.0",
    packages=find_packages(include=['capybara_sui_bot', 'capybara_sui_bot.*']),
    install_requires=[
        "tweepy>=4.14.0",
        "openai>=1.0.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.0",
        "discord.py>=2.0.0",
        "python-telegram-bot>=20.0",
        "pysui>=0.80.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "websockets>=11.0.0",
        "python-dateutil>=2.8.2",
        "pytz>=2023.3",
        "tqdm>=4.65.0",
        "loguru>=0.7.0",
        "textblob==0.17.1"
    ],
    extras_require={
        'dev': [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "Sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "sphinx-autodoc-typehints>=1.23.0",
            "sphinx-multiversion>=0.2.4"
        ]
    },
    python_requires=">=3.8",
    author="IgRomanych",
    description="A Sui ecosystem-focused AI bot using the Eliza framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 