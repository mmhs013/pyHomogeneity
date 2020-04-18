#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import versioneer

__author__ = "Md. Manjurul Hussain Shourov"
__version__ = versioneer.get_version()
__email__ = "mmhs013@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright Md. Manjurul Hussain Shourov (2020)"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "pyhomogeneity",
    version = __version__,
    author = __author__,
    author_email = __email__,
    description = ("A python package for homogeneity test."),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/mmhs013/pyhomogeneity",
    packages = ["pyhomogeneity"],
    license = __license__,
    install_requires = ["numpy", "scipy"],
    classifiers = [
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
		"Intended Audience :: Science/Research",
		"Operating System :: OS Independent",
		"Topic :: Scientific/Engineering",
		"Development Status :: 5 - Production/Stable"
    ]
)