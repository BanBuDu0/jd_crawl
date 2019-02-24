# -*- coding: UTF-8 -*-
import requests
import re
import json
import db_control
from module import Item


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
    pattern = re.compile(r'<li([\S\s]*?)class="p-icons"')
    shop = pattern.findall(r)[count]
    # print(shop)

    p = re.compile(r'data-sku="(.*?)"')
    it.id = p.search(shop).group(1)

    p = re.compile(r'p-price[\S\s]*?<i>(.*?)</i>')
    try:
        it.price = float(p.search(shop).group(1))
    except:
        p = re.compile(r'data-price="(.*?)"')
        it.price = float(p.search(shop).group(1))

    p = re.compile(r'<div class="p-name p-name-type-2">[\S\s]*?<em>(.*?)</em>')
    it.name = p.search(shop).group(1)

    p = re.compile(r'p-shop[\S\s]*?title="(.*?)"')
    if p.search(shop) is not None:
        it.seller = p.search(shop).group(1)
    else:
        it.seller = "京东自营"

    # p = re.compile(r'p-img[\S\s]*?source-data-lazy-img="(.*?)"')
    # it.img = p.search(shop).group(1)
    return it


def comments(i, item: {}):
    # item = db_control.minPrice()
    goodsID = item['id']
    comments_url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv46561\
    &productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(goodsID, i)
    # shopurl = 'https://item.jd.com/{}.html'.format(id)
    r = getHTML(comments_url)
    r = r[(r.find('(') + 1):r.rfind(');')]
    r = r.replace('\\', '\\\\')
    comment_json = json.loads(r)
    return comment_json


def hotcomments(item: {}):
    comment_json = comments(1, item)
    hot_comments = comment_json['hotCommentTagStatistics']
    ci = {}
    for i in hot_comments:
        name = str(i['name'])
        count = float(i['count'])
        ci.update({name: count})
    return ci


def pcomments(i, item):
    # for i in range(10):
    comment_json = comments(i, item)
    p_comments = comment_json['comments']
    for j in p_comments:
        yield j['content']
