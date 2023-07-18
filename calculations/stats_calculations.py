import pandas as pd
from statsmodels.stats.weightstats import ztest, zconfint
from scipy.stats import ttest_1samp

def calc_ttest1(df, value, alternative, alpha):

    col1 = df.iloc[:, 0]

    t_test = ttest_1samp(col1, value, alternative=alternative)

    t_stat = t_test[0]
    p_value = t_test[1]
    freedom = t_test.df


    interval = t_test.confidence_interval(1-alpha)

    low = interval[0]
    high = interval[1]

    context = {
        "test" : "t",
        "calculations" : True,
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

    if alternative == "greater":
        alternative = "larger"

    elif alternative == "less":
        alternative = "smaller"

    z_test = ztest(col1, value=value, alternative=alternative)

    z_stat = z_test[0]
    p_value = z_test[1]

    interval = zconfint(col1, value=value, alpha=alpha, alternative=alternative)

    low = interval[0]
    high = interval[1]
    context = {
        "test" : "z",
        "calculations" : True,
        "z_stat" : round(z_stat, 4),
        "p_value" : round(p_value, 4),
        "confidence" : (1-alpha)*100,
        "low" : round(low, 4),
        "high" : round(high, 4),
        "alpha" : alpha
    }

    return context
