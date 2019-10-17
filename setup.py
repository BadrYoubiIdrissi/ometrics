import setuptools

setuptools.setup(
    name="ometrics",
    version="1.0.1",
    author="Badr Youbi Idrissi",
    author_email="badryoubiidrissi@gmail.com",
    description="Metrics aggregation, dumping and loading",
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