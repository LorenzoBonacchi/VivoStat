## Functions for managing tables
from pathlib import Path
import pandas as pd
## Function to read input table (.csv, .tsv, .xls/.xlsx)

def read_table(filename):

    if filename is None:
        return None

    try:
        return pd.read_csv(filename, sep=None, engine="python")
    except Exception:
        pass
    try:
        return pd.read_excel(filename)
    except Exception:
        raise ValueError(
            "Unsupported file format. Try tsv, csv or Excel files"
        )