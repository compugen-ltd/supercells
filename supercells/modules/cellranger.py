#!/usr/bin/env python
"""
supercells - module to parse cellranger output data
"""
import pandas as pd
import glob as glob


class CellRanger:
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
        df.to_csv(self.OUTPATH + "qc_data.csv")
        # TODO: make this fucntion nicer, define where to save the file and in what format
