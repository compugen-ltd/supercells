OUTPUT_FOLDER = "supercells_data"

CUTOFFS_DICT: dict[str, float] = {
    "Mean Reads per Cell": 20_000,
    "Median Genes per Cell": 1_500,
    "Valid Barcodes": "75%",
    # "Valid UMIs": 75, # TODO: replace with valid metric found in CellRanger output summary
    "Sequencing Saturation": "30%",
    "Q30 Bases in RNA Read": 65,
    "Fraction Reads in Cells": "70%",
    "Reads Mapped to Genome": "75%",
    "Reads Mapped Confidently to Transcriptome": "30%"
}
