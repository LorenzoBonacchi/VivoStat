# ----------------------------------------------------------------------- #
# Functions for managing tables
# ----------------------------------------------------------------------- #
from pathlib import Path
import pandas as pd
## Function to read input table (.csv, .tsv, .xls/.xlsx)
def read_table(filename):
    if filename is None:
        return None

    try:
        filename_lower = filename.name.lower()
        if filename_lower.endswith(".csv"):
            return pd.read_csv(filename)
        elif filename_lower.endswith(".tsv"):
            return pd.read_csv(filename, sep="\t")
        elif filename_lower.endswith((".xls", ".xlsx")):
            return pd.read_excel(filename)
        else:
            raise ValueError(f"Unsupported file format. Please provide a .csv, .tsv, or .xlsx file.")

    except FileNotFoundError:
        print(f"Error: '{filename}' was not found.")
        return None
