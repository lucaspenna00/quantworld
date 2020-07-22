import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from xgboost import XGBRegressor
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import svm
from scipy.stats import spearmanr

def get_feature_importance(X, Y, scaler):

    features = X.columns

    X['controle'] = np.random.normal(0, 1, X.shape[0])

    features_behaviour = pd.DataFrame()

    # -------- Pearson ------------

    features_behaviour['features'] = features

    corr = []

    for feature in X.columns:
        
        corr.append(np.corrcoef(X[feature], Y)[0][1])

    features_behaviour['pearson'] = corr

    # -------- XGBoost ------------
    
    model = XGBRegressor(n_jobs=-1, n_estimators=100)
    
    model.fit(X, Y)

    feature_important = model.get_booster().get_score()

    keys = list(feature_important.keys())

    values = list(feature_important.values())

    data = pd.DataFrame(data=values, index=keys, columns=["score"]).sort_values(by = "score", ascending=False)

    xgbl = []

    for feature in X.columns:
        
        xgbl.append(data.loc[feature]['score'])
        
    features_behaviour['xgboost_reg_score'] = xgbl

    X_esc = scaler.fit_transform(X)

    # -------- Lasso ------------

    lasso = (Lasso(alpha=0.05))

    lasso.fit(X_esc, Y)

    lasso_coef = []

    i=0

    for feature in X.columns:
        
        lasso_coef.append(lasso.coef_[i])
        i=i+1
        
    features_behaviour['lasso'] = lasso_coef

    # -------- Linear Regression ------------

    lr = LinearRegression()

    lr.fit(X_esc, Y)

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
