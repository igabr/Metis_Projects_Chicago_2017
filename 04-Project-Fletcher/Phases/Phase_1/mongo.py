from pymongo import MongoClient
from pymongo import errors
from pymongo.collection import Collection
from pymongo.database import Database
from pprint import pprint

client = MongoClient()
prefix = str(client)+"."

def view_all_dbs(): #done
	"""
	Argument Order: None

	Shows all databases currently in MongoDB
	"""
	return client.database_names()

def drop_database(db_name, safety=True): #done
	"""
	Argument Order: db_name

	Safety defaults to True - this will initialize a confirmation request from the user to delete the database.

	db can be a database type or a string

	Drops a database in mongoDB
	"""
	if type(db_name) == str:

		if db_name not in client.database_names():
			print("{} is not a current database - nothing to drop".format(db_name))
		else:
			if safety:
				check = input("Are you sure you want to delete {}. [y/n]: ".format(db_name))
				print()
				
				if check == "y":
					client.drop_database(db_name) #can take a string
					print("{} has been deleted".format(db_name))
				else:
					print("Deletion aborted")
			else:
				client.drop_database(db_name)
				print("{} has been deleted".format(db_name))
	else:
		if db_name.name not in client.database_names():
			print("{} database has not been created lazily yet - nothing to drop".format(db_name.name))
		else:
			if safety:
				check = input("Are you sure you want to delete {}. [y/n]: ".format(db_name.name))
				print()
				if check == "y":
					client.drop_database(db_name)
					print("{} has been deleted".format(db_name.name))
				else:
					print("Deletion aborted")
			else:
				client.drop_database(db_name)
				print("{} has been deleted".format(db_name.name))

def view_collections_in_db(db_name):
	"""
	Argument Order: db_name

	Will return a list of collection names
	"""
	if type(db_name) == str:

		if db_name not in client.database_names():
			print("{} is not a current database - no collections".format(db_name))
		else:
			db = eval(prefix+db_name)
			return db.collection_names()
	else:
		if db_name.name not in client.database_names():
			print("{} database has not been created lazily yet - add a collection to create it".format(db_name.name))
		else:
			return db_name.collection_names()

def connect_to_db(db_name):
	"""
	Argument Order: db_name

	This is a lazy operator, database isnt actually created until a collection is placed in it.

	Will return a database object
	"""
	assert type(db_name) == str, "Pass the database name as a string"

	if db_name in view_all_dbs():
		print("This database is already present in MongoDB")
	else:
		print("{} database is not present in MongoDB - it will be created lazily".format(db_name))

	return eval(str(client)+"."+str(db_name))

def connect_to_collection(db, collection_name):
	"""
	Argument Order: db, collection name
	Connect to a collection in a database

	returns a collection object
	"""
	assert type(db) == Database, "Please pass in a datbase object"

	if collection_name not in db.collection_names():
		print("This collection does not exist in the {} database".format(db.name))
	else:
		print("You are now connected to the {} collection in the {} database".format(collection_name, db))
		return db[collection_name]

def insert_collection(db, collection_name):
	"""
	Argument Order: db, collection_name

	Note: Collections are added in place.

	This function returns the collection object. This is excellent for further actions on the collection.
	"""
	assert type(db) == Database, "Please pass in a database object"
	
	try:
		collection = db.create_collection(collection_name)
		print("{} collection created in {} database".format(collection_name, db.name))
		return collection
	except errors.CollectionInvalid as e:
		print("This collection already exists. Access with {}.{}".format(db.name, collection_name))

def remove_collection(db, collection_name, safety=True):
	"""
	Argument Order: db, collection name
	Safety defaults to True - this will initialize a confirmation request from the user to delete the collection.
	Can take collection object or name of collection
	"""
	assert type(db) == Database, "Please pass in a database object"
	
	if type(collection_name) == str:
		if safety:
			check= input("Are you sure you want to delete {} from the {} database. [y/n]: ".format(collection_name, db.name))
			print()
			if check == "y":
				db.drop_collection(collection_name)
				print("{} removed from{}".format(collection_name, db.name))
			else:
				print("Removal Aborted")
		else:
			db.drop_collection(collection_name)
			print("{} removed from{}".format(collection_name, db.name))
	else:
		if safety:
			check= input("Are you sure you want to delete {} from the {} database. [y/n]: ".format(collection_name.name, db.name))
			print()
			if check == "y":
				db.drop_collection(collection_name)
				print("{} removed from {}".format(collection_name.name, db.name))
			else:
				print("Removal Aborted")
		else:
			db.drop_collection(collection_name)
			print("{} removed from {}".format(collection_name.name, db.name))


def size_of_collection(collection):
	"""
	Must enter a collection.

	Returns count of records inside the collection
	"""
	assert type(collection) == Collection, "Enter a collection!"

	print("The {} collection in the {} database has {} entries".format(collection.name, collection.database.name, collection.count()))

	return collection.count()

def display_first_20_in_collection(collection):
	"""
	Must enter a collection.

	Returns the first 20 documents in a collection
	"""
	assert type(collection) == Collection, "Enter a collection!"

	for post in collection.find(limit=20):
		pprint(post)
		print()

def insert_one_into_collection(collection, item):
	"""
	Argument Order: collection, item

	Inserts a single item into the collection
	"""
	assert type(collection) == Collection, "Enter a collection!"
	assert type(item) == dict, "Item must be a dictionary!"

	collection.insert_one(item)

	print("Inserted {} into {} collection inside {} database".format(list(item.keys())[1], collection.name, collection.database.name))

def insert_many_into_collection(collection, lst):
	"""
	Argument Order: collection, lst

	Inserts multiple items into a collection.
	"""
	assert type(collection) == Collection, "Enter a collection!"
	assert type(lst) == list, "Enter a list of dictionary's!"

	collection.insert_many(lst)

	print("Inserted a list with {} records into {} collection inside {} database".format(len(lst), collection.name, collection.database.name))

def display_all_in_collection(collection, item):
	"""
	Argument Order: collection, item

	Find's all instances of an item in a collection.

	This should be used likea search tool!

	Provides information about the count too.
	"""
	assert type(collection) == Collection, "Enter a collection!"
	assert type(item) == dict, "Item must be a dictionary!"

	print("{} records match your query in {}, located in {} database".format(collection.find(item).count(), collection.name, collection.database.name))
	print()

	for record in collection.find(item):
		pprint(record)
		print()
		print()

# def all_documents_in_collection(collection):
# 	"""
# 	Returns a cursor object that needs to be iterated over!
# 	"""
# 	assert type(collection) == Collection, "Enter a collection!"

# 	return collection.find()

def extract_all_documents_in_collection(collection):
	"""
	Returns a list of all documents in a collection.

	This will be a list of dict's
	"""

	assert type(collection) == Collection, "Enter a collection!"

	lst_docu = []

	for document in collection.find():
		lst_docu.append(document)

	return lst_docu

def delete_document_from_collection(collection, item, many=False, safety=True):
	"""
	Argument Order: collection, item, many=False, Safety=True

	safety defaults to True - this will initialize a confirmation request from the user to delete the document.

	many defaults to False - this will only delete the first document that matches the query.

	If many set to True - all documents matching query will be deleted.
	"""
	assert type(collection) == Collection, "Enter a collection!"
	assert type(item) == dict, "Item must be a dictionary"

	if safety:

		check = input("Are you sure you want to delete {} from the {} collection in {} database? [y/n]: ".format(item, collection.name, collection.database.name))
		print()

		if check =='y':
			if many:
				collection.delete_many(item)
				print("Deleted all documents matching the query {} from {} collection in the {} database".format(item, collection.name, collection.database.name))
			else:
				collection.delete_one(item)
				print("Deleted a single document matching the query {} from {} collection in the {} database".format(item, collection.name, collection.database.name))
		else:
			print("Deletion Aborted")
	else:
		if many:
			collection.delete_many(item)
			print("Deleted all documents matching the query {} from {} collection in the {} database".format(item, collection.name, collection.database.name))
		else:
			collection.delete_one(item)
			print("Deleted a single document matching the query {} from {} collection in the {} database".format(item, collection.name, collection.database.name))
