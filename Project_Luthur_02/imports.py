"""
This python file contains imports I use often.

Instead of typing them all out into a Jupyter Notebook cell

I can just type %run imports.py and I'll have everything I need.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from datetime import datetime
import re
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, Imputer, StandardScaler
from sklearn.externals import joblib


###general use parameters - alter as desired!
plt.rcParams["figure.figsize"] = (15,10)
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["axes.labelsize"] = 20
plt.rcParams['legend.fontsize'] = 22


 