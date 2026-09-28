from setuptools import setup, find_packages

setup(
    name="llm-cache",
    version="0.1.0",
    packages=find_packages(),
    author="Your Name",
    description="A high-speed SQLite caching SDK to eliminate redundant LLM API calls and optimize costs.",
    python_requires=">=3.12",
)
