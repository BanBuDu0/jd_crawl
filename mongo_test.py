import pymongo


def insert():
    client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db = client['test_database']
    col = db["test_collection"]  #
    tom = {
        'name': 'Tom',
        'age': 18,
        'sex': '男',
        'hobbies': ['吃饭', '睡觉', '打豆豆']
    }
    alice = {
        'name': 'Alice',
        'age': 19,
        'sex': '女',
        'hobbies': ['读书', '跑步', '弹吉他']
    }
    # col.delete_one(tom)
    col.insert_one(tom)
    col.insert(alice)
    cursor = col.find()
    print(cursor.count())  # 获取文档个数
    for item in cursor:
        print(item)
