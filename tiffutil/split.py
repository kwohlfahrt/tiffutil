import click
from tifffile import TiffWriter
from itertools import chain

from .util import SingleTiffFile, tiffChain, chunk

@click.command()
@click.argument("images", nargs=-1, type=SingleTiffFile)
@click.argument("outfile", type=str)
@click.option("-n", type=int, required=True)
def split(images, outfile, n):
    """Splits input images into chunks, writing them to the output with '{}'
    replaced by the split number.

    For example, 'split -n 30 in.tif "out.{}.tif"' will produce files labelled
    out.0.tif, out.1.tif, ... until the input has been completely split.
    """

    from contextlib import ExitStack

    with ExitStack() as stack:
        for tif in images: stack.enter_context(tif)
        frames = tiffChain(chain.from_iterable(tif.series for tif in images))
        for i, c in enumerate(chunk(frames, n)):
            with TiffWriter(outfile.format(i)) as writer:
                for frame in c:
                    writer.save(frame)
