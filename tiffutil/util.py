from itertools import chain, islice
from tifffile import TiffFile
from tifffile.tifffile import TiffPage

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
