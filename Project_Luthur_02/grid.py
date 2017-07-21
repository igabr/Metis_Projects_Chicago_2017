import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_predict
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, Imputer, StandardScaler
from sklearn.externals import joblib

from helper_functions import *

final_df = unpickle_object("analysis_dataframe.pkl")


def baseline_model(train_feature, test_feature, train_target, test_target):
    """

    This function performs a baseline model assessment for our dataframe.

    This function is primarily informative, although it does return a fitted model which could be used elsewhere

    Inputs:
        - train_feature - analogous to X_train
        - test_feature - analogous to X_test
        - train_target - analogous to y_train
        - test_target - y_test

    Returns:
        - fittened Linear Regression Model
    """
    top_3_coef = []
    best_feature_index = []

    lin_reg = LinearRegression()
    fitted_model = lin_reg.fit(train_feature, train_target)
    r2_sq = fitted_model.score(test_feature, test_target)
    coef_array = fitted_model.coef_

    print(f"The R2 score of a basline regression model is {r2_sq}")
    print()

    # The mean squared error
    print("Mean squared error: %.2f"
          % np.mean((lin_reg.predict(test_feature) - test_target) ** 2))
    print()

    for index, value in enumerate(coef_array.reshape(-1,1)):
        top_3_coef.append((index, value))

    top_3_coef = sorted(top_3_coef, key=lambda x: x[1], reverse=True)[:3]

    for i in top_3_coef:
        best_feature_index.append(i[0])

    feature_names = list(final_df.iloc[:, best_feature_index].columns)

    print()
    print(f"The top 3 features for predictive power according to the baseline model is {feature_names}")

    joblib.dump(fitted_model, "baseline_linear_regression_model");

    return fitted_model


def regular_grid(lst, features, target):
    """
    This function will run a 'regular grid' meaning that no holdout sets should be passed to the function.

    This function employs cross validation voa the GridSearchCV class.

    Inputs:
        - lst: lst of model names. Should be one of "Ride", "Lasso", "Elastic Net"
        - features: Numpy array consisting of all features to be included in model.
        - target: Numpy array consisting of entire target variable values to be included in model

    Returns:
        - all_results: Dictionary of results of each model specified.
    """
    
    all_results = {}
    
    
    models = {"Ridge": {"clf": Ridge(), "parameters": {'alpha': np.arange(0.1,1000,0.1)}},
         "Lasso": {"clf": Lasso(),"parameters": {'alpha': np.arange(0.1,1000,0.1)}},
         "Elastic Net": {"clf":ElasticNet(),"parameters": {'alpha': [0.01, 0.1, 0.5,1],'l1_ratio': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]}}}
    
    for i in lst:
        
        top_3_coef = []
        
        graphical_info = []
        
        object_ = models[i]['clf']
        
        params = models[i]['parameters']
        
        grid = GridSearchCV(object_, params, cv=11)
        
        fitted_model = grid.fit(features, target)
        
        r_sq = fitted_model.score(features, target)
        
        ideal_param = fitted_model.best_params_
        
        best_cross_val_score = fitted_model.best_score_
        
        best_model = fitted_model.best_estimator_
        
        coef_array = best_model.coef_
        
        for index, value in enumerate(coef_array.reshape(-1,1)):
            top_3_coef.append((index, value))
        
        top_3_coef = sorted(top_3_coef, key=lambda x: x[1], reverse=True)[:3]
        
        for row in fitted_model.grid_scores_:
            alpha = row[0]['alpha']
            mean_score = row[1]
            graphical_info.append((alpha, mean_score))
        
        all_results[i] = {'R_sq': r_sq, "best_model": best_model,
                     "tuned_params": ideal_param,
                     "Best_cv_score": best_cross_val_score,
                    "important_features": top_3_coef,
                    "graphical_info": graphical_info,
                    "grid_object": fitted_model}
        
        joblib.dump(fitted_model, i+"grid_search_model");
    
    return all_results

def holdout_grid(lst, train_feature, test_feature, train_target, test_target):
    """
    This function will run a holdout grid - meaning that train/test splits of the features and target should be passed.

    Implementation of this function relies on teh GridSearchCV class!

    Inputs:
        - lst: lst of model names. Should be one of "Ride", "Lasso", "Elastic Net"
        - train_feature - analogous to X_train
        - test_feature - analogous to X_test
        - train_target - analogous to y_train
        - test_target - y_test

    Returns:
        - all_results: Dictionary of results of each model specified.
    """
    
    all_results = {}
    
    models = {"Ridge": {"clf": Ridge(), "parameters": {'alpha': np.arange(0.1,1000,0.1)}},
         "Lasso": {"clf": Lasso(),"parameters": {'alpha': np.arange(0.1,1000,0.1)}},
         "Elastic Net": {"clf":ElasticNet(),"parameters": {'alpha': [0.01, 0.1, 0.5,1],'l1_ratio': [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]}}}
    
    for i in lst:
        
        top_3_coef = []
        
        graphical_info = []
        
        object_ = models[i]['clf']
        
        params = models[i]['parameters']
        
        grid = GridSearchCV(object_, params, cv=11)
        
        fitted_model = grid.fit(train_feature, train_target)
        
        r_sq = fitted_model.score(test_feature, test_target)
        
        ideal_param = fitted_model.best_params_
        
        best_cross_val_score = fitted_model.best_score_
        
        best_model = fitted_model.best_estimator_
        
        coef_array = best_model.coef_
        
        for index, value in enumerate(coef_array.reshape(-1,1)):
            top_3_coef.append((index, value))
        
        top_3_coef = sorted(top_3_coef, key=lambda x: x[1], reverse=True)[:3]
        
        for row in fitted_model.grid_scores_:
            alpha = row[0]['alpha']
            mean_score = row[1]
            graphical_info.append((alpha, mean_score))
        
        all_results[i] = {'R_sq': r_sq, "best_model": best_model,
                     "tuned_params": ideal_param,
                     "Best_cv_score": best_cross_val_score,
                    "important_features": top_3_coef,
                    "graphical_info": graphical_info,
                    "grid_object": fitted_model}
        
        joblib.dump(fitted_model, i+"grid_search_holdout_model");
    
    return all_results

def extract_model_comparisons(model_1_dict, model_2_dict, model_name):
    """
    This function will compare the results of models run through cross-validation with a holdout and without a holdout.

    This function is informative only.

    Inputs:
        - model_1_dict: A dictionary relating to the CV holdout models
        - model_2_dict: A dictionary relating to the CV non-holdout models

    Returns:
        - None
    """
    
    model_1_feature_index = []

    model_2_feature_index = []

    r_sq_1 = model_1_dict[model_name]['R_sq']
    optimal_params_1 = model_1_dict[model_name]['tuned_params']
    mean_cross_val_score_1 = model_1_dict[model_name]['Best_cv_score']
    model_1_graph_list = model_1_dict[model_name]['graphical_info']
    
    for i in model_1_dict[model_name]['important_features']:
        model_1_feature_index.append(i[0])

    model_1_top_features = list(final_df.iloc[:, model_1_feature_index].columns)


    
    r_sq_2 = model_2_dict[model_name]['R_sq']
    optimal_params_2 = model_2_dict[model_name]['tuned_params']
    mean_cross_val_score_2 = model_2_dict[model_name]['Best_cv_score']
    model_2_graph_list = model_2_dict[model_name]['graphical_info']

    for i in model_2_dict[model_name]['important_features']:
        model_2_feature_index.append(i[0])

    model_2_top_features = list(final_df.iloc[:, model_2_feature_index].columns)
    
    print()
    
    if r_sq_1 > r_sq_2:
        print(f"The Model with the holdout set has a higher R2 of {r_sq_1}. This is higher by {r_sq_1-r_sq_2}")
        print()
        print(f"The optimal parameters for this model are {optimal_params_1}")
        print()
        print(f"The mean cross validation score on the test set is: {mean_cross_val_score_1}")
        print()
        print(f"The most important features accordning to this model is {model_1_top_features}")
    else:
        print(f"The Model with no holdout set has a higher R2 of {r_sq_2}. This is higher by {r_sq_2-r_sq_1}")
        print()
        print(f"The optimal parameters for this model are {optimal_params_2}")
        print()
        print(f"The mean cross validation score for all of the data is: {mean_cross_val_score_2}")
        print()
        print(f"The most important features accordning to this model is {model_2_top_features}")
    
    print()
    print("Graphical Comparison below: ")
    print()
    
    if model_name == "Lasso" or model_name == "Elastic Net":
        x_vals = (-0.2, 1.25)
        y_vals = (-1,1)

    if model_name == "Ridge":
        x_vals = (0,100)
        y_vals = (0.3, 0.5)

        
    plt.figure(figsize=(12,6))
    
    plt.plot(*zip(*model_1_graph_list), '--r') #holdout
    plt.plot(*zip(*model_2_graph_list), '--b') #no holdout
    

    plt.ylim(y_vals)
    plt.xlim(x_vals)
    plt.xlabel("Alpha Value")
    plt.ylabel("Mean Test Score")

    plt.legend(['Holdout Cross-Validation', 'No Holdout Cross-Validation'])
    
    plt.tight_layout()