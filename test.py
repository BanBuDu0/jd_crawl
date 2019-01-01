# -*- coding: UTF-8 -*-
import requests
import re
import pymongo
import db_control
import json


class Item:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.price = 0
        self.seller = ''
        self.img = ''


def connect():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['spider']
    col = db['spider']
    return col


def insert(d: Item):
    if connect().insert_one(d.__dict__):
        return 1
    else:
        return 0


def getHTML(u):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/66.0.3359.139 Safari/537.36'
    }
    r = requests.get(u, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text


def crawl(r, it: Item, count: int):
    pattern = re.compile(r'gl-i-wrap([\S\s]*?)class="p-icons"')
    shop = pattern.findall(r)[count]
    # print(shop)

    p = re.compile(r'data-sku="(.*?)"')
    it.id = p.search(shop).group(1)

    p = re.compile(r'<div class="p-name p-name-type-2">[\S\s]*?<em>(.*?)</em>')
    it.name = p.search(shop).group(1)

    p = re.compile(r'p-price[\S\s]*?<i>(.*?)</i>')
    it.price = float(p.search(shop).group(1))

    p = re.compile(r'p-shop[\S\s]*?title="(.*?)"')
    if p.search(shop) is not None:
        it.seller = p.search(shop).group(1)
    else:
        it.seller = "京东自营"

    p = re.compile(r'p-img[\S\s]*?source-data-lazy-img="(.*?)"')
    it.img = p.search(shop).group(1)


def minComments():
    item = db_control.minPrice()
    id = item['id']
    comments_url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv46561\
                   &productId={}&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&fold=1'.format(id)
    # shopurl = 'https://item.jd.com/{}.html'.format(id)
    r = getHTML(comments_url)
    r = r[(r.find('(') + 1):r.rfind(')')]
    comment_json = json.loads(r)
    return comment_json


def hotcomments():
    comment_json = minComments()
    hot_comments = comment_json['hotCommentTagStatistics']
    ci = {}
    for i in hot_comments:
        ou = i['name'] + '  ' + str(i['count'])
        name = str(i['name'])
        count = float(i['count'])
        s = {
            name: count
        }
        ci.update(s)
    return ci

        
def pcomments():
    comment_json = minComments()
    p_comments = comment_json['comments']
    for i in p_comments:
        print(i['content'])


if __name__ == '__main__':
    minComments()




