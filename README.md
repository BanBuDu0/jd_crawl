# jd_goods_crawl

## RUN
>apt install mongodb
>
>apt install redis
>
>apt install python3-tk
>
>pip3 install -r requirements.txt
>
>python3 app.py

## jd goods spider

requests + mongo + wordcloud

抓取搜索同类商品30条信息存储在mongo中。可以进一步抓取综合最优或者价格最低的商品评论，并通过wordcloud生成热评图和100条私人评论图，帮助更好了解商品信息

0122:
首页提交之后开始爬取
