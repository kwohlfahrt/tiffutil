from itertools import chain, islice, zip_longest
from tifffile import TiffFile
from tifffile.tifffile import TiffPage
from numpy import dtype
import numpy as np
import operator as op
from functools import partial

def SingleTiffFile(*args, **kwargs):
    return TiffFile(*args, multifile=False)

def atleast3D(data):
    pad_dims = (1,) * max(0, 3 - data.ndim)
    return data.reshape(pad_dims + data.shape)

def tiffChain(series, start=None, end=None):
    from tifffile.tifffile import TiffPageSeries
    from itertools import chain

    # TODO: Skip files at start which are not read
    pages = map(TiffPage.asarray, chain.from_iterable(s.pages for s in series))
    # Fix ImageJ sometimes storing 3D data in one page
    pages = chain.from_iterable(map(atleast3D, pages))
    return islice(pages, start, end)

def signed(dt):
    if dt.kind in {'i', 'f'}:
        return dt
    elif dt.kind == 'u':
        size = min(dt.itemsize * 8 * 2, 64)
        return dtype('int{}'.format(size))
    else:
        raise ValueError("Expected an integer dtype, not {}".format(dt))

def chunk(data, width):
    chunks = zip_longest(*([iter(data)] * width))
    yield from map(partial(filter, partial(op.is_not, None)), chunks)
