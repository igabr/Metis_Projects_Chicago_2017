import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

def unique_pairs(df):
	'''Get diagonal and lower triangular pairs of correlation matrix'''
	drop_cols = set()
	cols = df.columns
	for i in range(0, df.shape[1]):
		for j in range(0, i+1):
			drop_cols.add((cols[i], cols[j]))
	return drop_cols

def extract_top_correlations(df, n=5):
	"""
	Extract the columns which are highly correlated.

	Default value is top 5 columns. Play with this if you have a threshold in mind.

	"""
	corr_matrix = df.corr().abs().unstack()
	unique_cols = unique_pairs(df)
	corr_matrix = corr_matrix.drop(labels=unique_cols).sort_values(ascending=False)
	return corr_matrix[0:n]


def skew(mean, median):
    if mean > median:
        print("Right skew")

    if mean < median:
        print("Left Skew")

    diff = mean - median

    print("Diff between mean and median is : {}".format(diff))


def lookup_description(col_name):
    return data_dict[col_name]


def percentage_missing(df):
    """
    Calculates missing data for each column in a dataframe.

    This function is informative.

    Inputs:
        - df: Pandas dataframe

    Returns:
        - None
    """
    for c in df.columns:
        missing_perc = (sum(pd.isnull(df[c]))/len(df))*100
        if missing_perc > 0:
            print("%.1f%% missing from: Column %s" %(missing_perc, c))

def pickle_object(obj, name):
    """
    Short helper function to pickle any object in python

    WARNING: NOT FOR USE WITH BEAUTIFULSOUP OBJECTS - see bs4 documentation.

    Inputs:
        - obj: Python object to be pickled
        - name: resulting name of pickle file. NOTE: No need to add .pkl in the name

    Returns:
        - None. Function writes straight to disk.
    """
    with open(name+".pkl", 'wb') as f:
        pickle.dump(obj, f, protocol=4)


def unpickle_object(pkl):
    """
    Short helper fucntion to unpickle any object in python

    Inputs:
        - pickle object from disk.

    Returns:
        - unpickled file now available in python namespace
    """
    return pickle.load(open(pkl, 'rb'))

data_dict = unpickle_object("data_dict.pkl")

def plot_corr_matrix(data):

    '''

    Heatmap of correlation matrix

    Inputs: dataframe

    Returns: Heatmap

            (Green + corr. Red - corr.)

    '''

    sns.set(font_scale=1.4)#for label size

    ax = plt.axes()

    sns.heatmap(data.corr(), square=True, cmap='RdYlGn')

    ax.set_title('Correlation Matrix')

#functions below relate to logisitic regression coef interpretation
def convert_to_prob(coef):
    numerator = np.exp(coef)

    denom = 1 + np.exp(coef)

    return numerator/denom

def convert_to_odds(coef):
    return np.exp(coef)

def compare_odds(odd1, odd2):
    return odd1/odd2
