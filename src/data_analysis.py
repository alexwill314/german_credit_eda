import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, chi2_contingency
import matplotlib.pyplot as plt

#define analysing functions

#define a function for creating crosstabs and plotting barcharts
def ctbplot(df: pd.DataFrame,  feature: str):
    ct = pd.crosstab(df[feature], df['credit_risk'], normalize = 'index')
    ax = ct.plot(kind='barh', stacked=True)
    ax.axvline(0.30, color='black', linestyle='--', linewidth=1.5, label='Baseline default rate (30%)')
    ax.set_title(f'{feature} vs risk')
    ax.legend()
    plt.tight_layout()
    plt.show()
    print(ct)

# effect size
def cohens_d(x, y):
    x = x.dropna()
    y = y.dropna()
    return abs(x.mean() - y.mean()) / np.sqrt((x.std()**2 + y.std()**2) / 2)

def cramers_v(x, y):
    contingency = pd.crosstab(x, y)
    chi2 = chi2_contingency(contingency)[0]
    n = contingency.sum().sum()
    r, k = contingency.shape
    return np.sqrt(chi2 / (n * (min(r - 1, k - 1))))

# main function
def analyse_feature(df, feature):

    result = {}

    # numerical → t-test
    if pd.api.types.is_numeric_dtype(df[feature]):

        good = df[df['credit_risk'] == 'good'][feature]
        bad = df[df['credit_risk'] == 'bad'][feature]

        t_stat, p_value = ttest_ind(good, bad, equal_var=False)
        effect = cohens_d(good, bad)

        result['type'] = 'numerical'
        result['test'] = 't-test'
        result['p_value'] = p_value
        result['effect_size'] = effect

        # interpretation effect size
        if abs(effect) < 0.2:
            interpretation = 'weak effect'
        elif abs(effect) < 0.5:
            interpretation = 'moderate effect'
        else:
            interpretation = 'strong effect'

    # categorical -> chisquared test
    else:

        contingency = pd.crosstab(df[feature], df['credit_risk'])

        chi2, p_value, _, _ = chi2_contingency(contingency)
        effect = cramers_v(df[feature], df['credit_risk'])

        result['type'] = 'categorical'
        result['test'] = 'chi-square'
        result['p_value'] = p_value
        result['effect_size'] = effect

        # interpretation of effect size
        if effect < 0.1:
            interpretation = 'weak association'
        elif effect < 0.3:
            interpretation = 'moderate association'
        else:
            interpretation = 'strong association'

    #statistical significance
    if p_value < 0.001:
        significance = '***'
    elif p_value < 0.01:
        significance = '**'
    elif p_value < 0.05:
        significance = '*'
    else:
        significance = ''

    result['significance'] = significance
    # general info
    result['n'] = len(df)
    result['interpretation'] = interpretation

    return pd.Series(result)