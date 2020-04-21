import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utaromkan", # Replace with your own username
    version="1.0.0",
    author="Tart",
    author_email="conemusicproductions@gmail.com",
    description="hiragana <-> romaji conversion for utau",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Danalog/utaromkan",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)