from helper_functions import *
from mongo import *
from tweepy_wrapper import *
from s3 import *
import random

def go():

	working_bucket = view_all_buckets()[0]

	handles_not_followed = unpickle_object("handles_not_followed.pkl")

	handle_sample = random.sample(handles_not_followed, int(0.05*len(handles_not_followed))+1)

	handle_sample = list(set(handle_sample)) #ensure's unique handle's

	pickle_object(handle_sample, "handle_sample")

	print()
	print("Pickled handle sample")
	print()

	upload_to_bucket("handle_sample.pkl","handle_sample.pkl", working_bucket)
	print()

	handle_extraction_db = connect_to_db("handle_extraction_db")
	print()

	tweets_collection = insert_collection(handle_extraction_db, "tweets")
	print()
	print(type(tweets_collection), "---------------------------")

	for handle in handle_sample:
		print(handle, "-----------------------")
		mongo_dict = dict()
		mongo_dict[handle] = {"content": [], "hashtags": [], "retweet_count" : [], "favorite_count": []}
		tweets = extract_users_tweets(handle, 200)

		for tweet in tweets:
			content = extract_text(tweet) #returns a string
			hashtags = extract_hashtags(tweet) #returns a list
			rts_count = tweet.retweet_count
			fav_count = tweet.favorite_count

			mongo_dict[handle]["content"].append(content)

			mongo_dict[handle]["hashtags"].append(hashtags)

			mongo_dict[handle]['retweet_count'].append(rts_count)

			mongo_dict[handle]['favorite_count'].append(fav_count)

		insert_one_into_collection(tweets_collection, mongo_dict)
		print()

	print("Script Finished")


if __name__ == '__main__':
	go()
