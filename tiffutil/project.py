from tifffile import TiffWriter
from numpy import mean, median, percentile, fmax, fmin
from enum import Enum
from multiprocessing import Pool
from itertools import chain, islice
from functools import reduce, partial
from operator import add
from contextlib import ExitStack
from pathlib import Path

import click
from .util import SingleTiffFile, tiffChain

def rollingMedian(data, width, pool=None):
    from functools import partial
    from itertools import tee, count
    from numpy import stack, median

    slices = tee(data, width)
    slices = map(lambda data, start: islice(data, start, None), slices, count())
    slices = map(stack, zip(*slices))

    if pool is None:
        return map(partial(median, axis=0), slices)
    else:
        return pool.imap(partial(median, axis=0), slices)

def multiReduce(functions, iterable):
    from functools import reduce
    from itertools import tee

    def reducer(accs, values):
        return tuple(map(lambda f, a, v: f(a, v), functions, accs, values))
    return reduce(reducer, zip(*tee(iterable, len(functions))))

def count(acc, v):
    return acc + 1

class Projection(Enum):
    mean = add
    max = fmax
    min = fmin

@click.command()
@click.argument("images", nargs=-1, type=SingleTiffFile)
@click.argument("output", type=TiffWriter)
@click.option("--projection", type=click.Choice(["mean", "max", "min"]), default="max",
              help="The projection to use")
@click.option("--filter-size", type=int, default=1,
              help="The number of frames to running-median filter")
@click.option("--start", type=int, default=None,
              help="The frame to start the projection")
@click.option("--end", type=int, default=None,
              help="The frame to end the projection")
def project(images, output, projection, filter_size, start, end):
    if not images:
        return

    functions = (count, Projection[projection].value)
    with ExitStack() as stack:
        for tif in images:
            stack.enter_context(tif)
        frames = tiffChain(chain.from_iterable(tif.series for tif in images), start, end)
        nframes, projected = multiReduce(
            functions, rollingMedian(frames, filter_size, pool=Pool())
        )

    with output:
        if projection == "mean":
            output.save((projected / nframes).astype('float32'))
        else:
            output.save(projected.astype('float32'))
