from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import time

# str = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
def generateByfrequent(ci, path):
    font = r'./simhei.ttf'
    wordcloud = WordCloud(background_color="white", width=1000, height=860, font_path=font).generate_from_frequencies(
        ci)
    # path = r"./static/{}hotcomments.jpg".format(name)
    wordcloud.to_file(path)
    # return path


def generateByText(path):
    font = r'./simhei.ttf'
    ci_path = r"./data/pcomments.txt"
    f = open(ci_path, 'r').read()
    stopwords = STOPWORDS.copy()
    stopwords.add('此用户未填写评价内容')
    wordcloud = WordCloud(background_color="white", width=1000, height=860, font_path=font, stopwords=stopwords).generate(f)
    # path = r"./static/{}pcosmments.jpg".format(name)
    wordcloud.to_file(path)
    # return path
