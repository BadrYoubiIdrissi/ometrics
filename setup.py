import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ometrics",
    version="0.0.1",
    author="Badr Youbi Idrissi",
    author_email="badryoubiidrissi@gmail.com",
    description="Metrics aggregation, dumping and loading",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/badryoubiidrissi/ometrics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)