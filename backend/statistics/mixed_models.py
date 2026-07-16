
import statsmodels.formula.api as smf

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

    return model.fit()

