import pandas as pd
import string
from nltk.corpus import stopwords
nltk_stopwords = stopwords.words("english")+["rt", "via","-»","--»","--","---","-->","<--","->","<-","«--","«","«-","»","«»"]

def make_df(lst, mongo=False):
    assert type(lst) == list, "Please enter a list of dictionarys"
    
    if mongo:
        for i in lst:
            del i["_id"]
    df = pd.DataFrame.from_dict(lst[0], orient='index')
    
    lst_df = []
    
    for i in lst[1:]:
        lst_df.append(pd.DataFrame.from_dict(i, orient='index'))
    
    df = df.append(lst_df)
    
    return df

def filtration(dataframe, column):
    for handle in dataframe.index:
        for index, tweet in enumerate(dataframe.loc[handle, :][column]):
            tweet = tweet.lower()
            clean = [x for x in tweet.split() if x not in string.punctuation]
            clean = [x for x in clean if x not in nltk_stopwords]
            clean = [x for x in clean if "@" not in x]
            clean = [x for x in clean if "…" not in x]
            clean = [x for x in clean if x[0] not in string.digits]
            clean = [x for x in clean if x[0] not in string.punctuation]
            clean = list(map(lambda x: x.replace("#", ""), clean))
            clean = list(map(lambda x: x.replace('"', ""), clean))
            clean = list(map(lambda x: x.replace(".",""), clean))
            clean = list(map(lambda x: x.replace("-&gt;", ""), clean))
            clean = list(map(lambda x: x.replace("&gt;", "greater than"), clean))
            clean = list(map(lambda x: x.replace("&lt;", "less than"), clean))
            clean = list(map(lambda x: x.replace(":", ""), clean))
            clean = list(map(lambda x: x.replace("&amp;", "&"), clean))
            clean = list(map(lambda x: x.replace("/", ""), clean))
            clean = list(map(lambda x: x.replace("...", ""), clean))
            clean = list(map(lambda x: x.replace("(", ""), clean))
            clean = list(map(lambda x: x.replace(")", ""), clean))
            clean = list(map(lambda x: x.replace("“", '"'), clean))
            clean = list(map(lambda x: x.replace("”", '"'), clean))
            clean = list(map(lambda x: x.replace("’", ""), clean))
            clean = list(map(lambda x: x.replace("-"," "), clean))
            clean = list(map(lambda x: x.replace("*", ""), clean))
            clean = list(map(lambda x: x.replace("!", ""), clean))
            clean = list(map(lambda x: x.replace("⬛️", ""), clean))
            clean = list(map(lambda x: x.replace("\u200d", ""), clean))
            clean = list(map(lambda x: x.replace("\U0001f986", ""), clean))
            clean = list(map(lambda x: x.replace("\U0001f942", ""), clean))
            clean = list(map(lambda x: x.replace("\U0001f92f", ""), clean))
            clean = list(map(lambda x: x.replace("\U0001f911", ""), clean))
            clean = list(map(lambda x: x.replace("[", ""), clean))
            clean = list(map(lambda x: x.replace("]", ""), clean))
            clean = list(map(lambda x: x.replace("{", ""), clean))
            clean = list(map(lambda x: x.replace("}", ""), clean))
            clean = list(map(lambda x: x.replace("ô", "o"), clean))
            clean = list(map(lambda x: x.replace("ó", "o"), clean))
            clean = list(map(lambda x: x.replace("é", "e"), clean))
            clean = list(map(lambda x: x.replace("ï","i"), clean))
            clean = list(map(lambda x: x.replace("®", ""), clean))
            clean = list(map(lambda x: x.replace("á", "a"), clean))
            clean = list(map(lambda x: x.replace("ã", "a"), clean))
            clean = list(map(lambda x: x.replace("ç", "c"), clean))
            clean = list(map(lambda x: x.replace("$", ""), clean))
            clean = list(map(lambda x: x.replace("'ve", ""), clean))
            clean = list(map(lambda x: x.replace("'ll", ""), clean))
            clean = list(map(lambda x: x.replace("n't", ""), clean))
            clean = list(map(lambda x: x.replace("'re", ""), clean))
            clean = list(map(lambda x: x.replace("l'", ""), clean))
            clean = list(map(lambda x: x.replace("?i", ""), clean))
            clean = " ".join(clean)
            dataframe.loc[handle, :][column][index] = clean
    return dataframe


def dataframe_to_dict(dataframe):
    dict_lst = []
    for handle in dataframe.index:
        temp_dict = dict()
        temp_dict[handle] = pd.Series.to_dict(dataframe.loc[handle, :])
        dict_lst.append(temp_dict)
    return dict_lst



