from tweepy_wrapper import *
from s3 import *
from helper_functions import *
from mongo import *
from df_functions import *
import string
import nltk
import spacy
nlp = spacy.load('en')
stopwords = nltk.corpus.stopwords.words('english')
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from sklearn.cluster import KMeans

handles_to_follow_list = unpickle_object("final_database_lda_verified.pkl")

handle_names = unpickle_object("verified_handles_lda.pkl")

temp_follow_df = make_df(handles_to_follow_list)

temp_follow_df = filtration(temp_follow_df, "content")

handles_to_follow_list = dataframe_to_dict(temp_follow_df)

def go():

	cnt = -1

	for handle in handle_names:
		cnt += 1
		text = []
		totalvocab_1 = []
		totalvocab_2 = []
		sentence = ""
		print("processing {}".format(handle))

		tweets = handles_to_follow_list[cnt][handle]['content']

		for tweet in tweets:
			
			to_process = nlp(tweet)

			for token in to_process:
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
					sentence += str(token.lemma_) + " "
					totalvocab_1.append(str(token.lemma_))
					totalvocab_2.append(str(token.lemma_))
			text.append(sentence)

		handles_to_follow_list[cnt][handle]["temp_tfidf"] = text
		temp_df = pd.DataFrame.from_dict(handles_to_follow_list[cnt], orient='index')
		temp_df = filtration(temp_df, "temp_tfidf")
		handles_to_follow_list[cnt] = dataframe_to_dict(temp_df)[0]
		text = handles_to_follow_list[cnt][handle]["temp_tfidf"]
		del handles_to_follow_list[cnt][handle]["temp_tfidf"]

		vocab_frame = pd.DataFrame({'words': totalvocab_1}, index = totalvocab_2)
		tfidf_vectorizer = TfidfVectorizer(max_features=200000, stop_words='english', ngram_range=(0,2))
		tfidf_matrix = tfidf_vectorizer.fit_transform(text)
		
		if tfidf_matrix.shape[0] < 10:
			num_clusters = tfidf_matrix.shape[0]
		else:
			num_clusters = 10 
		
		terms = tfidf_vectorizer.get_feature_names()
		km = KMeans(n_clusters=num_clusters, n_jobs=-1)
		km.fit(tfidf_matrix)
		clusters = km.labels_.tolist()
		order_centroids = km.cluster_centers_.argsort()[:, ::-1] 
		cluster_dict = dict()

		for i in range(num_clusters):
			for ind in order_centroids[i, :20]:
				word = str(vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0])
				if i not in cluster_dict:
					cluster_dict[i] = [word]
				else:
					cluster_dict[i].append(word)

		cluster_values = []

		for k,v in cluster_dict.items():
			cluster_values.extend(v)

		counter_tfidf = Counter(cluster_values)

		handles_to_follow_list[cnt][handle]['tfid_counter'] = counter_tfidf

		counter_lda = handles_to_follow_list[cnt][handle]["LDA"]

		tfidf_set = set()

		lda_set = set()

		for key, value in counter_tfidf.items():
			tfidf_set.add(key)

		for key, value in counter_lda.items():
			lda_set.add(key)

		intersection_set = lda_set.intersection(tfidf_set)

		handles_to_follow_list[cnt][handle]["lda_tfid_intersection"] = intersection_set

		print("loop complete for {}".format(handle))

	pickle_object(handles_to_follow_list, "FINAL_2ND_DEGREE_DATABASE_LDA_TFIDF_VERIFIED.pkl")

	print("Script Complete")

if __name__ == '__main__':
	go()







