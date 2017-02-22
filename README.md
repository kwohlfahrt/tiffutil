# TIFF Utils

A collection of useful scripts for handling .tif stacks.

# Installation

The scripts are designed to be installed with `setup.py`. Detailed instructions
can be found in the [official documentation][setuptools].

## Dependencies

[Python 3][python], [Numpy][numpy] and [tifffile][tifffile]. All are available
from [PyPI][pypi] and can be installed as described in
the [pip documentation][pip-install].

# Usage

The entry point `tiffutil` is installed. This should be followed by the command
to be used, e.g. `crop`, `unstack` or `project`. For further details, consult
the help provided for each command:

    tiffutil unstack --help
    
[setuptools]: https://docs.python.org/3.3/install/#the-new-standard-distutils
[Python]: https://python.org
[Numpy]: https://www.numpy.org
[tifffile]: http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html
[pypi]: https://pypi.python.org/pypi
[pip-install]: https://pip.pypa.io/en/stable/user_guide/#installing-packages
