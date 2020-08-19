from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['apptp-db']

location_collection = db['location_collection']
tp_shows = db['tp_shows']
