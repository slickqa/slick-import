#!/usr/bin/env python

__author__ = 'Jason Corbett'

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

requirements = []
with open('requirements.txt', 'r') as reqfile:
    requirements.extend(reqfile.read().split())

setup(
    name="slickqa-slick-import",
    description="A utility that imports data into the slick test manager",
    version="1.0" + open("build.txt").read(),
    license="License :: OSI Approved :: Apache Software License",
    long_description=open('README.md').read(),
    packages=find_packages(),
    package_data={'': ['*.txt', '*.rst', '*.html']},
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': ['slick-import = slickimport.main:main',],
    },
    author="Slick Developers",
    url="http://github.com/slickqa/slick-import"
)
