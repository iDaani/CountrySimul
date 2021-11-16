import json
from pymongo import MongoClient

# Making Connection
client = MongoClient("mongodb://localhost:27017/")



# Connecting to database
db = client["CSCFinalProject"]

# Created or Switched to collection
Collection = db["SampleProject"]

# Finding the document (JSON) from the database
cursor = Collection.find()
docs = list(cursor)

# Printing out the document
print(docs)





