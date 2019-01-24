import pymongo
import sys
import spir
from module import Item


def connectDB(table_name):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['spider']
    col = db[table_name]
    return col


def insert(d: Item, table_name):
    connectDB(table_name).insert_one(d.__dict__)


def best(table_name):
    i = finddata(table_name)
    next(i)
    return next(i)


def minPrice(table_name):
    i = finddata(table_name)
    row = next(i)
    while True:
        try:
            temp = next(i)
            if temp["price"] < row["price"]:
                row = temp
        except StopIteration:
            return row


def finddata(table_name):
    cn = connectDB(table_name)
    data1 = cn.find({}, {'_id': 0})
    for i in data1:
        yield i


def insertList(goods: str, table_name): 
    url = 'http://search.jd.com/Search?keyword={}&enc=utf-8'.format(goods)
    r = spir.getHTML(url)
    for i in range(30):
        item = Item()
        item = spir.crawl(r, item, i)
        j = item.name.find('<')
        while j != -1:
            rear = item.name.find('>') + 1
            item.name = item.name[: j] + item.name[rear:]
            j = item.name.find('<')
        insert(item, table_name)


if __name__ == '__main__':
    goods = '鞋子'
    # insertList(goods)
    j = finddata(goods)
    for i in j:
        print(i)
