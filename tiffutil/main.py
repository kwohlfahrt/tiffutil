#!/usr/bin/env python3
import click
from importlib import import_module


@click.group()
def main(args=None):
    pass


modules = ["project", "background", "crop", "unstack", "bin", "split"]
opt_modules = ["plot"]

for module in modules:
    mod = import_module(".{}".format(module), __package__)
    main.add_command(getattr(mod, module))

for module in opt_modules:
    try:
        mod = import_module(".{}".format(module), __package__)
    except ImportError:
        continue
    main.add_command(getattr(mod, module))

if __name__ == "__main__":
    main()
