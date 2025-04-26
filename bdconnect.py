import pymongo
import json
from pymongo import MongoClient, InsertOne

def insert_data_to_mongo(filename):
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/jupitor")
    db = client.AILog
    collection = db.YoutubeCollections

    requesting = []

    with open(f"{filename}.json") as f:
        for jsonObj in f:
            myDict = json.loads(jsonObj)
            requesting.append(InsertOne(myDict))

    result = collection.bulk_write(requesting)
    client.close()

    print(f"Inserted {result.inserted_count} documents into the collection.")