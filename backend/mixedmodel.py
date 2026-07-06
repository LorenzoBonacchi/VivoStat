
# -------------- Data input ---------- #
# Input files:  
# data: csv, tsv, xlsx 
# input type of test
# input type of data (e.g. gene expression, methylation, etc.)
# input type of plots
import os 
import pandas as pd
import csv
import statsmodels.formula.api as smf
import streamlit as st
from statsmodels.stats.anova import anova_lm
from utils.table import read_table

def main():

    data = input(
        'Write the data-file name\n'
    )

    try:
        df = read_table(data)
    except ValueError as e:
        print(e)


    test_type = input(
        'What type of test do you want to perform?\n'
        'mixed model: 1\n'
        'other test: 2\n'
    )


    # Search for the metadata/factors 
    # The idea is to check for strings and numbers to identify metadata

    # with open(data, newline='') as csvfile: #it seems to read rows by default
    #     reader = csv.reader(csvfile)
    #     print('I recognized the following columns: \n', reader.__next__()) #print the first row of the csv file, which should be the column names
    #     print('I need to know which columns you want to use as variables for the test, so please write the name of the column exactly as it appears above')
    print('I recognized the following columns: \n', df.columns.values.tolist())
    print('I need to know which columns you want to use as variables for the test, so please write the name of the column exactly as it appears above')
    print(df.columns[0])
    
    # ora come ora non va bene test_data.csv => andrebbe trasformato in un formato long
    # Name | Time | Treatment | Genotype | Sex
    # VEHF1-
    # VEHF2-
    # ----

    # --------------- Indipendence check ------------------ #

    # Indipendence check --> check if the variables are indipendent or not, if not we need to use a mixed model
    # In test data --> Time means not indipendent from Mouse

    identifier = {'sample', 'id', 'mouse', 'subject', 'patient', 'individual','Names'} #list of possible identifiers for the samples, to check if the variables are indipendent or not

    def dependence_checker(variable1, variable2):
        # code to check if the variables are indipendent or not
        # if not indipendent, return True, else return False
        print("Checking variables dependency...")
        if data.columns[0] in identifier:
            for sample in identifier:
                if variable1 == variable2:
                    print("The variables are not indipendent, you should use a mixed model")
                else:
                    print("The variables seems indipendent, you can use a simple test")


    # ------------------------------------------------------ #

    # Autocheck measures WIP --> ci lascio value come variaibile solo per testare che funzioni il codice 

    outcome_col = input("Outcome variable (Y): ")
    group_col = input("Random effect (subject/id): ")

    fixed_effects = input(
        "Fixed effects (comma separated): "
    ).split(",")

    fixed_effects = [x.strip() for x in fixed_effects]

    # --- check columns ---
    all_cols = [outcome_col, group_col] + fixed_effects

    missing = [c for c in all_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # --- formula ---
    formula = outcome_col + " ~ " + " * ".join(fixed_effects)

    print("Using formula:", formula)

    # --- model ---
    model = smf.mixedlm(
        formula,
        data=df,
        groups=df[group_col]
    )

    result = model.fit()
    print(result.summary())

    
    
    # to add post hoc




    # ------- Plot function call ---------- #




    # -------- Utils ---------------------- #


if __name__ == "__main__":
    main()