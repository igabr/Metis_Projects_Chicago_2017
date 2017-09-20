import pandas as pd
import numpy as np
import string
from nltk.corpus import stopwords
nltk_stopwords = stopwords.words("english")+["rt", "via","-»","--»","--","---","-->","<--","->","<-","«--","«","«-","»","«»", " →", "→"]
punc = '!"%&\'()*+,-./:;<=>?@[\\]^_`{|}~'


def filtration_1(dataframe, column_to_clean, new_col):
	cleaned_tweets = []
	for label in dataframe.index:
		tweet = dataframe.loc[label, :][column_to_clean]
		tweet = tweet.lower()
		clean = [x for x in tweet.split() if x not in string.punctuation]
		clean = [x for x in clean if x not in nltk_stopwords]
		clean = [x for x in clean if "@" not in x]
		clean = [x for x in clean if "฿" not in x]
		clean = [x for x in clean if x[0] not in string.digits]
		clean = [x for x in clean if x[0] not in punc]
		clean = [x for x in clean if len(x) != 1]
		clean = " ".join(clean)
		clean = clean.strip()
		cleaned_tweets.append(clean)

	dataframe[new_col] = cleaned_tweets
	
	return dataframe

def filtration_2(dataframe, column):

	# clean = list(map(lambda x: x.replace("#", ""), clean)) #we want to maintain hashtags!
	dataframe[column] = dataframe[column].apply(lambda x: x.replace('"', ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("♬♫♩♪", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("…", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(".",""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("⋆", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ⋆ ", " "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("#rt", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("#re", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" alime ", " all time "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" alltime ", " all time "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" →", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("alime", "all time "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("atm", "at the moment"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ath ", " all time high "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("str8", "straight"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" v ", " very "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" #d", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ddos ", " distributed denial of service "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("btce", "btc"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("bitcoina", "bitcoin"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("rbitcoin", "bitcoin"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" – ", " "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("-&gt;", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ➤ ", " "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("◄►", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("◄", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ur ", " your "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" u ", " you "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("forthen", "for then"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("&gt;", "greater than"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("&lt;", "less than"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("lt", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("gt", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(":", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("&amp;", "and"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("ampamp", "and"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("amp", "and"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" amp ", " and "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" bu ", " but "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("/", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("...", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("(", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(")", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("“", '"'))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("”", '"'))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("‘", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("’", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("-"," "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("*", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("!", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("⬛️", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("\u200d", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001f986", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001f942", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001f92f", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001f911", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("\U0001F193", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" ⭕ ", " "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("🤔", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("☞ ", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("[", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("]", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("{", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("}", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("ô", "o"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("ó", "o"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("é", "e"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("ï","i"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("®", ""))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("á", "a"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("ã", "a"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("ç", "c"))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" jan ", " january "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" feb ", " february "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" mar ", " march "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" apr ", " april "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" jun ", " june "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" jul ", " july "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" aug ", " august "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" sept ", " september "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" oct ", " october "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" nov ", " november "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace(" dec ", " december "))
	dataframe[column] = dataframe[column].apply(lambda x: x.replace("washinon", "washington"))
	return dataframe
