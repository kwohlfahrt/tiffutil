from functools import partial, reduce
from itertools import chain, tee
from contextlib import ExitStack
import operator as op

from tifffile import TiffWriter
import numpy as np
from scipy.ndimage import morphology
import click

from .util import tiffChain, SingleTiffFile, signed


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
    function = morphology.grey_closing if invert else morphology.grey_opening
    structure, footprint = ball(radius, a.ndim)
    return function(a, structure=structure, footprint=footprint)


@click.command("smooth")
@click.argument("images", nargs=-1, type=SingleTiffFile)
@click.argument("output", type=TiffWriter)
@click.option("--radius", type=float, required=True, help="The smoothing radius")
@click.option("--invert", is_flag=True, help="Invert the image")
@click.option("--correct", is_flag=True,
              help="Subtract the background instead of saving it")
def background(images, output, radius, invert=False, correct=False):
    smooth_ = partial(smooth, radius=radius, invert=invert)

    with ExitStack() as stack:
        for tif in images:
            stack.enter_context(tif)
        dtype = reduce(np.promote_types, (s.dtype for s in chain.from_iterable(
            tif.series for tif in images
        )))
        frames = tiffChain(chain.from_iterable(tif.series for tif in images))
        frames = map(partial(np.asarray, dtype=signed(dtype)), frames)
        if correct:
            frames = tee(frames, 2)
            data = map(op.sub, frames[1], map(smooth_, frames[0]))
        else:
            data = map(smooth_, frames)

        with output:
            for frame in data:
                output.save(frame.astype(dtype))
