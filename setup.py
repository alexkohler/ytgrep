#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='ytgrep',
    version='0.5.0',
    description='CLI tool to search youtube captions',
    long_description=readme,
    author='Alex Kohler',
    author_email='alexjohnkohler@gmail.com',
    packages=find_packages(exclude=('test')),
    py_modules=['ytgrep'],
    entry_points={
        "console_scripts": ['ytgrep = ytgrep:main']
    },
    install_requires=[
        "colorama>=0.4.1",
        "pycaption>=1.0.1",
        "youtube-dl>=2019.4.24",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ]
)
