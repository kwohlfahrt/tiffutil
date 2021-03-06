#!/usr/bin/env python3

from setuptools import setup

setup(
    name="tiffutil",
    version="0.1.2",
    description="A collection of scripts for working with .tif stacks.",
    packages=['tiffutil'],
    install_requires=[
        'tifffile (>=0.10.0)', 'numpy (>=1.10)', 'click (>= 5.0)', 'scipy (>= 0.19.0)'
    ],
    extras_require={
        'plot': ['matplotlib (>=2.0.0)'],
    },
    entry_points={'console_scripts': ['tiffutil=tiffutil.main:main']}
)
