#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

with open('LICENSE') as f:
    license = f.read()

with open('README.md') as f:
    readme = f.read()

setup(
    name='ytgrep',
    version='0.1.0',
    description='CLI tool to search youtube captions',
    long_description=readme,
    author='Alex Kohler',
    author_email='alexjohnkohler@gmail.com',
    license=license,
    packages=find_packages(exclude=('test')),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: Apache Software License'
    ]
)
