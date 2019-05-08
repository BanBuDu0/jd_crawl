import pymongo
import crawl
from module import Item


def con_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['spider']
    return db


def con_table(table_name):
    db = con_db()
    col = db[table_name]
    return col


def insert(d: Item, table_name):
    con_table(table_name).insert_one(d.__dict__)


def best(table_name):
    rows = find_data(table_name)
    for row in rows:
        if not row['isAD']:
            return row

'''
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
'''


def min_price(table_name):
    cn = con_table(table_name)
    data1 = cn.find({}, {'_id': 0}).sort('price')[0]
    return data1


def find_data(table_name):
    cn = con_table(table_name)
    data1 = cn.find({}, {'_id': 0})
    for i in data1:
        yield i


def find_by_id(table_name, id):
    cn = con_table(table_name)
    return cn.find({'id': id}, {'_id': 0})[0]


def insert_list(goods: str, table_name):
    url = 'https://search.jd.com/Search?keyword={}&enc=utf-8'.format(goods)
    r = crawl.getHTML(url)
    items = crawl.crawl(r)
    for item in items:
        j = item.name.find('<')
        while j != -1:
            rear = item.name.find('>') + 1
            item.name = item.name[: j] + item.name[rear:]
            j = item.name.find('<')
        insert(item, table_name)


if __name__ == '__main__':
    goods = '鞋子'
    # insertList(goods)
    j = find_data(goods)
    for i in j:
        print(i)
