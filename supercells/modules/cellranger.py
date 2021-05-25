#!/usr/bin/env python
"""
supercells - module to parse cellranger output data
"""
import pandas as pd
import glob as glob


class CellRanger:
    def __init__(self, folder_path):
        # initialize the object
        self.PATH = folder_path

        # parse the input folder
        print("Parsing folder: " + self.PATH)
        self.STUDIES = glob.glob(self.PATH + "*/outs/")
        self.NUM_STUDIES = len(self.STUDIES)
        if self.NUM_STUDIES:
            print("Found " + str(self.NUM_STUDIES) + " studies")
            self.parse_studies()
        else:
            print("No valid studies found")

    def parse_studies(_self):
        print("Parsing studies")  # TODO: implement the function
