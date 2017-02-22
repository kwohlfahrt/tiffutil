#!/usr/bin/env python3

from setuptools import setup

setup(name="TIFF Stack Utils",
      version="0.0.1",
      description="A collection of scripts for working with .tif stacks.",
      packages=['tiffutil'],
      requires=['tifffile (>=0.10.0)', 'numpy (>=1.10)'],
      entry_points={'console_scripts': ['tiffutil=tiffutil:entry']}
)
