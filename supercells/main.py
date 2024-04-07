#!/usr/bin/env python
"""
supercells - only the finest of cells
"""
from pathlib import Path
import argparse

from supercells.modules.general import read_and_check_cutoff_dict
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
        dest="outpath",
        required=False,
        default=Path("."),
        help="Specify the location of the output files, default is current wd",
    )
    parser.add_argument(
        "--cutoff-dict",
        "-c",
        default=None,
        dest="cutoff_dict_path",
        required=False
    )
    return parser


def main():
    """main function that runs supercells"""
    p = get_argument_parser()
    args = p.parse_args()
    cutoff_dict = read_and_check_cutoff_dict(args.cutoff_dict_path)

    CellRanger(args.inpath, args.outpath, cutoff_dict).run()


if __name__ == "__main__":
    main()
