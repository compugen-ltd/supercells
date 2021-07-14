#!/usr/bin/env python
"""
supercells - only the finest of cells
"""
from .version import __version__
import sys
import argparse
from .modules.cellranger import CellRanger


def get_argument_parser():
    desc = "supercells: Easily assess quality control data across multiple single cell datasets"
    parser = argparse.ArgumentParser(description=desc, add_help=True)
    parser.add_argument("--version", "-v", action="version", version=__version__)
    parser.add_argument(
        "--input",
        "-i",
        metavar="DIRECTORY",
        required=True,
        help=("Enter the location of the input files"),
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="DIRECTORY",
        required=False,
        default="./",
        help=("Specify the location of the output files, defualt is current wd"),
    )
    return parser


def main():
    """main function that runs supercells"""
    p = get_argument_parser()
    args = p.parse_args()
    CellRanger(args)
    success = True
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
