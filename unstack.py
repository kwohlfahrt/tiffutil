#!/usr/bin/env python3

from contextlib import ExitStack
from itertools import cycle
from functools import partial
from pathlib import Path

from tifffile import TiffFile, TiffWriter

def unstack(data, nstacks):
    slices = (slice(i, None, nstacks) for i in range(nstacks))
    return (data[s] for s in slices)

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Unstack a TIFF containing interleaved channels.")
    parser.add_argument("channels", type=str, nargs='+', help="The channel names.")
    parser.add_argument("image", type=Path, help="The image to unstack.")
    parser.add_argument("--prefix", type=str, nargs='?',
                        help="A prefix to add to the output. Default is the base-name of the input.")

    args = parser.parse_args()
    output_prefix = args.prefix if args.prefix is not None else args.image.parent / args.image.stem
    out_paths = map(partial('{}_{}.tif'.format, output_prefix), args.channels)

    with TiffFile(args.image.path) as tif, ExitStack() as output_stack:
        outfiles = [output_stack.enter_context(TiffWriter(path)) for path in out_paths]
        for outfile, page in zip(cycle(outfiles), iter(tif.pages)):
            outfile.save(page.asarray())

