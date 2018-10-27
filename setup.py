# coding: UTF-8

import os
from setuptools import setup, find_packages

with open('./README.md', 'r') as f:
    readme_str = f.read()

setup(
    name='pconst',
    version='1.0.0',
    url='https://github.com/simon-ritchie/pconst',
    author='simon-ritchie',
    author_email='antisocial.sid2@gmail.com',
    maintainer='simon-ritchie',
    maintainer_email='antisocial.sid2@gmail.com',
    description='"pconst" library provide you const-like function on Python.',
    long_description=readme_str,
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
),
