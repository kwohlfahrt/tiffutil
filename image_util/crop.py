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

def cropFile(data, roi_path):
    with roi_path.open("r") as f:
        rois = map(tuple, map(reversed, map(parseROI, f)))
        yield from map(lambda roi: data[(Ellipsis,) + roi], rois)

def main(args=None):
    from argparse import ArgumentParser
    from sys import argv

    parser = ArgumentParser(description="Crop an image (sequence) based on a list of ROIs")
    parser.add_argument("image", type=Path, help="The image to read")
    parser.add_argument("rois", type=Path, help="The ROIs to extract from the image")
    parser.add_argument("--prefix", type=str, help="The prefix for the output images.")
    args = parser.parse_args(argv[1:] if args is None else args)

    output_prefix = args.prefix if args.prefix is not None else args.image.parent / args.image.stem

    image = imread(str(args.image))
    for i, view in enumerate(fromFile(image, args.rois)):
        outfile_name = "{}{}.tif".format(output_prefix, i)
        imsave(outfile_name, view)

if __name__ == "__main__":
    main()
