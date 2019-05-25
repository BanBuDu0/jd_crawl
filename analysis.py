from wordcloud import WordCloud, STOPWORDS
import jieba_fast as jieba
import redis
import time
from snownlp import SnowNLP
from multiprocessing import Pool
import os
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl

import crawl
import controller

r = redis.Redis(host='localhost', port=6379, db=0)
font = r'./static/simhei.ttf'
mpl.rcParams['font.sans-serif'] = ['SimHei']


def by_frequent(ci, path):
    wordcloud = WordCloud(background_color="white", width=1000, height=860, font_path=font).generate_from_frequencies(
        ci)
    wordcloud.to_file(path)


def by_text(path, name):
    f = r.get(name).decode('utf-8')
    stopwords = STOPWORDS.copy()
    stopwords.add('此用户未填写评价内容')
    wordcloud = WordCloud(background_color="white", width=1000, height=860, font_path=font, stopwords=stopwords).generate(f)
    wordcloud.to_file(path)


# return words iterator
def cut_words(words):
    return jieba.cut(words)


def history_price(item, table_name):
    try:
        historyPrice = crawl.get_history_price(item['id'])
    except:
        historyPrice = {time.strftime("%Y,%m,%d", time.localtime()): item['price']}
    controller.con_table(table_name).update_one({"id": item['id']}, {"$set": {"historyPrice": historyPrice}})


# P_COMMERNTS = ""
def get_comments(i, item_id, name, has_sentiments):
    print('Run task %s (%s)...' % (i, os.getpid()))
    texts = crawl.private_comments(i, item_id)
    temp = ""
    for i in texts:
        i = i.replace('hellip', "")
        # sentiments
        if not has_sentiments:
            p = SnowNLP(i).sentiments
            r.append('sentiments', str(p) + ',')

        comments_list = cut_words(i)
        for j in comments_list:
            if j == '不' or j == '非常' or j == '很' or '不太':
                temp += j
            else:
                temp += j + " "
        temp += '\n'
    r.append(name, temp)


def get_p_pic(table_name, path, item_id, item_sentiments):
    name = table_name + item_id
    r.set(name, "")
    r.set("sentiments", "")
    p = Pool()
    flag = True if item_sentiments else False
    for i in range(10):
        p.apply_async(get_comments, args=(i, item_id, name, flag, ))
    p.close()
    p.join()
    if not flag:
        controller.con_table(table_name).update_one({"id": item_id}, {"$set": {"sentiments": str(r.get('sentiments'), encoding='utf-8')}})
    try:
        by_text(path, name)
    except:
        r.set(name, '暂无评价～\n')
        by_text(path, name)


def get_hot_pic(path, item_id):
    frequent_ci = crawl.hot_comments(item_id)
    by_frequent(frequent_ci, path)


def sentiments_pic(sentiments, name):
    s = []
    for i in sentiments:
        s.append(float(i[0:5]))
    plt.hist(s, bins=np.arange(0, 1, 0.01), facecolor='#83bff6')
    plt.title("情感分析")
    plt.xlabel("正面情感概率")
    plt.ylabel("数量")
    path = r"./static/data/{}sentiments.jpg".format(name)
    plt.savefig(path)
    return path





