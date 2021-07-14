#!/usr/bin/env python
"""
supercells - module to parse cellranger output data
"""
import pandas as pd
import glob as glob
import os
from datetime import datetime
import json


class CellRanger:
    """CellRanger class"""

    def __init__(self, args):
        # initialize the object
        self.PATH = args.input
        self.OUTPATH = args.output
        # parse the input folder
        print("Parsing folder: " + self.PATH)
        self.STUDIES = glob.glob(self.PATH + "*/outs/")
        self.NUM_STUDIES = len(self.STUDIES)
        if self.NUM_STUDIES:
            print("Found " + str(self.NUM_STUDIES) + " studies")
            self.parse_studies()
        else:
            print("No valid studies found")

    def parse_studies(self):
        """Parse located studies"""
        print("Parsing studies")
        lst = []
        names = []
        for f in self.STUDIES:
            lst.append(pd.read_csv(f + "metrics_summary.csv", thousands=","))
            names.append(f.split("/")[-3])
        print(names)
        df = pd.concat(lst)
        df["name"] = names
        df = df.set_index("name").T  # .drop(columns=['Hash_2','Hash_1'])
        out_dir = self.OUTPATH + "supercells_data/"
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        df.to_csv(out_dir + "supercells_data.csv")
        df.to_html(self.OUTPATH + "supercells_report.html")
        # save log
        log_dict = {
            "input": self.PATH,
            "output": self.OUTPATH,
            "module": "cellranger",
            "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        with open(out_dir + "log.json", "w") as json_file:
            json.dump(log_dict, json_file)
