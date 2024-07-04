"""
supercells - module to parse cellranger output data
"""
from __future__ import annotations

import operator
import json
from datetime import datetime
from numbers import Number
from pathlib import Path
import logging
from typing import Optional, Union
import sys

import pandas as pd
from pandas.io.formats.style import Styler

from supercells.config import OUTPUT_FOLDER, CUTOFFS_DICT
from supercells.modules.general import get_scatterplot_fig


def style_low(v, props: str = "", cutoff_val: Number = 0,
              my_operator: Optional[Union[operator.ge, operator.lt]] = None):
    if isinstance(v, str):
        v = float(v.strip("%"))
    if isinstance(cutoff_val, str):
        cutoff_val = float(cutoff_val.strip("%"))

    return props if my_operator(v, cutoff_val) else None


def style_df(df: pd.DataFrame, cutoff_dict: dict) -> Styler:
    styler = Styler(df)
    warning_style = "color:red;background-color:pink;"
    ok_style = "color:green;background-color:#D7FFE4;"

    for k, cutoff_val in cutoff_dict.items():
        logging.info(f"Styling- '{k}'")
        slice_ = pd.IndexSlice[k, :]

        styler = (
            styler.map(style_low, subset=slice_, props=warning_style, cutoff_val=cutoff_val, my_operator=operator.lt)
            .map(style_low, subset=slice_, props=ok_style, cutoff_val=cutoff_val, my_operator=operator.ge)
        )

    return styler


class CellRanger:
    """CellRanger class"""

    def __init__(self: CellRanger, inpath: str, output: Optional[str] = None, cutoff_dict: Optional[dict] = None):
        # initialize the object
        self.inpath = Path(inpath)
        self.outpath = Path(output) if output else Path()
        self.outdir = Path(self.outpath).joinpath(OUTPUT_FOLDER)
        self.cutoff_dict = cutoff_dict if cutoff_dict else CUTOFFS_DICT
        # parse the input folder
        logging.info(f"Parsing folder: {self.inpath}")
        self.studies_directories = list(self.inpath.rglob("*/outs"))

    def parse_studies(self):
        if self.studies_directories:
            logging.info(f"Found {len(self.studies_directories)} studies")
        else:
            logging.error("No valid studies found")
            return

        """Parse located studies"""
        logging.info("Parsing studies")
        dfs = []
        for f in self.studies_directories:
            logging.info(f)
            try:
                df = pd.read_csv(f.joinpath("metrics_summary.csv"), thousands=",")
                df["name"] = f.parent.name
                dfs.append(df)
            except FileNotFoundError:
                logging.error(f"Failed to find metrics_summary file in '{f}'")

        df = pd.concat(dfs).set_index("name").T

        self.outdir.mkdir(exist_ok=True)

        styled_df = style_df(df, self.cutoff_dict)
        df.to_csv(self.outdir.joinpath("supercells_data.csv"))
        styled_df.to_html(self.outpath.joinpath("supercells_report.html"))
        styled_df.to_excel(self.outpath.joinpath("supercells_report.xlsx"), sheet_name="Super")

        fig = get_scatterplot_fig(df)
        fig.write_html(self.outpath.joinpath('supercells_plots.html'))

        # save log
        log_dict = {
            "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "command": sys.argv
        }
        with self.outdir.joinpath("log.json").open("w+") as json_file:
            json.dump(log_dict, json_file)

        logging.info(f"Done.\nOutput in {self.outpath}")

    def run(self):
        self.parse_studies()
