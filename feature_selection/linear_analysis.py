import statsmodels.api as sm
import numpy as np
import pandas as pd
    
def get_linear_analysis(X, Y):    
    
    '''
    Input:
    X: (set of features, pandas DataFrame)
    Y: (set of labels)
    
    Return:
    DataFrame containing the linear regression coefficients and respectives p-values.
    
    If P-Value is lesser than significance (usually 0.05), then we can conclude that the coefficient is not
    useful to the regression. 
    '''
    
    mod = sm.OLS(Y, X)
    res = mod.fit()
    
    table = pd.DataFrame()
    
    table['index'] = pd.Series(X.columns)
    
    table.set_index("index", inplace=True)
    
    table['coeff'] = res.params
    
    table['pvalues'] = res.pvalues
    
    return table
