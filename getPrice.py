# -*- coding: UTF-8 -*-
import requests
import re
import json
import matplotlib.pyplot as plt
def getHTML(u, data=None):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
                       Chrome/66.0.3359.139 Safari/537.36'
    }
    r = requests.get(u, params=data, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text
if __name__ == "__main__":
    url = 'http://p.zwjhl.com/price.aspx?'
    item_url = 'http://item.jd.com/{}.html'.format('100000710048')
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
    res = {}
    p = re.compile(r"\((.*?)\)")
    for i in datas:
        Ptime = p.search(i).group(1)
        j = len(i) - 1
        while j > 0 and i[j] != ',':
            j = j - 1
        price = i[j + 1:]
        res.update({Ptime: float(price)})
    # plt.plot(res[])