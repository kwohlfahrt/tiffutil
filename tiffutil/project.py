#!/usr/bin/env python3

from tifffile import TiffFile, TiffWriter
from numpy import mean, median, percentile, fmax, fmin
from enum import Enum
from multiprocessing import Pool
from itertools import chain
from functools import reduce, partial
from operator import add
from contextlib import ExitStack
from pathlib import Path

def rollingMedian(data, width, pool=None):
    from functools import partial
    from itertools import tee, islice, count
    from numpy import stack, median

    slices = tee(data, width)
    slices = map(lambda data, start: islice(data, start, None), slices, count())
    slices = map(stack, zip(*slices))

    if pool is None:
        return map(partial(median, axis=0), slices)
    else:
        return pool.imap(partial(median, axis=0), slices)

def tiffChain(series):
    from tifffile.tifffile import TiffPageSeries
    from itertools import chain

    return chain.from_iterable(map(TiffPageSeries.asarray, series))

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

def main(args=None):
    from argparse import ArgumentParser
    from sys import argv

    parser = ArgumentParser(description="Various projections of TIFFs")
    parser.add_argument("images", nargs='+', type=partial(TiffFile, multifile=False),
                        help="The image(s) to project")
    parser.add_argument("output", type=TiffWriter, help="The output filename")
    parser.add_argument("--projection", type=str,
                        choices={"mean", "max", "min"}, default="max",
                        help="The projection to use.")
    parser.add_argument("--filter-size", type=int, default=1,
                        help="The number of frames to running-median filter")
    args = parser.parse_args(argv[1:] if args is None else args)

    functions = (count, Projection[args.projection].value)
    with ExitStack() as stack:
        for tif in args.images:
            stack.enter_context(tif)
        frames = tiffChain(chain.from_iterable(tif.series for tif in args.images))
        nframes, projection = multiReduce(
            functions, rollingMedian(frames, args.filter_size, pool=Pool())
        )

    with args.output:
        if args.projection == "mean":
            args.output.save((projection / nframes).astype('float32'))
        else:
            args.output.save(projection.astype('float32'))

if __name__ == "__main__":
    main()
