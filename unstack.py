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
    parser.add_argument("image", type=Path, help="The image to unstack.")
    parser.add_argument("outputs", type=Path, nargs='+', help="The channel names.")

    args = parser.parse_args()

    with TiffFile(str(args.image)) as tif, ExitStack() as output_stack:
        outfiles = [output_stack.enter_context(TiffWriter(str(path))) for path in args.outputs]
        for outfile, page in zip(cycle(outfiles), iter(tif.pages)):
            outfile.save(page.asarray())

