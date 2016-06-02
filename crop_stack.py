#!/usr/bin/env python3

from pathlib import Path
from tifffile import imread, imsave

def parseROI(roi):
    coords = roi.split(",")
    starts, ends = coords[::2], coords[1::2]

    r = ()
    for start, end in zip(starts, ends):
        start = int(start)
        end = start + int(end[1:]) if end.startswith('+') else int(end)
        r = r + (slice(int(start), end),)
    return r

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Crop an image (sequence) based on a list of ROIs")
    parser.add_argument("image", type=Path, help="The image to read")
    parser.add_argument("rois", type=Path, help="The ROIs to extract from the image")
    parser.add_argument("--prefix", type=str, help="The prefix for the output images.")
    args = parser.parse_args()

    output_prefix = args.prefix if args.prefix is not None else args.image.parent / args.image.stem

    image = imread(str(args.image))
    with args.rois.open("r") as f:
        rois = map(tuple, map(reversed, map(parseROI, f)))
        views = map(lambda roi: image[(Ellipsis,) + roi], rois)
        for i, view in enumerate(views):
            outfile_name = "{}{}.tif".format(output_prefix, i)
            imsave(outfile_name, view)
