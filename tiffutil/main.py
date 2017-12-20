#!/usr/bin/env python3
import click


@click.group()
def main(args=None):
    pass


from .project import project  # noqa: E402
main.add_command(project)
from .smooth import run_smooth  # noqa: E402
main.add_command(run_smooth)
from .crop import crop  # noqa: E402
main.add_command(crop)
from .unstack import unstack  # noqa: E402
main.add_command(unstack)
from .bin import bin  # noqa: E402
main.add_command(bin)
try:
    from .plot import plot  # noqa: E402
except ImportError:
    pass
else:
    main.add_command(plot)
from .split import split  # noqa: E402
main.add_command(split)

if __name__ == "__main__":
    main()
