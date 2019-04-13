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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    r = requests.get(u, params=data, headers=headers)
    r.encoding = r.apparent_encoding
    print(r.text)

getHTML("https://search.jd.com/Search?keyword=gtx1050")