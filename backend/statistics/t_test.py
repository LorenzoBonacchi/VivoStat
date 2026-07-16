
import statsmodels.formula.api as smf

# ----------------------------------------------------------------------- #
# T-test
# ----------------------------------------------------------------------- #

def run_t_test(df, outcome, subject, fixed_effects):

    formula = outcome + " ~ " + " * ".join(fixed_effects)

    model = smf.mixedlm(
        formula,
        data=df,
        groups=df[subject]
    )

    return model.fit()



## NOTES FORM STAT MODELS
#statsmodels.stats.weightstats.ttest_ind(x1, x2, alternative='two-sided', usevar='pooled', weights=(None, None))

#
#x1, x2: Arrays containing sample data for the groups being compared.
#alternative: The hypothesis to test. Options include:
#
#    'two-sided': Default, tests for any difference.
#    'larger': Tests if the mean of x1 is greater than x2.
#    'smaller': Tests if the mean of x1 is less than x2.
#
#usevar: Assumptions about variance. Options include:
#
#    'pooled': Default, assumes equal variance.
#    'unequal': Does not assume equal variance.
#
#weights: A tuple specifying weights for x1 and x2, used in weighted t-tests.