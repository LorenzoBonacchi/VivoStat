
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
from plots.mixed_models_plots import (
    plot_predicted_vs_observed,
    plot_residuals,
    plot_qq,
    plot_random_effects,
    plot_fixed_effects
)
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

    # ----------------------------------------------------------------------- #
    # Data input
    # ----------------------------------------------------------------------- #
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

        # ----------------------------------------------------------------------- #
        # Test selection
        # ----------------------------------------------------------------------- #
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
                st.subheader("Fixed effects")
                st.dataframe(result["fixed_effects"])
                st.subheader("Random effects")
                st.dataframe(result["random_effects"])
                with st.expander("Full model summary"):
                    st.text(result["model"].summary())
                # ----------------------------------------------------------------------- #
                # Plots
                st.pyplot(plot_predicted_vs_observed(result["model"], df, outcome_col))
                st.subheader("Model diagnostics")
                col1, col2 = st.columns(2)
                with col1:
                    st.pyplot(plot_residuals(result["model"]))
                with col2:
                    st.pyplot(plot_qq(result["model"]))
                col3, col4 = st.columns(2)
                with col3:
                    st.pyplot(plot_random_effects(result["model"]))
                with col4:
                    st.pyplot(plot_fixed_effects(result["model"]))
            
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

            # NB solo per mixed model, per gli altri test non c'è summary
            # da pensare a come gestire i risultati dei test diversi
    

    
    # to add post hoc




    # ------- Plot function call ---------- #




    # -------- Utils ---------------------- #


if __name__ == "__main__":
    main()