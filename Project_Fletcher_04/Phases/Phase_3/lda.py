import spacy
import nltk
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence
from gensim.corpora import Dictionary, MmCorpus
from gensim.models.ldamulticore import LdaMulticore
import pyLDAvis
import pyLDAvis.gensim
from collections import Counter
from gensim.corpora.dictionary import Dictionary
from tweepy_wrapper import *
from s3 import *
from helper_functions import *
from df_functions import *
nlp = spacy.load('en')

def bag_of_words_generator(lst, dictionary):
	assert type(dictionary) == Dictionary, "Please enter a Gensim Dictionary"
	for i in lst: 
		yield dictionary.doc2bow(i)

def LDA_Machine(lst_dict, handle_lst):
	assert type(lst_dict) == list, "Please enter a list of dictionary's"
	assert type(handle_lst) == list, "Please enter a list of handles"

	file_path_corpus = "/home/igabr/new-project-4/mm_corpus/"

	cnt_1 = -1
	cnt_2 = -1

	for handle in handle_lst:
		cnt_1 += 1

		clean_tweet_list = []

		handle_tweets = lst_dict[cnt_1][handle]['content']

		if handle_tweets == []:
			continue
		else:
			for raw_tweet in handle_tweets:

				clean_tweet = ""

				tokenized_tweet = nlp(raw_tweet)

				for token in tokenized_tweet:
					if token.is_space:
						continue
					elif token.is_punct:
						continue
					elif token.is_stop:
						continue
					elif token.is_digit:
						continue
					elif len(token) == 1:
						continue
					elif len(token) == 2:
						continue
					else:
						clean_tweet += str(token.lemma_) + " "

				clean_tweet_list.append(clean_tweet)
			clean_tweet_list = list(map(str.strip, clean_tweet_list))
			clean_tweet_list = [x for x in clean_tweet_list if x != ""]
			lst_dict[cnt_1][handle]['tokenized_tweets'] = clean_tweet_list
			print("{} tokenized_tweets inserted!".format(handle))
			print()

	master_df = make_df(lst_dict)

	to_remove = list(master_df[master_df['tokenized_tweets'].isnull()].index)

	index_to_remove = []
	for i in to_remove:
		index_to_remove.append(handle_lst.index(i))

	new_handle_list = [v for i,v in enumerate(handle_lst) if i not in frozenset(index_to_remove)]

	master_df.dropna(subset=['tokenized_tweets'], inplace=True)
    
	master_df = filtration(master_df, "tokenized_tweets")

	clean_lst_dict = dataframe_to_dict(master_df)
	print()
	print("Cleaning of master dataframe complete!")

	for handle in new_handle_list:
		cnt_2 += 1

		try:
			list_of_tweets = clean_lst_dict[cnt_2][handle]['tokenized_tweets']
		except KeyError:
			continue

		gensim_format_tweets = []

		for tweet in list_of_tweets:
			list_form = tweet.split()
			gensim_format_tweets.append(list_form)

		gensim_dictionary = Dictionary(gensim_format_tweets)
		gensim_dictionary.filter_extremes(no_below=10, no_above=0.4)
		gensim_dictionary.compactify() # remove gaps after words that were removed

		MmCorpus.serialize(file_path_corpus+"{}.mm".format(handle), bag_of_words_generator(gensim_format_tweets, gensim_dictionary))

		corpus = MmCorpus(file_path_corpus+"{}.mm".format(handle)) #loading the corpus from disk

		if corpus.num_terms == 0:
			continue
		else:
			lda = LdaMulticore(corpus, num_topics=10, id2word=gensim_dictionary, passes=100, workers=100)
			lda.save(file_path_corpus+"lda_model_{}".format(handle))
			print("LDA model for {} saved!".format(handle))

			word_list = []

			for i in range(10):
				for term, frequency in lda.show_topic(i, topn=100):
					if frequency != 0:
						word_list.append(term)

			LDA_Counter = Counter(word_list)

			clean_lst_dict[cnt_2][handle]['LDA'] = LDA_Counter
			print("Inserted LDA Counter into {} dictionary".format(handle))

	pickle_object(clean_lst_dict, "2nd_degree_connections_LDA_complete")
	print("Script Complete")

