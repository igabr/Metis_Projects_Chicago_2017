from helper_functions import *
import spacy
nlp = spacy.load('en')
import random

follower_db = unpickle_object("FINAL_2ND_DEGREE_DATABASE_LDA_TFIDF_VERIFIED.pkl.pkl")

gabr_db = unpickle_object("FINAL_GABR_DATABASE_LDA_TFIDF_VERIFIED.pkl")

handles = unpickle_object("verified_handles_lda.pkl")

def go(phrase):

	phrase = phrase.lower()

	handles_to_follow = []

	word_list = []
	to_process = nlp(phrase)

	for token in to_process:
		word_list.append(token.lemma_)

	cnt = -1

	for handle in handles:
		cnt += 1

		for word in word_list:
			if word in follower_db[cnt][handle]['lda_tfid_intersection']:
				handles_to_follow.append(handle)


	print("The topics of {} are present in the following handles: ".format(phrase.split()))
	print()

	unique_lst = list(set(handles_to_follow))

	if len(unique_lst) < 5:
		to_search = unique_lst
	elif len(unique_lst) == 0:
		to_search = "Sorry, we don't have suggestions for that topic!"
	else:
		to_search = random.sample(unique_lst, 5)

	to_search = random.sample(unique_lst, 5)

	print("Here are 5 handles randomly selected from the overall list:")
	print()
	print(to_search)
	print()

if __name__ == '__main__':
	to_input = input("What topics are of interest to you? : ")
	go(to_input)


