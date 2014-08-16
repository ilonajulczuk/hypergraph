#! /usr/bin/env python
import os
from setuptools import setup

def read(fname):
    """Utility function to read the README file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "hypergraph",
    version = "0.0.1",
    author = "Justyna Ilczuk",
    author_email = "justyna.ilczuk@gmail.com",
    description = ("Library for hypegraphs in python"),
    license = "BSD",
    keywords = "hypergraph diffusion",
    url = "http://atte.ro",
    packages=['hypergraph'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
