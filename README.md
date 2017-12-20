# TIFF Utils

[![Build Status](https://travis-ci.org/kwohlfahrt/tiffutil.svg?branch=master)](https://travis-ci.org/kwohlfahrt/tiffutil)
[![codecov](https://codecov.io/gh/kwohlfahrt/tiffutil/branch/master/graph/badge.svg)](https://codecov.io/gh/kwohlfahrt/tiffutil)

A collection of useful scripts for handling .tif stacks.

# Installation

The scripts are designed to be installed with `setup.py`. Detailed instructions
can be found in the [official documentation][setuptools]. To quickly install
from the source, run:

    pip3 install --user git+https://github.com/kwohlfahrt/tiffutil.git

Add the `--upgrade` flag to update to the latest version. Plotting support must
be explicitly enabled, as this requires [matplotlib][matplotlib]:

    pip3 install --user git+https://github.com/kwohlfahrt/tiffutil.git[plot]

## Dependencies

[Python 3][python], [Numpy][numpy] and [tifffile][tifffile]. All are available
from [PyPI][pypi] and can be installed as described in
the [pip documentation][pip-install].

# Usage

The entry point `tiffutil` is installed. This should be followed by the command
to be used, e.g. `crop`, `unstack`, `smooth` or `project`. For further details,
consult the help provided for each command (e.g. `tiffutil project --help`).

Some examples are shown below.

## Unstack

This command unstacks TIFF files where multiple channels are interleaved. For
example:

    tiffutil unstack stack.tif DAPI.tif CENPA.tif

splits the file `stack.tif` into `DAPI.tif` and `CENPA.tif`, with even-numbered
(starting at 0) frames in `DAPI.tif` and odd-numbered frames in `CENPA.tif`. Any
number of output images is permitted.

## Project

This command projects multiple TIFF images into a single frame, optionally with
a running-median filter. Custom start and end frames are also possible. It only
loads the frames currently being processed, so is useful in memory-constrained
situations. For example:

    tiffutil project --projection max --end 4000 in001.tif in002.tif out.tif

projects the first 4000 frames of a video (split over two files) into `out.tif`
using a maximum intensity projection.

## Smooth

The smooth function runs a [rolling-ball][rolling-ball] smoothing pass over each
image in a stack of images. The smoothed image approximates the background. Pass
the `--correct` option to subtract the background instead of extracting it.

    tiffutil smooth --radius 2.0 in001.tif in002.tif out.tif

*Note*: 3D (or nD) smoothing would be straightforward to add, please file a bug
if this is a feature you would like.
    
[setuptools]: https://docs.python.org/3.3/install/#the-new-standard-distutils
[Python]: https://python.org
[Numpy]: https://www.numpy.org
[tifffile]: http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html
[matplotlib]: https://matplotlib.org
[pypi]: https://pypi.python.org/pypi
[pip-install]: https://pip.pypa.io/en/stable/user_guide/#installing-packages
[rolling-ball]: https://dx.doi.org/10.1109/MC.1983.1654163
