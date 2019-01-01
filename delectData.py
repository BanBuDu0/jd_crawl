import pymongo


def connectDB():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['spider']
    col = db['spider']
    return col


if __name__ == '__main__':
    cn = connectDB()
    cn.delete_many({})
