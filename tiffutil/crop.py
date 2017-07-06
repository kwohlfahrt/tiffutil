from pathlib import Path
from tifffile import imread, imsave
import click

from .main import main

def parseROI(roi):
    coords = roi.split(",")
    starts, ends = coords[::2], coords[1::2]

    r = ()
    for start, end in zip(starts, ends):
        start = int(start)
        end = start + int(end[1:]) if end.startswith('+') else int(end)
        r = r + (slice(int(start), end),)
    return r

def cropFile(data, roi_path):
    with roi_path.open("r") as f:
        rois = map(tuple, map(reversed, map(parseROI, f)))
        yield from map(lambda roi: data[(Ellipsis,) + roi], rois)

@main.command()
@click.argument("image", type=Path)
@click.argument("rois", type=Path)
@click.option("--prefix", type=str, help="The prefix for the output images.")
def crop(image, rois, prefix):
    output_prefix = (prefix if prefix is not None else image.parent / image.stem)

    image = imread(str(image))
    for i, view in enumerate(cropFile(image, rois)):
        outfile_name = "{}{}.tif".format(output_prefix, i)
        imsave(outfile_name, view)
