![Supercells](https://user-images.githubusercontent.com/9028967/122049119-b81ece00-cdea-11eb-9f13-9f09e20eb537.png)
---


**Easily assess quality control data across multiple single cell datasets**

Supercells is a tool which generates a single report for multiple 10x cellranger samples - thus saving time and allowing comparative QC analysis.

It is written in Python (tested with v3.7-3.9).

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![PyPI Version](https://img.shields.io/pypi/v/supercells.svg?style=flat-square)](https://pypi.python.org/pypi/supercells/)
[![Downloads](https://static.pepy.tech/badge/supercells)](https://pepy.tech/project/supercells)
[![Compugen on Twitter](https://img.shields.io/twitter/follow/CompugenLtd.svg?style=social&label=Follow)](https://twitter.com/CompugenLtd)


<br /> 




## 📦  Installation

Using PyPI:

`pip install supercells`

Clone or download the repository and navigate to the package directory, then invoke:

`pip install . `


## 💻  Usage

Once supercells is installed it is run by invoking:

`supercells -i <experiment folder>`

Unless specified otherwise it will generate `supercells_report.html` within the input folder as well as `supercells_report` folder containing summarizing xlsx file and CSV with the raw data. To specify an output directory use the ` -o <output folder>` flag

![image](https://user-images.githubusercontent.com/9028967/222570081-d8db435a-5683-4c0b-bc86-42c95b54c186.png)

### More options

```
usage: supercells [-h] [--version] --input INPATH [--output OUTPATH] [--cutoff-dict CUTOFF_DICT_PATH]

supercells: Easily assess quality control data across multiple single cell datasets

options:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --input INPATH, -i INPATH
                        Enter the location of the input files
  --output OUTPATH, -o OUTPATH
                        Specify the location of the output files, default is current wd
  --cutoff-dict CUTOFF_DICT_PATH, -c CUTOFF_DICT_PATH
```

`cutoff-dict` parameters is a file path to a json file. 
This is a sample of the json:
```json
{
    "Mean Reads per Cell": 20000,
    "Median Genes per Cell": 1500,
    "Valid Barcodes": 75,
    "Sequencing Saturation": 30,
    "Q30 Bases in RNA Read": 65,
    "Fraction Reads in Cells": 70,
    "Reads Mapped to Genome": 75,
    "Reads Mapped Confidently to Transcriptome": 30
}
```
The keys are the field names and the values are cutoff values for that field. i.e. **Mean Reads per Cell** cutoff  
value is **20000**. So for each sample if the **Mean Reads per Cell** is less than **20000** the output would show  
that cell in <span style="color:red">red</span>, else in <span style="color:green">green</span>.



## Further development
Suggestions for additional features and code contributions are welcomed
