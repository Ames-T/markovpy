from setuptools import setup, find_packages

setup(
    name="markovpy",
    version="0.2.0",
    packages=find_packages(),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.26",  # Required for matrix operations
    ],
    extras_require={
        "dev": [
            "pytest>=7.4",  # For running tests
        ],
    },
    python_requires=">=3.8",
    description="A Python library for discrete-time Markov chains",
    author="Ames T.",
    url="https://github.com/Ames-T/markovpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
