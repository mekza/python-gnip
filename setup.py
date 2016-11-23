# coding=utf-8
from setuptools import find_packages
from setuptools import setup

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name="python-gnip",
    version="0.0.2",
    description="Gnip Powertrack Wrapper",
    long_description=long_description,
    author="Bright SAS",
    author_email="oss@brig.ht",
    license="MIT License",
    url="https://github.com/bright/python-bright/",
    keywords="gnip data twitter",
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests>=2.10.0'],
    zip_safe=False
)
