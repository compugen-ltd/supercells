"""
supercells - module to parse cellranger output data
"""
import pandas as pd
import glob as glob
import os
from datetime import datetime
import json
from pathlib import Path
# import multiqc

class CellRanger:
    """CellRanger class"""

    def __init__(self, args):
        # initialize the object
        self.PATH = args.input
        self.OUTPATH = args.output
        self.OUTDIR = self.OUTPATH
        # parse the input folder
        print("Parsing folder: " + self.PATH)
        self.STUDIES = []
        for p in Path(self.PATH).rglob("*.csv"):
            self.STUDIES.append(p)
        self.NUM_STUDIES = len(self.STUDIES)
        if self.NUM_STUDIES:
            print("Found " + str(self.NUM_STUDIES) + " studies")
            self.parse_studies()
        else:
            print("No valid studies found")
    
    def export_to_(self, df, extype):
        """export data to Excel/HTML""" 
        print("Exporting to "+ extype)

        idx = pd.IndexSlice
        slice_ = idx["Median Genes per Cell", :]
        
        def style_low(v, props=""):
            return props if v < 1500 else None
        def style_pass(v, props=""):
            return props if v > 1500 else None
        
        slice_2 = idx["Sequencing Saturation", :]
        
        def style_low2(v, props=""):
            v = float(v.strip(' \t\n\r%'))
            return props if v < 30 else None
        def style_pass2(v, props=""):
            v = float(v.strip(' \t\n\r%'))
            return props if v > 30 else None

        slice_3 = idx["Reads Mapped Confidently to Transcriptome", :]
        
        def style_low3(v, props=""):
            v = float(v.strip(' \t\n\r%'))
            return props if v < 70 else None
        def style_pass3(v, props=""):
            v = float(v.strip(' \t\n\r%'))
            return props if v > 70 else None
        
        final_df = df.style.applymap(
            style_low, props="color:red;background-color:pink;", subset=slice_
        )\
        .applymap(style_pass, props="color:green;background-color:#D7FFE4;", subset=slice_)

        final_df = final_df.applymap(
            style_low2, props="color:red;background-color:pink;", subset=slice_2
        )\
        .applymap(style_pass2, props="color:green;background-color:#D7FFE4;", subset=slice_2)

        final_df = final_df.applymap(
            style_low3, props="color:red;background-color:pink;", subset=slice_3
        )\
        .applymap(style_pass3, props="color:green;background-color:#D7FFE4;", subset=slice_3)
        
        if (extype == "HTML" or extype == "html"):
            final_df.to_html(os.path.join(self.OUTDIR , "supercells_report.html"))
        else:
            final_df.to_excel(os.path.join(self.OUTDIR , "supercells_data.xlsx"), sheet_name = "Super")

    def parse_studies(self):
        """Parse located studies"""
        print("Parsing studies")
        lst = []
        names = []
        for f in self.STUDIES:
            try:
                lst.append(pd.read_csv(f, thousands = ","))
                names.append(f.parent.parent.name)
            except:
                print(f"Failed to find summary for {f}")
        print(names)
        df = pd.concat(lst)
        df["name"] = names
        df = df.set_index('name').T  # .drop(columns=['Hash_2','Hash_1'])
        
        if not os.path.exists(self.OUTDIR):
            os.makedirs(self.OUTDIR)
        df.to_csv(self.OUTDIR + "supercells_data.csv")
        df.to_json(self.OUTDIR + "supercells_json_report.json")
        df.to_html(self.OUTPATH + "supercells_report.html")
        try:
            self.export_to_(df, "HTML")
            self.export_to_(df, "Excel")
        except:
            print(f"Failed to generate report.")
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

    # multiqc.run("C:\\Users\\toma\\Documents\\supercells\\supercells")
