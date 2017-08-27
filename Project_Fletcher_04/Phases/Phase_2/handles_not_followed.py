from tweepy_wrapper import *
from helper_functions import *
from s3 import *

def go():
	"""
	This script will take just under 2 hours to run.
	"""

	working_bucket = view_all_buckets()[0]

	download_from_bucket(working_bucket, "gabr_ibrahim_following_lst.pkl", "gabr_ibrahim_following_lst.pkl")

	download_from_bucket(working_bucket,"following_sample_gabr_ibrahim.pkl","following_sample_gabr_ibrahim.pkl")

	gabr_ibrahim_following = unpickle_object("gabr_ibrahim_following_lst.pkl")

	following_sample = unpickle_object("following_sample_gabr_ibrahim.pkl")

	second_layer = second_layer_following(following_sample)

	pickle_object(second_layer, "second_layer_lst")
	print()
	print("Pickle complete 1")
	upload_to_bucket("second_layer_lst.pkl", "second_layer_lst.pkl", working_bucket)
	print()

	handles_not_followed = distinct(gabr_ibrahim_following, second_layer)

	pickle_object(handles_not_followed, "handles_not_followed")
	print()
	print("Pickle complete 2")
	print()

	upload_to_bucket("handles_not_followed.pkl", "handles_not_followed.pkl", working_bucket)

	print()
	print("script finished")
	print()

if __name__ == '__main__':
	go()

