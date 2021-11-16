import json
from pymongo import MongoClient


# Making a connection with the database
client = MongoClient('mongodb://localhost:27017/')

# Database
db = client['CSCFinalProject']

# Created or switched to the Collection
collection = db['SampleProject']

# Loading/Opening the JSON file
with open('sample.json') as f:
    file_data = json.load(f)

# Inserting data in the database

collection.insert_one(file_data)