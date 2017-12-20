import click
import numpy as np

from contextlib import ExitStack
from itertools import cycle

from tifffile import TiffWriter

from .util import SingleTiffFile


@click.command()
@click.argument("image", type=SingleTiffFile)
@click.argument("outputs", type=TiffWriter, nargs=-1)
@click.option("--axis", type=int, default=0)
@click.option("--series", type=int, default=0)
def unstack(image, outputs, axis=0, series=0):
    with image as tif, ExitStack() as output_stack:
        outfiles = [output_stack.enter_context(output) for output in outputs]
        series = tif.series[series]

        pages = np.asarray(series.pages).reshape(series.shape[:-2]).T
        pages = np.rollaxis(pages, axis)

        for outfile, page in zip(cycle(outfiles), pages.ravel()):
            outfile.save(page.asarray())
