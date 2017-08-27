#tweepy wrapper
import tweepy
from helper_functions import *
import os
import time
auth = tweepy.AppAuthHandler(os.environ["TWITTER_CONSUMER_KEY"], os.environ["TWITTER_CONSUMER_SECRET"]) #higher limits
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
from tweepy.models import Status, ResultSet
import re
from datetime import datetime
import random

def view_rate_limits():
	"""
	View's key rate limits for Twitter REST API with application authentication.
	"""

	rate_limit_dict = api.rate_limit_status()['resources'] #only one API call!

	follow_remain = rate_limit_dict["friends"]['/friends/list']['remaining']

	follow_reset_time = convert_UNIX_time(rate_limit_dict["friends"]['/friends/list']['reset'])

	search_remain = rate_limit_dict['search']['/search/tweets']['remaining']

	search_reset_time = convert_UNIX_time(rate_limit_dict['search']['/search/tweets']['reset'])

	application_remain = rate_limit_dict['application']['/application/rate_limit_status']['remaining']

	application_reset_time = convert_UNIX_time(rate_limit_dict['application']['/application/rate_limit_status']['reset'])

	user_remain = rate_limit_dict['statuses']['/statuses/user_timeline']["remaining"]

	user_reset = convert_UNIX_time(rate_limit_dict['statuses']['/statuses/user_timeline']["reset"])

	print("""
		Search Remaining: {}, Search Reset: {}

		Follow Remaining: {}, Follow Reset: {}

		User Remaining: {}, User Reset: {}

		Application Remaining: {}, Application Reset: {}

		The Current time is: {}
		""".format(search_remain, search_reset_time, follow_remain, follow_reset_time, user_remain, user_reset, application_remain, application_reset_time, datetime.now().time()))


def search_twitter(query, number):
	"""
	Argument Order: query, number

	Will search twitter for the query. Query can be a list.
	Number relates to how many tweets

	Returns a list of tweets
	"""
	assert type(query) == str, "Please enter a query in the form of a string"
	assert type(number) == int, "Please enter the number of as an integer"

	return list(tweepy.Cursor(api.search, q=query, lang='en', tweet_mode='extended').items(number))

def extract_handle(tweet):
	"""
	Argument Order: tweet

	Extracts the twitter handle for a given tweet. @ symbol not included.

	Returns the handle - string type
	"""
	assert type(tweet) == Status, "Please enter in a tweet of type Status"

	return tweet.__dict__['user'].screen_name

def extract_text(tweet):
	"""
	Argument Order: tweet

	Extracts the clean text of a tweet. Remove links and emoji's
	Returns clean text of the tweet
	"""

	#this function can be mapped to a list of tweets (status type)

	assert type(tweet) == Status, "Please enter in a tweet of type Status"

	regex = r"http\S+"
	subset = ""

	emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

	if hasattr(tweet, "text"):
		clean = re.sub(regex, subset, tweet.text.strip())
		clean = emoji_pattern.sub(subset, clean).strip()
	else:
		clean = re.sub(regex, subset, tweet.full_text.strip())
	return clean

# def extract_hashtags(tweet):
# 	"""
# 	Argument Order: tweet

# 	Returns hastags present in a given tweet

# 	list(map(extract_hashtags, no_rt_gabr))
# 	"""
# 	assert type(tweet) == Status, "Please enter in a tweet of type Status"
	
# 	if hasattr(tweet, "text"):
# 		return [i for i in tweet.text.split() if i.startswith("#")]
# 	else:
# 		return [i for i in tweet.full_text.split() if i.startswith("#")]

def extract_hashtags(tweet):
	"""
	Argument Order: tweet

	Return a list of hastags present in a given tweet
	"""
	hashtags = []
	assert type(tweet) == Status, "Please enter in a tweet of type Status"

	if hasattr(tweet, "entities"):
		if tweet.entities['hashtags'] == []:
			return []
		else:
			for i in tweet.entities['hashtags']:
				hashtags.append(i['text'])
	else:
		print("No entity method!")
	return hashtags


def extract_datetime(tweet):
	"""
	Argument Order: tweet

	Returns a datetime object
	"""
	assert type(tweet) == Status, "Please enter in a tweet of type Status"

	return tweet.created_at

def extract_users_tweets(handle, number):
	"""
	Argument Order: handle, number of tweets to extract
	
	Extract's a user's tweets
	"""
	final = ResultSet() #can change to resultset later if I want

	try:
		for status in tweepy.Cursor(api.user_timeline, screen_name=handle, count=200, include_rts=True).items(number):
			final.append(status)
	except:
		print("{} is a protected user!")
		return []

	return final

# def remove_retweets(lst):
# 	"""
# 	Given a ResultSet of tweets, removes those that are RT's

# 	Returns a ResultSet.
# 	"""
# 	assert type(lst) == ResultSet, "Please enter a ResultSet of user's tweets to be filtered."

# 	final = ResultSet() 

# 	if hasattr(lst[0], "text"):

# 		aux = (x for x in lst if "RT @" not in x.text) #dont need it to be a list

# 		for i in aux:
# 			final.append(i)
# 	else:
# 		aux = (x for x in lst if "RT @" not in x.full_text) #dont need it to be a list

# 		for i in aux:
# 			final.append(i)

# 	return final

def average_retweets(lst, handle):
	"""
	Argument Order: lst, handle

	Given a ResultSet of tweets, calculate the average retweet count for all tweets in ResultSet.

	Be sure to only apply this on a ResultSet that excludes retweets.

	This function would be amazing with firehose API
	"""
	assert type(lst) == ResultSet, "Please enter a ResultSet of user's tweets."

	count = 0
	
	for tweet in lst:
		count += tweet.retweet_count

	return count/len(lst)

def get_all_following(handle):
	"""
	Argument Order: handle

	Returns all the followers for a particular handle.

	Warning: This burns through rate limit
	"""
	final = []

	for friend in tweepy.Cursor(api.friends, screen_name=handle, count=200).items():
		final.append(friend.screen_name)
	return final

def get_100_following(handle):
	"""
	Argument Order: handle

	Returns the 100 most recent handles that the specified user followed.

	This function has been optimised for rate limiting.

	NOTE: If given access to firehose API - this function could be altered slightly to obtain all friends.
	"""

	final = []

	try:
		for friend in tweepy.Cursor(api.friends, screen_name=handle, count=100).items(100):
			final.append(friend.screen_name)
	except:
		print("Skipping - {} has protected tweets!".format(handle))
		return []

	return final

def second_layer_following(lst):
	"""
	Argument Order: lst

	For a given list of twitter handles, extract who they follow.

	This function will only extract the first 100 of followers for a given handle - this is due to rate limiting.

	This function will return a 'flat' list of all followers.

	NOTE: If given access to firehose API - this function could be altered slightly to obtain the entire secondary layer
	"""
	cnt = 0

	second_layer = []

	for handle in lst:
		print("processing {}".format(handle))
		second_layer.append(get_100_following(handle))
		print()
		cnt+= 1
		if cnt%10 == 0:
			print()
			print("processed {} handles from a total of {}".format(cnt, len(lst)))
			print()

	flat_second_layer = sum(second_layer, [])

	return flat_second_layer

def random_sample_lst(lst):
	"""
	Argument Order: lst

	Extracts the a random 25% of a given list
	"""
	return random.sample(lst, len(lst)//4)

def distinct(lst1, lst2):
	"""
	Argument order: source following list, accumulated source's following list
	"""

	following = lst1

	second_layer_following = lst2

	unique = set(following)

	final = [x for x in second_layer_following if x not in unique]

	return final






