import pandas as pd
from statsmodels.stats.weightstats import ztest, zconfint, ttest_ind, CompareMeans, DescrStatsW
from statsmodels.stats.proportion import proportions_ztest, proportion_confint, test_proportions_2indep, confint_proportions_2indep
from scipy.stats import ttest_1samp, ttest_ind as sci_t_ind 

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


def calc_ttest2(df, value, alternative, alpha, equal_var, paired):
    
    col1 = df.iloc[:, 0]
    col1_mean = col1.mean()
    col1_std = col1.std()

    col2 = df.iloc[:, 1]
    col2_mean = col2.mean()
    col2_std = col2.std()

    if equal_var == "pooled":
        sci_equal_var = True
    else:
        sci_equal_var = False

    if alternative == "greater":
        stats_alternative = "larger"

    elif alternative == "less":
        stats_alternative = "smaller"

    else:
        stats_alternative = "two-sided"

    if paired:

        diff = col1 - col2
        
        t_test = ttest_1samp(diff, value, alternative=alternative)

        t_stat = t_test[0]
        p_value = t_test[1]
        freedom = t_test.df

        low, high = t_test.confidence_interval(1-alpha)

    else:

        t_stat, p_value, freedom = ttest_ind(col1, col2, stats_alternative, equal_var, value=value)

        t_test = sci_t_ind(col1, col2, alternative=alternative, equal_var=sci_equal_var)

        low, high = t_test.confidence_interval(1-alpha)

    context = {
        "test" : "2t",
        "calculations" : True,
        "col1_mean" : round(col1_mean, 4),
        "col1_std" : round(col1_std, 4),
        "col2_mean" : round(col2_mean, 4),
        "col2_std" : round(col2_std, 4),
        "t_stat" : round(t_stat, 4),
        "p_value" : round(p_value, 4),
        "freedom" : freedom,
        "confidence" : (1-alpha)*100,
        "low" : round(low, 4),
        "high" : round(high, 4),
        "alpha" : alpha
    }

    return context


def calc_ztest2(df, value, alternative, alpha, equal_var, paired):
    
    col1 = df.iloc[:, 0]
    col1_mean = col1.mean()
    col1_std = col1.std()

    col2 = df.iloc[:, 1]
    col2_mean = col2.mean()
    col2_std = col2.std()

    if alternative == "greater":
        alternative = "larger"

    elif alternative == "less":
        alternative = "smaller"


    if paired:

        diff = col1 - col2
        
        # Have to insert a dummy column filled with zeroes for this function.
        compare_obj = CompareMeans(DescrStatsW(diff), DescrStatsW([0 for i in range(len(col1))]))
        z_stat, p_value = compare_obj.ztest_ind(alternative, value=value)

        low, high = compare_obj.zconfint_diff(alpha, alternative)

    else:

        compare_obj = CompareMeans(DescrStatsW(col1), DescrStatsW(col2))
        z_stat, p_value = compare_obj.ztest_ind(alternative, equal_var, value)

        low, high = compare_obj.zconfint_diff(alpha, alternative, equal_var)

    context = {
        "test" : "2z",
        "calculations" : True,
        "col1_mean" : round(col1_mean, 4),
        "col1_std" : round(col1_std, 4),
        "col2_mean" : round(col2_mean, 4),
        "col2_std" : round(col2_std, 4),
        "z_stat" : round(z_stat, 4),
        "p_value" : round(p_value, 4),
        "confidence" : (1-alpha)*100,
        "low" : round(low, 4),
        "high" : round(high, 4),
        "alpha" : alpha
    }

    return context

def calc_prop2(successes1, trials1, successes2, trials2, value, alternative, alpha, method):

    if alternative == "greater":
        alternative = "larger"

    elif alternative == "less":
        alternative = "smaller"

    z_stat, p_value = test_proportions_2indep(successes1, trials1, successes2, trials2, value, method, alternative=alternative, return_results=False)

    low, high = confint_proportions_2indep(successes1, trials1, successes2, trials2, method, alpha=alpha)

    context = {
        "test" : "ind-prop",
        "calculations" : True,
        "z_stat" : round(z_stat, 4),
        "p_value" : round(p_value, 4),
        "success_pct1" : round(((successes1/trials1) * 100), 2),
        "success_pct2" : round(((successes2/trials2) * 100), 2),
        "confidence" : (1-alpha)*100,
        "low" : round(low, 4),
        "high" : round(high, 4),
        "alpha" : alpha
    }

    return context