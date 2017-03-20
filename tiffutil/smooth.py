#!/usr/bin/env python3

from functools import partial
from itertools import chain, tee
from contextlib import ExitStack
import operator as op

import numpy as np
from scipy.ndimage import morphology
from .project import tiffChain

def ball(r, ndim):
    return ellipse((r,) * (ndim + 1))

def ellipse(rs):
    from functools import reduce
    from operator import sub

    z, *rs = rs
    rs = np.asarray(rs)
    size = np.ceil(2 * rs)
    xs = np.ogrid[tuple(map(slice, -size/2, size/2, size * 1j))]
    xs = map(lambda x, r: np.power(x, 2) / r, xs, rs ** 2)
    ys = np.sqrt((reduce(sub, xs, 1) * z ** 2).clip(0))
    return ys - ys.max(), ys > 0

def smooth(a, radius, invert=False):
    if radius <= 1.0:
        raise ValueError("Radius must be > 1.0") # due to scipy bug #7202
    function = morphology.grey_closing if invert else morphology.grey_opening
    structure, footprint = ball(radius, a.ndim)
    return function(a, structure=structure, footprint=footprint)

def main(args=None):
    from sys import argv
    from argparse import ArgumentParser
    from tifffile import TiffFile, TiffWriter

    parser = ArgumentParser(description="Smooth an image using the rolling-ball method")
    parser.add_argument("images", nargs='+', type=partial(TiffFile, multifile=False),
                        help="The images to smooth")
    parser.add_argument("output", type=TiffWriter, help="The output filename")
    parser.add_argument("--radius", type=float, required=True, help="The smoothing radius")
    parser.add_argument("--invert", action="store_true", help="Invert the image")
    parser.add_argument("--correct", action="store_true",
                        help="Subtract the background instead of saving it")
    args = parser.parse_args(argv[1:] if args is None else args)

    smooth_ = partial(smooth, radius=args.radius, invert=args.invert)

    with ExitStack() as stack:
        for tif in args.images:
            stack.enter_context(tif)
        frames = tiffChain(chain.from_iterable(tif.series for tif in args.images))
        if args.correct:
            frames = tee(frames, 2)
            output = map(op.sub, frames[1], map(smooth_, frames[0]))
        else:
            output = map(smooth_, frames)

        with args.output:
            for frame in output:
                args.output.save(frame)

if __name__ == "__main__":
    main()
