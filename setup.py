#!/usr/bin/env python3

from setuptools import setup

setup(name="Image Utils",
      version="0.0.1",
      description="A collection of utilities for working with image stacks.",
      packages=['image_util'],
      requires=['tifffile (>=0.10.0)', 'numpy (>=1.10)'],
      entry_points={'console_scripts': ['stack_util=image_util:entry']}
)
