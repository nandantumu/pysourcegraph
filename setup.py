"""
This module exists to facilitate installation.
"""
import os
from setuptools import setup

def read(fname):
    """
    Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pysourcegraph",
    version="0.0.4",
    author="Nandan Tumu",
    author_email="renukanandan.tumu@uconn.edu",
    description=("A package designed to make large python codebases easier to"
                 "understand by making structure easily visible"),
    license="CC BY-NC-SA 4.0",
    keywords="structure, sourcecode, graphing, visualization, modules",
    url="http://github.com/nandantumu/pysourcegraph",
    packages=['pysourcegraph'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: Free for non-commercial use",
    ],
)
