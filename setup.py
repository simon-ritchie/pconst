# coding: UTF-8

from setuptools import setup, find_packages
from pconst import __version__

with open('./README.md', 'r') as f:
    readme_str = f.read()

setup(
    name='pconst',
    version=__version__,
    url='https://github.com/simon-ritchie/pconst',
    author='simon-ritchie',
    maintainer='simon-ritchie',
    maintainer_email='antisocial.sid2@gmail.com',
    description='"pconst" library provide you const-like function on Python.',
    long_description=(
        '"pconst" library provide you const-like function on Python.'
        '\n\nFor more details, please see GitHub repository: '
        'https://github.com/simon-ritchie/pconst'
    ),
    packages=find_packages(),
    install_requires=[],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
    ],
),
