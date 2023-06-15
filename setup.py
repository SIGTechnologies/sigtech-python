from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="sigtech",
    version="0.1",
    description="SigTech API Python Interface",
    author="SigTech",
    # author_email="",
    # url="",
    # keywords=["SigTech"],
    # license='UNLICENSED',
    python_requires=">=3.6.0",
    install_requires=[
        "pytz",
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
        "Operating System :: OS Independent",
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
