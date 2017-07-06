import click
from tifffile import TiffWriter
from itertools import chain

from .util import SingleTiffFile, tiffChain

def iterBin(data, width, pool=None):
    from functools import partial
    from itertools import tee, islice, count
    from numpy import stack, sum as asum

    slices = tee(data, width)
    slices = map(lambda data, start: islice(data, start, None, width), slices, count())
    slices = map(stack, zip(*slices))

    func = partial(asum, axis=0, dtype='uint32')
    return map(func, slices) if pool is None else pool.imap(func, slices)

@click.command()
@click.argument("images", nargs=-1, type=SingleTiffFile)
@click.argument("outfile", type=TiffWriter)
@click.option("-n", type=int, required=True)
def bin(images, outfile, n):
    from contextlib import ExitStack

    with ExitStack() as stack, outfile as outfile:
        for tif in images: stack.enter_context(tif)
        frames = tiffChain(chain.from_iterable(tif.series for tif in images))
        for frame in iterBin(frames, n):
            outfile.save(frame)
