from pathlib import Path
from tifffile import imread, imsave
import click

from .main import main

def parseROI(coords):
    starts, ends = coords[::2], coords[1::2]

    r = []
    for start, end in zip(starts, ends):
        start = int(start)
        end = start + int(end[1:]) if end.startswith('+') else int(end)
        r.append(slice(int(start), end))
    return r

@main.command()
@click.argument("image", type=Path)
@click.argument("output", type=Path)
@click.argument("roi", type=str, nargs=-1)
def crop(image, output, roi):
    image = imread(str(image))
    imsave(str(output), image[(Ellipsis,) + tuple(reversed(parseROI(roi)))])
