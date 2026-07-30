
# -------------- Data input ---------- #
# Input files:  
# data: csv, tsv, xlsx 
# input type of test
# input type of data (e.g. gene expression, methylation, etc.)
# input type of plots
import os ##useless for now
import pandas as pd
import csv # useless for now
import statsmodels.formula.api as smf
import streamlit as st
from statsmodels.stats.anova import anova_lm
import utils.table as tb
from statistics.mixed_models import run_mixed_model
from statistics.dependency import dependency_check
from PIL import Image  

DATA_DIR = "../data"


def main():
    # ----------------------------------------------------------------------- #
    # Streamlit
    # ----------------------------------------------------------------------- #
    
    ### Title and logo image
    img = Image.open(f"{DATA_DIR}/streamlit_image.png") # Open the image file
    col1, col2 = st.columns([1, 6], gap="xxsmall", vertical_alignment="center")
    with col1:
        st.image(img, width=90) 
    with col2:
        st.title('VivoStat')

    file_types = ["csv", "tsv", "xlsx"] # fixed non MIME types for file uploader

    data = st.file_uploader('Load your table: ', type = file_types)

    if data is not None:
        df = tb.read_table(data)
        report = dependency_check(df)
        st.subheader('This is your data: ')
        st.write(df)
        st.subheader("Dataset inspection")

        if any(report["repeated_measurements"].values()): # not working as intended
            st.warning(
            """
            Repeated measurements detected.
        
            Some observations are not independent.
            Mixed Model or repeated-measures ANOVA are recommended.
            """
        )

        else:

            st.success("No repeated measurements detected.")
        
        st.text('Select the columns you want to use as variables for the test')
        df = tb.read_table(data)
        report = dependency_check(df)
        st.subheader('This is your data: ')
        st.text('Select the correct category for the variables:')
        data_vars, possible_variables = tb.check_cols(df)
        cols = st.columns(len(df.columns))

        # Managing selection boxes
        for i, column in enumerate(df.columns):
            detected_variables = data_vars[column]

            if len(detected_variables) == 1:
                detected_variable = detected_variables[0]
                options = [detected_variable] + [var for var in possible_variables if var != detected_variable]
                default_index = 0

            else:
                options = ["Select..."] + possible_variables
                default_index = 0

            with cols[i]:
                selected_variable = st.selectbox(label="Variable", options=options, index=default_index, key=f"select_{column}")
        
        st.dataframe(df, width="stretch", hide_index=True)
        st.subheader("Dataset inspection")

        if any(report["repeated_measurements"].values()): # not working as intended
            st.warning(
            """
            Repeated measurements detected.
        
            Some observations are not independent.
            Mixed Model or repeated-measures ANOVA are recommended.
            """
        )

        else:

            st.success("No repeated measurements detected.")
        
        st.text('Select the columns you want to use as variables for the test')

        test_type = st.selectbox("Test",["Mixed Model","ANOVA","T-test"])
    

        # ----------------------------------------------------------------------- #
        # Mixed Models parameters 
        # ----------------------------------------------------------------------- #
        if test_type == "Mixed Model":
            st.subheader("Mixed Models parameters")
            # Outcome
            outcome_col = st.selectbox("Outcome variable (Y)",df.columns)
            # Random effect
            group_col = st.selectbox("Subject / Random effect",df.columns)
            # Fixed effects
            fixed_effects = st.multiselect("Fixed effects",[c for c in df.columns if c not in [outcome_col, group_col]])


        # ----------------------------------------------------------------------- #
        # T-test parameters
        # ----------------------------------------------------------------------- #
        elif test_type == "T-test":

            st.subheader("T-test parameters")

            outcome = st.selectbox("Measurement variable", df.select_dtypes(include="number").columns)
            group_variable = st.selectbox("Grouping variable", df.select_dtypes(exclude="number").columns)


        # ----------------------------------------------------------------------- #
        # Anova parameters
        # ----------------------------------------------------------------------- #
        elif test_type == "ANOVA":

            st.subheader("ANOVA parameters")
            
            outcome_col = st.selectbox("Measurement variable", df.select_dtypes(include="number").columns)
            factors = st.multiselect("Factors",df.select_dtypes(exclude="number").columns)

        # ----------------------------------------------------------------------- #
        # Run analysis
        ## To add a summary before starting
        ## Maybe there's a more elegant way to do this, but for now it works
        if st.button("Run analysis"):

            if test_type == "Mixed Model":

                result = run_mixed_model(
                    df,
                    outcome_col,
                    group_col,                    
                    fixed_effects
                )
        
            elif test_type == "ANOVA":
        
                result = run_anova(
                    df,                    
                    outcome_col,
                    factors
                )
        
            elif test_type == "T-test":
                
                result = run_ttest(
                    df,
                    outcome,
                    group_variable                
                )

            st.text(result.summary())
            # NB solo per mixed model, per gli altri test non c'è summary
            # da pensare a come gestire i risultati dei test diversi
    

    # ----------------------------------------------------------------------- #
    # Backened 
    # ----------------------------------------------------------------------- #
    # Search for the metadata/factors 
    # The idea is to check for strings and numbers to identify metadata

    # with open(data, newline='') as csvfile: #it seems to read rows by default
    #     reader = csv.reader(csvfile)
    #     print('I recognized the following columns: \n', reader.__next__()) #print the first row of the csv file, which should be the column names
    #     print('I need to know which columns you want to use as variables for the test, so please write the name of the column exactly as it appears above')
    #print('I recognized the following columns: \n', df.columns.values.tolist())
    #print('I need to know which columns you want to use as variables for the test, so please write the name of the column exactly as it appears above')
    #print(df.columns[0])
    
    # ora come ora non va bene test_data.csv => andrebbe trasformato in un formato long
    # Name | Time | Treatment | Genotype | Sex
    # VEHF1-
    # VEHF2-
    # ----

    # --------------- Indipendence check ------------------ #

    # Indipendence check --> check if the variables are indipendent or not, if not we need to use a mixed model
    # In test data --> Time means not indipendent from Mouse

    #identifier = {'sample', 'id', 'mouse', 'subject', 'patient', 'individual','Names'} #list of possible identifiers for the samples, to check if the variables are indipendent or not

    #def dependence_checker(variable1, variable2):
        # code to check if the variables are indipendent or not
        # if not indipendent, return True, else return False
    #    print("Checking variables dependency...")
    #    if data.columns[0] in identifier:
    #        for sample in identifier:
    #            if variable1 == variable2:
    #                print("The variables are not indipendent, you should use a mixed model")
    #            else:
    #                print("The variables seems indipendent, you can use a simple test")


    # ------------------------------------------------------ #

    # Autocheck measures WIP --> ci lascio value come variaibile solo per testare che funzioni il codice 

    #outcome_col = input("Outcome variable (Y): ")
    #group_col = input("Random effect (subject/id): ")

    #fixed_effects = input(
    #    "Fixed effects (comma separated): "
    #).split(",")

    #fixed_effects = [x.strip() for x in fixed_effects]

    # --- check columns ---
    #all_cols = [outcome_col, group_col] + fixed_effects

    #missing = [c for c in all_cols if c not in df.columns]
    #if missing:
    #    raise ValueError(f"Missing columns: {missing}")


    
    
    # to add post hoc




    # ------- Plot function call ---------- #




    # -------- Utils ---------------------- #


if __name__ == "__main__":
    main()