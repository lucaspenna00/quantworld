import statsmodels.api as sm
import numpy as np
import pandas as pd

def get_linear_analysis(X, Y):
    
    mod = sm.OLS(Y, X)
    res = mod.fit()
    
    table = pd.DataFrame()
    
    table['index'] = pd.Series(X.columns)
    
    table.set_index("index", inplace=True)
    
    table['coeff'] = res.params
    
    table['pvalues'] = res.pvalues
    
    return table
