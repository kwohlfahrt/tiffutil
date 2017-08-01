#!/usr/bin/env python3

from setuptools import setup

setup(name="TIFF Stack Utils",
      version="0.0.5",
      description="A collection of scripts for working with .tif stacks.",
      packages=['tiffutil'],
      requires=['tifffile (>=0.10.0)', 'numpy (>=1.10)', 'click (>= 5.0)'],
      entry_points={'console_scripts': ['tiffutil=tiffutil:entry']}
)
