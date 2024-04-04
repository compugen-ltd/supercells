#!/usr/bin/env python
"""
supercells - only the finest of cells
"""
from pathlib import Path
import argparse

from supercells.version import __version__
from supercells.modules.cellranger import CellRanger


def get_argument_parser():
    desc = "supercells: Easily assess quality control data across multiple single cell datasets"
    parser = argparse.ArgumentParser(description=desc, add_help=True)
    parser.add_argument("--version", "-v", action="version", version=__version__)
    parser.add_argument(
        "--input",
        "-i",
        dest="inpath",
        required=True,
        help="Enter the location of the input files",
    )
    parser.add_argument(
        "--output",
        "-o",
        dest="output",
        required=False,
        default=Path("."),
        help="Specify the location of the output files, default is current wd",
    )
    parser.add_argument(
        "--cutoff-dict",
        "-c",
        default=None,
        dest="cutoff_dict",
        required=False
    )
    return parser


def main():
    """main function that runs supercells"""
    p = get_argument_parser()
    args = p.parse_args()
    CellRanger(**args.__dict__).run()


if __name__ == "__main__":
    main()
