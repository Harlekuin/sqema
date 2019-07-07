from io import open

from setuptools import find_packages, setup

with open("sqema/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split("=")[1].strip(' \'"')
            break
    else:
        version = "0.0.1"

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

REQUIRES = ["simqle==0.3.3"]

setup(
    name="sqema",
    version=version,
    description="Ensure Database Schemas",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Tom Malkin",
    author_email="tommalkin28@gmail.com",
    maintainer="Tom Malkin",
    maintainer_email="tommalkin28@gmail.com",
    url="https://github.com/Harlekuin/sqema",
    license="MIT",

    keywords=[
        "sql",
    ],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    install_requires=REQUIRES,
    tests_require=["codecov", "behave", "coverage"],

    packages=find_packages(),
)
