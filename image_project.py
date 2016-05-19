#!/usr/bin/env python3

from tifffile import TiffFile, imsave
from numpy import mean, median, percentile, amax, amin

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Various projections of TIFFs")
    parser.add_argument("image", type=str, help="The image to project")
    parser.add_argument("output", type=str, help="The output filename")
    parser.add_argument("--projection", type=str,
                        choices={"mean", "max", "min", "median", "quartile"}, default="max",
                        help="The projection to use.")

    args = parser.parse_args()
    # Could modify to minimize memory use later
    with TiffFile(args.image) as tif:
        data = tif.asarray(memmap=True)

    if args.projection == 'mean':
        data = mean(data, axis=0)
    elif args.projection == 'median':
        data = median(data, axis=0, overwrite_input=True)
    elif args.projection == 'quartile':
        data = percentile(data, 25.0, axis=0, overwrite_input=True)
    elif args.projection == 'max':
        data = amax(data, axis=0)
    elif args.projection == 'min':
        data = amin(data, axis=0)
    else:
        # Should never happen
        raise ValueError("Invalid projection method.")

    imsave(args.output, data.astype('float32'))
