from wordcloud import WordCloud, STOPWORDS
import jieba
import redis

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


# return words list
def cut_words(words):
    return jieba.cut(words)
