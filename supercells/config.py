OUTPUT_FOLDER = "supercells_data"

CUTOFFS_DICT: dict[str, float] = {
    "Mean reads per cell": 20_000,
    "Median genes per cell": 1_500,
    "Valid barcodes": 75,
    "Valid UMIs": 75,
    "Sequencing saturation": 20000,
    "Q30 bases in RNA read": 65,
    "Fraction reads in cells": 70,
    "Reads mapped to genome": 75,
    "Reads mapped confidently to transcriptome": 30
}
