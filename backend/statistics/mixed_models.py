
import statsmodels.formula.api as smf
import pandas as pd
# ----------------------------------------------------------------------- #
# Mixed Model
# ----------------------------------------------------------------------- #

def run_mixed_model(df, outcome, subject, fixed_effects):

    formula = outcome + " ~ " + " * ".join(fixed_effects)

    model = smf.mixedlm(
        formula,
        data=df,
        groups=df[subject]
    )
    result = model.fit()
    return {
        "model": result,
        "fixed_effects": pd.DataFrame({
            "Estimate": result.fe_params,
            "SE": result.bse_fe,
            "p-value": result.pvalues[:len(result.fe_params)]
        }),
        "random_effects": pd.DataFrame(result.random_effects).T
    }

