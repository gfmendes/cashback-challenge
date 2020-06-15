import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Cash Back Boticario",
    version="0.0.1",
    author="Guilherme Mendes",
    author_email="gmendes@gmail.com",
    description="Desafio técnico Boticário - Cash Back API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gfmendes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    test_suite="tests/unit",
)