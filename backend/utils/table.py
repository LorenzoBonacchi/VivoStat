# ----------------------------------------------------------------------- #
# Functions for managing tables
# ----------------------------------------------------------------------- #
from pathlib import Path
import pandas as pd
import re


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


## Function that checks the variable type in the dataset
def check_cols(data):

    colnames_dict = {
        "Names": r"\bn(?:a|o)m(?:e|es|i)s\b",
        "Genotypes": r"\bgenot(?:y|i)p(?:e|es|o|i)?|variant(?:s|e|i)?\b",
        "Treatment": r"\btreatments?|trattament(?:o|i)\b",
        "Sex": r"\bse(?:|x|xes|sso)\b",
        "Time": r"\btimes?|temp(?:o|i)\b",
        "Measure": r"\bmeasures?|misur(?:a|e)|values?|valor(?:e|i)\b"
    }

    possible_variables = list(colnames_dict.keys()).copy()

    result = {}
    for column in data.columns:
        for key, pattern in colnames_dict.items():
            if re.search(pattern, column, re.IGNORECASE):
                result[column] = [key]
                break
        else:
            result[column] = list(colnames_dict.keys())

    return result, possible_variables



## Function that makes a longer table depending on auto-detected or user-specified columns
# def make_longer():
    
    
