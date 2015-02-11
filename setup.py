#!/usr/bin/env python
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

source_directory = dirname(abspath(__file__))
requirements = [l.strip() for l in open(join(source_directory, 'requirements.txt'))]

setup(
    name='checkio_cli',
    version='0.0.3',
    description='CheckiO common line interface for run and debug mission',
    author='CheckiO',
    author_email='igor@checkio.org',
    url='https://github.com/CheckiO/checkio-cli',
    download_url='https://github.com/CheckiO/checkio-cli/tarball/0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['checkio-cli = checkio_cli.cli:main'],
    },
    install_requires=requirements,
)
