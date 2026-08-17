import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

def plot_predicted_vs_observed(model, df, outcome):

    fig, ax = plt.subplots(figsize=(6,6))

    observed = df[outcome]
    predicted = model.fittedvalues

    ax.scatter(observed, predicted)

    mn = min(observed.min(), predicted.min())
    mx = max(observed.max(), predicted.max())

    ax.plot([mn, mx], [mn, mx], "r--")

    ax.set_xlabel("Observed")
    ax.set_ylabel("Predicted")
    ax.set_title("Predicted vs Observed")

    return fig

def plot_residuals(model):

    fig, ax = plt.subplots(figsize=(5,4))

    ax.scatter(model.fittedvalues, model.resid)

    ax.axhline(0, color="red", linestyle="--")

    ax.set_xlabel("Fitted")
    ax.set_ylabel("Residuals")

    return fig

def plot_qq(model):

    fig = plt.figure(figsize=(5, 4))

    sm.qqplot(
        model.resid,
        line="45",
        fit=True,
        ax=plt.gca()
    )

    plt.title("Normal Q-Q")

    return fig

def plot_random_effects(model):

    fig, ax = plt.subplots(figsize=(5, 4))

    random_effects = model.random_effects

    labels = []
    values = []

    for subject, effect in random_effects.items():

        labels.append(str(subject))

        if hasattr(effect, "iloc"):
            values.append(effect.iloc[0])
        else:
            values.append(list(effect.values())[0])

    order = np.argsort(values)

    labels = np.array(labels)[order]
    values = np.array(values)[order]

    ax.scatter(values, range(len(values)))

    ax.axvline(0, color="red", linestyle="--")

    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)

    ax.set_xlabel("Random intercept")
    ax.set_title("Random effects")

    return fig

def plot_fixed_effects(model):

    fig, ax = plt.subplots(figsize=(6, 4))

    params = model.fe_params

    conf = model.conf_int().loc[params.index]

    estimates = params.values
    lower = conf.iloc[:, 0].values
    upper = conf.iloc[:, 1].values

    y = np.arange(len(params))

    ax.errorbar(
        estimates,
        y,
        xerr=[estimates - lower, upper - estimates],
        fmt="o",
        capsize=4
    )

    ax.axvline(0, color="red", linestyle="--")

    ax.set_yticks(y)
    ax.set_yticklabels(params.index)

    ax.set_xlabel("Estimate")
    ax.set_title("Fixed effects")

    return fig