![Supercells](https://user-images.githubusercontent.com/9028967/122049119-b81ece00-cdea-11eb-9f13-9f09e20eb537.png)
---


**Easily assess quality control data across multiple single cell datasets**

Supercells is a tool which generates a single report for multiple 10x cellranger samples - thus saving time and allowing comparative QC analysis.

It is written in Python (tested with v3.7-3.9).

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![Compugen on Twitter](https://img.shields.io/twitter/follow/CompugenLtd.svg?style=social&label=Follow)](https://twitter.com/CompugenLtd
)<br /> 



## 📦  Installation

Clone or download the repository and navigate to the package directory, then invoke:

`pip install . `

(PyPI coming soon..)


## 💻  Usage

Once supercells is installed it is run by invoking:

`supercells -i <experiment folder>`

Unless specified otherwise it will generate `supercells_report.html` within the input folder as well as `supercells_report` folder containing the raw CSV files. To specify an output directory use the ` -o <output folder>` flag

## Further development
Suggestions for additional features and code contributions are welcomed
