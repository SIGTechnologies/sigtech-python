from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="sigtech",
    version="0.1",
    description="SigTech API Python Interface",
    author="SigTech",
    author_email="support@sigtech.com",
    url="https://github.com/SIGTechnologies/sigtech-python",
    download_url="https://github.com/SIGTechnologies/sigtech-python",
    keywords=["SIGTECH", "FINANCE", "TRADING", "BACKTEST", "QUANT"],
    license='MIT',
    python_requires=">=3.6.0",
    install_requires=[
        "requests",
        "pandas",
        "tqdm"
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-mock'
        ],
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    include_package_data=True,

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
