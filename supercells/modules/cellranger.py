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
        self.OUTDIR = self.OUTPATH + "supercells_data/"
        # parse the input folder
        print("Parsing folder: " + self.PATH)
        self.STUDIES = glob.glob(self.PATH + "*/outs/")
        self.NUM_STUDIES = len(self.STUDIES)
        if self.NUM_STUDIES:
            print("Found " + str(self.NUM_STUDIES) + " studies")
            self.parse_studies()
        else:
            print("No valid studies found")

    def export_to_excel(self, df):
        """export data to XLSX and whilight issues"""
        print("Exporting to Excel")

        idx = pd.IndexSlice
        slice_ = idx["Median Genes per Cell", :]

        def style_low(v, props=""):
            return props if v < 1500 else None
        def style_pass(v, props=""):
            return props if v > 1500 else None

        df = df.style.applymap(
            style_low, props="color:red;background-color:pink;", subset=slice_
        )\
        .applymap(style_pass, props="color:green;background-color:#D7FFE4;", subset=slice_
        )
        df.to_excel(self.OUTDIR + "supercells_data.xlsx", sheet_name="Super")

    def parse_studies(self):
        """Parse located studies"""
        print("Parsing studies")
        lst = []
        names = []
        for f in self.STUDIES:
            try:
                lst.append(pd.read_csv(f + "metrics_summary.csv", thousands=","))
                names.append(f.split("/")[-3])
            except:
                print(f"Failed to find summary for {f}")
        print(names)
        df = pd.concat(lst)
        df["name"] = names
        df = df.set_index("name").T  # .drop(columns=['Hash_2','Hash_1'])
        
        if not os.path.exists(self.OUTDIR):
            os.makedirs(self.OUTDIR)
        df.to_csv(self.OUTDIR + "supercells_data.csv")
        df.to_html(self.OUTPATH + "supercells_report.html")
        try:
            self.export_to_excel(df)
        except:
                print(f"Failed to generate XLSX")
        # save log
        log_dict = {
            "input": self.PATH,
            "output": self.OUTPATH,
            "module": "cellranger",
            "datetime": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        with open(self.OUTDIR + "log.json", "w") as json_file:
            json.dump(log_dict, json_file)
        print("Done.\nOutput in "+str(self.OUTPATH))
