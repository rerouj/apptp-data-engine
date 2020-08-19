from pymongo import MongoClient
from bson.json_util import dumps
import json

client = MongoClient('localhost', 27017)
db = client['apptp-db']

show_collection = db['locations']

from pprint import pprint

doc = show_collection.find({}, {"scripts": 0, "speechToTexts": 0, "_id": 0})

with open('/Users/renato/Admin/master/memoire/db/repo/locations.json', 'w') as file:
    file.write('[')
    for document in doc:
        file.write(dumps(document))
        file.write(',')
    file.write(']')
