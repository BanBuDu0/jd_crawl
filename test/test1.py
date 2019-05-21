# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup


def getHTML(u, data=None):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Referer': 'https://item.jd.com'
    }
    r = requests.get(u, params=data, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text

#
# url = 'https://search.jd.com/Search?keyword={}&enc=utf-8'.format("电脑")
# r = getHTML(url)
# print(r)

s = 'aaaa'
m = str(s)
print(m)

