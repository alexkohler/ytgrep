#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='ytgrep',
    version='0.4.8',
    description='CLI tool to search youtube captions',
    long_description=readme,
    author='Alex Kohler',
    author_email='alexjohnkohler@gmail.com',
    packages=find_packages(exclude=('test')),
    py_modules=['ytgrep'],
    entry_points={
        "console_scripts": ['ytgrep = ytgrep:main']
    },
    install_requires=required,
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ]
)
