import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mantle-firestore",
    version="0.0.1",
    author="Billcountry Mwaniki",
    author_email="me@billcountry.tech",
    description="A module allowing you to freely model your code on top of Google cloud firestore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Billcountry/mantle-model",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)