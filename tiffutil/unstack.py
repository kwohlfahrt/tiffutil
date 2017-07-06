import click

from contextlib import ExitStack
from itertools import cycle
from functools import partial
from pathlib import Path

from tifffile import TiffWriter

from .util import SingleTiffFile

def unstack(data, nstacks):
    slices = (slice(i, None, nstacks) for i in range(nstacks))
    return (data[s] for s in slices)

@click.command()
@click.argument("image", type=SingleTiffFile)
@click.argument("outputs", type=Path)
def unstack(image, outputs):
    with image as tif, ExitStack() as output_stack:
        outfiles = [output_stack.enter_context(TiffWriter(str(path)))
                    for path in outputs]
        for outfile, page in zip(cycle(outfiles), iter(tif.pages)):
            outfile.save(page.asarray())
