#!/usr/bin/env python3
import click

@click.group()
def main(args=None):
    pass

from .project import project
main.add_command(project)
from .smooth import run_smooth
main.add_command(run_smooth)
from .crop import crop
main.add_command(crop)
from .unstack import unstack
main.add_command(unstack)
from .bin import bin
main.add_command(bin)
from .plot import plot
main.add_command(plot)
from .split import split
main.add_command(split)

if __name__ == "__main__":
    main()
