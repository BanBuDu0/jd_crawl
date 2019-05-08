# -*- coding: UTF-8 -*-
import requests
import crawl


def getHTML(u, data=None):
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Referer': 'https://item.jd.com'
    }
    r = requests.get(u, params=data, headers=headers)
    r.encoding = r.apparent_encoding
    print(r.text)


bad_iterator = crawl.bad_private_comments(0, 1686632)
for i in bad_iterator:
    print(i)
god_iterator = crawl.private_comments(0, 1686632)
print("now it's good")
for i in god_iterator:
    print(i)
