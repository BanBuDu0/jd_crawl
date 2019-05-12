from wordcloud import WordCloud, STOPWORDS
import jieba
import redis
import time
from snownlp import SnowNLP
from multiprocessing import Pool
import os

import crawl
import controler

r = redis.Redis(host='localhost', port=6379, db=0)
font = r'./static/simhei.ttf'


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
    controler.con_table(table_name).update_one({"id": item['id']}, {"$set": {"historyPrice": historyPrice}})


# P_COMMERNTS = ""
def get_comments(i, item_id, name):
    print('Run task %s (%s)...' % (i, os.getpid()))
    texts = crawl.private_comments(i, item_id)
    temp = ""
    for i in texts:
        i = i.replace('hellip', "")
        if i != '此用户未填写评价内容':
            p = SnowNLP(i).sentiments
        comments_list = jieba.cut(i)
        for j in comments_list:
            if j == '不' or j == '非常' or j == '很':
                temp += j
            else:
                temp += j + " "
        temp += '||||||' + str(p) + '\n'
    r.append(name, temp)


def get_p_pic(name, path, item_id):
    r.set(name, "")
    p = Pool()
    for i in range(10):
        p.apply_async(get_comments, args=(i, item_id, name,))
    p.close()
    p.join()
    try:
        by_text(path, name)
    except:
        r.set(name, '暂无评价～\n')
        by_text(path, name)


def get_hot_pic(path, item_id):
    frequent_ci = crawl.hot_comments(item_id)
    by_frequent(frequent_ci, path)


