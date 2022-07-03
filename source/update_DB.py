import os
import json
from pymongo import MongoClient

# import sqlite3

#MongoDB information
HOST = 'dbsools.wx4vlbk.mongodb.net'
USER = 'Jinskim'
PASSWORD = 'Hu0nncK39KnwIV84'
DATABASE_NAME = HOST.split('.')[0]
COLLECTION_NAME = ['sools', 'reviewSools']
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/?retryWrites=true&w=majority"
# "mongodb+srv://Jinskim:<password>@dbsools.wx4vlbk.mongodb.net/?retryWrites=true&w=majority"

# define obj
client = MongoClient(MONGO_URI)
database = client[DATABASE_NAME]
collection_s = database[COLLECTION_NAME[0]]
collection_p = database[COLLECTION_NAME[1]]
file1 = open("data/json/sools.json")
file2 = open("data/json/reviews.json")

sools = json.load(file1)
reviews = json.load(file2)
collection_s.insert_many(sools);
collection_p.insert_many(reviews);
