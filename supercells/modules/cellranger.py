"""
supercells - module to parse cellranger output data
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
import logging
from typing import Optional

import pandas as pd

from config import OUTPUT_FOLDER, CUTOFFS_DICT


def style_df(df: pd.DataFrame, cutoffs_dict: dict):
    styled_df = df

    for key_name, cutoff_value in cutoffs_dict.items():
        slice_ = pd.IndexSlice[key_name, :]

        def style_low(v, props=""):
            return props if v < cutoff_value else None

        def style_pass(v, props=""):
            return props if v >= cutoff_value else None

        styled_df = (
            styled_df.style.applymap(style_low, props="color:red;background-color:pink;", subset=slice_)
            .applymap(style_pass, props="color:green;background-color:#D7FFE4;", subset=slice_)
        )

    return styled_df


class CellRanger:
    """CellRanger class"""

    def __init__(self: CellRanger, inpath: str, output: Optional[str] = None, cutoffs_dict: Optional[dict] = None):
        # initialize the object
        self.inpath = Path(inpath)
        self.outpath = Path(output) if output else Path()
        self.outdir = Path(self.outpath).joinpath(OUTPUT_FOLDER)
        self.cutoffs_dict = cutoffs_dict if cutoffs_dict else CUTOFFS_DICT
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
        print("Parsing studies")
        lst = []
        names = []
        for f in self.studies_directories:
            try:
                lst.append(pd.read_csv(f.joinpath("metrics_summary.csv"), thousands=","))
                names.append(f.stem)
            except FileNotFoundError:
                logging.error(f"Failed to find summary for {f}")
        logging.info(names)
        df = pd.concat(lst)
        df["name"] = names
        df = df.set_index("name").T

        self.outdir.mkdir(exist_ok=True)

        styled_df = style_df(df, self.cutoffs_dict)
        styled_df.to_csv(self.outdir.joinpath("supercells_data.csv"))
        styled_df.to_json(self.outdir.joinpath("supercells_json_report.json"))
        styled_df.to_html(self.outpath.joinpath("supercells_report.html"))
        styled_df.to_excel(self.outpath.joinpath("supercells_report.excel"), sheet_name="Super")
        styled_df.to_html(self.outpath.joinpath("supercells_report.excel"))

        # save log
        log_dict = {
            "input": self.inpath,
            "output": self.outpath,
            "module": "cellranger",
            "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        with self.outdir.joinpath("log.json").open("w") as json_file:
            json.dump(log_dict, json_file)

        logging.info(f"Done.\nOutput in {self.outpath}")

    def run(self):
        self.parse_studies()
