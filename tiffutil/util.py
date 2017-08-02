from itertools import chain, islice
from tifffile import TiffFile

def SingleTiffFile(*args, **kwargs):
    return TiffFile(*args, multifile=False)

def atleast3D(data):
    pad_dims = (1,) * max(0, 3 - data.ndim)
    return data.reshape(pad_dims + data.shape)

def tiffChain(series, start=None, end=None):
    from tifffile.tifffile import TiffPageSeries
    from itertools import chain

    # TODO: Skip files at start which are not read
    data = map(atleast3D, map(TiffPageSeries.asarray, series))
    return islice(chain.from_iterable(data), start, end)
