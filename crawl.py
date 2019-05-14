# -*- coding: UTF-8 -*-
import requests
import re
import json
from module import Item
from bs4 import BeautifulSoup


def getHTML(u, data=None):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Referer': 'https://item.jd.com',
        'cookie': 'o2Control=webp; __jdu=1554098654071998291655; shshshfpa=54f8bb81-fb23-5ffd-1b52-d0d371e6ba4a-1554098655; shshshfpb=z48NlvVUNuHVqXQNmVhcTDQ%3D%3D; areaId=15; ipLoc-djd=15-1213-2963-49961; user-key=57cae156-5e2d-4124-86b5-f5051d85dc56; cn=0; pinId=9gq1oBJ3itkhCdM2MK-FZA; pin=15857822107_p; unick=%E5%AD%99%E6%82%A6%E9%9A%BD%E5%95%8A; _tp=r2Y09vKeaWHL3Hg%2BAMntCQ%3D%3D; _pst=15857822107_p; __jda=122270672.1554098654071998291655.1554098654.1557285661.1557846132.12; __jdc=122270672; __jdv=122270672|direct|-|none|-|1557846131858; PCSYCityID=1213; TrackID=1tbUSrxYVam20s7A8d1TFVM1-U9qtOy762-8OHJLxHsuw3C1GG_V7OaSws0FdBTaHmNwjxvCm_MwpW1MEds6be9Xv_YlPBdAIDcOoPvWCbZ0; thor=F708E859185E4F0A460DA0C80647A3CD9481135A8DF7B47E61625081F202802217B657ED11282A54969176FDBF95E8AD367465256CB3DBDD8F426CE66340DE11EB43509451E2F5520003AB85E830584013B891567AAF3373272CB6473FCF752E55F2A810F2FDB4ED4D86EF15E3FE98C42611FDAABAB9A8122680BF86802B765CAFF9FADB203883FA18C02650C09E4D60; ceshi3.com=103; shshshfp=9f312c4b387ca75b44d286762a7075c9; __jdb=122270672.6.1554098654071998291655|12.1557846132; shshshsID=a7392f1511ce81ef1970711f339a7bc0_4_1557846171536; 3AB9D23F7A4B3C9B=744EPUGDNNK6LFADXHVFMQWP3O7LNFYUI3NE4NAACY3ZUP6QFUUN5IPKKOX77DU5M5CYAG5KVI4EXTAH34VBQTRXOY'
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
        yield it


def get_shops(goods: str):
    url = 'https://search.jd.com/Search?keyword={}&enc=utf-8'.format(goods)
    r = getHTML(url)
    return crawl(r)


def comments(i, item_id, flag=1):
    if flag == 1:
        comments_url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98vv46561\
        &productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(item_id, i)
    else:
        comments_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv236\
        &productId={}&score=1&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(item_id, i)
    # shopurl = 'https://item.jd.com/{}.html'.format(id)
    r = getHTML(comments_url)
    r = r[(r.find('(') + 1):r.rfind(');')]
    r = r.replace('\\', '\\\\')
    comment_json = json.loads(r)
    return comment_json


def hot_comments(item_id):
    comment_json = comments(1, item_id)
    hot = comment_json['hotCommentTagStatistics']
    ci = {}
    for i in hot:
        name = str(i['name'])
        count = float(i['count'])
        ci.update({name: count})
    if not ci:
        ci.update({"此商品暂时还没有买家印象哦~": 100})
    return ci


def private_comments(i, item_id):
    # for i in range(10):
    comment_json = comments(i, item_id)
    p_comments = comment_json['comments']
    for j in p_comments:
        yield j['content']


def bad_private_comments(i, item_id):
    comment_json = comments(i, item_id, 0)
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
    p = re.compile(r"\[(.*?)\]")  # [ ]具有去特殊符号的作用,匹配[]用\转义
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
