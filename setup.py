"""Setup script for the trading bot."""
from setuptools import setup, find_packages

setup(
    name="information-markets-bot",
    version="0.1.0",
    description="Trading bot for Kalshi and Polymarket prediction markets",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "python-dotenv>=1.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.14.0",
        "scipy>=1.10.0",
        "beautifulsoup4>=4.12.0",
        "praw>=7.7.0",
        "sqlalchemy>=2.0.0",
        "aiohttp>=3.8.0",
        "python-dateutil>=2.8.0",
        "pytz>=2023.3",
        "tqdm>=4.65.0",
    ],
    python_requires=">=3.8",
)

