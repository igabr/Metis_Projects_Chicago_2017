from multiprocessing import Pool #witness the power
import wikipedia
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
from bs4 import BeautifulSoup
import seaborn as sns
import pickle
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from fuzzywuzzy import fuzz
from collections import defaultdict

base_url = "https://www.rottentomatoes.com"
starting_url = "https://www.rottentomatoes.com/top/"

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
        else:
            print(f"No data missing in {c} column")

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
        pickle.dump(obj, f)


def unpickle_object(pkl):
    """
    Short helper fucntion to unpickle any object in python

    Inputs:
        - pickle object from disk.

    Returns:
        - unpickled file now available in python namespace
    """
    return pickle.load(open(pkl, 'rb'))

def extract_unique_movies_across_genre(list_of_dicts):
    """
    Short helper function to extract unique movies from a list of dictionaries containing movies across genres.

    Default dict used for speed.

    Inputs:
        - list_of_dicts: list of dictionaries.

    Returns:
        unique_movie_dict: dictionary containing unique movies and their respective information.
    """
    unique_movie_dict = defaultdict()
    for dictionary in list_of_dicts:
        for key, value in dictionary.items():
            if key not in unique_movie_dict:
                unique_movie_dict[key] = value
    return unique_movie_dict

def witness_the_power(func, array):
    """
    My favourite function!

    This function was pivotal in allowing me to scrape all of rotton tomatoes in 30-45 seconds!

    Inputs:
        - func: function to be applied to each element in an array
        - array: array of items that are compatible with the passed func.
    
    Returns:
        - List of results from the func for EACH element in passed array.
            example: if 17 urls in an array, then results will be a list of 17 elements.
                     Each element relating to the output of each element in the input array

    example:
        array is a list of url's
        func is a webscraper
    """
    p = Pool(len(array))
    
    results = p.map(func, array)
    
    p.terminate()
    
    p.join()
    
    return results

def extract_sub_genre_links(webpage):
    """
    Short helper function to help guide my webscraper to sub-links within the same genre.

    Inputs:
        - Takes a webspage url address
    Returns:
        - A list of sub-urls that need to be visited.
    """
    list_of_urls = []
    response = requests.get(webpage)
    raw_html_text = response.text
    soup = BeautifulSoup(raw_html_text, 'lxml')
    
    for i in soup.find(class_='genrelist').find_all('a'):
        path = base_url+i.get('href')
        list_of_urls.append(path)
    
    return list_of_urls

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