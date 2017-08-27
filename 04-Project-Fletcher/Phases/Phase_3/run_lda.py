from lda import *
from helper_functions import *
from df_functions import *

def go():

	print()
	print("Starting Go function")
	print()

	clean_database = unpickle_object("clean_database.pkl")

	temp_df = make_df(clean_database)

	temp_df = filtration(temp_df, "content")

	final_database = dataframe_to_dict(temp_df)
	
	print("Initial Filtration of 2nd degree connections complete!")
	
	print()

	handle_names = unpickle_object("list_of_handle_names.pkl")

	LDA_Machine(final_database, handle_names)

if __name__ == '__main__':
	go()
