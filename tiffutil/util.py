from itertools import chain, islice
from tifffile import TiffFile

def SingleTiffFile(*args, **kwargs):
    return TiffFile(*args, multifile=False)

def tiffChain(series, start=None, end=None):
    from tifffile.tifffile import TiffPageSeries
    from itertools import chain

    # TODO: Skip files at start which are not read
    return islice(chain.from_iterable(map(TiffPageSeries.asarray, series)), start, end)
