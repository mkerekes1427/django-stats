import pandas as pd
from statsmodels.stats.weightstats import ztest, zconfint
from statsmodels.stats.proportion import proportions_ztest, proportion_confint
from scipy.stats import ttest_1samp

def calc_ttest1(df, value, alternative, alpha):

    col1 = df.iloc[:, 0]
    col1_mean = col1.mean()
    col1_std = col1.std()

    t_test = ttest_1samp(col1, value, alternative=alternative)

    t_stat = t_test[0]
    p_value = t_test[1]
    freedom = t_test.df

    low, high = t_test.confidence_interval(1-alpha)

    context = {
        "test" : "t",
        "calculations" : True,
        "mean" : round(col1_mean, 4),
        "std" : round(col1_std, 4),
        "t_stat" : round(t_stat, 4),
        "p_value" : round(p_value, 4),
        "freedom" : freedom,
        "confidence" : (1-alpha)*100,
        "low" : round(low, 4),
        "high" : round(high, 4),
        "alpha" : alpha
    }

    return context


def calc_ztest1(df, value, alternative, alpha):

    col1 = df.iloc[:, 0]
    col1_mean = col1.mean()
    col1_std = col1.std()


    if alternative == "greater":
        alternative = "larger"

    elif alternative == "less":
        alternative = "smaller"

    z_stat, p_value = ztest(col1, value=value, alternative=alternative)

    low, high = zconfint(col1, alpha=alpha, alternative=alternative)

    context = {
        "test" : "z",
        "calculations" : True,
        "mean" : round(col1_mean, 4),
        "std" : round(col1_std, 4),
        "z_stat" : round(z_stat, 4),
        "p_value" : round(p_value, 4),
        "confidence" : (1-alpha)*100,
        "low" : round(low, 4),
        "high" : round(high, 4),
        "alpha" : alpha
    }

    return context

def calc_prop1(successes, trials, value, alternative, alpha, method):

    if alternative == "greater":
        alternative = "larger"

    elif alternative == "less":
        alternative = "smaller"

    z_stat, p_value = proportions_ztest(successes, trials, value, alternative)

    low, high = proportion_confint(successes, trials, alpha, method)

    context = {
        "test" : "prop",
        "calculations" : True,
        "z_stat" : round(z_stat, 4),
        "p_value" : round(p_value, 4),
        "success_pct" : round(((successes/trials) * 100), 2),
        "confidence" : (1-alpha)*100,
        "low" : round(low, 4),
        "high" : round(high, 4),
        "alpha" : alpha
    }

    return context

