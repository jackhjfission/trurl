from setuptools import find_packages, setup

setup(
    name="trurl",
    version="v0.1.2",
    packages=find_packages(
        include=["trurl*"],
        exclude=["trurl.tests"],
    ),
    entry_points={
        "console_scripts": [
            "trurl = trurl.cli:main",
        ]
    },
    python_requires=">=3.7",
    install_requires=[
        "click==8.*",
    ],
    description="Another python package for traceable and reproducible data science.",
    author="Jack Coggins",
    author_email="jackhjfission@gmail.com",
    url="https://github.com/jackhjfission/trurl",
    license_files="LICENSE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
