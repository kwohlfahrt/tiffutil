import numpy as np
import matplotlib

from pathlib import Path
import click
from .util import SingleTiffFile


def normalize(a):
    return (a - a.min()) / (a.max() - a.min())


@click.command()
@click.option("--channel", type=(float, float, float, SingleTiffFile), multiple=True)
@click.option("--scalebar", type=(float, str, int))
@click.option("--output", type=Path)
@click.option("--figsize", type=(float, float), default=(8.0, 8.0))
def plot(channel, scalebar=None, output=None, figsize=(8.0, 8.0)):
    from mpl_toolkits.axes_grid.anchored_artists import AnchoredAuxTransformBox
    from matplotlib.text import Text
    from matplotlib.text import Line2D

    if output is not None:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    images = []
    for *ch, tif in channel:
        with tif:
            img = normalize(tif.asarray())[:, :, None] * np.array(ch)[None, None, :]
        images.append(img)

    fig, ax = plt.subplots(1, 1, figsize=figsize, sharex=True, sharey=True)
    ax.imshow(normalize(sum(images)))
    ax.set_xticks([])
    ax.set_yticks([])

    if scalebar is not None:
        pixel, units, length = scalebar

        box = AnchoredAuxTransformBox(ax.transData, loc=4)
        box.patch.set_alpha(0.8)
        bar = Line2D([-length/pixel/2, length/pixel/2], [0.0, 0.0], color='black')
        box.drawing_area.add_artist(bar)
        label = Text(
            0.0, 0.0, "{} {}".format(length, units),
            horizontalalignment="center", verticalalignment="bottom"
        )
        box.drawing_area.add_artist(label)
        ax.add_artist(box)

    if output is None:
        plt.show()
    else:
        fig.tight_layout()
        fig.savefig(str(output))
