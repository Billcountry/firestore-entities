import setuptools


install_requires = ["google-cloud-firestore"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mantle-firestore",
    version="0.0.6",
    author="Billcountry Mwaniki",
    author_email="me@billcountry.tech",
    description="Implementation of entities concept on top of Google cloud firestore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mantle-studio/models",
    packages=['mantle', 'mantle.firestore'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires
)
