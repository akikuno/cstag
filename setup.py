import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cstag",
    version="0.0.2",
    author="Akihiro Kuno",
    author_email="akuno@md.tsukuba.ac.jp",
    description="Convert cstag format from short to long, vice versa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akikuno/cstag",
    packages=setuptools.find_packages(
        where='src',
    ),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
