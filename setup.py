""" Setup file for 
"""
from setuptools import setup

setup(
    name='pysourcegraph',
    version="0.1dev",
    description='Pacakge to graph python source code',
    author='Renukanandan Tumu',
    author_email='renukanandan.tumu@uconn.edu',
    packages=['pysourcegraph'],
    install_requires=['graphviz']
)