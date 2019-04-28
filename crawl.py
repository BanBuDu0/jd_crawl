# -*- coding: UTF-8 -*-
import requests
import re
import json
from module import Item
from bs4 import BeautifulSoup
import time


def getHTML(u, data=None):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Referer': 'https://item.jd.com'
    }
    r = requests.get(u, params=data, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text


def crawl(r):
    soup = BeautifulSoup(r, 'html.parser')
    li = soup.find_all("li", class_="gl-item")
    # pattern = re.compile(r'<li([\S\s]*?)class="p-icons"')
    # shop = pattern.findall(r)[count]
    # print(shop)
    for shop in li:
        it = Item()
        shop = str(shop)
        # with open('abc.html', 'a') as f:
        #     f.write(shop)
        p = re.compile(r'data-sku="(.*?)"')
        it.id = p.search(shop).group(1)
        # print(it.id)

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
            it.seller = "Advertisement"

        p = re.compile(r'p-img[\S\s]*?source-data-lazy-img="(.*?)"')
        it.img = p.search(shop).group(1)

        p = re.compile(r'p-promo-flag')
        if p.search(shop) is not None:
            it.isAD = True
        '''
        start = time.time()
        try:
            it.historyPrice = get_history_price(it.id)
        except:
            day = str(time.strftime('%Y.%m.%d',time.localtime(time.time())))
            day = day.replace('.', ',')
            it.historyPrice = {day: float(it.price)}
        end = time.time()
        print(end - start)
        '''
        yield it


def comments(i, item_id):
    comments_url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv46561\
    &productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(item_id, i)
    # shopurl = 'https://item.jd.com/{}.html'.format(id)
    r = getHTML(comments_url)
    r = r[(r.find('(') + 1):r.rfind(');')]
    r = r.replace('\\', '\\\\')
    comment_json = json.loads(r)
    return comment_json


def hotcomments(item_id):
    comment_json = comments(1, item_id)
    hot_comments = comment_json['hotCommentTagStatistics']
    ci = {}
    for i in hot_comments:
        name = str(i['name'])
        count = float(i['count'])
        ci.update({name: count})
    if not ci:
        ci.update({"此商品暂时还没有买家印象哦~": 100})
    return ci


def pcomments(i, item_id):
    # for i in range(10):
    comment_json = comments(i, item_id)
    p_comments = comment_json['comments']
    for j in p_comments:
        yield j['content']


def get_history_price(item_id):
    url = 'http://p.zwjhl.com/price.aspx?'
    item_url = 'http://item.jd.com/{}.html'.format(item_id)
    data = {
        'url': item_url
    }
    r = getHTML(url, data)
    # r = requests.get(url,params=data, headers=headers)
    # r.encoding = r.apparent_encoding
    # r = r.text
    p = re.compile(r"<script type='text/javascript'(.*?)</script>")
    # data = p.findall(r)
    data = p.search(r).group(1)
    p = re.compile(r"\[(.*?)\]") #[ ]具有去特殊符号的作用,匹配[]用\转义
    datas = p.findall(data)

    p = re.compile(r"\((.*?)\)")
    res = {}
    for i in datas:
        Ptime = p.search(i).group(1)
        j = len(i) - 1
        while j > 0 and i[j] != ',':
            j = j - 1
        price = i[j + 1:]
        res.update({Ptime: float(price)})
    return res