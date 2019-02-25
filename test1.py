import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['spider']
colist = db.list_collection_names()
print(colist)
