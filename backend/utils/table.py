## Functions for managing tables
from pathlib import Path
import pandas as pd
## Function to read input table (.csv, .tsv, .xls/.xlsx)

def read_table(filename):
    filename=Path(filename)
    ext = filename.suffix.lower()
    if ext in [".xlsx", ".xls"]:
        return pd.read_excel(filename)
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