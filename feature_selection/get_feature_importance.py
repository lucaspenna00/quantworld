import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from xgboost import XGBRegressor
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from scipy.stats import spearmanr

def get_feature_importance(X, Y, scaler, controle):

    if controle == True:

        X['controle'] = np.random.normal(0, 1, X.shape[0])

    features_behaviour = pd.DataFrame()

    # -------- Pearson ------------

    features_behaviour['features'] = X.columns

    corr = []

    for feature in X.columns:
        
        corr.append(np.corrcoef(X[feature], Y)[1][0])

    features_behaviour['pearson'] = corr

    print(features_behaviour.head(1000))

    # -------- XGBoost ------------
    
    model = XGBRegressor(n_jobs=-1, n_estimators=100)

    print(X.columns)
    
    model.fit(X, Y)

    xgbl = []

    i=0

    for feature in X.columns:
        
        xgbl.append(model.feature_importances_[i])
        i=i+1
        
    features_behaviour['xgboost_reg_score'] = xgbl

    X_esc = scaler.fit_transform(X)

    # -------- Lasso ------------

    lasso = (Lasso(alpha=0.1))

    lasso.fit(X_esc, Y)

    lasso_coef = []

    i=0

    for feature in X.columns:
        
        lasso_coef.append(lasso.coef_[i])
        i=i+1
        
    features_behaviour['lasso'] = lasso_coef

    # -------- Linear Regression ------------

    lr = LinearRegression()

    lr.fit(X, Y)

    lr_coef = []

    i=0

    for feature in X.columns:
        
        lr_coef.append(lr.coef_[i])
        i=i+1
        
    features_behaviour['lin_reg_coef'] = lr_coef

    # -------- Random Forest ------------

    rfr = RandomForestRegressor(n_estimators=100, n_jobs=-1)

    rfr.fit(X, Y) 

    rfr_coef = []

    i=0

    for feature in X.columns:
        
        rfr_coef.append(rfr.feature_importances_[i])
        i=i+1
        
    features_behaviour['random_forest_featimportance'] = rfr_coef

    # -------- Support Vector Machine ------------

    svr = svm.LinearSVR()

    svr.fit(X_esc, Y)

    svr_coef = []

    i=0

    for feature in X.columns:
        
        svr_coef.append(svr.coef_[i])
        i=i+1
        
    features_behaviour['svr_coef'] = svr_coef

    # -------- Spearman Corr. ------------

    sp_corr = []

    for feature in X.columns:
        
        sp_corr.append(spearmanr(X[feature], Y)[0])
        
    features_behaviour['spearmanr'] = sp_corr

    return features_behaviour
