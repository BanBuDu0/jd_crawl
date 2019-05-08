import pymongo


def insert():
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = client['spider']
    col = db["gtx1060"]  #
    data1 = col.find({}, {'_id': 0}).sort('price')[1]
    print(type(data1))

insert()