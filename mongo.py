#!/usr/bin/env python
from pymongo import MongoClient
import pymongo
from random_words import RandomWords
import random

client = MongoClient()
db = client['test']
collection = db['people']

result = collection.insert_many(
[
	{
			'name': RandomWords().random_word(),
			'age': 0,
			'friends': [],
	}
	for i in range(random.randint(0, 10))
 ])

cursor = collection.find().sort([('age', pymongo.DESCENDING)])
for doc in cursor:
	collection.update_one(doc, { '$set': {'age': doc['age'] + 1} })
	print(doc['name'])

collection.delete_many({"age": {"$gt": 10}})

for doc in cursor:
	collection.update_one(doc, { '$set': {'age': doc['age'] + 1} })
