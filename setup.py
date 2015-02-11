#!/usr/bin/env python

from distutils.core import setup

setup(
    name='CheckiO-cli',
    version='1.0',
    description='CheckiO common line interface for run and debug mission',
    author='CheckiO',
    author_email='igor@checkio.org',
    entry_points={
        'console_scripts': ['checkio-cli = checkio_cli.cli:main'],
    },
    install_requires=[
        'GitPython==0.3.5',
        'docker-py==0.7.0',
        'tornado==4.0.2',
        'coloredlogs',
        'future',
    ],
)
